"""Warm all67 permitted child fits before loading the final meta training matrix."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]


def main():
    import train_nonlinear_stacking_bank_20261004 as bank
    import nonlinear_stacking_model_sources_20261004 as models
    gate=bank.OUT/'oof_audit.json'
    while not gate.exists():time.sleep(10)
    models.verify();out=ROOT/'analysis/nonlinear_stacking_fulltraining_warmup_20261004.json'
    if out.exists():assert models.read(out)['status']=='passed';return
    protocol=ROOT/'analysis/nonlinear_stacking_fulltraining_reserve_20261004.json'
    if not protocol.exists():
        models.dump(protocol,{'status':'frozen_scheduling_control','reserve_available_ram_GiB':8.,
            'reserve_interpretation':'Chosen free-memory reserve, not a measured physical boundary.',
            'child_fits_finish_before_loading_meta_matrix':True,'test_data_read':False,'script_sha256':models.sha(Path(__file__))},immutable=True)
    else:assert models.read(protocol)['script_sha256']==models.sha(Path(__file__))
    children={}
    for child in bank.MEMBERS:
        info_path=models.source_dir(child)/'info_2025.json'
        if not info_path.exists():bank.wait_for_fit_reserve()
        info=models.train_one(child,2025);meta=info['training_meta']
        assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
        assert info['fulltraining_only_test_prediction_not_generated']
        children[child]={'info_sha256':models.sha(info_path),'model_sha256':info['model_sha256'],'fit_seconds':info.get('fit_seconds',0.)}
        print('Full child ready: '+child,flush=True)
    name=next(iter(models.NEW_CONFIGS));models.train_one(name,2025)
    alias=name.rsplit('_',1)[0]+'_uniform';models.train_one(alias,2025)
    # Stored JSON gives a single canonical representation for tuple-valued fields.
    info=models.read(models.source_dir(name)/'info_2025.json');paired=models.read(models.source_dir(alias)/'info_2025.json')
    assert info['training_meta']==paired['training_meta'] and paired['new_model_fits']==0
    import numpy as np
    a=models.load_bundle(models.model_path(name,2025));b=models.load_bundle(models.model_path(alias,2025))
    assert len(a['member_bundles'])==len(b['member_bundles'])==67
    for key in ('mean','scale','coefficients'):assert np.array_equal(a['meta_bundle'][key],b['meta_bundle'][key])
    assert a['meta_bundle']['intercept']==b['meta_bundle']['intercept']
    models.dump(out,{'status':'passed','model':name,'paired_uniform_model':alias,'fulltraining_info':info,
        'paired_uniform_info':paired,'children':children,'child_count':67,'fulltraining_only_test_prediction_not_generated':True,
        'test_data_read':False,'scheduling_protocol_sha256':models.sha(protocol),'script_sha256':models.sha(Path(__file__))},immutable=True)
    print('67 full-training children and paired meta bundles ready before future inference.',flush=True)


if __name__=='__main__':main()
