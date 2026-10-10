"""Finish the warmup gate using canonical saved metadata; never refit or infer."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]


def main():
    import numpy as np
    import expanded_stacking_model_sources_20261004 as models
    models.verify();out=ROOT/'analysis/expanded_stacking_fulltraining_warmup_20261004.json'
    assert not out.exists()
    protocol=ROOT/'analysis/expanded_stacking_fulltraining_reserve_20261004.json'
    old_script=ROOT/'analysis/warm_expanded_stacking_fulltraining_20261004.py'
    assert models.read(protocol)['script_sha256']==models.sha(old_script)
    full={}
    for name in models.bank.MEMBERS:
        info_path=models.source_dir(name)/'info_2025.json';info=models.read(info_path);meta=info['training_meta']
        assert info['status']=='passed' and models.sha(models.model_path(name,2025))==info['model_sha256']
        assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
        full[name]={'info_sha256':models.sha(info_path),'model_sha256':info['model_sha256'],'fit_seconds':info.get('fit_seconds',0.)}
    name=next(iter(models.NEW_CONFIGS));alias=name.rsplit('_',1)[0]+'_uniform'
    info_path=models.source_dir(name)/'info_2025.json';alias_path=models.source_dir(alias)/'info_2025.json'
    info=models.read(info_path);alias_info=models.read(alias_path)
    assert info['training_meta']==alias_info['training_meta'] and alias_info['new_model_fits']==0
    assert alias_info['paired_info_sha256']==models.sha(info_path)
    a=models.load_bundle(models.model_path(name,2025));b=models.load_bundle(models.model_path(alias,2025))
    assert models.sha(models.model_path(name,2025))==info['model_sha256']
    assert models.sha(models.model_path(alias,2025))==alias_info['model_sha256']
    assert len(a['member_bundles'])==len(b['member_bundles'])==55
    assert a['member_model_sha256']==b['member_model_sha256']=={n:v['model_sha256'] for n,v in full.items()}
    for key in ('mean','scale','coefficients'):
        assert np.array_equal(a['meta_bundle'][key],b['meta_bundle'][key]),key
    assert a['meta_bundle']['intercept']==b['meta_bundle']['intercept']
    assert a['meta_bundle']['config']==b['meta_bundle']['config']
    models.dump(out,{'status':'passed','model':name,'paired_uniform_model':alias,
        'fulltraining_info':info,'paired_uniform_info':alias_info,'children':full,'child_count':55,
        'fulltraining_only_test_prediction_not_generated':True,'test_data_read':False,
        'scheduling_protocol_sha256':models.sha(protocol),'script_sha256':models.sha(Path(__file__)),
        'recovery':{'reason':'Original in-memory metadata uses tuples while reloaded JSON uses lists. Both saved metadata objects match exactly; no training or model change.',
            'original_warm_script_sha256':models.sha(old_script),'canonical_saved_training_metadata_exact':True,
            'paired_meta_coefficients_and_preprocessing_bit_identical':True,'actual_model_sha256_verified':True,
            'new_fits':0,'recovered_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')}},immutable=True)
    print('Recovered warmup gate:55 full children and paired coefficients verified; zero new fits.',flush=True)


if __name__=='__main__':main()
