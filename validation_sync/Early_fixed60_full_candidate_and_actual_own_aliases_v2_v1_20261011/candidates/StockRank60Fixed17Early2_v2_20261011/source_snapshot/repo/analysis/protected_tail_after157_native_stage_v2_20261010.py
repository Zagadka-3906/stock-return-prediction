"""Own saved-tensor replay and independent tail permutation after the complete157 forecast."""
from pathlib import Path
import gc,hashlib,importlib
GRAPH_KEY='protected_tail_after_complete157_native_v2_20261010'
BACKENDS={
 'huber010':('neural_BF16_medium2048_huber010_seed09_e64_native_v1_20261009','neural_BF16_medium2048_huber010_seed09_independent_forward_v1_20261009'),
 'seed09':('neural_BF16_medium2048_seed09_e64_native_v1_20261009','neural_BF16_medium2048_seed09_independent_forward_v1_20261009'),
 'seed10':('neural_BF16_medium2048_seed10_e64_native_v1_20261009','neural_BF16_medium2048_seed10_independent_forward_v1_20261009'),
 'drop05':('neural_BF16_medium2048_drop05_seed09_e64_native_v1_20261009','neural_BF16_medium2048_drop05_seed09_independent_forward_v1_20261009')}
CODECS={'CDF':'BF16Medium153_complete_parent_rank_CDF_v1_20261009','valid_pool_protection_v1':'protected_upper_tail_rank_permutation_v1_20261010',
        'official_Top_protection_v2':'protected_official_top_rank_permutation_v2_20261010'}

def after_parent(ns,context,parent,spec,component):
    import joblib,numpy as np,torch
    native=importlib.import_module(BACKENDS[spec['recipe']][0])
    decoder=importlib.import_module(BACKENDS[spec['recipe']][1])
    codec=importlib.import_module(CODECS[spec['codec']])
    assert torch.cuda.is_available() and 0.<spec['weight']<=1. and .1<=spec['protect_fraction']<=.5
    assert spec['sign'] in (-1.,1.) and spec['original_complete_parent_round']==157
    assert spec['position']=='after_complete_qualified_parent' and spec['first2020_active']
    assert context._whole_graph[GRAPH_KEY]==spec
    info=component['training_info'];meta=info['training_meta']
    assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
    assert meta['last']<meta['cutoff_exclusive']<int(context.dates.min()) and meta['last_label_end']<=meta['cutoff_exclusive']
    assert meta['features']==context._BF16_feature_names
    path=Path(component['path']);assert ns.sha(path)==component['sha256']==info['model_sha256']
    assert info['configuration']==native.CONFIG==component['configuration']
    x=np.ascontiguousarray(context._BF16_raw_features,dtype=np.float32);assert x.shape==(len(parent),63)
    original=joblib.load(path);assert original['config']==native.CONFIG and len(original['training_losses'])==64
    raw=native.predict_arrays(original,x);reloaded=joblib.load(path)
    repeated=native.predict_arrays(reloaded,x);independent=decoder.predict_saved_tensors(reloaded,x,device='cuda')
    assert np.array_equal(raw.view('u8'),repeated.view('u8')) and np.array_equal(raw.view('u8'),independent.view('u8'))
    raw[~context.valid]=-1e6;independent[~context.valid]=-1e6
    args=(context.dates,context.flags,context.valid,spec['weight'],spec['protect_fraction'],spec['sign'])
    value=codec.transform(parent,raw,*args);oracle=codec.pandas_oracle(parent,independent,*args)
    assert np.array_equal(value.view('u8'),oracle.view('u8'))
    codec.assert_invariants(parent,value,context.dates,context.flags,context.valid,spec['protect_fraction'])
    assert ns.sha(path)==component['sha256']
    controls=[{'name':'protected_tail_after157_'+component['name'],'sha256':component['sha256'],'reload_exact':True,
        'independent_saved_tensor_forward_exact':True,'rows':len(parent),'feature_count':63,'fixed8192_padded_FP32_inference':True}]
    report={'rows':len(parent),'controls':controls,'recipe':spec['recipe'],'codec':spec['codec'],'weight':spec['weight'],
        'protect_fraction':spec['protect_fraction'],'sign':spec['sign'],'native_reload_independent_tensor_forward_and_Pandas_tail_bits_exact':True,
        'complete_parent157_executed_before_new_stage':True,'labels_read_by_stage':False,
        'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()}
    del original,reloaded,raw,repeated,independent,oracle,x;gc.collect();torch.cuda.empty_cache()
    return value,report
