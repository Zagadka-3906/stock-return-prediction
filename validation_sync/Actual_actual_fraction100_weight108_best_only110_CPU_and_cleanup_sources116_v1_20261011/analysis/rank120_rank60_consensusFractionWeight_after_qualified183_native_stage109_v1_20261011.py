"""Replay two separately trained Rank20 bundles, average raw signals, then apply the frozen CDF."""
from pathlib import Path
import importlib,gc,hashlib
GRAPH_KEY='rank120_rank60_consensusFractionWeight_after_complete_qualified_parent109_v1_20261011'
RECIPE='stock_rank120_rank60_consensusFractionWeight_label_horizon_ID16_cross120_recent252_e64'
BACKENDS={RECIPE:(
    'stock_rank60_embedding_small512_BF16_native_v1_20261011','stock_rank60_embedding_saved_tensor_decoder_v1_20261011',
    'stock_rank120_embedding_small512_BF16_native_v1_20261011','stock_rank120_embedding_saved_tensor_decoder_v1_20261011')}

def after_parent(ns,context,parent,spec,component):
    import numpy as np,joblib,torch
    import rank120_rank60_consensus_raw_signal80_v1_20261011 as mixing
    import protected_upper_tail_rank_permutation_v1_20261010 as codec
    from stock_rank20_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import feature_matrix
    from frontier233_after_complete_parent_native_stage_v1_20261010 import stock_identity
    assert torch.cuda.is_available() and context._whole_graph[GRAPH_KEY]==spec
    assert spec['recipe']==RECIPE and spec['codec']=='valid_pool_protection_v1' and .1<=spec['protect_fraction']<=.5
    assert spec['stage_kind']=='rank120_rank60_consensus_confidence_fusion' and spec['decay'] is None
    assert spec['position']=='after_complete_qualified_parent' and spec['first2020_active']
    assert spec['original_complete_parent_round']==183
    assert 0.<spec['weight']<=1. and spec['sign'] in (-1.,1.)
    assert spec['disagreement_penalty'] in (.5,.75,1.,2.)
    members=component['horizon_components'];assert len(members)==2
    modules=BACKENDS[RECIPE];raws=[];independents=[];controls=[]
    stock_identity(context)
    for i,member in enumerate(members):
        native=importlib.import_module(modules[2*i]);decoder=importlib.import_module(modules[2*i+1])
        info=member['training_info'];meta=info['training_meta'];path=Path(member['path'])
        assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
        assert info['configuration']==member['configuration']==native.CONFIG
        assert native.CONFIG['seed']==20261009 and native.CONFIG['epochs']==64
        assert meta['last']<meta['cutoff_exclusive']<int(context.dates.min())
        assert meta['last_label_end']<meta['cutoff_exclusive']
        assert meta['training_calendar_window']==252 and meta['days']<=252 and meta['vocabulary_fitted_only_mature_training_rows']
        assert native.CONFIG['label_horizon_trading_days']==(60,120)[i]
        assert native.CONFIG['target']==('y_rank_60mean','y_rank_120mean')[i]
        # No equality is imposed on independently matured sixty-day and twenty-day training populations.
        assert ns.sha(path)==member['sha256']==info['model_sha256']
        bundle=joblib.load(path);assert bundle['config']==native.CONFIG and len(bundle['training_losses'])==64
        assert bundle['stock_vocabulary']==meta['stock_vocabulary']
        x=feature_matrix(context,meta)
        x=native.architecture.attach(x,context.frame['ts_code'].to_list(),bundle['stock_vocabulary'])
        assert x.shape==(len(parent),121)
        raw=native.predict_arrays(bundle,x);reload=joblib.load(path)
        repeated=native.predict_arrays(reload,x);independent=decoder.predict_saved_tensors(reload,x,device='cuda')
        assert np.array_equal(raw.view('u8'),repeated.view('u8')) and np.array_equal(raw.view('u8'),independent.view('u8'))
        raw[~context.valid]=-1e6;independent[~context.valid]=-1e6
        raws.append(raw);independents.append(independent)
        controls.append({'name':member['name'],'sha256':member['sha256'],'seed':native.CONFIG['seed'],'label_horizon_trading_days':native.CONFIG['label_horizon_trading_days'],'training_cutoff_exclusive':meta['cutoff_exclusive'],'last_training_label_end':meta['last_label_end'],
            'reload_exact':True,'independent_saved_tensor_forward_exact':True,'rows':len(parent),'feature_count':121})
        del bundle,reload,repeated,x;gc.collect();torch.cuda.empty_cache()
    assert members[0]['sha256']!=members[1]['sha256']
    raw=mixing.combine(*raws,spec['disagreement_penalty'])
    oracle_raw=mixing.scalar_oracle(*independents,spec['disagreement_penalty'])
    assert np.array_equal(raw.view('u8'),oracle_raw.view('u8'))
    args=(context.dates,context.flags,context.valid,spec['weight'],spec['protect_fraction'],spec['sign'])
    value=codec.transform(parent,raw,*args);oracle=codec.pandas_oracle(parent,oracle_raw,*args)
    assert np.array_equal(value.view('u8'),oracle.view('u8'))
    codec.assert_invariants(parent,value,context.dates,context.flags,context.valid,spec['protect_fraction'])
    for member in members:assert ns.sha(member['path'])==member['sha256']
    report={'rows':len(parent),'controls':controls,'recipe':RECIPE,'codec':'valid_pool_protection_v1','disagreement_penalty':spec['disagreement_penalty'],
        'actual_complete_parent_round':183,'native_reload_two_independent_decoders_scalar_mix_and_Pandas_protected_tail_bits_exact':True,
        'complete_selected_parent_executed_before_new_stage':True,'labels_read_by_stage':False,
        'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()}
    del raws,independents,raw,oracle_raw,oracle;gc.collect();torch.cuda.empty_cache()
    return value,report
