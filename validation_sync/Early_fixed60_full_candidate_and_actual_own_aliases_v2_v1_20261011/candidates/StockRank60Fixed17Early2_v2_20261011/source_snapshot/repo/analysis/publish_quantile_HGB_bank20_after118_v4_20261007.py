"""Publish actual20 quantile models and equivalence controls after the complete118 writer."""
from pathlib import Path
import gzip
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    for name in ('HGB_quarter_numeric28_round118_full_registration_v4','quantile_HGB_native_bank20_training_v2','quantile_HGB_large_batch20_benchmark'):
        closed(name)
    bank=A/'quantile_HGB_native_bank20_v2_20261007';proof=read(bank/'verification.json')
    assert proof['status']=='passed_actual20_CPU_quantile_HGB_native_independent_numpy_and_prefix_controls' and len(proof['actual_models'])==proof['actual_native_fits']==20
    bench_path=A/'quantile_HGB_large_batch20_benchmark_20261007/verification.json';bench=read(bench_path)
    assert bench['status']=='passed_actual20_saved_HGB_two_alternating_inference_repeats_all_bits_and_prefix_controls' and len(bench['records'])==40
    paths=[Path(__file__),A/'prepare_quantile_HGB_native_bank20_20261007.py',A/'quantile_HGB_native_bank20_plan_20261007.json',
      A/'recover_quantile_HGB_codec_and_bank20_v2_20261007.py',A/'quantile_HGB_native_bank20_source_recovery_preparation_v2_20261007.json',
      A/'quantile_HGB_native_bank20_source_recovery_actual_launch_v2_20261007.json',
      A/'verify_quantile_HGB_codec_preflight_v2_20261007.py',A/'admit_quantile_HGB_native_bank20_v2_20261007.py',
      A/'train_quantile_HGB_native_bank20_v2_20261007.py',A/'run_quantile_HGB_native_bank20_after_admission_v2_20261007.py',
      A/'quantile_HGB_cpu_codec_v2_20261007.py',A/'quantile_HGB_large_batch_codec_20261007.py',
      A/'prepare_quantile_HGB_large_batch20_controls_20261007.py',A/'benchmark_quantile_HGB_large_batch20_20261007.py',
      *bank.glob('*.json'),*bank.glob('*/info_*.json'),*bank.glob('*/oof_verification.json'),
      *list((A/'quantile_HGB_large_batch20_benchmark_20261007').glob('*.json')),
      *list((A/'quantile_HGB_codec_preflight_v2_20261007').glob('*.json')),
      A/'quantile_HGB_native_bank20_admission_v2_20261007.json',A/'github_validation_sync_main_20261005/round118_receipt.json']
    for name in ('quantile_HGB_codec4_preflight','quantile_HGB_native_bank20_source_admission','quantile_HGB_native_bank20_training',
        'quantile_HGB_codec4_preflight_v2','quantile_HGB_native_bank20_source_admission_v2','quantile_HGB_native_bank20_training_v2','quantile_HGB_large_batch20_benchmark'):
        f=A/'service_owned_workflows_20261006'/name;assert not owned(read(f/'native_launch.json'))
        paths += list(f.glob('*.json'))+list(f.glob('*.log'))
    paths=list(dict.fromkeys(paths));pins={**proof['input_sha256'],**bench['input_sha256'],**{str(p):sha(p) for p in paths}}
    out=A/'quantile_HGB_bank20_github_v4_20261007';assert not out.exists();out.mkdir()
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'new_quality_scores':0,'full119_qualification_not_claimed':True})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        row=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(row,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/quantile_HGB_bank20_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in [*paths,out/'frozen_before_main_publication.json']:
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                raw=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'original_sha256':raw,'published_sha256':hashlib.sha256(data).hexdigest(),'published_path':target}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual20_quantile_mature_native_fits_and40_batch_equivalence_repeats',
              'files':files,'previous_main':previous,'actual_selection_native_fits':20,'actual_successful_diagnostic_fits':4,'actual_failed_diagnostic_native_model_saved':1,
              'new_quality_scores':0,'training_and_native_controls_elapsed_seconds':proof['elapsed_seconds'],
              'native_phase_speedup':bench['native_phase_speedup'],'decoder_phase_speedup':bench['independent_decoder_phase_speedup'],
              'full119_official_comparison_freeze_future_candidate_QA30_not_claimed':True,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('20个成熟历史窗口模型：quantile损失0.25/0.75、7/15叶，128次迭代、最小叶64；固定106预测教师、64项特征。\n'
              '每个年度仅用此前成熟的训练标签拟合预处理和模型；0新官方评分。20原生重载、独立解码与冷前缀均通过。\n'
              '8192与256的推理路径对20模型按两个相反顺序核对全部预测位和前缀。未来完整候选仍须实际重放和QA30。保留原解码器限制引起的诊断失败。\n').encode('utf8')
            scope.reverify()
            for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','上传20个分位数HGB原生模型及全量等价推理检查',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'branch':'main','raw_git_blobs_verified':len(hashes),
              'actual_selection_native_fits':20,'new_quality_scores':0,'full119_not_yet_qualified':True})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})

if __name__=='__main__':main()
