"""Check four classification pilots and all40 inherited direct and future routes."""
from pathlib import Path
import hashlib
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT),str(A)]
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    import numpy as np
    import streaming_rank_classification_v3_20261005 as native
    import streaming_rank_classifier_model_sources_20261005 as router
    import memory_efficient_neural_model_sources_20261005 as previous
    import fourier_tuning_model_sources_20261004 as legacy
    from streaming_rank_classifier_future_codec_adapter_20261005 import install
    out=A/'streaming_rank_classifier_direct_router_preflight_20261005'
    assert not out.exists()
    out.mkdir()
    inherited_proof=A/'memory_efficient_neural_direct_router_preflight_20261005/verification.json'
    inherited=native.read(inherited_proof)
    assert inherited['status']=='passed' and len(inherited['checks'])==40
    cases=[(name,A/f'streaming_rank_classification_preflight_v3_20261005/{name}_4096row32epoch.joblib',native,True)
           for name in native.CONFIGS]
    cases += [(row['model'],Path(row['source']),previous,row['prototype_only']) for row in inherited['checks']]
    sources=[Path(__file__),Path(native.__file__),Path(router.__file__),Path(previous.__file__),inherited_proof,
        A/'streaming_rank_classifier_future_codec_adapter_20261005.py',
        A/'streaming_rank_classification_preflight_v3_20261005/verification.json']
    sources += [path for _,path,_,_ in cases]
    bindings={str(path):sha(path) for path in sources}
    native.dump(out/'frozen_before_actual_controls.json',{'status':'frozen_before44_actual_native_routes',
        'input_sha256':bindings,'new_full_fits_not_substituted_by_pilots':True,'test_labels_read':False},immutable=True)
    features=native.feature_names()
    batch=next(b for b in native.scanner(features,native.training_condition(native.cutoff(2020))) if len(b))
    x=native.matrix(batch.slice(0,131),features)
    controls=[]
    original=legacy.predict_arrays
    for name,path,engine,pilot in cases:
        bundle=router.load_bundle(path)
        actual=router.predict_arrays(bundle,x)
        expected=engine.predict_arrays(bundle,x)
        assert np.array_equal(actual,expected),name
        for count in (1,80,130):
            assert np.array_equal(actual[:count],router.predict_arrays(router.load_bundle(path),x[:count])),name
        controls.append({'model':name,'saved_kind':bundle['kind'],'model_source':str(path),
            'model_sha256':bindings[str(path)],'actual_unhooked_native131_and_prefixes_bit_identical':True,
            'pilot':pilot,'new_classifier':name in native.CONFIGS})
    assert legacy.predict_arrays is original
    restore=install()
    try:
        for name,path,engine,_ in cases:
            assert np.array_equal(legacy.predict_arrays(legacy.load_bundle(path),x),engine.predict_arrays(router.load_bundle(path),x)),name
    finally:restore()
    assert legacy.predict_arrays is original and len(controls)==44
    assert all(sha(path)==digest for path,digest in bindings.items())
    native.dump(out/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'source_sha256':bindings,'checks':controls,'actual_checks':44,
        'all_direct_and_hooked_routes_and_native_prefixes_bit_identical':True,
        'original_codec_restored':True,'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False},immutable=True)
    print('Passed44 actual direct, native prefix and restored complete future codec routes.',flush=True)


if __name__=='__main__':main()
