"""Publish completed85-bit controls or88 official records, preserving honest qualification status."""
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


def closed(name,require_pass=True):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(15)
    terminal=read(f/'service_execution.json')
    if require_pass:assert terminal['status']=='passed',name
    return f


def main(phase):
    assert phase in ('controls','scores')
    closed('CPU_ELASTIC44_round114_full_registration_v3')
    closed('CPU_full_bank_resource_observer_ElasticNet_main_publication_v3',False)
    closed('numpy_daily_ranks_full_parent_controls_main_publication_v3',False)
    science=closed('flagged_HGB_small_amplitude88_transform_preflight' if phase=='controls' else 'flagged_HGB_small_amplitude88_official_comparison_v3')
    folder=A/('flagged_HGB_small_amplitude88_transform_preflight_20261007' if phase=='controls' else 'flagged_HGB_small_amplitude88_official_comparison_v3_20261007')
    proof=read(folder/'verification.json')
    assert proof['status']==('passed_actual85_full5635800_flagged_HGB_small_amplitude_independent_oracle_and_cold80_260_975_controls' if phase=='controls' else 'passed_actual88_flagged_HGB_small_amplitude_full_official_comparisons')
    bank=A/'cpu_conditional_residual_hgb_bank20_20261007'
    sources=[Path(__file__),A/'refine_flagged_HGB_compatible_parent_transform_20261007.py',
        A/'prepare_flagged_HGB_small_amplitude88_plan_20261007.py',A/'flagged_HGB_small_amplitude88_plan_20261007.json',
        A/'verify_flagged_HGB_small_amplitude88_transform_20261007.py',A/'run_flagged_HGB_small_amplitude88_official_comparison_v3_20261007.py',
        A/'predict_refined_flagged_CPU_HGB_scheme_20261007.py',A/'prepare_flagged_HGB_small_amplitude88_candidate_sources_v2_20261007.py',
        A/'prepare_flagged_HGB_small_amplitude88_candidate_sources_20261007.py',
        A/'flagged_HGB_small_amplitude88_candidate_source_preparation_v2_20261007.json',
        A/'prepare_flagged_HGB_small_amplitude88_selected_candidate_v4_20261007.py',A/'seal_flagged_HGB_small_amplitude88_selected_candidate_v4_20261007.py',
        A/'flagged_HGB_small_amplitude88_workflow_admission_20261007.json',
        A/'conditional_residual_mlp_CDF_transform_20261007.py',A/'direct_flag_centered_rank_CDF_transform_20261007.py',
        *list(folder.glob('*.json')),*list(science.glob('*.json')),*list(science.glob('*.log')),
        bank/'verification.json',*list(bank.glob('*/info_*.json'))]
    if phase=='scores':
        assert len(proof['records'])==88
        for row in proof['records']:
            path=Path(row['official_score_cache']['official_metrics_source']);assert sha(path)==row['official_metric_capsule_sha256']
            assert read(path)['metrics']==row['metrics'];sources.append(path)
    sources += [A/'prepare_local115_alias_and116_dependency_recovery_20261007.py', *[p for name in ['protected_upper_pool_HGB66_round115_full_registration', 'flagged_HGB_small_amplitude88_official_comparison', 'flagged_HGB_small_amplitude88_scores_main_publication', 'flagged_HGB_small_amplitude88_selected_candidate_preparation', 'flagged_HGB_small_amplitude88_selected_candidate_sealing'] for p in (A/'service_owned_workflows_20261006'/name).glob('*.json')]]
    sources=list(dict.fromkeys(sources));out=A/f'flagged_HGB_small_amplitude88_{phase}_v3_github_20261007';assert not out.exists();out.mkdir()
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in sources}}
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'phase':phase,'future_full116_qualification_not_claimed':True,'test_labels_read':False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held=[];restore=install();sync=helpers.sync
    try:
        main7=read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent,worker,idle=suspended_idle(main7,'    main (watch_validations_main_v7_20261006.py:71)');held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path(f'validation_sync/flagged_HGB_small_amplitude88_{phase}_v3_20261007');payload={(prefix/'.gitattributes').as_posix():b'* -text\n'};files={}
            for p in [*sources,out/'frozen_before_main_publication.json']:
                data=p.read_bytes();assert not sync.SECRET.search(data),p
                raw=hashlib.sha256(data).hexdigest();target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0);assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw;target+='.gz'
                payload[target]=data;files[p.relative_to(ROOT).as_posix()]={'published_path':target,'original_sha256':raw,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual_flagged_HGB_small_amplitude_'+phase,
                'at_local':sync.now(),'files':files,'previous_main':previous,'only_branch':'main',
                'actual_full5635800_control_cases':85,'actual_cold_prefix_cases':255,
                'new_quality_score_records':88 if phase=='scores' else 0,'new_native_fits':0,'existing_native_bank_fits':20,
                'current112_original_branch_full_raw_bits_reproduced':True,'future116_qualification_not_claimed':True,
                'scientific_workers_stopped_suspended_or_restarted':0,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('# HGB涨停分支较小权重与移除分支对照\n\n'
                '复用20个已核验HGB模型：四个预测头和三个固定均值组合，12个较小权重，共84方案；另含移除分支及112、114、115三个合格锚点，总计88项。'
                '先按已完成完整资格的官方总分选比较基准。改动分支的父图必须与106核心相同，可保留已有涨停HGB和低分区HGB；不兼容的合格锚点仍保留参与选优。'
                '不增加Top、最差年度或显著性门槛；不把源码兼容条件作为淘汰其他完整模型的分数标准。\n\n'
                '实际85项在112父输出上通过全部5635800行独立Pandas百分位/CDF与冷80、260、975日前缀。'
                '新115父输出尚须在正式比较中重新控制；未来选中方案还须冻结、执行完整1599600行原生及独立重放、冷80日、CSV、完整QA27和main。'
                '本目录究竟是已完成控制还是完整88评分，以manifest的phase及原始verification为准。0新拟合、未读真实测试标签，未宣称116完整资格或优化穷尽。\n').encode('utf8')
            scope.reverify()
            for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','登记涨停HGB较小权重及移除分支的'+phase+'验证记录',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(data).hexdigest() for n,data in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit);scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'at_local':sync.now(),'branch':'main',
                'raw_git_blobs_verified':len(hashes),'new_quality_scores':88 if phase=='scores' else 0,
                'all_source_inputs_initial_and_final_read_locked_full_rehash':True,
                'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})


if __name__=='__main__':main(sys.argv[1])
