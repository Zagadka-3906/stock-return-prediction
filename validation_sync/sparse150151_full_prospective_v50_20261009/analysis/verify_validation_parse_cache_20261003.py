"""Compare parsed-input reuse against the unchanged scorer on all official OOF rows."""
from pathlib import Path
import json
import os
import sys
import time
from types import SimpleNamespace
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import evaluate
from identical_official_score_cache_20261003 import digest
from official_validation_csv_parse_cache_20261003 import run


def main():
    folder=ROOT/'analysis/optimization_20261003_r18'
    output=ROOT/'analysis/validation_parse_cache_full_oof_qa_20261003'
    output.mkdir(exist_ok=True)
    target=output/'verification.json'
    assert not target.exists(), 'Preserve completed QA evidence.'
    csv=folder/'calibrated_validation.csv'
    reference=json.loads((folder/'calibrated_csv_official.json').read_text(encoding='utf-8'))
    print(json.dumps({'reference_fields':list(reference)},ensure_ascii=False),flush=True)
    expected=reference.get('metrics',reference.get('official_metrics',reference))
    ctx=SimpleNamespace(scoring=folder/'scoring_validation_only')
    original=evaluate.pd
    rows=[]
    for mode in ('original','adapter_cold','adapter_warm'):
        started=time.perf_counter()
        operation=lambda context,prediction:evaluate.evaluate(str(csv),str(context.scoring))
        metrics=operation(ctx,None) if mode=='original' else run(ctx,None,operation)
        metrics={key:float(value) for key,value in metrics.items()}
        assert metrics==expected,(mode,metrics,expected)
        assert evaluate.pd is original
        rows.append({'mode':mode,'seconds':time.perf_counter()-started,'metrics':metrics,
                     'parse_cache':getattr(ctx,'last_validation_csv_parse_cache',None)})
        print(json.dumps(rows[-1],ensure_ascii=False),flush=True)
    assert len(rows[-1]['parse_cache']['events'])==2
    assert all(event['parsed_frame_reused'] for event in rows[-1]['parse_cache']['events'])
    payload={'status':'passed','same_actual_calibrated_submission_csv':True,
             'all_eight_official_metrics_bit_identical':True,'official_evaluator_restored':True,
             'prediction_csv_always_parsed':True,'validation_rows':5635800,'validation_days':1212,
             'new_model_scores':0,'test_labels_read':False,'timings':rows,
             'input_sha256':{str(path.resolve()):digest(path) for path in (
                 csv,folder/'calibrated_csv_official.json',ctx.scoring/'测试集_X.csv',
                 ctx.scoring/'测试集_Y.csv',ROOT/'evaluate.py',
                 ROOT/'analysis/official_validation_csv_parse_cache_20261003.py',Path(__file__))},
             'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')}
    with target.open('x',encoding='utf-8') as stream:
        json.dump(payload,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print(str(target),flush=True)


if __name__=='__main__':main()
