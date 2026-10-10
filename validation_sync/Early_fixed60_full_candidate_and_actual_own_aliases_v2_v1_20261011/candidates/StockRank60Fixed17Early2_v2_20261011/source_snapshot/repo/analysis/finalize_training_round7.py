"""Freeze a repaired OOF winner, causally calibrate it, and replay test-X inference."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import time

for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round7 as experiment
from optimize_training_round7 import OUT,PREVIOUS,HERE,YEARS,KEYS,BASE_POST,ARCHIVE,ENSEMBLES,read,dump,sha,log,verify
CANDIDATE=ROOT/'candidates/optimization_20261003_r7'
FORMAL=ROOT/'deliveries/connected_topk0175_20261003'


def selected():
    verify();record=read(OUT/'selection.json')
    for path,digest in record['frozen_sha256'].items():assert sha(ROOT/path)==digest,path
    return record


def configure(ctx,winner):
    if ctx.ensemble_name!=winner['ensemble_name']:ctx.install(winner['ensemble_name'])
    ctx.membership_mode=winner['membership_mode']
    ctx.rerank_weight=winner['membership_w5a_weight']
    ctx.top_slow_weight=winner['top_slow_weight']


def select():
    import numpy as np
    verify()
    if (OUT/'selection.json').exists():selected();return
    rows=[]
    for wave in experiment.WAVES:
        payload=read(OUT/f'wave{wave}_results.json');assert payload['status']=='complete'
        rows += [dict(wave=wave,arm=name,**row) for name,row in payload['results'].items()]
    def key(r):return (-r['connected_final_score'],len(ENSEMBLES[r['ensemble_name']]),r['membership_mode']=='block',r['wave'],r['arm'])
    rows.sort(key=key);winner=rows[0]
    ctx=experiment.Context();configure(ctx,winner)
    pred,_=ctx.predict(ctx.donor(ctx.finished('baseline',winner['recipe'])),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    metrics=ctx.score(pred);assert abs(metrics['final_score']-winner['connected_final_score'])<1e-12
    np.save(OUT/'selected_validation.npy',pred)
    baseline=read(OUT/'wave59_results.json')['results']['five_fold_local_membership0.0125']['connected_final_score']
    paths=[Path(__file__),OUT/'protocol.json',OUT/'component_audit.json',OUT/'fine_protocol.json',OUT/'role_protocol.json',
           *[OUT/f'wave{wave}_results.json' for wave in experiment.WAVES],OUT/'selected_validation.npy',
           OUT/'promote_baseline.npy',OUT/f'rankers/{winner["ensemble_name"]}.npy',ROOT/'active_release.json',
           FORMAL/'generation_inputs.parquet',PREVIOUS/'selection.json',ROOT/'candidates/optimization_20261003_r6/verification.json']
    dump(OUT/'selection.json',{'status':'frozen_before_test_prediction','frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'winner':winner,'ranking':rows,'scored_records':len(rows),'baseline_score':baseline,
         'score_gain':winner['connected_final_score']-baseline,
         'historical_uncorrected_score':experiment.HISTORICAL_SCORE,
         'historical_score_is_not_a_compliant_baseline':True,'fold_local_pruning_repaired':True,
         'test_labels_read':False,'selection_rule':'highest official connected score among repaired candidates',
         'frozen_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in paths}},immutable=True)
    log(f'Round7 selected {winner["ensemble_name"]}/{winner["arm"]}: {metrics["final_score"]:.9f}; repaired-baseline gain={winner["connected_final_score"]-baseline:+.9f}')


class ReleaseContext(experiment.Context):
    def __init__(self):
        super().__init__();configure(self,selected()['winner'])
    def promote(self,name):return self.finished(name)


def calibrate():
    import finalize_optimization as shared
    shared.OUT=OUT;shared.Context=ReleaseContext;shared.selected=selected;shared.read=read
    shared.calibrate()
    # Check the actual emitted return CSV as well as the independent in-memory scorer.
    from evaluate import evaluate
    ctx=ReleaseContext()
    metrics={k:float(v) for k,v in evaluate(str(OUT/'calibrated_validation.csv'),str(ctx.scoring)).items()}
    assert abs(metrics['final_score']-selected()['winner']['connected_final_score'])<1e-12
    dump(OUT/'calibrated_csv_official.json',{'status':'passed','metrics':metrics,'csv_sha256':sha(OUT/'calibrated_validation.csv'),
         'test_labels_read':False},immutable=True)


def predict():
    import numpy as np
    import pandas as pd
    import polars as pl
    import lightgbm as lgb
    from src.scoring import Panel
    from experiments.final_sweep_wave3 import ensemble_raw
    from optimize_wave6 import make_prediction_param
    from optimize_wave15 import daily_ranks
    from return_mapping import apply_mapping,daily_percentile
    from run import FEATURE_FILE,to_matrix
    record=selected();winner=record['winner']
    assert read(OUT/'causal_validation.json')['status']==read(OUT/'calibrated_csv_official.json')['status']=='passed'
    if (CANDIDATE/'verification.json').exists():
        assert sha(CANDIDATE/'submission.csv')==read(CANDIDATE/'verification.json')['csv_sha256'];return
    CANDIDATE.mkdir(parents=True,exist_ok=True)
    inputs=pl.read_parquet(FORMAL/'generation_inputs.parquet').with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
    metadata=read(FORMAL/'train_test.json');features=metadata['features']
    test=pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(KEYS+features).sort('trade_date','ts_code').collect()
    assert test.select(KEYS).equals(inputs.select(KEYS));vx=to_matrix(test,features)
    dates=inputs['trade_date'].to_numpy();valid=inputs['price_valid'].to_numpy()
    previous_models=read(ROOT/'candidates/optimization_20261003_r6/verification.json')['models']
    models={};topk_raw=[]
    for component in winner['recipe']['components']:
        name=f'seed{component["seed"]}_f{component["fraction"]:.3f}_r{component["rounds"]}'
        info=previous_models[name];assert sha(info['path'])==info['sha256']
        model=lgb.Booster(model_str=Path(info['path']).read_text(encoding='utf-8'))
        raw=model.predict(vx,num_threads=8);raw[~valid]=-1e6
        replay=lgb.Booster(model_str=Path(info['path']).read_text(encoding='utf-8')).predict(vx,num_threads=8);replay[~valid]=-1e6
        assert np.array_equal(raw,replay)
        target=CANDIDATE/f'model_{name}.txt';target.write_text(Path(info['path']).read_text(encoding='utf-8'),encoding='utf-8')
        models[name]={'path':str(target),'sha256':sha(target),'original':info,'weight':component['weight']}
        topk_raw.append((component,raw))
    source_paths={'lgb':ARCHIVE/'releases/pooled_rms25/backbone_raw.parquet',
                  'xgb':ARCHIVE/'releases/ensemble4/T2f_xgboost_test_raw.parquet',
                  'two':ARCHIVE/'releases/ensemble4/W2c_two_day_test_raw.parquet',
                  'pruned':ARCHIVE/'releases/ensemble4/W2d_pruned_test_raw.parquet',
                  'gru':HERE/'w5a_test/gru_raw_test.npy'}
    raw_members={}
    for name,path in source_paths.items():
        if path.suffix=='.npy':raw=np.load(path).astype(np.float64)
        else:
            frame=pl.read_parquet(path).sort('trade_date','ts_code');assert frame.select(KEYS).equals(inputs.select(KEYS))
            raw=frame['pred_raw'].to_numpy().astype(np.float64)
        assert len(raw)==len(inputs);raw_members[name]=raw
    panel=Panel.from_frame(inputs)
    old_raw=ensemble_raw(panel,ENSEMBLES['five_fold_local'],raw_members)
    assert np.array_equal(old_raw,inputs['w5a_raw'].to_numpy()),'Fulltrain five-way source reconstruction failed'
    final_selection=read(R4_path()/'summary.json')
    assert final_selection['final_feature_selection_matches_shipped_model'], 'Final training feature selector must match deployed pruned model'
    corrected_raw=ensemble_raw(panel,ENSEMBLES[winner['ensemble_name']],raw_members)
    ctx=experiment.Context.__new__(experiment.Context)
    ctx.dates=dates;ctx.flags=inputs['flag_limit_up'].to_numpy().astype(np.int64);ctx.valid=valid
    ctx.codes,unique=pd.factorize(inputs['ts_code'].to_pandas(),sort=True);ctx.codes=ctx.codes.astype(np.int64)
    ctx.n_codes=len(unique);ctx.tie_key=1-ctx.codes/max(ctx.n_codes-1,1)
    ctx.pdf=inputs.select(['trade_date','flag_limit_up']).to_pandas();ctx.ensemble_name=winner['ensemble_name']
    ctx.membership_mode=winner['membership_mode'];ctx.rerank_weight=winner['membership_w5a_weight'];ctx.top_slow_weight=winner['top_slow_weight']
    ctx.slow_finished=inputs['rank_score'].to_numpy()
    aux=inputs['aux_raw'].to_numpy()
    def process(raw,settings):return make_prediction_param(Panel.from_frame(inputs.with_columns(pl.Series('pred_raw',raw))),aux,**settings)
    ctx.w5a=process(corrected_raw,dict(BASE_POST,alpha=0,bonus=0))
    ctx.slow=process(inputs['pred_raw'].to_numpy(),dict(BASE_POST,alpha=0,bonus=0))
    ctx.ranks={'w5a':daily_ranks(ctx.w5a,valid,dates),'slow':daily_ranks(ctx.slow,valid,dates)}
    def construct():
        mixed=sum(component['weight']*daily_ranks(raw,valid,dates) for component,raw in topk_raw);mixed[~valid]=-10.
        promote=process(mixed,winner['recipe']['postprocessing'])
        return ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    rank,stats=construct();replay,_=construct();assert np.array_equal(rank,replay)
    mapping=read(OUT/'future_return_mapping.json');mapped=apply_mapping(mapping,daily_percentile(inputs.select('trade_date').to_pandas(),rank))
    assert np.array_equal(pd.Series(rank).groupby(dates).rank().to_numpy(),pd.Series(mapped).groupby(dates).rank().to_numpy())
    bridge=pl.read_csv(ROOT/'data/raw/测试集_X.csv',schema_overrides={'trade_date':pl.Int32}).select(KEYS).with_row_index('position')
    sub=inputs.select(KEYS).with_columns(pl.Series('pred',mapped)).join(bridge,on=KEYS,how='inner',validate='1:1').sort('position').select(KEYS+['pred'])
    target=CANDIDATE/'submission.csv';sub.write_csv(target,float_precision=17)
    parsed=pd.read_csv(target)
    assert len(parsed)==1599600 and not parsed.duplicated(KEYS).any() and not parsed.isna().any().any() and np.isfinite(parsed.pred).all()
    assert np.array_equal(parsed[KEYS].to_numpy(),bridge.select(KEYS).to_numpy())
    assert np.array_equal(parsed.groupby('trade_date')['pred'].rank().to_numpy(),pd.Series(sub['pred'].to_numpy()).groupby(parsed.trade_date.to_numpy()).rank().to_numpy())
    assert sub.write_csv(float_precision=17).encode('utf-8')==target.read_bytes()
    np.save(CANDIDATE/'rank_prediction.npy',rank)
    dump(CANDIDATE/'selection.json',record,immutable=True);dump(CANDIDATE/'return_mapping.json',mapping,immutable=True)
    dump(CANDIDATE/'verification.json',{'status':'passed','csv_sha256':sha(target),'rows':len(sub),'days':344,'codes':4650,
         'models':models,'model_reload_bit_identical':True,'pipeline_replay_bit_identical':True,'csv_replay_byte_identical':True,
         'csv_ranks_unchanged':True,'validation_score':winner['connected_final_score'],'test_labels_read':False,
         'fold_local_pruning_repaired':True,'final_pruned_features_match_train_only_selector':True,
         'source_predictions_sha256':{str(p):sha(p) for p in source_paths.values()},'construction':stats,
         'old_delivery_pointer_unchanged':sha(ROOT/'active_release.json')==record['frozen_sha256']['active_release.json']},immutable=True)
    log(f'Round7 candidate verified: {target}')


def R4_path():return ARCHIVE/'experiments/revalidation_20260926/validation'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('select','calibrate','predict'))
    globals()[parser.parse_args().stage]()


if __name__=='__main__':main()
