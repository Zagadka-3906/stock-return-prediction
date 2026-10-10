"""Reuse an unchanged frozen candidate if none of the standalone replacements wins."""
from pathlib import Path
import shutil


def reuse(record):
    import numpy as np
    from optimize_training_round32 import ROOT,OUT,PREVIOUS,read,dump,sha,log
    winner=record['winner'];previous=read(PREVIOUS/'selection.json')['winner']
    assert not winner['standalone_replacement']
    assert np.array_equal(np.load(OUT/'selected_validation.npy'),np.load(PREVIOUS/'selected_validation.npy'))
    assert winner['connected_final_score']==previous['connected_final_score']
    source=ROOT/'candidates/optimization_20261003_r31';target=ROOT/'candidates/optimization_20261003_r32';target.mkdir(parents=True,exist_ok=True)
    manifest=read(source/'manifest.json');verification=read(source/'verification.json');assert verification['status']=='passed'
    for name,metadata in manifest['files'].items():assert sha(source/name)==metadata['sha256'],name
    assert sha(OUT/'future_return_mapping.json')==sha(source/'return_mapping.json')
    for name in manifest['files']:
        if name in ('selection.json','verification.json'):continue
        destination=target/name;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/name,destination)
        assert sha(destination)==manifest['files'][name]['sha256']
    models={key:{**info,'path':str(target/Path(info['path']).name),'previous_candidate_source':info['path']} for key,info in verification['models'].items()}
    result={**verification,'models':models,'validation_score':winner['connected_final_score'],
            'frozen_previous_candidate_reused':True,'previous_candidate_verification_sha256':sha(source/'verification.json'),
            'new_fulltrain_models':0,'test_labels_read':False,
            'old_delivery_pointer_unchanged':sha(ROOT/'active_release.json')==record['frozen_sha256']['active_release.json']}
    dump(target/'selection.json',record,immutable=True);dump(target/'verification.json',result,immutable=True)
    log('Round32 unchanged complete candidate copied and all frozen inputs verified')
