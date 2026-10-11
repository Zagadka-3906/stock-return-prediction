"""Publish only real controls after current main publishers have finished round120."""
from pathlib import Path
import sys,time,gzip,hashlib
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from atomic_optimization_observer_writes_20261005 import write

def closed(name):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(10)
    assert read(f/'service_execution.json')['status']=='passed',name
    return f

def main():
    bank_service=closed('nonflag_residual_Ridge_native_bank10')
    from run_nonflag_residual_Ridge_hook3_after_bank_20261007 import main as hooks
    hooks()
    stage=A/'nonflag_residual_Ridge_followup_stage_20261007.json'
    write(stage,{'status':'actual10_native_fits_and3_historical_hook_controls_passed_waiting_round120_main',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_official_scores':0,'test_labels_read':False})
    closed('nonflag_HGB40_round120_full_registration_v4')
    for name in ('quantile_HGB88_scores_main_publication_v6','nonflag_HGB40_full37_controls_main_publication_v4','nonflag_HGB40_scores_main_publication_v4'):closed(name)
    bank=A/'nonflag_residual_Ridge_bank10_20261007'; proof=read(bank/'verification.json')
    assert proof['actual_native_fits']==len(proof['actual_models'])==10 and proof['status']=='passed_actual10_nonflag_residual_Ridge_mature_native_reload_independent_and_prefix_controls'
    hook=A/'nonflag_residual_Ridge_native_hook3_preflight_20261007'; assert len(read(hook/'verification.json')['records'])==3
    sources=[Path(__file__),*A.glob('*nonflag_residual_Ridge*20261007.py'),*A.glob('nonflag_residual_Ridge*20261007.json'),
        *bank.glob('*.json'),*bank.glob('*/info_*.json'),*bank.glob('*/oof_verification.json'),*bank.glob('*/independent_linear_state_*.json'),
        *(A/'nonflag_residual_Ridge_codec2_preflight_20261007').glob('*.json'),*hook.glob('*.json'),*bank_service.glob('*.json'),*bank_service.glob('*.log'),
        A/'quantile119_nonflag120_closed_dependency_recovery_source_v6_20261007.json',A/'quantile119_nonflag120_closed_dependency_recovery_actual_launches_v6_20261007.json',
        A/'recover_quantile119_and_nonflag120_closed_dependencies_v6_20261007.py',A/'verify_quantile_HGB88_actual_existing_admission_v6_20261007.py',
        A/'github_validation_sync_main_20261005/round120_receipt.json']
    failed=[]
    for folder in (A/'service_owned_workflows_20261006').iterdir():
        if not any(t in folder.name for t in ('quantile_HGB88','nonflag_HGB40','weighted_HGB340','flagged_HGB_weighted_quarters340','HGB_quarter_numeric28')):continue
        terminal=folder/'service_execution.json'
        if not terminal.exists() or read(terminal).get('status')!='failed':continue
        launch=folder/'native_launch.json'
        assert launch.exists() and not owned(read(launch))
        failed.append({'name':folder.name,'actual_failure':read(terminal).get('failure')})
        sources += [*folder.glob('*.json'),*folder.glob('*.log')]
    sources=[p for p in dict.fromkeys(sources) if p.resolve()!=stage.resolve()]; assert all(p.exists() for p in sources)
    out=A/'nonflag_residual_Ridge10_actual_controls_github_20261007'; assert not out.exists(); out.mkdir()
    pins={str(p):sha(p) for p in sources}
    create(out/'frozen_before_main_publication.json',{'input_sha256':pins,'actual_native_fits':10,'actual_historical_hook_controls':3,
        'failed_prior_scopes_preserved':failed,'actual_official_scores':0,'future_complete_Ridge_round_not_yet_qualified':True})
    from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
    from hidden_windows_child_creation_20261006 import install
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    import publish_classifier_consensus_workflows_20261006 as helpers
    held=[]; restore=install(); sync=helpers.sync
    try:
        parent,worker,idle=suspended_idle(read(A/'service_owned_workflows_20261006/main_publisher_v7/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)'); held.extend((worker,parent))
        with LockedReadHashCache(pins) as scope:
            prefix=Path('validation_sync/nonflag_residual_Ridge10_actual_controls_20261007'); payload={(prefix/'.gitattributes').as_posix():b'* -text\n'}; files={}
            for p in [*sources,out/'frozen_before_main_publication.json']:
                data=p.read_bytes(); assert not sync.SECRET.search(data),p
                raw=hashlib.sha256(data).hexdigest(); target=(prefix/p.relative_to(ROOT)).as_posix()
                if len(data)>=5*1024**2:
                    data=gzip.compress(data,mtime=0); assert hashlib.sha256(gzip.decompress(data)).hexdigest()==raw; target+='.gz'
                payload[target]=data; files[p.relative_to(ROOT).as_posix()]={'original_sha256':raw,'published_path':target,'published_sha256':hashlib.sha256(data).hexdigest()}
            previous=sync.git('rev-parse','HEAD'); helpers.verify_main(previous); assert not sync.git('status','--porcelain')
            payload[(prefix/'manifest.json').as_posix()]=sync.encoded({'status':'published_actual10_nonflag_Ridge_native_fits_and3_historical_hooks',
                'files':files,'previous_main':previous,'only_branch':'main','actual_native_fits':10,'actual_diagnostic_fits':2,'actual_historical_hook_controls':3,
                'actual_official_scores':0,'training_and_native_controls_seconds':proof['elapsed_seconds'],'new_large_feature_caches':0,
                'failed_prior_scopes_preserved':failed,'future_complete_Ridge_round_not_yet_qualified':True,'test_labels_read':False})
            payload[(prefix/'README.md').as_posix()]=('本机非涨停残差Ridge：两组训练样本数归一化L2，5个成熟年度窗口，共10个实际模型。复用E盘已有64维矩阵。\n'
                '实际原生、重载、独立线性状态及80/260/975日前缀逐位核对；3个历史603行组件/CDF诊断。未执行官方Ridge选模评分或完整未来候选资格。\n'
                '保留前序真实失败及依赖恢复证据，仅main。\n').encode('utf8')
            scope.reverify()
            for n,data in payload.items():sync.atomic(sync.WORKTREE/n,data)
            names=sorted(payload)
            for offset in range(0,len(names),50):sync.git('add','-f','--',*names[offset:offset+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())<=set(payload)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','上传本机残差Ridge10年度模型实际控制及前序失败恢复记录',timeout=180)
            commit=sync.git('rev-parse','HEAD'); hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()}
            assert helpers.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180); helpers.verify_main(commit); helpers.watcher.advance_source_index(commit); scope.reverify()
            create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','commit':commit,'branch':'main','raw_git_blobs_verified':len(hashes),
                'at_local':sync.now(),'actual_native_fits':10,'actual_official_scores':0,'test_labels_read':False})
            write(stage,{'status':'actual_native_and_historical_controls_published_main','at_local':sync.now(),'commit':commit,'actual_official_scores':0,'test_labels_read':False})
    finally:
        for p in reversed(held):
            if p.is_running():p.resume()
        create(out/'actual_hidden_publication_children.json',{'events':restore()})
if __name__=='__main__':main()
