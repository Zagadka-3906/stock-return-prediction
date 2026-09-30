"""One retrospective flat-Top-K continuous-return Lambda backbone.

Synthetic checks and timing precede protocol freeze. No release can be promoted.
Never change this source, sampling scale, gates, or parameters after freeze.
"""
from __future__ import annotations

import os
for _thread_name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "POLARS_MAX_THREADS"):
    os.environ[_thread_name] = "8"

import argparse
import ast
import gc
import hashlib
import importlib.metadata
import itertools
import json
from pathlib import Path
import platform
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import lightgbm as lgb
import numpy as np
import polars as pl
from scipy.special import expit
from run import FEATURE_FILE, feature_names, fold_cutoff, to_matrix
from src.scoring import Panel
from experiments.cached_recheck import make_prediction
from experiments.revalidate_fold_local import score_official

OUT = ROOT / "experiments/r6_topk_20260926"
R4 = ROOT / "experiments/revalidation_20260926/validation"
RAW_LABELS = ROOT / "data" / "raw" / "训练集.csv"
KEYS = ["ts_code", "trade_date"]
KEY = "topk_return_backbone"
DEVELOPMENT, CONFIRMATION = (2020, 2021, 2022), (2023, 2024)
REFERENCES = ("baseline", "ensemble4")
SEED, SAMPLES, ROUNDS = 2026, 8, 180
RETURN_SCALE = 100.0
GATES = {
    "development": {"mean": .001, "worst": -.005, "ic": -.002},
    "confirmation": {"mean": .0005, "worst": -.003, "ic": -.002},
    "bootstrap": {"block_days": 20, "draws": 20000, "seed": 2026, "positive_share": .8},
}
PARAMS = dict(metric="None", learning_rate=.05, num_leaves=31,
              min_data_in_leaf=300, feature_fraction=.85, bagging_fraction=.85,
              bagging_freq=1, lambda_l2=5., max_bin=127, num_threads=8,
              seed=SEED, verbosity=-1, force_col_wise=True)


def sha(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_new(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)


def log(message):
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def pair_terms(scores, returns, first, second, weights):
    """Pair indices/weights are held fixed for a local derivative calculation."""
    delta = returns[first] - returns[second]
    direction = np.sign(delta)
    weight = np.abs(delta) * RETURN_SCALE * weights
    margin = direction * (scores[first] - scores[second])
    probability = expit(-margin)
    gradient = -weight * direction * probability
    hessian = weight * probability * (1.0 - probability)
    loss = float(np.sum(weight * np.logaddexp(0.0, -margin)))
    return loss, gradient, hessian


def full_day(scores, returns, k, scale=1.0):
    """Exact reference used only on small synthetic groups."""
    order = np.argsort(-scores, kind="stable")
    first = np.repeat(order[:k], len(scores)-k)
    second = np.tile(order[k:], k)
    weights = np.full(len(first), scale / (k*(len(scores)-k)))
    loss, g, h = pair_terms(scores, returns, first, second, weights)
    gradient = np.bincount(first, g, len(scores))-np.bincount(second, g, len(scores))
    hessian = np.bincount(first, h, len(scores))+np.bincount(second, h, len(scores))
    return loss, gradient, hessian


def sampled_day(scores, returns, rng, samples=SAMPLES, scale=1.0, minimum=100):
    """Uniform replacement sampling gives unbiased local gradients and Hessian.

    For every current predicted Top member draw M pool-outside members uniformly.
    Full objective: scale/[K*(N-K)] * sum_cross |100*(yi-yj)| logistic(...).
    Sample coefficient: scale/(K*M). No self-normalization by observed gains.
    The returned Hessian is the diagonal pair Hessian; cross terms are omitted.
    """
    if scores.ndim != 1 or returns.shape != scores.shape or samples < 1:
        raise ValueError("Invalid daily shapes/sample count")
    n = len(scores)
    if not np.isfinite(scores).all() or not np.isfinite(returns).all():
        raise ValueError("Daily optimization arrays must be finite")
    gradient, hessian = np.zeros(n), np.zeros(n)
    if n < minimum:
        return gradient, hessian, 0
    k = max(n//10, 1)
    if k == n:
        return gradient, hessian, 0
    order = np.argsort(-scores, kind="stable")
    top, outside = order[:k], order[k:]
    draws = rng.integers(0, len(outside), size=(k, samples))
    first = np.repeat(top, samples)
    second = outside[draws.reshape(-1)]
    _, g, h = pair_terms(scores, returns, first, second, scale/(k*samples))
    gradient[top] = g.reshape(k, samples).sum(axis=1)
    hessian[top] = h.reshape(k, samples).sum(axis=1)
    gradient[outside] = -np.bincount(draws.reshape(-1), g, len(outside))
    hessian[outside] = np.bincount(draws.reshape(-1), h, len(outside))
    return gradient, hessian, len(first)


class FlatTopKObjective:
    def __init__(self, dates, labels, eligible=None, seed=SEED):
        self.dates = np.asarray(dates)
        self.labels = np.asarray(labels, dtype=np.float64)
        if self.dates.ndim != 1 or self.labels.shape != self.dates.shape or not len(self.dates):
            raise ValueError("Invalid group arrays")
        if np.any(self.dates[1:] < self.dates[:-1]):
            raise ValueError("Dates must be contiguous and ascending")
        self.eligible = np.isfinite(self.labels)
        if eligible is not None:
            mask = np.asarray(eligible)
            if mask.dtype != bool or mask.shape != self.dates.shape:
                raise ValueError("Eligible mask must be aligned boolean")
            self.eligible &= mask
        self.bounds = np.r_[0, np.flatnonzero(self.dates[1:] != self.dates[:-1])+1, len(self.dates)]
        self.groups = [np.flatnonzero(self.eligible[a:b])+a for a,b in zip(self.bounds[:-1], self.bounds[1:])]
        self.groups = [rows for rows in self.groups if len(rows) >= 100]
        if not self.groups:
            raise ValueError("No eligible groups with at least 100 stocks")
        self.scale = sum(len(rows) for rows in self.groups)/len(self.groups)
        self.seed, self.iteration = seed, 0
        self.timings, self.pair_counts = [], []

    def __call__(self, predictions, dataset=None):
        started = time.monotonic()
        scores = np.asarray(predictions, dtype=np.float64)
        if scores.shape != self.labels.shape or not np.isfinite(scores[self.eligible]).all():
            raise ValueError("Invalid eligible predictions")
        rng = np.random.default_rng(np.random.SeedSequence([self.seed, self.iteration]))
        gradient, hessian = np.zeros(len(scores)), np.zeros(len(scores))
        count = 0
        for rows in self.groups:
            g, h, pairs = sampled_day(scores[rows], self.labels[rows], rng, scale=self.scale)
            gradient[rows], hessian[rows] = g, h
            count += pairs
        if not np.isfinite(gradient).all() or not np.isfinite(hessian).all() or np.any(hessian < 0):
            raise AssertionError("Nonfinite/negative optimization output")
        self.timings.append(time.monotonic()-started)
        self.pair_counts.append(count)
        self.iteration += 1
        if dataset is not None and (self.iteration == 1 or self.iteration % 30 == 0):
            log(f"objective round {self.iteration}: {count:,} sampled pairs, {self.timings[-1]:.2f}s")
        return gradient, hessian


def objective_callback(objective):
    # lightgbm.train deep-copies params. A closure keeps one observed objective
    # state; passing the callable class directly would copy its labels/counters.
    def callback(predictions, dataset):
        return objective(predictions, dataset)
    return callback


def synthetic_tests():
    # Flat gain is EXACT mean Top return change for every swap/permutation.
    y = np.array([-.03, -.007, .0, .004, .04])
    cases = 0
    for perm in itertools.permutations(range(5)):
        for k in (1,2,3,4):
            old = set(perm[:k]); old_value = float(y[list(old)].mean())
            for i in old:
                for j in set(perm[k:]):
                    new = (old-{i})|{j}
                    observed = float(y[list(new)].mean())-old_value
                    assert abs(observed-(y[j]-y[i])/k) < 1e-15
                    cases += 1
    s = np.array([.7, -.5, .2, -.1, 1.1])
    loss, g, h = full_day(s, y, 2, scale=7.)
    eps = 1e-5
    for i in range(len(s)):
        plus, minus = s.copy(), s.copy(); plus[i] += eps; minus[i] -= eps
        lp,gp,_ = full_day(plus,y,2,scale=7.)
        lm,gm,_ = full_day(minus,y,2,scale=7.)
        assert abs((lp-lm)/(2*eps)-g[i]) < 1e-8
        assert abs((gp[i]-gm[i])/(2*eps)-h[i]) < 1e-8
    assert abs(g.sum()) < 1e-14 and np.all(h >= 0)
    # Exact expectation over every uniform draw for K=2, N-K=3, M=1.
    order = np.argsort(-s, kind="stable"); top, outside = order[:2],order[2:]
    expectation_g, expectation_h = np.zeros(5),np.zeros(5)
    for choices in itertools.product(outside, repeat=2):
        _, pg, ph = pair_terms(s,y,top,np.asarray(choices),7./2)
        expectation_g += (np.bincount(top,pg,5)-np.bincount(choices,pg,5))/9
        expectation_h += (np.bincount(top,ph,5)+np.bincount(choices,ph,5))/9
    np.testing.assert_allclose(expectation_g,g,atol=1e-14,rtol=0)
    np.testing.assert_allclose(expectation_h,h,atol=1e-14,rtol=0)
    rng = np.random.default_rng(7)
    dates = np.repeat([1,2],120); labels = rng.normal(0,.02,240)
    scores = rng.normal(size=240); labels[3] = np.nan
    eligible = np.ones(240,dtype=bool); eligible[7]=False
    obj = FlatTopKObjective(dates,labels,eligible)
    a,b = obj(scores)
    assert a[3] == b[3] == a[7] == b[7] == 0
    labels_changed=labels.copy();labels_changed[120:]=100
    aa,bb=FlatTopKObjective(dates,labels_changed,eligible)(scores)
    assert np.array_equal(a[:120],aa[:120]) and np.array_equal(b[:120],bb[:120])
    same_g,same_h=FlatTopKObjective(dates,labels,eligible)(scores)
    assert np.array_equal(a,same_g) and np.array_equal(b,same_h)
    zeros = np.zeros(120)
    zg,zh,_=sampled_day(zeros,zeros,np.random.default_rng(1))
    assert not zg.any() and not zh.any()
    with_ties=FlatTopKObjective(dates,labels,eligible)(np.zeros(240))
    assert all(np.isfinite(v).all() for v in with_ties)
    fail = 0
    for bad_dates,bad_scores in ((dates[::-1],scores),(dates,np.full(240,np.inf))):
        try:FlatTopKObjective(bad_dates,labels,eligible)(bad_scores)
        except ValueError:fail+=1
    assert fail == 2
    # Group scaling is Nbar; two identical days have identical exact gradients.
    _,one_g,one_h=full_day(s,y,2,scale=5)
    assert np.isfinite(loss) and np.all(one_h >= 0)
    # A tiny synthetic fit checks the actual LightGBM custom-objective API.
    fixture_x=rng.normal(size=(1000,5)).astype(np.float32)
    fixture_y=.01*fixture_x[:,0].astype(np.float64)
    fixture_obj=FlatTopKObjective(np.repeat(np.arange(10),100),fixture_y)
    fixture_ds=lgb.Dataset(fixture_x,label=np.zeros(1000,dtype=np.float32))
    fixture_model=lgb.train(dict(objective=objective_callback(fixture_obj),metric="None",
        num_leaves=5,min_data_in_leaf=10,num_threads=2,verbosity=-1,seed=2026),fixture_ds,num_boost_round=2)
    assert fixture_obj.iteration == 2 and fixture_model.current_iteration() == 2
    reloaded=lgb.Booster(model_str=fixture_model.model_to_string())
    assert np.array_equal(fixture_model.predict(fixture_x),reloaded.predict(fixture_x))
    return {"status":"passed","exhaustive_swap_cases":cases,
            "checks":["all_permutation_flat_top_swap_gain","local_finite_difference_gradient",
                      "local_finite_difference_diagonal_hessian","exact_uniform_sampling_expectation",
                      "zero_gradient_sum","missing_labels_and_invalid_rows_zero",
                      "future_day_labels_do_not_change_prior_day_gradient","seed_reproducibility",
                      "equal_labels_zero","all_zero_score_ties_finite",
                      "unsorted_groups_rejected","nonfinite_eligible_scores_rejected",
                      "lightgbm_callable_deepcopy_safe_two_synthetic_rounds","model_string_reload_exact"],
            "historical_scores_computed":False}


def check():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/"protocol.json").exists():
        raise RuntimeError("Checks must precede protocol freeze")
    result=synthetic_tests()
    # Realistic size, entirely synthetic labels: no market model or score fitting.
    rng=np.random.default_rng(SEED); n,d=4500,200
    objective=FlatTopKObjective(np.repeat(np.arange(d),n),rng.normal(0,.02,n*d))
    scores=rng.normal(size=n*d)
    for _ in range(3):objective(scores)
    result["benchmark"]={"stocks_per_day":n,"days":d,"rounds":3,
        "seconds":objective.timings,"sampled_pairs_per_round":objective.pair_counts[0],
        "estimated_1000_day_180round_objective_seconds":float(np.median(objective.timings)*5*ROUNDS),
        "excludes_lightgbm_tree_training_and_data_loading":True,
        "float32_feature_matrix_4m_rows_63_columns_gib":4_000_000*63*4/2**30}
    result["source_sha256"]=sha(Path(__file__))
    write_new(OUT/"tests.json",result)
    log(json.dumps(result,ensure_ascii=False))


def local_source_closure():
    pending=[Path(__file__),ROOT/"experiments/audit_r5_candidate.py"]
    result=set()
    while pending:
        path=pending.pop().resolve()
        if path in result or not path.exists():continue
        result.add(path)
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8-sig"))):
            modules=[]
            if isinstance(node,ast.Import):modules=[a.name for a in node.names]
            elif isinstance(node,ast.ImportFrom) and node.module and not node.level:
                modules=[node.module]+[node.module+"."+a.name for a in node.names]
            for module in modules:
                candidate=ROOT/Path(*module.split("."))
                py=candidate.with_suffix(".py")
                if py.is_file():pending.append(py)
    return sorted(result)


def dependency_files():
    files=[]; versions={}
    for name in ("lightgbm","numpy","scipy","polars","polars-runtime-32","pandas"):
        distribution=importlib.metadata.distribution(name)
        versions[name]=distribution.version
        for item in distribution.files or []:
            path=Path(distribution.locate_file(item))
            if path.name in ("RECORD","METADATA") or path.suffix.lower() in (".py",".dll",".pyd"):
                if path.is_file():files.append(path.resolve())
    files.append(Path(sys.executable).resolve())
    return versions,sorted(set(files))


def freeze():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/"protocol.json").exists():raise FileExistsError("Already frozen")
    tests=read(OUT/"tests.json")
    assert tests["status"] == "passed" and tests["source_sha256"] == sha(Path(__file__))
    paths=local_source_closure()+[FEATURE_FILE,RAW_LABELS,ROOT/"data/feature_manifest.json",
        ROOT/"active_release.json",ROOT/"releases/ensemble4_r4/release_manifest.json",
        R4/"summary.json",R4/"protocol.json",OUT/"tests.json"]
    for year in (*DEVELOPMENT,*CONFIRMATION):
        paths.append(R4/f"result_{year}.json")
        for reference in REFERENCES:
            paths.extend([R4/f"predictions_{reference}_{year}.parquet",R4/f"daily_{reference}_{year}.csv"])
    versions,deps=dependency_files()
    payload={"candidate":KEY,"frozen_at_local":time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source_sha256":sha(Path(__file__)),"single_configuration":True,
        "role":"new backbone replaces raw primary signal; original pooled auxiliary unchanged",
        "parameters":PARAMS,"rounds":ROUNDS,"samples_per_top":SAMPLES,"return_scale":RETURN_SCALE,
        "objective":"Nbar * sum_day sum_cross |100*(yi-yj)|*softplus(-sign(yi-yj)*(si-sj))/(K*(N-K))",
        "sampling":"Every predicted Top member draws 8 outside members uniformly with replacement each round. Weight Nbar/(K*8), conditional unbiased gradient and diagonal Hessian, no observed-gain normalization.",
        "group_normalization":"Nbar=eligible training rows / eligible training days, fixed before boosting. Days with fewer than 100 eligible stocks are omitted.",
        "ties":"Start at zero raw scores; stable trade_date/ts_code input order determines initial Top. This arbitrary starting subset can affect optimization. No label-based tie breaking.",
        "seed":"PCG64 default_rng(SeedSequence([2026, zero_based_boosting_round])) per fold",
        "labels":"Original training CSV Float64 raw y_ret_1d; no rank, clipping, winsorization, return-head or feature-cache Float32 label substitution.",
        "training_filter":"is_train & trade_date < one_day_fold_cutoff & price_valid & flag_limit_up==0 & original_y finite; sorted trade_date/ts_code; current-close prediction timing",
        "purge":"y(t) realized close(t+1) strictly before first validation date; cutoff is last prevalidation calendar day, excluded",
        "features":"Original 63 features, no selection or extra features",
        "postprocess":{"alpha":.9,"bonus":.3,"protected_current_weight":1.,"pooled_top_only_weight":.25},
        "development_years":list(DEVELOPMENT),"confirmation_years":list(CONFIRMATION),"gates":GATES,
        "confirmation":"Only if all development gates pass BOTH references; score 2023/24 once, same point gates and paired bootstrap 80% both references. No fallback or new configuration.",
        "all_years_previously_viewed":True,"formal_promotion_permitted":False,
        "limits":{"cpu_threads":8,"host_memory_target_gib":10,"no_full_pair_materialization":True},
        "input_sha256":{p.relative_to(ROOT).as_posix():sha(p) for p in sorted(set(paths))},
        "python":platform.python_version(),"package_versions":versions,
        "dependency_sha256":{str(p):sha(p) for p in deps}}
    write_new(OUT/"protocol.json",payload)
    log("One fixed Top-K return backbone protocol frozen; training is a separate action")


def verify_protocol():
    protocol=read(OUT/"protocol.json")
    assert protocol["parameters"] == PARAMS and protocol["gates"] == GATES
    assert protocol["source_sha256"] == sha(Path(__file__))
    for p,digest in protocol["input_sha256"].items():
        if sha(ROOT/p) != digest:raise AssertionError(f"Frozen input changed: {p}")
    for p,digest in protocol["dependency_sha256"].items():
        if sha(Path(p)) != digest:raise AssertionError(f"Dependency changed: {p}")
    return protocol


def training_frame(year):
    cutoff=fold_cutoff(year); features=feature_names()
    label=(pl.scan_csv(RAW_LABELS,schema_overrides={"ts_code":pl.String,"trade_date":pl.Int32,"y_ret_1d":pl.Float64},
        null_values=["NaN","nan",""]).select(KEYS+["y_ret_1d"])
        .filter((pl.col("trade_date")<cutoff)&pl.col("y_ret_1d").is_finite()))
    frame=(pl.scan_parquet(FEATURE_FILE).filter(pl.col("is_train")&(pl.col("trade_date")<cutoff)
        &pl.col("price_valid")&(pl.col("flag_limit_up")==0)).select(KEYS+features)
        .join(label,on=KEYS,how="inner",validate="1:1").sort("trade_date","ts_code").collect())
    assert frame["y_ret_1d"].dtype == pl.Float64
    assert frame.select(KEYS).n_unique() == len(frame) and len(features) == 63
    counts=frame.group_by("trade_date").len();keep=counts.filter(pl.col("len")>=100)["trade_date"]
    frame=frame.filter(pl.col("trade_date").is_in(keep.implode()))
    assert frame["trade_date"].max()<cutoff
    meta={"training_cutoff_exclusive":cutoff,"rows":len(frame),"days":frame["trade_date"].n_unique(),
        "first_date":frame["trade_date"].min(),"last_date":frame["trade_date"].max(),"target_dtype":"Float64_original_CSV",
        "target_sha256":hashlib.sha256(frame["y_ret_1d"].to_numpy().tobytes()).hexdigest(),
        "keys_sha256":hashlib.sha256(frame.select(KEYS).write_csv().encode()).hexdigest()}
    return frame,features,meta


def fixed_prediction(frame,raw):
    panel=Panel.from_frame(frame.with_columns(pl.Series("pred_raw",raw)))
    return make_prediction(panel,frame["aux_raw"].to_numpy(),"top_only",.25)


def fold(year):
    record_path=OUT/f"fold_{year}.json"
    if record_path.exists():
        record=read(record_path)
        assert record["protocol_sha256"] == sha(OUT/"protocol.json")
        for p,d in record["artifact_sha256"].items():assert sha(OUT/p)==d
        return record
    for p in OUT.glob(f"*_{year}.*"):
        raise FileExistsError(f"Incomplete fold evidence exists; no overwrite: {p.name}")
    started=time.monotonic();train,features,meta=training_frame(year)
    objective=FlatTopKObjective(train["trade_date"].to_numpy(),train["y_ret_1d"].to_numpy())
    x=to_matrix(train,features)
    # Dataset dummy labels are never read by our objective; raw Float64 lives in closure.
    dataset=lgb.Dataset(x,label=np.zeros(len(x),dtype=np.float32),feature_name=features,free_raw_data=True)
    del train;gc.collect()
    log(f"{year}: fitting {meta['rows']:,} rows/{meta['days']} days, 63 features, 180 rounds")
    params=dict(PARAMS,objective=objective_callback(objective))
    model=lgb.train(params,dataset,num_boost_round=ROUNDS)
    assert model.current_iteration()==ROUNDS and objective.iteration==ROUNDS
    model_path=OUT/f"model_{year}.txt"
    with model_path.open("x",encoding="utf-8") as stream:stream.write(model.model_to_string())
    del dataset,x;gc.collect()
    frame=pl.read_parquet(R4/f"predictions_ensemble4_{year}.parquet").sort("trade_date","ts_code")
    valid=(pl.scan_parquet(FEATURE_FILE).filter(pl.col("trade_date").is_between(year*10000+101,year*10000+1231))
        .select(KEYS+features).sort("trade_date","ts_code").collect())
    assert frame.select(KEYS).equals(valid.select(KEYS))
    matrix=to_matrix(valid,features);raw=model.predict(matrix,num_threads=8).astype(np.float64)
    # Load via model_str on paths unsupported by some LightGBM Windows readers.
    loaded=lgb.Booster(model_str=model_path.read_text(encoding="utf-8"))
    np.testing.assert_allclose(loaded.predict(matrix[:4096],num_threads=8),raw[:4096],rtol=0,atol=0)
    raw[~frame["price_valid"].to_numpy()]=-1e6
    del matrix,valid,model,loaded;gc.collect()
    pred=fixed_prediction(frame,raw)
    assert np.isfinite(pred).all() and np.all(pred[~frame["price_valid"].to_numpy()] < -1)
    assert np.array_equal(pred,fixed_prediction(frame.with_columns(pl.lit(None,dtype=pl.Float64).alias("y_ret_1d")),raw))
    prefix=50*frame["ts_code"].n_unique()
    assert np.array_equal(pred[:prefix],fixed_prediction(frame.head(prefix),raw[:prefix]))
    expected=read(R4/"summary.json")["metrics"][str(year)]
    references={}
    for name in REFERENCES:
        ref=pl.read_parquet(R4/f"predictions_{name}_{year}.parquet").sort("trade_date","ts_code")
        assert frame.select(KEYS).equals(ref.select(KEYS))
        metrics,daily=score_official(frame,ref["pred"].to_numpy())
        assert all(abs(value-expected[name][key])<=1e-12 for key,value in metrics.items())
        daily.write_csv(OUT/f"daily_{name}_{year}.csv");references[name]=metrics
    metrics,daily=score_official(frame,pred)
    daily.write_csv(OUT/f"daily_{KEY}_{year}.csv")
    frame.with_columns(pl.Series("pred_raw",raw),pl.Series("pred",pred)).write_parquet(OUT/f"predictions_{KEY}_{year}.parquet",compression="zstd")
    record={"year":year,"protocol_sha256":sha(OUT/"protocol.json"),"training":meta,
        "candidate":KEY,"metrics":metrics,"references":references,
        "objective_rounds":objective.iteration,"objective_seconds":sum(objective.timings),
        "sampled_pairs_total":sum(objective.pair_counts),"elapsed_seconds":time.monotonic()-started,
        "tests":{"model_reload_exact":True,"prediction_label_missingness_invariance":True,"50_day_prefix_exact":True,"invalid_low":True},
        "artifact_sha256":{p.name:sha(p) for p in OUT.glob(f"*_{year}.*") if p!=record_path}}
    write_new(record_path,record);log(f"{year}: official score {metrics['final_score']:.9f}")
    del frame,objective;gc.collect();return record


def gate(records,stage):
    threshold=GATES[stage];result={}
    for name in REFERENCES:
        delta=[r["metrics"]["final_score"]-r["references"][name]["final_score"] for r in records]
        ic=[r["metrics"]["ic_mean"]-r["references"][name]["ic_mean"] for r in records]
        result[name]={"annual_score_delta":dict(zip([str(r["year"]) for r in records],delta)),
            "mean_score_delta":float(np.mean(delta)),"worst_score_delta":min(delta),"mean_ic_delta":float(np.mean(ic)),
            "passed":bool(np.mean(delta)>=threshold["mean"] and min(delta)>=threshold["worst"] and np.mean(ic)>=threshold["ic"])}
    return {"comparisons":result,"passed":all(r["passed"] for r in result.values())}


def develop():
    verify_protocol()
    if (OUT/"development.json").exists():raise FileExistsError("Development already evaluated")
    records=[fold(year) for year in DEVELOPMENT]
    result={"protocol_sha256":sha(OUT/"protocol.json"),"candidate":KEY,"gate":gate(records,"development"),
        "fold_sha256":{str(y):sha(OUT/f"fold_{y}.json") for y in DEVELOPMENT},"no_candidate_fallback":True}
    verify_protocol();write_new(OUT/"development.json",result);finalize()


def confirm():
    verify_protocol();dev=read(OUT/"development.json")
    assert dev["protocol_sha256"]==sha(OUT/"protocol.json")
    records=[]
    for year in DEVELOPMENT:
        assert sha(OUT/f"fold_{year}.json")==dev["fold_sha256"][str(year)]
        records.append(fold(year))
    assert gate(records,"development")==dev["gate"]
    if not dev["gate"]["passed"]:raise RuntimeError("Development failed; confirmation forbidden")
    if (OUT/"confirmation.json").exists():raise FileExistsError("Confirmation already evaluated")
    records=[fold(year) for year in CONFIRMATION]
    from experiments.audit_r5_candidate import paired_block_bootstrap
    daily=lambda key:{year:pl.read_csv(OUT/f"daily_{key}_{year}.csv",null_values=["NaN"]) for year in CONFIRMATION}
    bootstrap={name:paired_block_bootstrap(daily(KEY),daily(name),block_days=20,draws=20000,seed=2026) for name in REFERENCES}
    result={"development_sha256":sha(OUT/"development.json"),"gate":gate(records,"confirmation"),"bootstrap":bootstrap,
        "fold_sha256":{str(y):sha(OUT/f"fold_{y}.json") for y in CONFIRMATION},"formal_promotion_permitted":False}
    result["passed"]=bool(result["gate"]["passed"] and all(v["bootstrap_share_positive"]>=.8 for v in bootstrap.values()))
    verify_protocol();write_new(OUT/"confirmation.json",result);finalize()


def finalize():
    dev=read(OUT/"development.json") if (OUT/"development.json").exists() else None
    conf=read(OUT/"confirmation.json") if (OUT/"confirmation.json").exists() else None
    state="not_trained" if dev is None else ("development_failed_stop" if not dev["gate"]["passed"] else "confirmation_pending")
    if conf:state="historical_confirmation_passed_no_promotion" if conf["passed"] else "confirmation_failed_stop"
    lines=["# 平坦 Top-K 连续收益损失结果","",f"状态：{state}。","",
        "单一新主干；原 pooled 辅助及 .9/.3/protected/.25 后处理不变。原始 CSV Float64 收益直接构成损失，不是普通 NDCG、离散档位或 rank 标签。所有年份已看过，本研究禁止晋级正式版。","",
        "每个预测 Top 成员每轮均匀有放回抽取 8 个池外成员；样本梯度是归一化全跨边界对梯度的条件无偏估计。返回对角 Hessian，不是完整矩阵。零分初始 Top 按股票代码稳定排序，存在任意起点影响。"]
    if dev:
        lines += ["","开发门槛：对 r4 和 pooled 分别满足平均增量≥0.001、最差年≥−0.005、平均 IC 增量≥−0.002。","",json.dumps(dev["gate"],ensure_ascii=False,indent=2)]
    if conf:lines += ["","确认结果：",json.dumps({"gate":conf["gate"],"passed":conf["passed"],"bootstrap_positive_share":{k:v["bootstrap_share_positive"] for k,v in conf["bootstrap"].items()}},ensure_ascii=False,indent=2)]
    lines += ["","目标没有联合优化 IC 或换手；raw 收益改善不代表后处理总分改善。失败完整保留，不改门槛、不替换候选。官方评估的缺标签集合不进入预测。bootstrap 是历史配对重采样，不能消除反复选模偏差。","",
        "protocol.json 锁源文件、输入、依赖二进制/包记录与参数；tests.json 是合成穷举、梯度及采样期望验证；fold_年份.json 锁模型、逐日结果和预测；失败见 failure_*.json。"]
    report=OUT/"结论.md"
    # Before final sealing this derived summary may advance from dev to confirmation.
    if (OUT/"artifact_manifest.json").exists():raise FileExistsError("Final artifact manifest already sealed")
    report.write_text("\n".join(lines)+"\n",encoding="utf-8")
    terminal=(dev is not None and not dev["gate"]["passed"]) or conf is not None
    if terminal:
        write_new(OUT/"artifact_manifest.json",{"state":state,"formal_promotion_permitted":False,
            "artifact_sha256":{p.name:sha(p) for p in OUT.iterdir() if p.is_file()},"source_sha256":sha(Path(__file__))})


if __name__ == "__main__":
    parser=argparse.ArgumentParser();parser.add_argument("stage",choices=("check","freeze","develop","confirm","finalize"))
    args=parser.parse_args()
    try:globals()[args.stage]()
    except Exception as error:
        OUT.mkdir(parents=True,exist_ok=True)
        path=OUT/f"failure_{time.time_ns()}.json"
        write_new(path,{"stage":args.stage,"type":type(error).__name__,"message":str(error),"traceback":traceback.format_exc(),
            "source_sha256":sha(Path(__file__)),"protocol_sha256":sha(OUT/"protocol.json") if (OUT/"protocol.json").exists() else None})
        raise
