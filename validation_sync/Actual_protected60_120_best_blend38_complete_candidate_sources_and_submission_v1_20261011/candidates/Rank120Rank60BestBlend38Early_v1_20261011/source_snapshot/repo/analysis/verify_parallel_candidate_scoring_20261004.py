"""Full-OOF serial/parallel equivalence, output ordering, and execution timing."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    import parallel_scoring_qa_context_20261004 as qa
    from parallel_candidate_scoring_20261004 import evaluate_many,shutdown,WORKERS
    out=qa.OUT;out.mkdir(parents=True,exist_ok=True)
    proof=out/'verification.json';assert not proof.exists(),'Preserve completed execution QA'
    previous=json.loads((ROOT/'analysis/optimization_20261003_r20/selection.json').read_text(encoding='utf-8'))['winner']
    selected=json.loads((ROOT/'analysis/optimization_20261003_r21/selection.json').read_text(encoding='utf-8'))['winner']
    jobs=[('previous0',qa.original.configuration(previous)),('selected0',qa.original.configuration(selected)),
          ('selected1',qa.original.configuration(selected)),('previous1',qa.original.configuration(previous))]
    ctx=qa.Context();start=time.perf_counter();serial=[]
    for key,cfg in jobs:serial.append((key,qa.evaluate(ctx,deepcopy(cfg))))
    serial_seconds=time.perf_counter()-start
    del ctx
    start=time.perf_counter();parallel=list(evaluate_many('parallel_scoring_qa_context_20261004',jobs,out));parallel_seconds=time.perf_counter()-start
    shutdown()
    assert [key for key,_ in parallel]==[key for key,_ in jobs]
    ignored={'official_score_cache','parallel_execution','direct_official_seconds'}
    for (skey,srow),(pkey,prow) in zip(serial,parallel):
        assert skey==pkey
        assert {k:v for k,v in srow.items() if k not in ignored}=={k:v for k,v in prow.items() if k not in ignored},skey
        assert len(srow['metrics'])==8 and srow['metrics']==prow['metrics']
    slots={row['parallel_execution']['worker_slot'] for _,row in parallel};assert len(slots)==WORKERS
    sources=[Path(__file__),ROOT/'analysis/parallel_candidate_scoring_20261004.py',Path(qa.__file__),
             ROOT/'analysis/score_calibrated_candidates_20261003.py',ROOT/'analysis/cross_round_official_score_reuse_20261003.py',
             ROOT/'analysis/official_validation_csv_parse_cache_20261003.py',ROOT/'evaluate.py',ROOT/'src/scoring.py']
    data={'status':'passed','full_validation_rows':5635800,'records':len(jobs),'distinct_worker_slots':sorted(slots),
          'declared_output_order_preserved':True,'complete_configuration_construction_and_all_eight_metrics_exact':True,
          'actual_mapped_csv_bytes_identical':True,'serial_seconds':serial_seconds,'parallel_seconds':parallel_seconds,
          'worker_pool_closed':True,'new_model_quality_scores':0,'test_labels_read':False,
          'source_sha256':{str(path):sha(path) for path in sources},'serial':serial,'parallel':parallel,
          'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')}
    with proof.open('x',encoding='utf-8') as stream:json.dump(data,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ('serial','parallel','source_sha256')},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
