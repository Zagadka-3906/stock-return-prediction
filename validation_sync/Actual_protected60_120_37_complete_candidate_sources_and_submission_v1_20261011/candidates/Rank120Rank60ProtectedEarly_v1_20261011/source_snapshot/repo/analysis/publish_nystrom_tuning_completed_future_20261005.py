"""Verify and publish all10 actual mature final models and fullfuture controls."""
from pathlib import Path
import hashlib
import json
import sys

import psutil

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import watch_validations_main_v2_20261005 as watcher
sync=watcher.sync
PREFIX=Path('validation_sync/nystrom_tuning_completed_future_20261005')


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    receipt_path=sync.OUT/'nystrom_tuning_completed_future_receipt.json'
    assert not receipt_path.exists()
    storage=sync.read(ROOT/'analysis/nystrom_tuning_storage_20261005.json')
    bank=Path(storage['output_directory'])
    qa=ROOT/'analysis/nystrom_tuning_future_qa_20261005'
    proof=sync.read(qa/'verification.json');resources=sync.read(qa/'resource_summary.json')
    assert proof['status']=='passed' and proof['actual_fulltraining_fits']==10
    assert proof['all10_models_fullfuture_reload_and_cold80_controls_passed'] and resources['status']=='passed'
    assert sha(qa/'resource_samples.jsonl')==resources['resource_samples_sha256']
    checks={}
    for row in proof['checks']:
        name=row['model'];info_path=bank/name/'info_2025.json';info=sync.read(info_path)
        assert info['status']=='passed' and info['new_model_fits']==1 and info['test_data_read'] is False
        assert info['training_meta']==row['mature_training'] and info['year']==2025
        assert sha(bank/name/'model_2025.joblib')==sha(qa/f'{name}.joblib')==info['model_sha256']==row['model_sha256']
        assert sha(qa/f'{name}_raw.parquet')==row['raw_sha256']
        checks[name]={'info_sha256':sha(info_path),'model_sha256':row['model_sha256'],'raw_sha256':row['raw_sha256']}
    assert len(checks)==10
    observer=psutil.Process(sync.read(sync.OUT/'owner.lock')['pid'])
    assert str(ROOT/'analysis/watch_validations_main_v2_20261005.py') in observer.cmdline()
    parent=observer.parent();assert parent is not None and parent.cmdline()[1:]==observer.cmdline()[1:]
    suspended=[]
    try:
        for process in (observer,parent):process.suspend();suspended.append(process)
        assert all(p.pid==observer.pid or p.name().lower()=='conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status','--porcelain')
        head=sync.git('rev-parse','HEAD')
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{head}\trefs/heads/main']
        files={p for p in qa.glob('*') if p.suffix in ('.json','.jsonl')}
        files.update(bank.glob('*/info_2025.json'))
        files.update([ROOT/'analysis/nystrom_tuning_future_run_20261005.json',
            sync.OUT/'nystrom_tuning_completed_oof_receipt.json'])
        paths,bindings=[],{}
        sync.atomic(sync.WORKTREE/PREFIX/'.gitattributes',b'* -text\n');paths.append((PREFIX/'.gitattributes').as_posix())
        for source in sorted(files):
            data=source.read_bytes();assert len(data)<5*1024**2 and not sync.SECRET.search(data)
            relative=source.relative_to(ROOT)
            destination=PREFIX/relative
            sync.atomic(sync.WORKTREE/destination,data);paths.append(destination.as_posix())
            bindings[str(source)]=hashlib.sha256(data).hexdigest()
        relative=Path(__file__).resolve().relative_to(ROOT)
        sync.atomic(sync.WORKTREE/relative,Path(__file__).read_bytes());paths.append(relative.as_posix())
        manifest={'status':'passed10_actual_final_model_raw_hashes_and_full_future_controls',
            'at_local':sync.now(),'checks':checks,'source_sha256':bindings,'actual_mature_final_fits':10,
            'rows_each_native_future_control':1599600,'days':344,'codes':4650,
            'resource_summary':resources,'prior_oof_git_commit_timeout_recovered_without_retraining':True,
            'original50fit_commit_and_its_complete_evidence_preserved':True,
            'complete_scheme_rounds65_66_official_quality_pending':True,'new_quality_scores':0,
            'weights_raw_predictions_remain_local_D_or_E':True,'global_resource_exhaustion_established':False,
            'test_labels_read':False}
        sync.atomic(sync.WORKTREE/PREFIX/'manifest.json',sync.encoded(manifest));paths.append((PREFIX/'manifest.json').as_posix())
        for source,value in bindings.items():assert sha(source)==value,source
        for offset in range(0,len(paths),50):sync.git('add','--',*paths[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())
        assert staged and staged<=set(paths)
        # Avoid waiting for unrelated automatic repository repacking during a publish.
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m',
            '核验扩展核10个成熟最终模型和全量未来X重载、冷前缀证据',timeout=180)
        commit=sync.git('rev-parse','HEAD')
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180)
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        receipt={'status':'pushed_verified_only_main','at_local':sync.now(),'commit':commit,
            'files':len(paths),'actual_final_fits':10,'new_quality_scores':0,
            'url':f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        with receipt_path.open('x',encoding='utf-8') as stream:json.dump(receipt,stream,ensure_ascii=False,indent=2)
        print(json.dumps(receipt,ensure_ascii=False),flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():process.resume()


if __name__=='__main__':main()
