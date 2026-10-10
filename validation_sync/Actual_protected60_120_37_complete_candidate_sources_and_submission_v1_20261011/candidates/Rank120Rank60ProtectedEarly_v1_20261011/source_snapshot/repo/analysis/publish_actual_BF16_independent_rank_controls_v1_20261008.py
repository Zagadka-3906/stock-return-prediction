"""Publish completed small controls, first verified annual metadata and the frozen next grid after134."""
from pathlib import Path
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from file_backed_hidden_git_runtime_20261007 import installed
import publish_classifier_consensus_workflows_20261006 as helpers
OUT=A/'actual_BF16_independent_rank_controls_main_v1_20261008'
PREFIX=Path('validation_sync/actual_BF16_independent_rank_controls_20261008')


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name
    return folder


def main():
    closed('nonflag_ReverseBayesFine40_round134_full_registration_v1')
    small_service=closed('BF16_independent_small_CPU_preflight_v1_20261008')
    small=A/'BF16_independent_small_CPU_preflight_v1_20261008'
    synthetic=A/'BF16_rank_CDF_synthetic_preflight_v1_20261008'
    assert read(small/'verification.json')['status']=='passed_actual_small32_CPU_saved_tensor_independent_forward_and_prefixes'
    assert read(synthetic/'verification.json')['status']=='passed_actual18_synthetic_BF16_rank_CDF_roles_and36_day_prefixes'
    bank=Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
    info=read(bank/'2020/info.json')
    assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
    assert info['actual_full_annual_reload_prediction_bits_exact'] and info['actual_cold80_prefix_bits_exact']
    sources=[Path(__file__), A/'neural_BF16_independent_forward_v1_20261008.py',
        A/'verify_BF16_independent_small_CPU_v1_20261008.py',
        A/'verify_BF16_full5_independent_GPU_v1_20261008.py',
        A/'verify_BF16_full5_independent_GPU_v2_20261008.py',
        A/'recover_BF16_full_oracle_key_pin_v2_20261008.py',
        A/'actual_BF16_full_oracle_key_pin_recovery_v2_20261008.json',
        A/'actual_BF16_full_oracle_key_pin_hidden_launch_v2_20261008.json',
        A/'start_BF16_independent_controls_v1_20261008.py',
        A/'actual_BF16_independent_controls_hidden_launches_v1_20261008.json',
        A/'BF16_complete_parent_rank_CDF_v1_20261008.py',
        A/'verify_BF16_rank_CDF_synthetic_v1_20261008.py',
        A/'verify_BF16_rank_CDF_full37_v1_20261008.py',
        A/'prepare_BF16wide40_rank_plan_and_controls_v1_20261008.py',
        A/'BF16wide40_round135_plan_v1_20261008.json',
        A/'actual_BF16wide40_rank_plan_and_full37_hidden_launch_v1_20261008.json',
        A/'refresh_actual_progress_dependencies_v3_20261008.py',
        A/'monitor_actual_manual_resume_v3_20261008.py',
        A/'actual_progress_dependency_observer_replacement_v3_20261008.json',
        A/'actual_progress_dependency_observer_hidden_launch_v3_20261008.json',
        A/'github_validation_sync_main_20261005/round134_receipt.json']
    sources += list(small.glob('*.json'))+list(synthetic.glob('*.json'))+list(small_service.glob('*.json'))+list(small_service.glob('*.log'))
    pairs=[(p,PREFIX/'sources_and_records'/p.relative_to(ROOT)) for p in dict.fromkeys(sources)]
    pairs += [(bank/'protocol.json',PREFIX/'actual_training/bank_protocol.json'),
              (bank/'2020/frozen_training_inputs.json',PREFIX/'actual_training/year2020_mature_inputs.json'),
              (bank/'2020/info.json',PREFIX/'actual_training/year2020_verified_metadata.json')]
    assert not OUT.exists();OUT.mkdir()
    payload={};bindings={}
    for source,target in pairs:
        data=source.read_bytes();assert len(data)<10_000_000 and not helpers.sync.SECRET.search(data),source
        payload[target.as_posix()]=data
        bindings[str(source)]={'sha256':hashlib.sha256(data).hexdigest(),'published_path':target.as_posix()}
    snapshot=read(A/'actual_manual_resume_progress_20261008.json')
    payload[(PREFIX/'observed_live_progress_snapshot.json').as_posix()]=helpers.sync.encoded(snapshot)
    payload[(PREFIX/'manifest.json').as_posix()]=helpers.sync.encoded({
        'status':'actual_small_CPU_and_synthetic_rank_controls_and_first_annual_metadata_with_pending_full_wide_admission',
        'at_local':helpers.sync.now(),'files':bindings,'actual_small_oracle_rows':10017,
        'actual_small_prefix_cases':4,'actual_synthetic_CDF_cases':18,'actual_synthetic_prefix_cases':36,
        'actual_first_annual_rows':info['rows'],'first_annual_fit_seconds':info['fit_seconds_including_checkpoints_this_process'],
        'large_model_state_and_checkpoint_not_copied_to_GitHub_SHA_and_storage_metadata_retained':True,
        'new_BF16_quality_scores_by_these_controls':0,'future40_grid_frozen_before_quality':True,
        'actual_GPU_wide5_independent_and_full37_CDF_controls_not_claimed_by_small_tests':True,
        'new_native_fits_by_publication':0,'test_labels_read':False,'global_exhaustion_claimed':False})
    payload[(PREFIX/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(PREFIX/'README.md').as_posix()]=(
        '# 新BF16方案的独立解码与排名融合准入记录\n\n'
        '已有32轮小模型在CPU上独立执行保存权重的Linear、LayerNorm、SiLU，不调用原网络构造器；'
        '10017行（含NaN、正负无穷和尾批）及0/1/4097/8192行前缀与原生路径逐位一致。'
        '这些小模型检查不替代大网络完整GPU检查。\n\n'
        '首份2020年度大模型已完成32轮，在1694259条成熟过去样本上拟合，保存模型后完成整年重载预测和80日冷前缀检查。'
        '实际模型和断点留在E盘，本记录保留参数、模型SHA和数据边界。新BF16正式质量评分仍待六份模型和全量检查完成。\n\n'
        '第135轮预先冻结三个有效样本群体与12个排名融合幅度，共36项新方案、三个合格锚点和一个零权重对照。'
        '融合在完整父方案之后执行，2020年参与，保留无效与未选群体原值。18项合成核对与36个日期前缀已经通过；'
        '全5635800行37项Pandas独立CDF和111个冷前缀、完整候选推理与登记仍待实际执行。仅main，未读取真实测试标签。\n').encode('utf8')
    held=[]
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        create(OUT/'actual_idle_main_hold.json',idle)
        with installed(OUT/'file_backed_git'):
            sync=helpers.sync;previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous)
            assert not sync.git('status','--porcelain')
            for p,info in bindings.items():assert sha(p)==info['sha256'],p
            for p,data in payload.items():sync.atomic(sync.WORKTREE/p,data)
            names=sorted(payload)
            for start in range(0,len(names),50):sync.git('add','-f','--',*names[start:start+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','保存BF16首年度记录与独立权重解码和135轮排名融合预定检查',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={p:hashlib.sha256(data).hexdigest() for p,data in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
            create(OUT/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),
                'branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'new_quality_scores':0})
            print('Actual independent/rank controls and verified first annual metadata pushed to main: '+commit,flush=True)
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()


if __name__=='__main__':main()

