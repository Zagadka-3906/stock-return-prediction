"""Publish actual CPU epoch-resume controls and the preserved failed first attempt to main."""
from pathlib import Path
from datetime import datetime
import hashlib,sys,time
import psutil
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers
OUT=A/'signed132_actual_import_recovery_github_20261007'

def main():
    proof_path=A/'signed132_actual_import_and_publication_recovery_v2_20261007.json';proof=read(proof_path)
    assert proof['status']=='resolved_actual_signed132_executor_import_and_publication_metadata_before_any_scores'
    sources=[Path(__file__),A/'prepare_signed132_recovery_main_and_live_monitor_v29_20261007.py',proof_path,A/'signed132_recovered_actual_hidden_queue_launch_v2_20261007.json',*[Path(p) for p in proof['input_sha256']]]
    sources=list(dict.fromkeys(sources));pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    for p,d in pins.items():assert sha(p)==d,p
    assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_actual_main_publication.json',{'input_sha256':pins,'signed_scheme_not_yet_officially_scored_or_adopted':True,'new_quality_scores':0})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        while any(psutil.Process(pid).status()==psutil.STATUS_STOPPED for pid in (row['pid'],row['owned_worker_pid'])):
            assert time.time()<datetime.fromisoformat('2026-10-07T23:45:00+08:00').timestamp()
            time.sleep(10)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/signed132_actual_import_recovery_20261007')
            payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for path in [*sources,OUT/'frozen_before_actual_main_publication.json']:
                data=path.read_bytes();assert not sync.SECRET.search(data),path
                target=(prefix/path.relative_to(ROOT)).as_posix();payload[target]=data
                files[path.relative_to(ROOT).as_posix()]={'published_path':target,'sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_signed132_import_recovery_preserving_all_original_sources',
              'files':files,'previous_main':previous,'only_branch':'main','official_scores_and_full_candidate_not_yet_claimed':True,'residual_sign':-1,
              'completed_native_annual_fits_added':0,'new_quality_scores':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('第132轮实际启动源码的导入路径修复：保留已上传V1，新增V2启动器与准入器；实际数学评分器仍为原V1。检查所有反向融合模块引用，预生成的登记模块按冻结生成器核对。只替换等待中的调度器，没有终止训练或评分。原失败检查及源文件完整保留。仍须第131轮完成main、实际准入及23:12前方可启动40项官方比较；当前新增官方分数为0。仅main，23:55停工，明早用户继续后恢复。\n').encode('utf8')
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存反向融合实际导入引用修复及原始失败记录',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(data).hexdigest() for n,data in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit);scope.reverify()
            create(OUT/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'branch':'main',
              'at_local':sync.now(),'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,'test_labels_read':False})
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
        create(OUT/'actual_hidden_publication_children.json',{'events':restore()})

if __name__=='__main__':main()
