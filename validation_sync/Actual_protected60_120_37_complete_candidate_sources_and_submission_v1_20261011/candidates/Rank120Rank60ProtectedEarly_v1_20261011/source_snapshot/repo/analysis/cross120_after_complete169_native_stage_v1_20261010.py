"""Own saved-tensor replay and independent tail permutation after the complete167 forecast."""
from pathlib import Path
import gc,hashlib,importlib
GRAPH_KEY='cross120_after_complete169_native_v1_20261010'
BACKENDS={'cross120recent252forward5huber050':('neural_BF16_medium2048_cross120recent252forward5huber050_seed09_e64_native_v1_20261009','neural_BF16_medium2048_cross120recent252forward5huber050_seed09_independent_forward_v2_20261010')}
CODECS={'CDF':'BF16Medium153_complete_parent_rank_CDF_v1_20261009','valid_pool_protection_v1':'protected_upper_tail_rank_permutation_v1_20261010',
        'official_Top_protection_v2':'protected_official_top_rank_permutation_v2_20261010'}

def feature_matrix(context,meta):
    import numpy as np
    from daily_cross_sectional_feature_encoder120_v1_20261010 import encode,names,pandas_oracle
    raw=np.ascontiguousarray(context._BF16_raw_features,dtype=np.float32)
    features=context._BF16_feature_names
    assert len(features)==63 and meta['raw_features']==features
    assert meta['features']==names(features)[0] and raw.shape==(len(context.dates),63)
    dates=np.asarray(context.dates);assert len(dates)==len(raw)
    assert np.all(np.unique(dates,return_counts=True)[1]==4650),'Complete provided daily peer cohort required'
    value=encode(raw,dates,features)
    assert np.array_equal(value.view('u4'),pandas_oracle(raw,dates,features).view('u4'))
    assert np.array_equal(value[:,:63].view('u4'),raw.view('u4'))
    return value


def after_parent(ns,context,parent,spec,component):
    import joblib,numpy as np,torch
    native=importlib.import_module(BACKENDS[spec['recipe']][0])
    decoder=importlib.import_module(BACKENDS[spec['recipe']][1])
    codec=importlib.import_module(CODECS[spec['codec']])
    assert torch.cuda.is_available() and 0.<spec['weight']<=1.
    if spec['codec']!='CDF':assert .1<=spec['protect_fraction']<=.5
    assert spec['sign'] in (-1.,1.) and spec['original_complete_parent_round']==169
    assert spec['position']=='after_complete_qualified_parent' and spec['first2020_active']
    assert context._whole_graph[GRAPH_KEY]==spec
    info=component['training_info'];meta=info['training_meta']
    assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
    assert meta['last']<meta['cutoff_exclusive']<int(context.dates.min()) and meta['last_label_end']<=meta['cutoff_exclusive']
    assert meta['training_calendar_window']==252 and meta['days']<=252
    if native.CONFIG.get('label_horizon_trading_days',1)>1:assert meta['last_label_end']<meta['cutoff_exclusive']
    assert meta['raw_features']==context._BF16_feature_names
    path=Path(component['path']);assert ns.sha(path)==component['sha256']==info['model_sha256']
    assert info['configuration']==native.CONFIG==component['configuration']
    x=feature_matrix(context,meta);assert x.shape==(len(parent),120)
    original=joblib.load(path);assert original['config']==native.CONFIG and len(original['training_losses'])==64
    raw=native.predict_arrays(original,x);reloaded=joblib.load(path)
    repeated=native.predict_arrays(reloaded,x);independent=decoder.predict_saved_tensors(reloaded,x,device='cuda')
    assert np.array_equal(raw.view('u8'),repeated.view('u8')) and np.array_equal(raw.view('u8'),independent.view('u8'))
    raw[~context.valid]=-1e6;independent[~context.valid]=-1e6
    if spec['codec']=='CDF':
        args=(context.dates,context.flags,context.valid,spec['role'],spec['weight'],spec['sign'])
    else:args=(context.dates,context.flags,context.valid,spec['weight'],spec['protect_fraction'],spec['sign'])
    value=codec.transform(parent,raw,*args);oracle=codec.pandas_oracle(parent,independent,*args)
    assert np.array_equal(value.view('u8'),oracle.view('u8'))
    if spec['codec']=='CDF':
        cohort=codec.selected(context.flags,context.valid,spec['role'])
        assert np.array_equal(value[~cohort].view('u8'),np.asarray(parent,dtype=np.float64)[~cohort].view('u8'))
    else:codec.assert_invariants(parent,value,context.dates,context.flags,context.valid,spec['protect_fraction'])
    assert ns.sha(path)==component['sha256']
    controls=[{'name':'protected_tail_after167_'+component['name'],'sha256':component['sha256'],'reload_exact':True,
        'independent_saved_tensor_forward_exact':True,'rows':len(parent),'feature_count':120,'original_parent_feature_count':63,'all_current_raw_peer_feature_encoding_before_price_filter':True,'fixed8192_padded_FP32_inference':True}]
    report={'rows':len(parent),'controls':controls,'recipe':spec['recipe'],'codec':spec['codec'],'weight':spec['weight'],
        'protect_fraction':spec['protect_fraction'],'sign':spec['sign'],'native_reload_independent_tensor_forward_and_Pandas_tail_bits_exact':True,
        'actual_complete_parent_round':spec['original_complete_parent_round'],'complete_selected_parent_executed_before_new_stage':True,'labels_read_by_stage':False,
        'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()}
    del original,reloaded,raw,repeated,independent,oracle,x;gc.collect();torch.cuda.empty_cache()
    return value,report
