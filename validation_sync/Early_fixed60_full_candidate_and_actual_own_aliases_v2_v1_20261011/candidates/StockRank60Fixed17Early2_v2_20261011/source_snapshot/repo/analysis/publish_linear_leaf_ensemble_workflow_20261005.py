"""Publish full composite workflow, real forty annual checks and monitor repair to main."""
from pathlib import Path
import hashlib,json,sys
import psutil
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import watch_validations_main_v2_20261005 as watcher
sync=watcher.sync
PREFIX=Path('validation_sync/linear_leaf_ensemble_workflow_20261005')
def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def main():
    receipt_path=sync.OUT/'linear_leaf_ensemble_workflow_receipt.json';assert not receipt_path.exists()
    folders=('linear_leaf_ensemble_search_generator_preflight_v2_20261005','linear_leaf_ensemble_future_codec_preflight_20261005','linear_leaf_ensemble_cost_inventory_qa_20261005','actual_monitor_v7_handoff_20261005')
    proofs=[sync.read(ROOT/'analysis'/name/'verification.json') for name in folders]
    assert proofs[0]['status']==proofs[1]['status']=='passed'
    assert [item['generated_records'] for item in proofs[0]['controls']]==[148,178,178]
    assert proofs[2]['status']=='passed_actual_saved_artifact_counts_idempotence_and_Windows_lock_retry'
    assert proofs[3]['status']=='passed_owned_observer_handoff'
    for proof in proofs:
        for source,digest in proof.get('source_sha256',{}).items():assert sha(source)==digest,source
    bank=Path(sync.read(ROOT/'analysis/linear_leaf_ensemble_storage_20261005.json')['output_directory'])
    assert sync.read(bank/'oof_audit.json')['actual_virtual_annual_outputs']==40
    assert sync.read(bank/'construction_execution_scope.json')['status']=='passed'
    assert sync.read(ROOT/'analysis/linear_leaf_future_qa_20261005/verification.json')['actual_fulltraining_fits']==6
    launch=sync.read(ROOT/'analysis/linear_leaf_ensemble_followup_launch_receipt_20261005.json')
    for job in [launch['future'],*launch['quality_rounds']]:assert job['script'] in psutil.Process(job['pid']).cmdline()
    monitor=sync.read(ROOT/'analysis/actual_optimization_monitor_run_v7_20261005.json')
    assert monitor['script'] in psutil.Process(monitor['pid']).cmdline()
    owner=psutil.Process(sync.read(sync.OUT/'owner.lock')['pid'])
    assert str(ROOT/'analysis/watch_validations_main_v2_20261005.py') in owner.cmdline()
    parent=owner.parent();assert parent is not None and parent.cmdline()[1:]==owner.cmdline()[1:]
    # The earlier six-parent publisher reached a verified terminal publication.
    old=sync.read(ROOT/'analysis/linear_leaf_native_github_state_20261005.json')
    assert old['status']=='completed_native_evidence_publication'
    assert not psutil.pid_exists(old['pid'])
    suspended=[]
    try:
        for p in (owner,parent):p.suspend();suspended.append(p)
        assert all(p.pid==owner.pid or p.name().lower()=='conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status','--porcelain')
        head=sync.git('rev-parse','HEAD')
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{head}\trefs/heads/main']
        sources=set((ROOT/'analysis').glob('*linear_leaf_ensemble*20261005.py'))
        sources.update(ROOT/'analysis'/f'{prefix}{number}{suffix}.py' for number in (71,72) for prefix,suffix in (('optimize_training_round',''),('optimize_training_round','_v2'),('finalize_training_round',''),('run_training_round','_v2_pipeline')))
        sources.update(ROOT/'analysis'/name for name in ('monitor_actual_optimization_progress_v7_20261005.py','handoff_actual_monitor_v7_20261005.py','recover_actual_monitor_v7_20261005.py','refresh_optimization_boundary_evidence_v6_20261005.py','atomic_optimization_observer_writes_20261005.py'))
        evidence=set((ROOT/'analysis').glob('linear_leaf_ensemble*20261005.json'))
        evidence.add(ROOT/'analysis/actual_optimization_monitor_run_v7_20261005.json')
        evidence.update(bank.glob('*.json'));evidence.update(bank.glob('*/info_202[0-4].json'))
        for folder in folders:evidence.update((ROOT/'analysis'/folder).glob('*.json'))
        snapshots={ROOT/'analysis'/name for name in ('optimization_fit_cost_evidence_20261004.json','optimization_boundary_evidence_20261004.json','next_experiment_directions_20261003.json','actual_optimization_monitor_state_20261005.json','resumed_rounds_nystrom_locked_20261004.json')}
        paths=[];bindings={}
        sync.atomic(sync.WORKTREE/PREFIX/'.gitattributes',b'* -text\n');paths.append((PREFIX/'.gitattributes').as_posix())
        for source in sorted(sources|evidence|snapshots):
            data=source.read_bytes();assert len(data)<5*2**20 and not sync.SECRET.search(data)
            if source.suffix=='.json':json.loads(data.decode('utf-8-sig'))
            relative=source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('authorized_E_bank')/source.relative_to(bank)
            destination=relative if source in sources else PREFIX/relative
            sync.atomic(sync.WORKTREE/destination,data);paths.append(destination.as_posix())
            bindings[str(source)]={'sha256':hashlib.sha256(data).hexdigest(),'observational_snapshot':source in snapshots,'published_path':destination.as_posix()}
        failed=ROOT/'analysis/run_logs/actual_optimization_monitor_v6_20261005.stderr.log'
        destination=PREFIX/'prior_monitor_v6_failure.txt'
        sync.atomic(sync.WORKTREE/destination,failed.read_bytes());paths.append(destination.as_posix())
        manifest={'status':'passed_actual_all40_composite_annual_controls_codec_generator_and_OS_lock_retry','at_local':sync.now(),'input_files':bindings,'actual_virtual_annual_outputs':40,'actual_new_annual_fits':0,'actual_native_parent_annual_fits':30,'actual_native_parent_final_fits':6,'codec_saved_models_verified':24,'prespecified_official_records':{'71':148,'72':178},'generator_ordering_values_synthetic_not_official_scores':True,'all8_fullfuture_controls_started_still_pending':True,'whole_complete_scheme_official_quality_selection_still_pending':True,'observer_monitors_through_qualified_round':72,'old_observer_failure_preserved_and_actual_Windows_lock_retry_passed':True,'actual_cost_ledger_counts':proofs[2]['central_counts'],'raw_weights_and_predictions_retained_local_D_or_E':True,'only_publication_branch':'main','global_resource_exhaustion_established':False,'new_quality_scores':0,'test_labels_read':False}
        sync.atomic(sync.WORKTREE/PREFIX/'manifest.json',sync.encoded(manifest));paths.append((PREFIX/'manifest.json').as_posix())
        doc='# 普通树与线性树的固定权重集成完整方案验证\n\n排名和收益率分别比较三模型等权、两档线性正则等权、普通树与lambda1线性树等权、普通树与lambda10线性树等权，共8种预先冻结配置。每种均由真实300轮同目标成熟父模型组成。\n\n40个完整年度输出均通过保存模型重载及80日原生前缀检查；全部模型和原始预测哈希再次实际核对。新增模型拟合为0，父模型30次年度和6次最终拟合只计一次。\n\n预测接口逐位复现8个集成、6个父模型、10个既有核模型。第71/72轮计划148/178项完整官方评分，两种独立方案胜负分支生成检查均通过；这些合成排序值不计入成绩。全部8种全量未来X模型重载和冷前缀检查已启动，结果另行自动同步。\n\n实际官方分数决定最终采用，完整流程保留方案冻结、训练期收益校准、因果检查、候选推理、完整榜和main同步；训练验证年份重复使用的选模偏差未校正。\n\n新版进度监视器保留旧异常，真实Windows文件占用释放测试通过，状态写入原子化并短暂重试。未宣告优化或计算资源边界耗尽。\n'
        sync.atomic(sync.WORKTREE/PREFIX/'README.md',doc.encode('utf-8'));paths.append((PREFIX/'README.md').as_posix())
        for source,item in bindings.items():
            if not item['observational_snapshot']:assert sha(source)==item['sha256'],source
        for offset in range(0,len(paths),50):sync.git('add','--',*paths[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged and staged<=set(paths)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','核验8种线性树集成40个年度输出，登记326项完整评分并恢复实际进度监视',timeout=180)
        commit=sync.git('rev-parse','HEAD');sync.git('push','origin','HEAD:refs/heads/main',timeout=180)
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        result={'status':'pushed_verified_only_main','at_local':sync.now(),'commit':commit,'files':len(paths),'actual_virtual_annual_outputs':40,'actual_new_model_fits':0,'new_quality_scores':0,'url':f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        sync.atomic(receipt_path,sync.encoded(result));print(json.dumps(result,ensure_ascii=False),flush=True)
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
if __name__=='__main__':main()
