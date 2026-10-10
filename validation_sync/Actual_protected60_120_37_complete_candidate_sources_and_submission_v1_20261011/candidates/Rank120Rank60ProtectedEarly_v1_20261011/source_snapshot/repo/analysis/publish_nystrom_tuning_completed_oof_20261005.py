"""Verify and publish the actual50-fold kernel bank and all maturity/prefix evidence."""
from pathlib import Path
import hashlib
import json
import sys

import psutil

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import watch_validations_main_v2_20261005 as watcher
sync=watcher.sync
PREFIX=Path('validation_sync/nystrom_tuning_completed_oof_20261005')


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    receipt_path=sync.OUT/'nystrom_tuning_completed_oof_receipt.json'
    assert not receipt_path.exists()
    storage=sync.read(ROOT/'analysis/nystrom_tuning_storage_20261005.json')
    bank=Path(storage['output_directory'])
    audit=sync.read(bank/'oof_audit.json')
    assert audit['status']=='passed' and audit['actual_annual_fits']==50
    protocol=sync.read(bank/'protocol.json')
    assert len(protocol['configurations'])==10
    evidence={bank/'protocol.json',bank/'oof_audit.json'}
    evidence.update(bank.glob('boundary_control_*.json'))
    evidence.update(bank.glob('prefix_control_*.json'))
    evidence.update(bank.glob('*/info_202[0-4].json'))
    assert len(list(bank.glob('*/info_202[0-4].json')))==50
    assert len(list(bank.glob('prefix_control_*.json')))==50
    assert len(list(bank.glob('boundary_control_*.json')))==50
    sources={str(Path(__file__)):sha(Path(__file__))}
    for path,value in sync.read(ROOT/'analysis/nystrom_tuning_bank_run_20261005.json')['input_sha256'].items():
        assert sha(path)==value,path
        sources[path]=value
    artifacts={}
    for name,cfg in protocol['configurations'].items():
        for year in range(2020,2025):
            info_path=bank/name/f'info_{year}.json';info=sync.read(info_path)
            assert info['status']=='passed' and info['configuration']==cfg and info['new_model_fits']==1
            assert info['model']==name and info['year']==year
            meta=info['training_meta']
            assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
            model=bank/name/f'model_{year}.joblib';raw=bank/name/f'raw_{year}.parquet'
            assert sha(model)==info['model_sha256'] and sha(raw)==info['prediction_sha256']
            assert sync.read(bank/f'prefix_control_{name}_{year}.json')['status']=='passed'
            assert sync.read(bank/f'boundary_control_{name}_{year}.json')['status']=='passed'
            for path in (info_path,model,raw):artifacts[str(path)]=sha(path)
    observer=psutil.Process(sync.read(sync.OUT/'owner.lock')['pid'])
    assert str(ROOT/'analysis/watch_validations_main_v2_20261005.py') in observer.cmdline()
    parent=observer.parent()
    assert parent is not None and parent.cmdline()[1:]==observer.cmdline()[1:]
    suspended=[]
    try:
        for process in (observer,parent):process.suspend();suspended.append(process)
        assert all(p.pid==observer.pid or p.name().lower()=='conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status','--porcelain')
        head=sync.git('rev-parse','HEAD')
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{head}\trefs/heads/main']
        paths=[]
        sync.atomic(sync.WORKTREE/PREFIX/'.gitattributes',b'* -text\n');paths.append((PREFIX/'.gitattributes').as_posix())
        for source in sorted(evidence):
            data=source.read_bytes()
            assert len(data)<5*1024**2 and not sync.SECRET.search(data)
            destination=PREFIX/'annual_bank'/source.relative_to(bank)
            sync.atomic(sync.WORKTREE/destination,data);paths.append(destination.as_posix())
        relative=Path(__file__).resolve().relative_to(ROOT)
        sync.atomic(sync.WORKTREE/relative,Path(__file__).read_bytes());paths.append(relative.as_posix())
        manifest={'status':'passed_all50_actual_model_raw_hashes_maturity_and_prefix_evidence',
            'at_local':sync.now(),'actual_annual_fits':50,'configurations':10,'boundary_controls':50,'prefix_controls':50,
            'annual_training_only_final_models_and390_quality_records_pending':True,
            'actual_artifact_sha256':artifacts,'source_sha256':sources,'new_quality_scores':0,
            'training_weights_and_large_raw_predictions_remain_local_D_or_E':True,'test_labels_read':False}
        sync.atomic(sync.WORKTREE/PREFIX/'manifest.json',sync.encoded(manifest));paths.append((PREFIX/'manifest.json').as_posix())
        for source,value in sources.items():assert sha(source)==value,source
        for offset in range(0,len(paths),50):sync.git('add','--',*paths[offset:offset+50])
        changed=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())
        assert changed and changed<=set(paths)
        sync.git('commit','-m','核验并保存扩展核全部50次实际年度拟合、标签边界与冷前缀证据')
        commit=sync.git('rev-parse','HEAD')
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180)
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        receipt={'status':'pushed_verified_only_main','at_local':sync.now(),'commit':commit,
            'files':len(paths),'actual_annual_fits':50,'new_quality_scores':0,
            'url':f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        with receipt_path.open('x',encoding='utf-8') as stream:json.dump(receipt,stream,ensure_ascii=False,indent=2)
        print(json.dumps(receipt,ensure_ascii=False),flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():process.resume()


if __name__=='__main__':main()
