"""Four full prediction workers against the already frozen serial full-OOF proof."""
from copy import deepcopy
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]


def main():
    import json
    import psutil
    import parallel_scoring_four_qa_context_20261004 as qa
    import parallel_candidate_scoring_four_20261004 as pool
    from optimize_training_round21 import read,dump,sha
    gate=ROOT/'analysis/official_parallel_capacity_qa_20261004/verification.json'
    assert read(gate)['status']=='passed'
    assert next(r for r in read(gate)['execution_controls'] if r['workers']==4)['status']=='passed'
    original_proof=ROOT/'analysis/parallel_candidate_scoring_qa_20261004/verification.json'
    old=read(original_proof);assert old['status']=='passed'
    for path,digest in old['source_sha256'].items():assert sha(path)==digest,path
    serial=old['serial'];jobs=[(key,qa.original.configuration(row)) for key,row in serial]
    out=qa.OUT;out.mkdir(parents=True,exist_ok=True);assert not (out/'verification.json').exists()
    sources=[Path(__file__),Path(qa.__file__),Path(pool.__file__),original_proof,gate,
             ROOT/'analysis/score_calibrated_candidates_20261003.py',ROOT/'evaluate.py',ROOT/'src/scoring.py']
    dump(out/'diagnostic_frozen_before_scoring.json',{'status':'frozen_execution_control','workers':4,
         'records':[key for key,_ in jobs],'comparison':'Frozen original serial proof on full5635800-row OOF andactual emitted mapped CSV',
         'new_model_quality_scores':0,'test_labels_read':False,
         'source_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    start=time.perf_counter();parallel=[];samples=[]
    for key,row in pool.evaluate_many('parallel_scoring_four_qa_context_20261004',jobs,out):
        parallel.append((key,row));samples.append({'available_bytes':psutil.virtual_memory().available,
         'worker_rss':{pid:psutil.Process(pid).memory_info().rss for pid in {r['parallel_execution']['worker_pid'] for _,r in parallel}}})
    seconds=time.perf_counter()-start;pool.shutdown()
    assert [key for key,_ in parallel]==[key for key,_ in serial]
    for (skey,srow),(pkey,prow) in zip(serial,parallel):
        assert skey==pkey and srow['metrics']==prow['metrics'] and len(prow['metrics'])==8
        assert qa.original.configuration(srow)==qa.original.configuration(prow)
        assert srow['construction']==prow['construction']
        assert srow['actual_mapped_csv_sha256']==prow['actual_mapped_csv_sha256']
    slots={row['parallel_execution']['worker_slot'] for _,row in parallel};assert len(slots)==4
    dump(out/'verification.json',{'status':'passed','full_validation_rows':5635800,'workers':4,'records':len(jobs),
         'declared_output_order_preserved':True,'complete_configuration_construction_and_all_eight_metrics_exact':True,
         'actual_mapped_csv_bytes_identical':True,'worker_pool_closed':True,'new_model_quality_scores':0,'test_labels_read':False,
         'parallel_seconds_under_concurrent_R23_workload':seconds,'memory_samples_at_results':samples,
         'source_sha256':{str(p.resolve()):sha(p) for p in sources},'parallel':parallel,
         'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print(f'Four full prediction workers passed: all configuration/construction,8 metrics andactual CSV hashes exact, {seconds:.2f}s',flush=True)


if __name__=='__main__':main()
