"""Two separately fitted mature seeds; native/reloaded/oracle mean before signed parent-rank mixing."""
from pathlib import Path
import gc,hashlib,importlib
GRAPH_KEY='BF16_two_seed09_seed10_equal_mean_complete_parent_rank_CDF'
SEEDS=(20261009,20261010)
NAMES=('rank_MLP2048_BF16_seed09_e64','rank_MLP2048_BF16_seed10_e64')
def after_parent(ns,context,parent,spec,components):
    import joblib,numpy as np,torch,pandas as pd
    from BF16Medium153_complete_parent_rank_CDF_v1_20261009 import transform,pandas_oracle,selected
    assert torch.cuda.is_available()
    assert 0.<spec['weight']<=1. and spec['rank_universe']=='all_current_raw_forecasts'
    assert spec['sign'] in (-1.,1.) and spec['first2020_active'] and spec['position']=='after_complete_qualified_parent'
    assert spec['seed_weights']==[.5,.5] and spec['seed_values']==list(SEEDS)
    graph=context._whole_graph[GRAPH_KEY]
    for key in ('model','role','weight','sign','rank_universe','first2020_active','seed_weights','seed_values'):
        assert graph[key]==spec[key],key
    assert len(components)==2 and [c['name'] for c in components]==list(NAMES)
    modules=[]
    # Check both temporal contracts before calling either network.
    for c,seed,tag in zip(components,SEEDS,('seed09','seed10')):
        native=importlib.import_module('neural_BF16_medium2048_'+tag+'_e64_native_v1_20261009')
        oracle=importlib.import_module('neural_BF16_medium2048_'+tag+'_independent_forward_v1_20261009')
        info=c['training_info'];meta=info['training_meta']
        assert info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
        assert meta['last']<meta['cutoff_exclusive']<int(context.dates.min()) and meta['last_label_end']<=meta['cutoff_exclusive']
        assert meta['features']==context._BF16_feature_names and native.CONFIG['seed']==seed
        assert c['configuration']==info['configuration']==native.CONFIG
        assert ns.sha(c['path'])==c['sha256']==info['model_sha256']
        modules.append((native,oracle))
    assert components[0]['sha256']!=components[1]['sha256']
    x=np.ascontiguousarray(context._BF16_raw_features,dtype=np.float32);assert x.shape==(len(parent),63)
    raw_vectors=[];oracle_vectors=[];controls=[]
    for c,(native,oracle) in zip(components,modules):
        bundle=joblib.load(c['path']);assert bundle['config']==native.CONFIG and len(bundle['training_losses'])==64
        raw=native.predict_arrays(bundle,x);reloaded=joblib.load(c['path'])
        repeated=native.predict_arrays(reloaded,x);independent=oracle.predict_saved_tensors(reloaded,x,device='cuda')
        assert raw.dtype==repeated.dtype==independent.dtype==np.float64
        assert np.array_equal(raw.view('u8'),repeated.view('u8')) and np.array_equal(raw.view('u8'),independent.view('u8'))
        raw[~context.valid]=independent[~context.valid]=-1e6
        raw_vectors.append(raw);oracle_vectors.append(independent)
        controls.append({'name':'BF16_two_seed_full_'+c['name'],'sha256':c['sha256'],'rows':len(parent),'feature_count':63,
            'reload_exact':True,'independent_saved_tensor_forward_exact':True,'fixed8192_padded_FP32_inference':True})
        assert ns.sha(c['path'])==c['sha256']
        del bundle,reloaded,repeated;gc.collect();torch.cuda.empty_cache()
    mean=(raw_vectors[0]+raw_vectors[1])*.5
    independent_mean=((pd.Series(oracle_vectors[0])+pd.Series(oracle_vectors[1]))/2.).to_numpy()
    assert np.array_equal(mean.view('u8'),independent_mean.view('u8')) and np.all(mean[~context.valid]==-1e6)
    value=transform(parent,mean,context.dates,context.flags,context.valid,spec['role'],spec['weight'],spec['sign'])
    oracle=pandas_oracle(parent,independent_mean,context.dates,context.flags,context.valid,spec['role'],spec['weight'],spec['sign'])
    assert np.array_equal(value.view('u8'),oracle.view('u8'))
    mask=selected(context.flags,context.valid,spec['role']);assert np.array_equal(value[~mask].view('u8'),np.asarray(parent)[~mask].view('u8'))
    report={'rows':len(parent),'actual_selected_rows':int(mask.sum()),'controls':controls,'role':spec['role'],'weight':spec['weight'],'sign':spec['sign'],
        'native_reload_independent_tensor_forward_and_Pandas_CDF_bits_exact':True,'two_seed_equal_mean_and_Pandas_arithmetic_bits_exact':True,
        'all_original_parent_branches_executed_before_new_BF16_stage':True,'invalid_and_declared_unselected_parent_forecast_bits_preserved':True,
        'first2020_not_assumed_identity':True,'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()}
    del x,raw_vectors,oracle_vectors,mean,independent_mean,oracle
    gc.collect();torch.cuda.empty_cache()
    return value,report
