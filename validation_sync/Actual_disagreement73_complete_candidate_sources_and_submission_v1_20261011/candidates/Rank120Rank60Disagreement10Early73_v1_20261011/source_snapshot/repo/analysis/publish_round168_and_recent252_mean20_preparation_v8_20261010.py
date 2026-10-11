"""Publish the actual independent Huber restart controls, before any quality claim."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys, os, gzip, hashlib, time
A=Path(__file__).resolve().parent; ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    read(A/'current_user_runtime_control_20261009.json')
    control=read(A/'current_user_runtime_control_20261010.json')
    assert control['status']=='optimization_active_after_explicit_manual_resume'
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    assert len(read(A/'recent252_forward20_mature_population_actual_CPU_controls_v1_20261010.json')['records'])==7
    paths=[Path(__file__),ROOT/'后续选模标准.md']+[A/name for name in ['prepare_RecentReturn252Protected168_complete67_v1_20261010.py', 'prepare_protected168_full_registry_sources_v1_20261010.py', 'protected168_candidate_sources_preparation_v2_20261010.json', 'protected168_full_registry_source_preparation_v1_20261010.json', 'RecentReturn252Protected168_actual_own_bank_pointer_correction_v1_20261010.json', 'prepare_protected168_selected_candidate_v4_20261010.py', 'run_RecentReturn252Protected168_complete_family_v1_20261010.py', 'run_RecentReturn252Protected168_full_registration_v1_20261010.py', 'verify_RecentReturn252Protected168_full67_preflight_v1_20261010.py', 'recent252_forward20_mature_training_population_v1_20261010.py', 'verify_recent252_forward20_mature_population_v1_20261010.py', 'recent252_forward20_mature_population_actual_CPU_controls_v1_20261010.json', 'prepare_Recent252Forward20_own_bank_sources_v1_20261010.py', 'Recent252Forward20Huber050_own_bank_controls_source_admission_v1_20261010.json', 'actual_Recent252Forward20Huber050_past_fixture_location_v2_20261010.json', 'run_recent252_forward20_own_controls_and_training_queue_v1_20261010.py', 'shared_string_pack_full167_benchmark_location_v1_20261010.json']]
    paths.extend(Path(p) for p in read(A/'Recent252Forward20Huber050_own_bank_controls_source_admission_v1_20261010.json')['input_sha256'])
    paths.extend([Path('E:/赛题五_本机临时/shared_string_pack_full167_benchmark_v1_20261010')/n for n in ('frozen_before_actual_benchmark.json','original_result.json','proposed_result.json','verification.json')])
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/round168_and_recent252_mean20_preparation_v8_20261010'); payload={}; bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest()
        rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix(); data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'passed7_joint_recent252_mean20_population_CPU_cases_real49153_fixture_and_completed_nonadopted_full_pack_benchmark_round168_sources_compiled','files':bindings,'new_recent252_mean20_GPU_and_round168_full_candidate_completion_not_claimed':True,'new_quality_scores_by_publication':0,'test_labels_read':False,'deadline_local':control['stop_at_local']})
    out=Path('E:/赛题五_本机临时/round168_and_recent252_mean20_preparation_main_v8_20261010');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    from owned_idle_publication_wait_runtime_v1_20261010 import hold as suspended_idle
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire()
        assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(read(A/'current_user_runtime_control_20261010.json')['stop_at_local'])
        launch=read(A/'service_owned_workflows_20261006/main_publisher_v11_20261010/native_launch.json')
        parent,worker,idle=suspended_idle(launch,'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;h.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存第168轮完整验证准备、近期252日与20日收益联合方案7项CPU检查及49153真实样本、完整榜编码未采用基准结果',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'round168_and_recent252_mean20_preparation_main_receipt_v8_20261010.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
