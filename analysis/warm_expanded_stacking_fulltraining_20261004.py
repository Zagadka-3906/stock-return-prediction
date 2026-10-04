"""Warm children before the meta fit, keeping its feature matrix out of child fits."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]


def main():
    import psutil
    import expanded_stacking_model_sources_20261004 as models
    gate=ROOT/'analysis/expanded_stacking_bank_20261004/oof_audit.json'
    while not gate.exists():time.sleep(10)
    models.verify();out=ROOT/'analysis/expanded_stacking_fulltraining_warmup_20261004.json'
    if out.exists():assert models.read(out)['status']=='passed';return
    protocol=ROOT/'analysis/expanded_stacking_fulltraining_reserve_20261004.json'
    if not protocol.exists():
        models.dump(protocol,{'status':'frozen_scheduling_control','reserve_available_ram_GiB':8.,
            'reserve_interpretation':'Chosen scheduling reserve; not a measured hardware limit or model-memory requirement.',
            'child_fits_finish_before_loading_full_meta_feature_matrix':True,'test_data_read':False,
            'script_sha256':models.sha(Path(__file__))},immutable=True)
    else:assert models.read(protocol)['script_sha256']==models.sha(Path(__file__))
    full={}
    for name in models.bank.MEMBERS:
        info_path=models.source_dir(name)/'info_2025.json'
        if not info_path.exists():
            last_notice=time.monotonic()
            while psutil.virtual_memory().available<8*2**30:
                time.sleep(10)
                if time.monotonic()-last_notice>=50:
                    print(f'Waiting for scheduling reserve before full fit {name}; available={psutil.virtual_memory().available/2**30:.2f}GiB',flush=True)
                    last_notice=time.monotonic()
        info=models.train_one(name,2025);meta=info['training_meta']
        assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
        full[name]={'info_sha256':models.sha(info_path),'model_sha256':info['model_sha256'],
                    'fit_seconds':info.get('fit_seconds',0.)}
        print('Full child ready: '+name,flush=True)
    name=next(iter(models.NEW_CONFIGS));info=models.train_one(name,2025)
    alias=name.rsplit('_',1)[0]+'_uniform';alias_info=models.train_one(alias,2025)
    assert info['training_meta']==alias_info['training_meta'] and alias_info['new_model_fits']==0
    models.dump(out,{'status':'passed','model':name,'paired_uniform_model':alias,'fulltraining_info':info,
        'paired_uniform_info':alias_info,'children':full,'child_count':55,
        'fulltraining_only_test_prediction_not_generated':True,'test_data_read':False,
        'scheduling_protocol_sha256':models.sha(protocol),'script_sha256':models.sha(Path(__file__))},immutable=True)
    print('55 full-training children and paired expanded meta bundles ready before any test inference.',flush=True)


if __name__=='__main__':main()
