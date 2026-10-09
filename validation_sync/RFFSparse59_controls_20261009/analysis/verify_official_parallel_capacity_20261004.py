"""Measure official scorer capacity on one frozen, previously scored OOF CSV."""
from concurrent.futures import ProcessPoolExecutor,wait,FIRST_COMPLETED
from pathlib import Path
import multiprocessing
import os
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
QA=ROOT/'analysis/official_parallel_capacity_qa_20261004'


def work(job):
    from evaluate import evaluate
    import psutil
    number,slot=job;folder=QA/f'workers{number}'/f'worker{slot}'
    started=time.perf_counter()
    result={key:float(value) for key,value in evaluate(str(folder/'submission.csv'),str(folder)).items()}
    return {'pid':os.getpid(),'seconds':time.perf_counter()-started,
            'rss_at_return':psutil.Process().memory_info().rss,'metrics':result}


def main():
    from optimize_training_round22 import read,dump,sha
    import psutil
    gate=ROOT/'analysis/stacking_future_pipelines_qa_20261004/verification.json'
    while not gate.exists():time.sleep(10)
    assert read(gate)['status']=='passed'
    source=ROOT/'analysis/optimization_20261003_r22/scoring_validation_only'
    expected=read(source.parent/'calibrated_csv_official.json')
    submission=source.parent/'calibrated_validation.csv'
    if not submission.exists():
        candidates=[p for p in source.glob('*.csv') if p.name not in ('测试集_X.csv','测试集_Y.csv') and sha(p)==expected['csv_sha256']]
        assert len(candidates)==1,candidates;submission=candidates[0]
    assert sha(submission)==expected['csv_sha256']
    sources=[Path(__file__),ROOT/'evaluate.py',ROOT/'src/scoring.py',submission,
             source/'测试集_X.csv',source/'测试集_Y.csv',source.parent/'calibrated_csv_official.json']
    protocol=QA/'diagnostic_frozen_before_scoring.json'
    assert not protocol.exists()
    dump(protocol,{'status':'frozen_execution_control','workers':(2,3,4),'jobs_each': 'two times worker count',
         'source':'Same complete 5635800-row mature-label annual OOF CSV already selected andscored inR22',
         'other_active_work':'R23 continues withtwo scoring processes; measured times include that concurrent workload.',
         'memory_reserve_bytes':4*1024**3,'minimum_available_before_launch':'4GiB reserve plus1.5GiB per measured worker',
         'new_model_scores':0,'test_labels_read':False,
         'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    results=[]
    for number in (2,3,4):
        available=psutil.virtual_memory().available
        required=(4+1.5*number)*1024**3
        if available<required:
            results.append({'workers':number,'status':'not_launched_for_current_memory_budget','available_bytes':available,'required_bytes':required})
            continue
        for slot in range(number):
            folder=QA/f'workers{number}'/f'worker{slot}';folder.mkdir(parents=True,exist_ok=True)
            for name,original in [('submission.csv',submission),('测试集_X.csv',source/'测试集_X.csv'),('测试集_Y.csv',source/'测试集_Y.csv')]:
                os.link(original,folder/name)
        started=time.perf_counter();samples=[];jobs=[]
        with ProcessPoolExecutor(max_workers=number,mp_context=multiprocessing.get_context('spawn')) as pool:
            pending={pool.submit(work,(number,i%number)) for i in range(2*number)}
            while pending:
                completed,pending=wait(pending,timeout=.25,return_when=FIRST_COMPLETED)
                rss=0
                for process in pool._processes.values():
                    try:rss+=psutil.Process(process.pid).memory_info().rss
                    except psutil.NoSuchProcess:pass
                samples.append({'available_bytes':psutil.virtual_memory().available,'worker_rss_sum':rss})
                jobs.extend(future.result() for future in completed)
        seconds=time.perf_counter()-started
        assert len(jobs)==2*number and all(job['metrics']==expected['metrics'] for job in jobs)
        result={'status':'passed','workers':number,'jobs':len(jobs),'total_seconds_including_spawn_and_shutdown':seconds,
                'records_per_minute':len(jobs)*60/seconds,'minimum_available_bytes_sampled':min(s['available_bytes'] for s in samples),
                'maximum_worker_rss_sum_sampled':max(s['worker_rss_sum'] for s in samples),'all_eight_metrics_bit_identical':True,
                'jobs_details':jobs,'sampling_interval_seconds':.25}
        results.append(result);dump(QA/f'workers{number}_result.json',result,immutable=True)
        print(f'Official capacity {number}workers: {seconds:.2f}s, {result["records_per_minute"]:.2f}records/min, metrics exact',flush=True)
    for path,digest in read(protocol)['input_sha256'].items():assert sha(path)==digest,path
    dump(QA/'verification.json',{'status':'passed','execution_controls':results,'new_model_scores':0,'test_labels_read':False,
         'diagnostic_freeze_sha256':sha(protocol),'global_search_exhaustion_established':False,
         'scope':'Official CSV parsing/scoring capacity under concurrentR23 workload; no forecast construction or model-training throughput claim.'},immutable=True)


if __name__=='__main__':main()
