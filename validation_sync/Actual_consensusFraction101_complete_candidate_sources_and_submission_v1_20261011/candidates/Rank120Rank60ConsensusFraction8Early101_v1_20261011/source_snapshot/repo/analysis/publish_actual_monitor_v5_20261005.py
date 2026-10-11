"""Publish the verified observer handoff and actual cost ledger snapshot to main."""
from pathlib import Path
import hashlib
import json
import sys

import psutil

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import watch_validations_main_v2_20261005 as watcher
sync=watcher.sync
PREFIX=Path('validation_sync/actual_monitor_v5_20261005')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    receipt_path=sync.OUT/'actual_monitor_v5_receipt.json'
    assert not receipt_path.exists()
    verification=sync.read(ROOT/'analysis/actual_monitor_v5_handoff_20261005/verification.json')
    assert verification['status']=='passed_owned_observer_handoff'
    run_path=ROOT/'analysis/actual_optimization_monitor_run_v5_20261005.json'
    run=sync.read(run_path)
    for path,value in run['input_sha256'].items():assert sha(path)==value,path
    process=psutil.Process(run['pid'])
    assert run['script'] in process.cmdline()
    observer=psutil.Process(sync.read(sync.OUT/'owner.lock')['pid'])
    assert str(ROOT/'analysis/watch_validations_main_v2_20261005.py') in observer.cmdline()
    parent=observer.parent()
    assert parent is not None and parent.cmdline()[1:]==observer.cmdline()[1:]
    suspended=[]
    try:
        for target in (observer,parent):target.suspend();suspended.append(target)
        assert all(p.pid==observer.pid or p.name().lower()=='conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status','--porcelain')
        head=sync.git('rev-parse','HEAD')
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{head}\trefs/heads/main']
        sources={ROOT/'analysis'/name for name in (
            'monitor_actual_optimization_progress_v5_20261005.py','handoff_actual_monitor_v5_20261005.py',
            'refresh_neural16384_cost_evidence_20261005.py','refresh_optimization_boundary_evidence_v4_20261005.py',
            'publish_actual_monitor_v5_20261005.py')}
        evidence={p for p in (ROOT/'analysis/actual_monitor_v5_handoff_20261005').glob('*') if p.is_file()}
        evidence.add(run_path)
        snapshots={ROOT/'analysis'/name for name in (
            'optimization_fit_cost_evidence_20261004.json','optimization_boundary_evidence_20261004.json',
            'next_experiment_directions_20261003.json','actual_optimization_monitor_state_20261005.json')}
        paths,bindings=[],{}
        sync.atomic(sync.WORKTREE/PREFIX/'.gitattributes',b'* -text\n');paths.append((PREFIX/'.gitattributes').as_posix())
        for source in sorted(sources|evidence|snapshots):
            data=source.read_bytes()
            if source.suffix=='.json':json.loads(data.decode('utf-8-sig'))
            assert len(data)<5*1024**2 and not sync.SECRET.search(data)
            relative=source.relative_to(ROOT)
            destination=relative if source in sources else PREFIX/relative
            sync.atomic(sync.WORKTREE/destination,data);paths.append(destination.as_posix())
            bindings[str(source)]={'sha256':hashlib.sha256(data).hexdigest(),'observational_snapshot':source in snapshots}
        manifest={'status':'passed_owned_observer_handoff_and_original_cost_source_extended',
            'at_local':sync.now(),'input_files':bindings,'actual_observer_root_pid':process.pid,
            'monitors_through_qualified_round':68,'scientific_controllers_untouched':True,
            'declared154_configurations_include_one_untrained_full16384_model':True,
            'actual_fit_counts_read_only_from_saved_info_artifacts':True,
            'small_and_single_step_controls_excluded_from_annual_fit_counts':True,
            'cost_and_boundary_files_are_observational_snapshots_not_completion_certificates':True,
            'new_quality_scores':0,'global_resource_exhaustion_established':False,'test_labels_read':False}
        sync.atomic(sync.WORKTREE/PREFIX/'manifest.json',sync.encoded(manifest));paths.append((PREFIX/'manifest.json').as_posix())
        for source,item in bindings.items():
            if not item['observational_snapshot']:assert sha(source)==item['sha256'],source
        for offset in range(0,len(paths),50):sync.git('add','--',*paths[offset:offset+50])
        changed=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())
        assert changed and changed<=set(paths)
        sync.git('commit','-m','延续实际进度核验至第68轮并按保存产物计数16384完整训练')
        commit=sync.git('rev-parse','HEAD')
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180)
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        receipt={'status':'pushed_verified_only_main','at_local':sync.now(),'commit':commit,'files':len(paths),
            'url':f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        with receipt_path.open('x',encoding='utf-8') as stream:json.dump(receipt,stream,ensure_ascii=False,indent=2)
        print(json.dumps(receipt,ensure_ascii=False),flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():process.resume()


if __name__=='__main__':main()
