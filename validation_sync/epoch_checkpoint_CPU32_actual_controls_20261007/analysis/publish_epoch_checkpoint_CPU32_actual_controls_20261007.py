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
OUT=A/'epoch_checkpoint_CPU32_actual_controls_github_20261007'

def main():
    proof_path=A/'epoch_durable_neural_checkpoint_CPU32_preflight_v2_20261007/verification.json';proof=read(proof_path)
    assert proof['status']=='passed_actual_fresh_process_CPU32_epoch7_restart_all_weights_losses_and_predictions_exact'
    assert proof['actual_GPU_equivalence_not_yet_verified'] and proof['new_quality_scores']==0
    sources=[Path(__file__),A/'epoch_durable_neural_checkpoint_adapter_20261007.py',
      A/'epoch_durable_neural_checkpoint_adapter_v2_20261007.py',
      A/'verify_epoch_durable_neural_checkpoint_CPU32_20261007.py',
      A/'verify_epoch_durable_neural_checkpoint_CPU32_v2_20261007.py',
      A/'prepare_epoch_checkpoint_CPU32_retry_v2_20261007.py',A/'epoch_checkpoint_CPU32_v2_retry_admission_20261007.json',
      A/'train_diverse_backbones_20261003.py',
      *list((A/'epoch_durable_neural_checkpoint_CPU32_preflight_20261007').glob('*.json')),
      *list((A/'epoch_durable_neural_checkpoint_CPU32_preflight_20261007').glob('*.log')),
      *list((A/'epoch_durable_neural_checkpoint_CPU32_preflight_v2_20261007').glob('*.json')),
      *list((A/'epoch_durable_neural_checkpoint_CPU32_preflight_v2_20261007').glob('*.log'))]
    sources=list(dict.fromkeys(sources));pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    for p,d in pins.items():assert sha(p)==d,p
    assert not OUT.exists();OUT.mkdir()
    create(OUT/'frozen_before_actual_main_publication.json',{'input_sha256':pins,'actual_GPU_training_adapter_not_yet_admitted':True,'new_quality_scores':0})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        while any(psutil.Process(pid).status()==psutil.STATUS_STOPPED for pid in (row['pid'],row['owned_worker_pid'])):
            assert time.time()<datetime.fromisoformat('2026-10-07T23:45:00+08:00').timestamp()
            time.sleep(10)
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/epoch_checkpoint_CPU32_actual_controls_20261007')
            payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for path in [*sources,OUT/'frozen_before_actual_main_publication.json']:
                data=path.read_bytes();assert not sync.SECRET.search(data),path
                target=(prefix/path.relative_to(ROOT)).as_posix();payload[target]=data
                files[path.relative_to(ROOT).as_posix()]={'published_path':target,'sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_CPU32_fresh_process_epoch_resume_controls',
              'files':files,'previous_main':previous,'only_branch':'main','actual_GPU_equivalence_not_yet_verified':True,
              'completed_native_annual_fits_added':0,'new_quality_scores':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('训练恢复点实际核对：连续32轮与独立进程7轮保存再继续25轮，CPU权重、训练损失、预处理与预测逐位一致；篡改训练输入被拒绝。保留首轮Windows只读句柄fsync失败及写句柄修复记录。GPU等价性尚待验证，当前16384年度训练仍使用原程序；没有新增正式年度模型或评分。仅main。\n').encode('utf8')
            scope.reverify()
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','记录神经训练按轮次落盘与独立进程恢复的实际CPU32核对',timeout=180)
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
