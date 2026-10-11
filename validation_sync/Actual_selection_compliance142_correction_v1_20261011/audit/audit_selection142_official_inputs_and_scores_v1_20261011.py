"""Bounded selection audit: unchanged official evaluator, TRAIN data only, no models."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import os,sys,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
OUT=Path('E:/赛题五_本机临时/选模标准审计142_20261011')
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[name]='4'
scratch=OUT/'tmp';scratch.mkdir(exist_ok=True)
for name in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[name]=str(scratch)
import tempfile;tempfile.tempdir=str(scratch)

def sha(p):
    digest=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(4*1024**2),b''):digest.update(chunk)
    return digest.hexdigest()

def save(p,data):
    raw=(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf8')
    with Path(p).open('xb') as f:f.write(raw)

def control():
    state=[json.loads((A/f'current_user_runtime_control_202610{d}.json').read_text(encoding='utf8')) for d in ('10','09')]
    assert all(not s['automatic_restart_enabled'] for s in state)
    return {'local_time':datetime.now(timezone(timedelta(hours=8))).isoformat(),'optimization_control':[s['status'] for s in state],'authorization':'用户指出训练、测试使用或评分口径不符合后续选模标准；仅复核已选方案，不恢复优化队列'}

def main():
    import polars as pl,numpy as np
    import evaluate
    proof=A/'Rank120Rank60ConsensusFraction8Early101_selected_release_v1_20261011/calibrated_csv_official.json'
    selected=Path('E:/赛题五_本机临时/60与120日保护比例8项完整候选101_20261011/selected_scoring/scoring_validation_only')
    submission=selected/'submission.csv';expected=json.loads(proof.read_text(encoding='utf8'))
    assert sha(submission)==expected['csv_sha256']
    names=[ROOT/'evaluate.py',ROOT/'后续选模标准.md',ROOT/'data/raw/训练集.csv',submission,selected/'测试集_X.csv',selected/'测试集_Y.csv',proof,Path(__file__)]
    pins={str(p):sha(p) for p in names}
    save(OUT/'frozen_audit_before_uncached_official_calls.json',{'control':control(),'pins':pins,'actual_test_Y_read':False,'training_or_prediction_started':False,'comparison':'existing_final_validation_CSV_on_cached_TRAIN_labels_vs_original_decimal_text_TRAIN_labels','official_evaluator_runtime_adapters':[]})
    rawdir=OUT/'original_TRAIN_text_inputs';rawdir.mkdir(exist_ok=False)
    # Read labels as strings to preserve every provided decimal digit and NA token.
    raw=pl.scan_csv(ROOT/'data/raw/训练集.csv',schema_overrides={'trade_date':pl.Int32,'y_ret_1d':pl.String,'flag_limit_up':pl.Int64}).filter(pl.col('trade_date').is_between(20200101,20241231)).select('ts_code','trade_date','y_ret_1d','flag_limit_up').collect(engine='streaming')
    assert raw.height==5635800 and raw.select('ts_code','trade_date').n_unique()==5635800
    assert raw['trade_date'].n_unique()==1212 and raw['ts_code'].n_unique()==4650
    raw.select('ts_code','trade_date','flag_limit_up').write_csv(rawdir/'测试集_X.csv')
    raw.select('ts_code','trade_date','y_ret_1d').write_csv(rawdir/'测试集_Y.csv')
    input_stats={'rows':raw.height,'days':raw['trade_date'].n_unique(),'first':raw['trade_date'].min(),'last':raw['trade_date'].max(),'labels_preserved_as_original_text':True,'actual_test_Y_read':False}
    del raw
    import gc;gc.collect()
    results=[]
    for name,folder in [('cached_TRAIN_input',selected),('original_TRAIN_decimal_text',rawdir)]:
        current=control();print({'phase':'unchanged_official_evaluator','input':name,'at':current['local_time']},flush=True)
        started=time.monotonic();metrics={k:float(v) for k,v in evaluate.evaluate(str(submission),str(folder)).items()}
        assert all(np.isfinite(v) for v in metrics.values())
        row={'input':name,'metrics':metrics,'seconds':time.monotonic()-started,'control':current,'X_sha256':sha(folder/'测试集_X.csv'),'Y_sha256':sha(folder/'测试集_Y.csv')}
        save(OUT/(name+'_uncached_official.json'),row);results.append(row);print(row,flush=True)
    delta={k:results[1]['metrics'][k]-results[0]['metrics'][k] for k in expected['metrics']}
    baseline_delta={k:results[0]['metrics'][k]-expected['metrics'][k] for k in expected['metrics']}
    for p,digest in pins.items():assert sha(p)==digest,p
    status={'status':'completed_two_uncached_unchanged_official_calls_TRAIN_only','official_evaluator_sha256':pins[str(ROOT/'evaluate.py')],'source_inputs':input_stats,'cached_metrics_minus_published':baseline_delta,'original_text_metrics_minus_cached':delta,'results':results,'selected_validation_CSV_unchanged':True,'real_test_labels_read':False,'new_training':0,'new_model_inference':0,'optimization_queue_resumed':False}
    save(OUT/'verification.json',status);print(status,flush=True)

if __name__=='__main__':main()
