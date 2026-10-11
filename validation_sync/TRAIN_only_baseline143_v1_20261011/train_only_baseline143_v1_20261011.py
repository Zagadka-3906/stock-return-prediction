"""Fixed TRAIN-only one-day return baseline, declared before its first fit.

No historical winners, teachers, member/orderer split, TEST outcomes, calibration,
or postprocessing are imported. The feature names and tree parameters are anchored
to a model hash frozen before the first historical TEST return revelation.
"""
from __future__ import annotations
import os
os.environ.setdefault('POLARS_MAX_THREADS', '8')
os.environ.setdefault('OMP_NUM_THREADS', '16')
import argparse, gc, hashlib, importlib.util, json, shutil, sys, time, zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
import numpy as np
import polars as pl
import lightgbm as lgb
from train_only_features143_v1_20261011 import features, source, RAW

ROOT = Path(__file__).resolve().parents[1]
KEYS = ['ts_code', 'trade_date']
RUN_ID = 'train_only_baseline143_v1_20261011'
PRETEST_MODEL_SHA = '7df4d394f964c1051dd354a88eceb6f3b7c7858809768202ace4d7b0592c587c'
PARAMS = dict(objective='regression', metric='l2', learning_rate=.05,
              num_leaves=31, min_data_in_leaf=300, feature_fraction=.85,
              bagging_fraction=.85, bagging_freq=1, lambda_l2=5., max_bin=127,
              num_threads=16, seed=2026, verbosity=-1,
              deterministic=True, force_col_wise=True)


def now():
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(8*1024*1024), b''): h.update(b)
    return h.hexdigest()


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def put(p, d):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    tmp.replace(p)


def log(s):
    print(f'[{now()}] {s}', flush=True)


def guard(a, stage):
    if a.control_root:
        for day in ['10', '09']:
            c = read(a.control_root/f'analysis/current_user_runtime_control_202610{day}.json')
            assert c['status']=='user_authorized_bounded_TRAIN_only_baseline_training', c
            assert c['bounded_training_run_id']==RUN_ID and not c['automatic_restart_enabled']
        assert read(a.control_root/'analysis/user_authorized_train_only_baseline143_v1_20261011.json')['actual_user_instruction']=='训练符合要求的模型'
    log(f'Control/time check passed: {stage}')


def matrix(frame, names):
    return np.ascontiguousarray(frame.select(names).to_numpy(), dtype=np.float32)


def exact(a, b):
    assert np.array_equal(a, b, equal_nan=True)


def synthetic():
    rng=np.random.default_rng(2026)
    days=125; stocks=4
    n=days*stocks
    close=10+np.cumsum(rng.normal(0,.02,n).reshape(stocks,days),axis=1).reshape(-1)
    f=pl.DataFrame({'ts_code':np.repeat(['a','b','c','d'],days),
                    'trade_date':np.tile(np.arange(days,dtype=np.int32)+20000101,stocks),
                    'open':close*.999,'high':close*1.01,'low':close*.99,'close':close,
                    'vol':rng.uniform(1,100,n),'amount':rng.uniform(100,1000,n),
                    'flag_limit_up':np.zeros(n,dtype=np.int8),'flag_limit_down':np.zeros(n,dtype=np.int8),
                    'row_id':np.arange(n,dtype=np.uint32)})
    cutoff=20000101+85
    full,names=features(f.lazy()); full=full.collect().sort(KEYS)
    prefix,_=features(f.filter(pl.col('trade_date')<cutoff).lazy());prefix=prefix.collect().sort(KEYS)
    expected=full.filter(pl.col('trade_date')<cutoff)
    assert expected.equals(prefix)
    poisoned=f.with_columns(pl.when(pl.col('trade_date')>=cutoff).then(pl.col('close')*1000)
                             .otherwise(pl.col('close')).alias('close'),
                             pl.lit(999.).alias('y_ret_1d'))
    future,_=features(poisoned.lazy()); future=future.collect().sort(KEYS)
    assert future.filter(pl.col('trade_date')<cutoff).equals(prefix)
    # Changing a label everywhere cannot change a feature anywhere.
    assert full.equals(features(f.with_columns(pl.lit(-999.).alias('y_ret_1d')).lazy())[0].collect().sort(KEYS))
    return {'status':'passed','feature_count':len(names),'prefix_rows':len(prefix),
            'trailing_features_prefix_exact':True,'future_price_poison_prefix_exact':True,
            'all_label_columns_removed_before_feature_construction':True}


def freeze(a):
    guard(a,'freeze protocol before fitting/scoring')
    w=a.work_dir; w.mkdir(parents=True,exist_ok=True)
    assert not (w/'protocol.json').exists(), 'Use the existing sealed protocol; do not overwrite it.'
    old=a.historical_root/'analysis/frozen_holdout_20260928/protocol.json'
    p=read(old); native=a.historical_root/'releases/xgboost_seed8_r6/auxiliary.txt'
    assert p['frozen_at_utc']<'2026-09-28T14:53:02.315174+00:00'
    assert p['input_sha256']['releases/xgboost_seed8_r6/auxiliary.txt']==sha(native)==PRETEST_MODEL_SHA
    b=lgb.Booster(model_str=native.read_text(encoding='utf-8'))
    _,names=features(pl.DataFrame(schema={**{x:pl.Float32 for x in RAW if x not in KEYS},
                                              'ts_code':pl.String,'trade_date':pl.Int32,'row_id':pl.UInt32}).lazy())
    assert names==b.feature_name() and b.current_iteration()==180
    for k,v in {'learning_rate':'.05','num_leaves':'31','min_data_in_leaf':'300','lambda_l2':'5','max_bin':'127','seed':'2026'}.items():
        import re
        val=re.search(r'\['+k+r': ([^\]]+)\]', native.read_text(encoding='utf-8')).group(1)
        assert float(val)==float(v),(k,val)
    s=synthetic(); put(w/'synthetic_causality.json',s)
    pipeline=Path(__file__); module=pipeline.with_name('train_only_features143_v1_20261011.py')
    for src in [pipeline,module,a.control_root/'evaluate.py' if a.control_root else ROOT/'evaluate.py']:
        shutil.copyfile(src,w/src.name)
    d={'status':'fixed_single_candidate_protocol_before_first_new_training_or_scoring',
       'frozen_at_local':now(),'run_id':RUN_ID,'candidate_count':1,
       'candidate':'Original63_LightGBM31_180_DirectReturn_seed2026',
       'choice_reason':'Simple direct one-day regression requested by the user; architecture and features fixed using a pre-revelation native-model hash, not historical TEST performance.',
       'pre_revelation_architecture_anchor':{'frozen_at_utc':p['frozen_at_utc'],
            'protocol_sha256':sha(old),'model_sha256':PRETEST_MODEL_SHA,
            'native_model_used_for_predictions_or_warm_start':False},
       'features':names,'params':PARAMS,'rounds':180,'years':[2020,2021,2022,2023,2024],
       'target':'Original TRAIN y_ret_1d; finite labels and positive finite current close; no label reconstruction, clipping, auxiliary targets or calibration.',
       'boundary':'For each annual validation, exclude the immediately previous market date; every fitted label end is strictly before first validation date. Final fit excludes last TRAIN date because its label may depend on TEST.',
       'postprocessing':'None; direct native-model return output for every row, including missing-price records.',
       'selection':'One candidate fixed before this run. Official continuous connected TRAIN score is diagnostic; no switching based on TEST scores.',
       'score_scope':'TRAIN_only_2020_2024_continuously_connected',
       'score_authority':'Unchanged official evaluate.py, no adapter or cached score.',
       'train_csv':str(a.train_csv),'train_csv_sha256':sha(a.train_csv),
       'evaluate_sha256':sha(w/'evaluate.py'),
       'source_sha256':{x.name:sha(w/x.name) for x in [pipeline,module]},
       'historical_test_feedback_not_erased':True,
       'new_design_not_claimed_to_be_the_exact_pre_revelation_complete_scheme':True,
       'current_run_test_outcomes_forbidden':True,
       'organizer_submission_eligibility_not_certified_by_this_record':True,
       'training_authorization':'训练符合要求的模型'}
    put(w/'protocol.json',d); (w/'protocol.sha256').write_text(sha(w/'protocol.json')+'\n',encoding='ascii')
    log(f'Protocol frozen {sha(w/"protocol.json")}')


def protocol(a):
    w=a.work_dir;d=read(w/'protocol.json')
    assert sha(w/'protocol.json')==(w/'protocol.sha256').read_text().strip()
    assert d['params']==PARAMS and d['candidate_count']==1
    for n,h in d['source_sha256'].items():assert sha(w/n)==h
    assert sha(w/'evaluate.py')==d['evaluate_sha256']
    return d


def build_train(a):
    guard(a,'build TRAIN-only features')
    w=a.work_dir; d=protocol(a)
    assert sha(a.train_csv)==d['train_csv_sha256']
    target=source(a.train_csv,True).select(KEYS+['y_ret_1d'])
    lf,names=features(source(a.train_csv,True))
    assert names==d['features']
    log('Building fresh causal 63-feature TRAIN parquet; TEST X is not opened.')
    path=w/'train_features.parquet'
    lf.join(target,on=KEYS,how='left',validate='1:1',maintain_order='left').sink_parquet(path,compression='zstd')
    dates=(pl.scan_parquet(path).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy())
    n=pl.scan_parquet(path).select(pl.len()).collect().item()
    assert n==7900350 and len(dates)==1699 and int(dates[-1])==20241231
    put(w/'train_features_manifest.json',{'rows':n,'days':len(dates),'sha256':sha(path),
                                        'TRAIN_csv_only':True,'TEST_X_opened':False,'label_not_a_feature':True})
    return dates


def fit(a, year, dates, final=False):
    guard(a,f'fit {"final" if final else year}')
    w=a.work_dir;d=protocol(a);names=d['features']
    tag='final' if final else str(year)
    meta_path=w/f'model_{tag}.json'; model_path=w/f'model_{tag}.txt'
    if meta_path.exists():
        meta=read(meta_path);assert meta['protocol_sha256']==sha(w/'protocol.json')
        assert sha(model_path)==meta['model_sha256'];log(f'Reusing verified completed fit {tag}')
        return lgb.Booster(model_str=model_path.read_text(encoding='utf-8'))
    if final:
        cutoff=int(dates[-1]);first_valid=20250102
    else:
        i=int(np.searchsorted(dates,year*10000+101));cutoff=int(dates[i-1]);first_valid=int(dates[i])
    lazy=pl.scan_parquet(w/'train_features.parquet')
    train=(lazy.filter((pl.col('trade_date')<cutoff)&pl.col('price_valid')&pl.col('y_ret_1d').is_finite())
           .select(names+['y_ret_1d','trade_date']).collect())
    last=int(train['trade_date'].max());end=int(dates[np.searchsorted(dates,last)+1])
    assert last<cutoff and end<first_valid
    count=len(train);x=matrix(train,names);y=train['y_ret_1d'].to_numpy()
    assert np.isfinite(y).all();del train;gc.collect()
    log(f'Fitting {tag}: {count:,} TRAIN rows, last observation={last}, last label end={end}, first prediction date={first_valid}')
    start=time.perf_counter();ds=lgb.Dataset(x,label=y,feature_name=names,free_raw_data=True)
    b=lgb.train(PARAMS,ds,num_boost_round=180)
    sample=x[:min(8192,len(x))].copy();before=b.predict(sample,num_threads=16)
    model_path.write_text(b.model_to_string(),encoding='utf-8',newline='\n')
    reloaded=lgb.Booster(model_str=model_path.read_text(encoding='utf-8'))
    exact(before,reloaded.predict(sample,num_threads=16))
    del x,y,ds,sample;gc.collect()
    put(meta_path,{'status':'completed_native_fit_and_reload_exact','training_rows':count,
        'first_training_date':20180102,'last_training_date':last,'last_training_label_end':end,
        'first_prediction_date':first_valid,'training_cutoff_exclusive':cutoff,
        'label_end_strictly_before_first_prediction_date':True,'model_sha256':sha(model_path),
        'protocol_sha256':sha(w/'protocol.json'),'rounds':b.current_iteration(),
        'seconds':time.perf_counter()-start,'completed_at_local':now(),
        'TEST_X_used_in_fit':False,'TEST_Y_used':False,'target':'one_day_return'})
    return reloaded


def folds(a, dates):
    w=a.work_dir;names=protocol(a)['features'];lazy=pl.scan_parquet(w/'train_features.parquet')
    for y in range(2020,2025):
        b=fit(a,y,dates)
        guard(a,f'infer TRAIN OOF {y}')
        valid=(lazy.filter(pl.col('trade_date').is_between(y*10000+101,y*10000+1231))
               .select(KEYS+names).sort('trade_date','ts_code').collect())
        x=matrix(valid,names);pred=b.predict(x,num_threads=16)
        assert np.isfinite(pred).all()
        reload=lgb.Booster(model_str=(w/f'model_{y}.txt').read_text(encoding='utf-8'))
        exact(pred,reload.predict(x,num_threads=16))
        valid.select(KEYS).with_columns(pl.Series('pred',pred)).write_parquet(w/f'oof_{y}.parquet',compression='zstd')
        del valid,x,b,reload,pred;gc.collect();log(f'OOF {y} completed and independently reloaded.')


def score(a):
    guard(a,'official TRAIN-only connected scoring')
    w=a.work_dir;protocol(a)
    p=w/'scoring_TRAIN_2020_2024';p.mkdir(exist_ok=True)
    oof=pl.concat([pl.scan_parquet(w/f'oof_{y}.parquet') for y in range(2020,2025)]).sort('trade_date','ts_code')
    assert oof.select(pl.len()).collect().item()==5635800
    oof.sink_csv(p/'submission.csv',float_precision=17)
    raw=source(a.train_csv,True).filter(pl.col('trade_date').is_between(20200101,20241231))
    raw.select(KEYS+['flag_limit_up']).sink_csv(p/'测试集_X.csv')
    # Original label decimal text is preserved instead of a Float32 feature cache label.
    raw_y=(pl.scan_csv(a.train_csv,schema_overrides={'ts_code':pl.String,'trade_date':pl.Int32,'y_ret_1d':pl.String},
                      null_values=['NaN','nan',''],low_memory=True)
           .filter(pl.col('trade_date').is_between(20200101,20241231)).select(KEYS+['y_ret_1d']))
    raw_y.sink_csv(p/'测试集_Y.csv')
    spec=importlib.util.spec_from_file_location('official_evaluate_143',w/'evaluate.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    result=m.evaluate(str(p/'submission.csv'),str(p))
    put(w/'official_TRAIN_metrics.json',{'status':'completed_uncached_unmodified_official_evaluate',
        'metrics':{k:float(v) for k,v in result.items()},'rows':5635800,'days':1212,
        'first':20200102,'last':20241231,'continuous_cross_year_turnover':True,
        'official_test_score':False,'actual_or_reconstructed_TEST_Y_used':False,
        'submission_sha256':sha(p/'submission.csv'),'evaluate_sha256':sha(w/'evaluate.py'),
        'protocol_sha256':sha(w/'protocol.json'),'completed_at_local':now()})
    log(f'Connected TRAIN score completed: {result["final_score"]:.10f}')


def seal(a, dates):
    assert (a.work_dir/'official_TRAIN_metrics.json').is_file()
    b=fit(a,2025,dates,True);del b;gc.collect()
    w=a.work_dir
    seal={'status':'final_return_model_and_all_training_choices_frozen_before_TEST_X_inference',
          'frozen_at_local':now(),'protocol_sha256':sha(w/'protocol.json'),
          'model_sha256':sha(w/'model_final.txt'),'metrics_sha256':sha(w/'official_TRAIN_metrics.json'),
          'TEST_X_opened_by_training_pipeline':False,'TEST_outcomes_used':False}
    put(w/'frozen_before_TEST_inference.json',seal)


def inference_features(a, limit=None):
    # Only the last 61 historical bars are needed for the maximum 60-row lag.
    train=source(a.train_csv,False)
    dates=train.select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    history=train.filter(pl.col('trade_date')>=int(dates[-61:][0])).select(RAW+['row_id'])
    test=source(a.test_x,False)
    if limit is not None:test=test.filter(pl.col('trade_date')<=limit)
    lf,names=features(pl.concat([history,test],how='vertical'))
    return lf.filter(pl.col('trade_date')>20241231),names


def infer(a):
    guard(a,'sealed model TEST-X causal inference')
    w=a.work_dir;d=protocol(a);s=read(w/'frozen_before_TEST_inference.json')
    assert sha(w/'model_final.txt')==s['model_sha256'] and sha(w/'protocol.json')==s['protocol_sha256']
    assert sha(w/'official_TRAIN_metrics.json')==s['metrics_sha256']
    b=lgb.Booster(model_str=(w/'model_final.txt').read_text(encoding='utf-8'))
    lf,names=inference_features(a);assert names==d['features']
    f=lf.sort('row_id').collect();x=matrix(f,names);pred=b.predict(x,num_threads=16)
    assert np.isfinite(pred).all() and len(pred)==1599600
    out=f.select(KEYS).with_columns(pl.Series('pred',pred))
    csv=w/'submission.csv';out.write_csv(csv,float_precision=17)
    parsed=pl.read_csv(csv,schema_overrides={'ts_code':pl.String,'trade_date':pl.Int32,'pred':pl.Float64})
    raw=source(a.test_x,False).select(KEYS).collect()
    assert parsed.columns==KEYS+['pred'] and parsed.select(KEYS).equals(raw)
    assert parsed.select(pl.struct(KEYS).n_unique()).item()==len(parsed)
    assert parsed['pred'].is_finite().all()
    dates=raw['trade_date'].unique().sort().to_numpy();cut=int(dates[79])
    prefix,names2=inference_features(a,cut);prefix=prefix.sort('row_id').collect()
    expected=f.filter(pl.col('trade_date')<=cut)
    assert expected.equals(prefix)
    p=b.predict(matrix(prefix,names),num_threads=16)
    exact(pred[:len(p)],p)
    independently_reloaded=lgb.Booster(model_str=(w/'model_final.txt').read_text(encoding='utf-8'))
    exact(pred,independently_reloaded.predict(x,num_threads=16))
    replay=w/'submission_replay.csv'
    f.select(KEYS).with_columns(pl.Series('pred',independently_reloaded.predict(x,num_threads=16))).write_csv(replay,float_precision=17)
    assert sha(replay)==sha(csv);replay.unlink()
    put(w/'verification.json',{'status':'passed_TRAIN_only_execution_native_reload_and_complete_TEST_X_submission',
        'rows':len(out),'days':len(dates),'codes':raw['ts_code'].n_unique(),
        'columns':out.columns,'keys_exact_in_original_order':True,'unique_keys':True,
        'all_predictions_finite':True,'prediction_semantics':'direct_future_one_day_return_regression',
        'native_model_reload_exact':True,'CSV_independent_replay_byte_exact':True,
        'cold80_feature_and_prediction_prefix_exact':True,'cold80_rows':len(prefix),
        'all5_OOF_models_and_final_labels_mature':True,
        'current_run_TEST_outcomes_read_or_reconstructed':False,
        'inherited_historical_winner_or_teacher':False,
        'single_candidate_predeclared':True,
        'pre_revelation_anchor_model_SHA256_verified':True,
        'entire_human_history_unviewed_not_claimed':True,
        'organizer_eligibility_not_certified':True,
        'official_TRAIN_score':read(w/'official_TRAIN_metrics.json')['metrics']['final_score'],
        'official_TEST_score':None,'submission_sha256':sha(csv),'TEST_X_sha256':sha(a.test_x),
        'final_model_sha256':sha(w/'model_final.txt'),'protocol_sha256':sha(w/'protocol.json'),
        'completed_at_local':now()})
    log('Full TEST-X keys, native reload, CSV replay and cold80 causality all passed.')


def package(a):
    guard(a,'package verified baseline')
    w=a.work_dir;v=read(w/'verification.json');assert v['status'].startswith('passed_')
    delivery=a.delivery_dir;delivery.mkdir(parents=True,exist_ok=True)
    names=['train_only_baseline143_v1_20261011.py','train_only_features143_v1_20261011.py',
           'evaluate.py','protocol.json','protocol.sha256','synthetic_causality.json',
           'model_final.txt','model_final.json','official_TRAIN_metrics.json',
           'frozen_before_TEST_inference.json','verification.json','submission.csv']
    for y in range(2020,2025):names += [f'model_{y}.txt',f'model_{y}.json']
    for n in names:shutil.copyfile(w/n,delivery/n)
    report=f'''# 固定训练内基线143：未来一天收益预测

这是用户在历史测试反馈问题确认后授权的新训练。采用测试收益揭示前已存在的63项量价特征和31叶、180轮LightGBM配置，直接拟合原始训练集的一天收益。新设计在本轮首次训练、评分前冻结，只有一个固定候选。

训练内部2020—2024年逐年向前预测连续连接，共1,212日、5,635,800行，未修改官方脚本的综合分为 **{v['official_TRAIN_score']:.10f}**。它不是比赛平台测试分，也不代表高于所有历史方案。每个年度及最终模型均剔除了边界上尚未成熟的标签；特征不读取标签，预处理不在验证/测试期拟合。

最终测试输入预测覆盖1,599,600行、344日、4,650只股票。保存模型重载、全量CSV独立重放和80日冷启动前缀检查已通过。pred是直接回归的一天收益率小数值。没有继承历史赢家模型、教师信号、成员与排序分离、后处理或收益校准。

限制：既有测试反馈及人类已接触测试信息的历史不能被抹去。预揭示哈希锚定的是架构和特征名，不是声称这一完整新方案早已在2026-09-28前冻结。本轮记录证明当前执行的数据边界与事前固定规则，比赛提交资格仍由组委会认定。旧37模型方案的选模合规更正继续有效。

## 重现推理

安装lightgbm、numpy、polars。将这份目录作为工作目录，运行（替换数据路径）：

```powershell
python -B -X utf8 train_only_baseline143_v1_20261011.py --stage infer --work-dir . --train-csv 'D:/路径/训练集.csv' --test-x 'D:/路径/测试集_X.csv'
```

训练与验证分阶段入口为freeze、train、score、final、infer、package；每次工作目录需要保留冻结协议。freeze需要原始历史哈希锚定目录。正常预测只依赖已保存最终模型和61日历史行情，不调用评分或读取测试答案。

submission.csv SHA256: {v['submission_sha256']}
'''
    (delivery/'README.md').write_text(report,encoding='utf-8',newline='\n')
    manifest={p.name:sha(p) for p in delivery.iterdir() if p.is_file() and p.suffix!='.zip'}
    put(delivery/'manifest.json',manifest)
    archive=delivery/'赛题五_固定训练内基线143_20261011.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in delivery.iterdir():
            if p.is_file() and p!=archive:z.write(p,p.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for n,h in manifest.items():assert hashlib.sha256(z.read(n)).hexdigest()==h
    put(w/'delivery.json',{'status':'verified_baseline_packaged','path':str(delivery),
        'archive':str(archive),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,
        'submission_sha256':sha(delivery/'submission.csv'),'official_TRAIN_score':v['official_TRAIN_score'],
        'models':6,'official_TEST_score':None,'competition_upload_performed':False})
    log(f'Verified delivery package ready: {delivery}')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--stage',choices=['freeze','train','score','final','infer','package','all'],required=True)
    p.add_argument('--work-dir',type=Path,default=Path('E:/赛题五_本机临时/固定训练内基线143_20261011'))
    p.add_argument('--train-csv',type=Path,default=ROOT/'data/raw/训练集.csv')
    p.add_argument('--test-x',type=Path,default=ROOT/'data/raw/测试集_X.csv')
    p.add_argument('--historical-root',type=Path,default=Path('D:/3.Study/数据分析/赛题五_历史归档_20261001'))
    p.add_argument('--control-root',type=Path)
    p.add_argument('--delivery-dir',type=Path,default=Path('E:/赛题五_最终提交/固定训练内基线143_20261011'))
    a=p.parse_args();a.work_dir=a.work_dir.resolve()
    if a.stage in ['freeze','all']:freeze(a)
    if a.stage in ['train','all']:
        dates=build_train(a) if not (a.work_dir/'train_features_manifest.json').exists() else pl.scan_parquet(a.work_dir/'train_features.parquet').select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
        assert sha(a.work_dir/'train_features.parquet')==read(a.work_dir/'train_features_manifest.json')['sha256']
        folds(a,dates)
    if a.stage in ['score','all']:score(a)
    if a.stage in ['final','all']:
        dates=pl.scan_parquet(a.work_dir/'train_features.parquet').select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
        seal(a,dates)
    if a.stage in ['infer','all']:infer(a)
    if a.stage in ['package','all']:package(a)


if __name__=='__main__':
    main()
