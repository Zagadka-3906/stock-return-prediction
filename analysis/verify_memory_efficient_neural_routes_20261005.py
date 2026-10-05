"""Validate new direct/codec routes using CPU prototypes and all36 inherited cases."""
from pathlib import Path
import hashlib
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    import numpy as np
    import polars as pl
    import torch
    import train_memory_efficient_neural_bank_20261005 as bank
    import memory_efficient_neural_model_sources_20261005 as router
    import fourier_tuning_model_sources_20261004 as legacy
    from memory_efficient_neural_future_codec_adapter_20261005 import install
    import train_gradient_sampling_bank_20261005 as goss
    import train_factorization_machine_bank_20261005 as fm
    import train_nystrom_tuning_bank_20261005 as nystrom
    import train_linear_leaf_bank_20261005 as leaves
    import build_linear_leaf_ensemble_bank_20261005 as ensemble
    assert not torch.cuda.is_available()
    out = A / 'memory_efficient_neural_direct_router_preflight_20261005'
    assert not out.exists()
    out.mkdir()
    proof = A / 'memory_efficient_mlp_preflight_20261005/verification.json'
    assert bank.read(proof)['status'].startswith('passed')
    cases = [(mode, A / f'memory_efficient_mlp_preflight_20261005/{mode}_512wide4096row32epoch.joblib', bank.engine, True)
        for mode in ('baseline','accumulate','checkpoint','combined')]
    cases += [(name,A / f'gradient_sampling_preflight_20261005/{name}.joblib',goss,True) for name in goss.CONFIGS]
    for native, folder in ((fm,'factorization_machine_future_qa_v2_20261005'),
        (nystrom,'nystrom_tuning_future_qa_20261005'),(leaves,'linear_leaf_future_qa_20261005'),
        (ensemble,'linear_leaf_ensemble_future_qa_20261005')):
        inherited = bank.read(A / folder / 'verification.json')
        assert inherited['status'] == 'passed'
        cases += [(row['model'],A / folder / f"{row['model']}.joblib",native,False) for row in inherited['checks']]
    assert len(cases) == 40
    sources = [Path(__file__), Path(bank.__file__), Path(router.__file__), proof,
        A / 'memory_efficient_neural_future_codec_adapter_20261005.py',
        A / 'memory_efficient_neural_source_generation_20261005.json']
    sources += [path for _,path,_,_ in cases]
    bindings = {str(path):sha(path) for path in sources}
    bank.dump(out / 'frozen_before_controls.json', {'status':'frozen_before_actual_CPU_direct_and_codec_controls',
        'input_sha256':bindings, '512_width_new_prototypes_are_not16384_fits':True,
        'new_quality_scores':0,'test_labels_read':False},immutable=True)
    features = bank.engine.feature_names()
    frame = bank.engine.training_frame(pl.scan_parquet(bank.engine.FEATURE_FILE),bank.engine.fold_cutoff(2020),
        next(iter(bank.CONFIGS.values()))).select(features).head(131).collect()
    x = bank.engine.to_matrix(frame,features)
    original = legacy.predict_arrays
    controls = []
    for name,path,native,pilot in cases:
        bundle = router.load_bundle(path)
        actual,expected = router.predict_arrays(bundle,x),native.predict_arrays(bundle,x)
        assert np.array_equal(actual,expected),name
        assert all(np.array_equal(actual[:n],router.predict_arrays(router.load_bundle(path),x[:n])) for n in (1,80,130))
        controls.append({'model':name,'saved_kind':bundle['kind'],'source':str(path),'model_sha256':sha(path),
            'actual_unhooked_direct131_and_prefixes_bit_exact':True,'prototype_only':pilot})
    assert legacy.predict_arrays is original
    restore = install()
    try:
        for name,path,native,_ in cases:
            assert np.array_equal(legacy.predict_arrays(legacy.load_bundle(path),x),native.predict_arrays(router.load_bundle(path),x)),name
    finally:
        restore()
    assert legacy.predict_arrays is original
    for source,expected in bindings.items():
        assert sha(source) == expected,source
    bank.dump(out / 'verification.json', {'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'source_sha256':bindings,'checks':controls,'actual_checks':40,
        'actual4_CPU_MLP_prototypes_and6_GOSS_pilots_and30_inherited_full_models':True,
        'all_direct_and_hooked_routes_bit_identical_and_original_codec_restored':True,
        'new_actual16384_annual_final_and_future_controls_still_pending':True,
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False},immutable=True)
    print('Passed40 actual unhooked direct, native prefix and restored complete codec routes',flush=True)


if __name__ == '__main__':
    main()
