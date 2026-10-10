"""Actual saved wide neural inference after the complete parent, with independent forward and CDF."""
from pathlib import Path
import gc
import hashlib

GRAPH_KEY='reusedNN165_complete_parent_rank_CDF'


def after_parent(ns,context,parent,spec,component):
    import joblib
    import numpy as np
    import torch
    from neural_BF16_medium2048_topweightedhuber010_seed09_e64_native_v1_20261009 import predict_arrays,CONFIG
    from neural_BF16_medium2048_topweightedhuber010_seed09_independent_forward_v1_20261009 import predict_saved_tensors
    from BF16Medium153_complete_parent_rank_CDF_v1_20261009 import transform,pandas_oracle,selected
    assert torch.cuda.is_available(),'The admitted full wide controls use the CUDA FP32 inference path.'
    assert 0.<spec['weight']<=1. and spec['rank_universe']=='all_current_raw_forecasts'
    assert spec['sign'] in (-1.,1.)
    assert spec['first2020_active'] and spec['position']=='after_complete_qualified_parent'
    graph_spec=context._whole_graph[GRAPH_KEY]
    for key in ('model','role','weight','sign','rank_universe','first2020_active'):
        assert graph_spec[key]==spec[key],key
    info=component['training_info'];meta=info['training_meta']
    assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
    assert meta['last']<meta['cutoff_exclusive']<int(context.dates.min())
    assert meta['last_label_end']<=meta['cutoff_exclusive']
    assert meta['features']==context._BF16_feature_names
    path=Path(component['path'])
    assert ns.sha(path)==component['sha256']==info['model_sha256']
    assert info['configuration']==CONFIG==component['configuration']
    x=np.ascontiguousarray(context._BF16_raw_features,dtype=np.float32)
    assert x.shape==(len(parent),63)
    original=joblib.load(path)
    assert original['config']==CONFIG and len(original['training_losses'])==64
    raw=predict_arrays(original,x)
    reloaded=joblib.load(path)
    repeated=predict_arrays(reloaded,x)
    independent=predict_saved_tensors(reloaded,x,device='cuda')
    assert np.array_equal(raw.view('u8'),repeated.view('u8'))
    assert np.array_equal(raw.view('u8'),independent.view('u8'))
    raw[~context.valid]=-1e6;independent[~context.valid]=-1e6
    value=transform(parent,raw,context.dates,context.flags,context.valid,spec['role'],spec['weight'],spec['sign'])
    oracle=pandas_oracle(parent,independent,context.dates,context.flags,context.valid,spec['role'],spec['weight'],spec['sign'])
    assert np.array_equal(value.view('u8'),oracle.view('u8'))
    cohort=selected(context.flags,context.valid,spec['role'])
    assert np.array_equal(value[~cohort].view('u8'),np.asarray(parent)[~cohort].view('u8'))
    assert ns.sha(path)==component['sha256']
    controls=[{'name':'reusedNN165_full_'+component['name'],'sha256':component['sha256'],
               'reload_exact':True,'independent_saved_tensor_forward_exact':True,
               'rows':len(parent),'feature_count':63,'fixed8192_padded_FP32_inference':True}]
    report={'rows':len(parent),'actual_selected_rows':int(cohort.sum()),'controls':controls,
            'role':spec['role'],'weight':spec['weight'],'sign':spec['sign'],
            'native_reload_independent_tensor_forward_and_Pandas_CDF_bits_exact':True,
            'all_original_parent_branches_executed_before_new_BF16_stage':True,
            'invalid_and_declared_unselected_parent_forecast_bits_preserved':True,
            'first2020_not_assumed_identity':True,
            'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()}
    del original,reloaded,raw,repeated,independent,oracle,x
    gc.collect();torch.cuda.empty_cache()
    return value,report

