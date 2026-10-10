"""Replay independent saved return/rank embedding tensors before same-day consensus."""
import gc,hashlib,importlib
from pathlib import Path
GRAPH_KEY='stock_dual_embedding_after_complete_parent_v1_20261010'
RETURN_RECIPE='stock_embedding16_cross120_return1d_recent252_small512_BF16_e24'
RANK_RECIPE='stock_rank_embedding16_cross120_rank1d_recent252_small512_BF16_e24'
BACKENDS={RETURN_RECIPE:('stock_embedding_small512_BF16_native_v1_20261010','stock_embedding_saved_tensor_decoder_v1_20261010'),RANK_RECIPE:('stock_rank_embedding_small512_BF16_native_v1_20261010','stock_rank_embedding_saved_tensor_decoder_v1_20261010')}
CODECS={'valid_pool_protection_v1':'protected_upper_tail_rank_permutation_v1_20261010','official_Top_protection_v2':'protected_official_top_rank_permutation_v2_20261010'}
def after_parent(ns,context,parent,spec,components):
    import numpy as np,torch,joblib
    from stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import feature_matrix
    from frontier233_after_complete_parent_native_stage_v1_20261010 import stock_identity
    import dual_target_daily_rank_consensus_v1_20261010 as dual
    assert torch.cuda.is_available() and len(components)==2
    assert spec['stage_kind']=='stock_return_rank_embedding_consensus' and spec['anchor_round'] in (169,170,171,172,173)
    assert spec['position']=='after_complete_qualified_parent' and spec['first2020_active']
    assert context._whole_graph[GRAPH_KEY]==spec and spec['mean_weight'] in (.25,.5,.75)
    assert 0.<spec['weight']<=1. and spec['sign'] in (-1.,1.) and .1<=spec['protect_fraction']<=.5
    assert spec['codec'] in CODECS
    stock_identity(context)
    x=None;raws=[];oracles=[];controls=[]
    for recipe,component in zip((RETURN_RECIPE,RANK_RECIPE),components):
        native=importlib.import_module(BACKENDS[recipe][0]);decoder=importlib.import_module(BACKENDS[recipe][1])
        info=component['training_info'];meta=info['training_meta']
        assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
        assert meta['last']<meta['cutoff_exclusive']<int(context.dates.min()) and meta['last_label_end']<=meta['cutoff_exclusive']
        assert meta['training_calendar_window']==252 and meta['days']<=252 and meta['vocabulary_fitted_only_mature_training_rows']
        assert info['configuration']==native.CONFIG==component['configuration']
        path=Path(component['path']);assert ns.sha(path)==component['sha256']==info['model_sha256']
        if x is None:x=feature_matrix(context,meta)
        else:assert meta['features']==components[0]['training_info']['training_meta']['features'] and meta['raw_features']==context._BF16_feature_names
        bundle=joblib.load(path);assert bundle['config']==native.CONFIG and len(bundle['training_losses'])==24
        assert bundle['stock_vocabulary']==meta['stock_vocabulary']
        attached=native.architecture.attach(x,context.frame['ts_code'].to_list(),bundle['stock_vocabulary'])
        first=native.predict_arrays(bundle,attached);del bundle
        reloaded=joblib.load(path);repeated=native.predict_arrays(reloaded,attached)
        independent=decoder.predict_saved_tensors(reloaded,attached,device='cuda')
        assert np.array_equal(first.view('u8'),repeated.view('u8')) and np.array_equal(first.view('u8'),independent.view('u8'))
        first[~context.valid]=-1e6;independent[~context.valid]=-1e6
        raws.append(first);oracles.append(independent)
        controls.append({'name':component['name'],'sha256':component['sha256'],'recipe':recipe,'reload_exact':True,'independent_saved_tensor_forward_exact':True,'rows':len(parent),'feature_count':121,'numeric_feature_count':120,'fixed8192_padded_FP32_inference':True,'vocabulary_fitted_only_mature_training_rows':True})
        assert ns.sha(path)==component['sha256'];del reloaded,repeated,attached;gc.collect();torch.cuda.empty_cache()
    mixed=dual.transform(raws[0],raws[1],context.dates,spec['mean_weight'])
    independent_mixed=dual.pandas_oracle(oracles[0],oracles[1],context.dates,spec['mean_weight'])
    assert np.array_equal(mixed.view('u8'),independent_mixed.view('u8'))
    codec=importlib.import_module(CODECS[spec['codec']]);args=(context.dates,context.flags,context.valid,spec['weight'],spec['protect_fraction'],spec['sign'])
    value=codec.transform(parent,mixed,*args);oracle=codec.pandas_oracle(parent,independent_mixed,*args)
    assert np.array_equal(value.view('u8'),oracle.view('u8'))
    codec.assert_invariants(parent,value,context.dates,context.flags,context.valid,spec['protect_fraction'])
    report={'rows':len(parent),'controls':controls,'native_reload_independent_tensor_and_Pandas_stage_bits_exact':True,'mean_weight':spec['mean_weight'],'return_embedding_first_rank_embedding_second':True,'complete_selected_parent_executed_before_new_stage':True,'labels_read_by_stage':False,'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()}
    del x,raws,oracles,mixed,independent_mixed,oracle;gc.collect();torch.cuda.empty_cache()
    return value,report
