"""Publish closed component scope and remaining root snapshots on main only."""
from pathlib import Path
import hashlib,json,subprocess,sys,time
import psutil
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import watch_validations_main_v2_20261005 as watcher
sync=watcher.sync
PREFIX=Path('validation_sync/linear_leaf_ensemble_scope_closeout_20261005')
def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def main():
    out=ROOT/'analysis/linear_leaf_ensemble_scope_closeout_20261005';out.mkdir(exist_ok=True)
    assert not (out/'receipt.json').exists()
    full=ROOT/'analysis/linear_leaf_ensemble_full_scope_audit_20261005/verification.json'
    proof=sync.read(full);assert proof['status']=='passed_actual_all8_fullfiveyear_native_reload_and_fullfuture_scope'
    for source,digest in proof['source_sha256'].items():assert sha(source)==digest,source
    completed=sync.read(ROOT/'analysis/linear_leaf_ensemble_native_github_state_20261005.json')
    assert completed['status']=='completed_native_evidence_publication' and completed['future']['actual_verified_model_count']==8
    assert not psutil.pid_exists(completed['pid'])
    for key in ('annual','future'):sync.git('merge-base','--is-ancestor',completed[key]['commit'],'HEAD')
    owner=psutil.Process(sync.read(sync.OUT/'owner.lock')['pid']);parent=owner.parent()
    assert str(ROOT/'analysis/watch_validations_main_v2_20261005.py') in owner.cmdline()
    assert parent is not None and parent.cmdline()[1:]==owner.cmdline()[1:]
    suspended=[]
    try:
        for p in (owner,parent):p.suspend();suspended.append(p)
        assert all(p.pid==owner.pid or p.name().lower()=='conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status','--porcelain')
        head=sync.git('rev-parse','HEAD');assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{head}\trefs/heads/main']
        def names(*args):return {n.decode('utf-8') for n in subprocess.check_output(['git',*args,'-z'],cwd=ROOT).split(b'\0') if n}
        chosen=names('ls-files','--modified')|names('ls-files','--others','--exclude-standard')
        chosen.add(Path(__file__).relative_to(ROOT).as_posix())
        assert all((ROOT/name).is_file() and (ROOT/name).suffix in ('.json','.py','.md') for name in chosen)
        paths=[];bindings={}
        sync.atomic(sync.WORKTREE/PREFIX/'.gitattributes',b'* -text\n');paths.append((PREFIX/'.gitattributes').as_posix())
        evidence={full,ROOT/'analysis/linear_leaf_ensemble_publication_blob_qa_20261005/verification.json'}
        for source in sorted({ROOT/name for name in chosen}|evidence):
            data=source.read_bytes();assert len(data)<5*2**20 and not sync.SECRET.search(data)
            if source.suffix=='.json':json.loads(data.decode('utf-8-sig'))
            relative=source.relative_to(ROOT);destination=PREFIX/relative if source in evidence else relative
            sync.atomic(sync.WORKTREE/destination,data);paths.append(destination.as_posix())
            bindings[str(source)]={'snapshot_sha256':hashlib.sha256(data).hexdigest(),'published_path':destination.as_posix(),'live_operational_snapshot':source not in evidence and source.suffix=='.json'}
        active=[]
        for job in sync.read(ROOT/'analysis/resumed_rounds_nystrom_locked_20261004.json'):
            if job['round']<65:continue
            try:
                p=psutil.Process(job['pid']);owned=job['script'] in p.cmdline()
            except psutil.NoSuchProcess:owned=False
            active.append({'round':job['round'],'root_pid':job['pid'],'actual_owned_root_live':owned})
        partial={}
        for p in (ROOT/'analysis/optimization_20261003_r65').glob('wave*_results.json'):
            value=sync.read(p);partial[p.stem]={'records':len(value['results']),'status':value['status'],'highest_partial_S':max((row['connected_final_score'] for row in value['results'].values()),default=None)}
        manifest={'status':'passed_closed_component_scope_with_complete_scheme_quality_remaining','at_local':sync.now(),'input_files':bindings,'component_scope':proof,'actual_completed_main_publications':completed,'active_roots_actual_ownership':active,'round65_actual_partial_official_records':partial,'last_qualified_complete_round':64,'last_qualified_complete_S':0.45100769827200593,'last_qualified_complete_board_records':9432,'remaining_complete_official_quality_rounds':list(range(65,73)),'previous_goal_turn_classification':'progress','this_goal_turn_progress':'40 actual virtual annual outputs and8 fullfuture composite checks closed;326 complete quality configurations preflighted andwaiters launched;observer recovered andmain publications verified','goal_status':'active','global_resource_exhaustion_established':False,'all_validation_years_reused_selection_bias_uncorrected':True,'test_labels_read':False,'only_branch':'main'}
        sync.atomic(sync.WORKTREE/PREFIX/'manifest.json',sync.encoded(manifest));paths.append((PREFIX/'manifest.json').as_posix())
        text='# 已完成的集成组件验证与继续工作状态\n\n8种集成的40个完整年度输出、8个最终复合模型和每种全部1,599,600条未来X检查已实际完成。模型重载、80日冷前缀、原生预测和保存文件哈希通过。父模型30次年度、6次最终拟合只计一次；集成新增拟合为0。\n\n上述组件验证已经自动提交main。第65轮仍进行真实官方评分，第66—72轮依次等待各自前置验证；8种集成的第71/72轮共326项完整方案评分尚未完成。现有最高完整验证S为0.451007698272，累计完整榜9,432条。\n\n当前有168种登记配置及667次实际年度拟合。实际未来推理资源采样767次，最低可用主存约2.611GiB、该推理进程最高RSS约2.344GiB，无观测错误。4GiB启动保留量是本虚拟组件的调度规则；继承采样器中的14GiB通用说明不表示这次采用14GiB规则。数据与临时文件留在D/E盘，模型和原始预测不重复上传。\n\n目标仍处于进行中：未证明全局方法或资源边界，未利用测试标签选模，重复使用验证年份的选模偏差未校正。后续完整方案仍须官方评分、冻结、因果检查、候选推理、完整榜更新及main同步。\n'
        sync.atomic(sync.WORKTREE/PREFIX/'README.md',text.encode('utf-8'));paths.append((PREFIX/'README.md').as_posix())
        for offset in range(0,len(paths),50):sync.git('add','-f','--',*paths[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged and staged<=set(paths)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','完成八种集成全量推理检查并同步实际进度，保留完整方案评分与边界任务',timeout=180)
        commit=sync.git('rev-parse','HEAD');sync.git('push','origin','HEAD:refs/heads/main',timeout=180)
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        result={'status':'pushed_verified_only_main','at_local':sync.now(),'commit':commit,'files':len(paths),'all8_component_fullfuture_controls_passed':True,'complete_official_scheme_quality_still_pending':True,'goal_active':True,'url':f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        sync.atomic(out/'receipt.json',sync.encoded(result));print(json.dumps(result,ensure_ascii=False),flush=True)
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
if __name__=='__main__':main()
