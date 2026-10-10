"""Replay either two own120 forecasts or a causal parent-only holding stability stage."""
from pathlib import Path
import gc,hashlib,importlib
GRAPH_KEY='frontier233_after_complete_qualified_parent_v1_20261010'

def stock_identity(context):
    import numpy as np
    codes=context.frame['ts_code'].to_numpy();dates=np.asarray(context.dates)
    assert np.array_equal(context.frame['trade_date'].to_numpy(),dates),'Date metadata must match the verified stock panel'
    assert len(codes)==len(dates)>0 and len(dates)%4650==0
    assert np.all(dates[1:]>=dates[:-1]) and np.all(np.unique(dates,return_counts=True)[1]==4650)
    panel=codes.reshape(-1,4650)
    assert len(set(panel[0]))==4650 and np.all(panel==panel[0]),'Fixed sorted stock identity is required'
    assert np.array_equal(panel[0],np.asarray(sorted(panel[0]))),'Canonical stock ordering is required'
    return codes

def saved_signals(ns,context,components):
    import joblib,numpy as np,torch
    from cross120_after_complete169_native_stage_v2_20261010 import BACKENDS,feature_matrix
    expected=['cross120recent252forward5huber050','cross120recent252rank5huber050']
    assert [component['recipe'] for component in components]==expected
    for component in components:
        info=component['training_info'];meta=info['training_meta'];native=importlib.import_module(BACKENDS[component['recipe']][0])
        assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
        assert meta['last']<meta['last_label_end']<meta['cutoff_exclusive']<int(context.dates.min())
        assert meta['training_calendar_window']==252 and meta['days']<=252
        assert info['configuration']==component['configuration']==native.CONFIG and meta['raw_features']==context._BF16_feature_names
        assert ns.sha(component['path'])==component['sha256']==info['model_sha256']
    assert torch.cuda.is_available()
    x=feature_matrix(context,components[0]['training_info']['training_meta']);signals=[];independent=[];controls=[]
    for component in components:
        assert components[0]['training_info']['training_meta']['features']==component['training_info']['training_meta']['features']
        native=importlib.import_module(BACKENDS[component['recipe']][0]);decoder=importlib.import_module(BACKENDS[component['recipe']][1])
        bundle=joblib.load(component['path']);reloaded=joblib.load(component['path'])
        assert bundle['config']==native.CONFIG and len(bundle['training_losses'])==64
        raw=native.predict_arrays(bundle,x);repeated=native.predict_arrays(reloaded,x);oracle=decoder.predict_saved_tensors(reloaded,x,device='cuda')
        assert np.array_equal(raw.view('u8'),repeated.view('u8')) and np.array_equal(raw.view('u8'),oracle.view('u8'))
        raw[~context.valid]=-1e6;oracle[~context.valid]=-1e6
        signals.append(raw);independent.append(oracle)
        controls.append({'name':component['name'],'sha256':component['sha256'],'reload_exact':True,'independent_saved_tensor_forward_exact':True,
            'rows':len(raw),'feature_count':120,'original_parent_feature_count':63,'fixed8192_padded_FP32_inference':True})
        assert ns.sha(component['path'])==component['sha256']
        del bundle,reloaded,repeated;gc.collect();torch.cuda.empty_cache()
    del x;return signals,independent,controls

def after_parent(ns,context,parent,spec,components):
    import numpy as np
    stock_identity(context)
    assert spec['anchor_round'] in (169,170) and spec['position']=='after_complete_qualified_parent'
    assert context._whole_graph[GRAPH_KEY]==spec and spec['stage_kind']!='anchor'
    if spec['stage_kind']=='parent_only_budget_stability':
        import budgeted_neural_Top_projection_v1_20261010 as codec
        assert components==[] and spec['weight']==spec['sign']==1.
        args=(context.dates,context.flags,context.valid,1.,spec['budget_fraction'],spec['margin'],1.)
        value,trace=codec.transform(parent,np.asarray(parent,dtype=np.float64),*args,return_trace=True)
        oracle,other=codec.pandas_oracle(parent,np.asarray(parent,dtype=np.float64),*args,return_trace=True)
        assert trace==other and all(row['optional_swaps']<=row['budget'] for row in trace)
        assert np.array_equal(value[:4650].view('u8'),np.asarray(parent[:4650],dtype=np.float64).view('u8'))
        controls=[];extra={'empty_first_date_state_original_parent_Top':True,'sequential_state_no_annual_reset':True,'optional_budget_trace':trace}
    else:
        assert spec['stage_kind']=='dual120_rank_consensus' and spec['anchor_round']==169
        from dual_target_daily_rank_consensus_v1_20261010 import transform,pandas_oracle
        from cross120_after_complete169_native_stage_v2_20261010 import CODECS
        raw,independent,controls=saved_signals(ns,context,components)
        mixed=transform(*raw,context.dates,spec['mean_weight']);mixed_oracle=pandas_oracle(*independent,context.dates,spec['mean_weight'])
        assert np.array_equal(mixed.view('u8'),mixed_oracle.view('u8'))
        codec=importlib.import_module(CODECS[spec['kind']])
        args=(context.dates,context.flags,context.valid,*((spec['role'],spec['weight'],spec['sign']) if spec['kind']=='CDF' else (spec['weight'],spec['protect_fraction'],spec['sign'])))
        value=codec.transform(parent,mixed,*args);oracle=codec.pandas_oracle(parent,mixed_oracle,*args)
        if spec['kind']=='CDF':
            chosen=codec.selected(context.flags,context.valid,spec['role'])
            assert np.array_equal(value[~chosen].view('u8'),np.asarray(parent,dtype=np.float64)[~chosen].view('u8'))
        else:codec.assert_invariants(parent,value,context.dates,context.flags,context.valid,spec['protect_fraction'])
        extra={'two_saved120_signals_same_date_consensus_before_eligibility_filter':True}
    assert np.array_equal(value.view('u8'),oracle.view('u8'))
    report={'rows':len(parent),'controls':controls,'stage_kind':spec['stage_kind'],'actual_complete_parent_round':spec['anchor_round'],
        'complete_selected_parent_executed_before_new_stage':True,'native_reload_independent_tensor_and_Pandas_stage_bits_exact':True,
        'stock_identity_grid_verified':True,'new_native_fits':0,'labels_read_by_stage':False,
        'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest(),**extra}
    del oracle;gc.collect();return value,report
