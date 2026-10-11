"""Audit the real complete baseline CSV and byte-exact prior official score reuse."""
from pathlib import Path
from datetime import datetime
import hashlib
import importlib.metadata
import json
import os
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
OUT=A/'reference66_full_baseline_csv_qa_20261005'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def create(path,value):
    with Path(path).open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)
def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')


def main():
    assert not OUT.exists()
    import psutil
    import polars as pl
    job=read(A/'reference66_linear_leaf_quality_followups_20261005/verification.json')['quality_rounds'][0]
    worker=psutil.Process(job['owned_worker_pid'])
    assert worker.create_time()==job['owned_worker_creation_time'] and worker.cmdline()[-2:]==job['script_args']
    assert not Path(job['stderr']).read_bytes()
    folder=A/'optimization_20261003_r81'
    csv=folder/'scoring_validation_only/submission.csv'
    stat_before=csv.stat()
    events=[json.loads(line) for line in (folder/'identical_official_scores/events.jsonl').read_text(encoding='utf-8').splitlines() if line]
    assert len(events)==1 and events[0]['cache_hit'] is True
    event=events[0]
    source=Path(event['official_metrics_source'])
    entry=read(source)
    protocol=read(folder/'protocol.json')
    assert protocol['explicit_parent_round']==66 and protocol['expected_scored_records']==124
    selection=A/'optimization_20261003_r66/selection.json'
    expected=read(selection)['winner']['metrics']
    assert entry['metrics']==expected
    assert hashlib.sha256(canonical(entry['metrics'])).hexdigest()==entry['metrics_sha256']
    assert hashlib.sha256(canonical(entry['scope'])).hexdigest()==event['cache_key']
    assert sha(csv)==entry['scope']['submission_csv_sha256']
    paths=[folder/'scoring_validation_only/测试集_X.csv',folder/'scoring_validation_only/测试集_Y.csv',
        ROOT/'evaluate.py',ROOT/'src/scoring.py',A/'identical_official_score_cache_20261003.py']
    for path in paths:assert sha(path)==entry['scope']['inputs_sha256'][path.name],path
    for name,version in entry['scope']['versions'].items():assert importlib.metadata.version(name)==version
    for filename in ('测试集_X.csv','测试集_Y.csv'):
        assert os.path.samefile(folder/'scoring_validation_only'/filename,A/'optimization_20261003_r66/scoring_validation_only'/filename)
    counts=pl.scan_csv(csv).select(pl.len().alias('rows'),pl.col('trade_date').n_unique().alias('days'),
        pl.col('ts_code').n_unique().alias('codes'),pl.col('pred').is_finite().all().alias('all_finite'),
        pl.col('trade_date').min().alias('first'),pl.col('trade_date').max().alias('last')).collect().to_dicts()[0]
    assert (counts['rows'],counts['days'],counts['codes'])==(5635800,1212,4650) and counts['all_finite']
    assert 20200101<=counts['first']<=counts['last']<=20241231
    stat_after=csv.stat()
    assert (stat_before.st_size,stat_before.st_mtime_ns)==(stat_after.st_size,stat_after.st_mtime_ns)
    assert sha(csv)==entry['scope']['submission_csv_sha256']
    files=[Path(__file__),source,selection,folder/'protocol.json',*paths,csv]
    bindings={str(path):sha(path) for path in files}
    OUT.mkdir()
    create(OUT/'verification.json',{'status':'passed_actual_full5635800_baseline_csv_and_exact_official_capsule_reuse',
        'at_local':datetime.now().isoformat(timespec='seconds'),'explicit_parent_round':66,'actual_round':81,
        'csv':str(csv),'csv_sha256':entry['scope']['submission_csv_sha256'],'counts':counts,
        'all8_actual_official_metrics_exact':True,'metrics':entry['metrics'],
        'actual_cached_official_scope_key':event['cache_key'],'actual_reuse_event':event,
        'actual_csv_validation_X_Y_scorer_and_runtime_versions_checked':True,
        'real_test_labels_read':False,'validation_labels_shared_with_qualified_R66_only':True,
        'new_candidate_configurations_scored':0,'fresh_official_scorer_calls':0,
        'matched_full_output_official_replay_controls':1,'new_candidate_quality_scores_and_future_component_checks_pending':True,
        'source_sha256':bindings,'no_new_claim_of_complete_round_or_resource_boundary':True})
    print(json.dumps({'status':'passed_actual_full_baseline_csv','score':entry['metrics']['final_score'],'counts':counts,
        'byte_exact_existing_official_score_reuse':True},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
