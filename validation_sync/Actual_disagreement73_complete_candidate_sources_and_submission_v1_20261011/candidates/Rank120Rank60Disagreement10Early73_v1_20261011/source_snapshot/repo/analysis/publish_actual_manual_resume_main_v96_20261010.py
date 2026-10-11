"""Publish verified resume, new deadline and every157 preparation artifact to main."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import os,sys,gzip,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    control=read(A/'current_user_runtime_control_20261010.json')
    assert datetime.now(timezone(timedelta(hours=8)))<datetime.fromisoformat(control['stop_at_local'])
    import publish_classifier_consensus_workflows_20261006 as h
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
    out=Path('E:/赛题五_本机临时/manual_resume_main_v96_20261010');out.mkdir(exist_ok=False)
    sources=[Path(__file__),ROOT/'AGENTS.md',A/'current_user_runtime_control_20261010.json',
        A/'current_user_runtime_control_20261009.json',A/'current_user_runtime_control_20261008.json',
        A/'manual_resume_saved_artifact_verification_v1_20261010.json']
    for pattern in ('*BF16FlagAfter152*.py','*BF16FlagAfter152*.json','*manual_resume*20261010.py','*manual_resume*20261010.json',
                    '*progress*v6_20261010.py','*import*20261010.py','*import*20261010.json','*overlap*20261010.py','*overlap*20261010.json','*byte_exact*20261010.py','*byte_exact*20261010.json','*QA*20261010.py','*QA*20261010.json','*runtime_handoff*20261010.json','*cold80*20261010.py','*cold80*20261010.json','*BF16Drop05*20261010.py','*BF16Drop05*20261010.json','*registration*20261010.json','*watcher*20261010.py','*stop1100*20261011.py','*resumed*20261010.py','*resumed*20261010.json','*ReusedNN*.py','*ReusedNN*.json','*reused*20261010.py','*reused*20261010.json','*continuous*20261010.py','*continuous*20261010.json'):
        sources.extend(p for p in A.glob(pattern) if p.is_file())
    sources.extend((A/'user_requested_stop1100_until_manual_continue_v1_20261011').glob('*.json'))
    sources.extend((A/'manual_resume_idle_dependency_handoff_v2_20261010').glob('*.json'))
    sources.extend((A/'manual_resume_dispatcher_handoff_v3_20261010').glob('*.json'))
    for folder in A.glob('ReusedNN158_*preflight_failure*'):
        if folder.is_dir():sources.extend(p for p in folder.glob('*') if p.is_file())
    sources.extend((A/'failed_dependency_and_cold80_recovery_v2_20261010').glob('*.json'))
    sources.extend(p for p in (A/'failed_dependency_and_cold80_recovery_v2_20261010/original_service_records').rglob('*') if p.is_file() and p.name in ('service_execution.json','job_definition.json','native_launch.json','stderr.log'))
    sources.extend((A/'progress_observer_handoff_v3_20261010').glob('*.json'))
    sources.extend((A/'pending_full_QA_path_hardening_v1_20261010').glob('*.json'))
    sources.extend((A/'continuous_fast_controller_handoff_v7_20261010').glob('*.json'))
    sources.extend((A/'progress_observer_handoff_v5_20261010').glob('*.json'))
    sources.extend((A/'actual157_import_failure_recovery_v1_20261010').glob('*.json'))
    sources.extend(p for p in (A/'actual157_import_failure_recovery_v1_20261010/original_service_records').rglob('*') if p.is_file() and p.name in ('service_execution.json','job_definition.json','native_launch.json','stderr.log'))
    sources.extend((A/'actual157_independent_controls_publication_overlap_v1_20261010').glob('*.json'))
    sources.extend((A/'progress_observer_handoff_v6_20261010').glob('*.json'))
    sources=list(dict.fromkeys(sources));prefix=Path('validation_sync/manual_resume_fast_optimization_v96_20261010')
    payload={};bindings={}
    for p in sources:
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix();blob=raw
        if len(blob)>=5*1024**2:blob=gzip.compress(blob,mtime=0);target+='.gz';assert gzip.decompress(blob)==raw
        assert len(blob)<95*1024**2;payload[target]=blob;bindings[str(p)]={'published_path':target,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({'status':'manual_resume_with_actual_saved_artifact_hashes_and_new_deadline',
        'files':bindings,'deadline_local':control['stop_at_local'],'completed_annual_fits_reused':5,
        'actual157_prospective_sources':40,'actual157_graph_controls':380,'actual158_prospective_sources':48,'actual158_graph_controls':456,'actual159_prospective_sources':16,'actual159_graph_controls':152,'actual160_prospective_sources':16,'actual160_graph_controls':152,'controller_version':8,'actual_import_scope_recovery':read(A/'actual157_import_failure_recovery_v1_20261010/verification.json'),'whole_board_byte_exact_speed_proof':read(A/'byte_exact_ranking_stream_benchmark_v1_20261010.json'),'future_QA_directory_resolver_version':44,'repair_reason':'156 had81 actual quality records but consumer expected80; eighteen dependent tasks exited before science; corrected cold80 report consumption and preserved old records','actual156_score_records':81,'registration_operator_correction_changes_science':False,'new_scores_by_publication':0,
        'test_labels_read':False,'global_exhaustion_not_proven':True})
    create(out/'frozen_before_publication.json',{'files':bindings})
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire()
        launch=read(A/'service_owned_workflows_20261006/main_publisher_v11_20261010/native_launch.json')
        parent,worker,idle=suspended_idle(launch,'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;previous=sync.git('rev-parse','HEAD');h.verify_main(previous);assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','恢复单机断点优化并改截止为10月11日11点，同步收益映射导入验证、零评分失败保存及14项依赖恢复，保留成熟控制并继续官方评分',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            value={'status':'pushed_and_remote_head_verified','commit':commit,'branch':'main','raw_git_blobs_verified':len(hashes),
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',value);create(A/'actual_manual_resume_main_v96_receipt_20261010.json',value);print(value,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
