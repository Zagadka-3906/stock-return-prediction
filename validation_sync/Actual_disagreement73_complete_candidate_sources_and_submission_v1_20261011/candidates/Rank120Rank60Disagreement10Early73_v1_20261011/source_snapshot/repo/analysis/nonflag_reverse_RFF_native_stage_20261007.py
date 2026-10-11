"""Real native linear residual stage preserving the complete parent's flagged outputs."""
import hashlib
import numpy as np

def after_parent(ns,context,teacher,parent,spec,components):
    import pandas as pd,joblib
    from nonflag_residual_RFFRidge_codec_20261007 import predict_native,predict_decoded
    from nonflag_reverse_RFF_CDF_transform_20261007 import prepare,apply_prepared
    from threadpoolctl import threadpool_limits
    assert spec['residual_sign']==-1
    assert spec['weight']>0. and spec['universe']=='all_current_raw_forecasts'
    assert [c['name'] for c in components]==spec['ordered_equal_mean_components'] and len(components) in (1,2)
    assert context._whole_graph['nonflag_CPU_RFFRidge_residual_CDF']['weight']==spec['weight']
    assert int(context.dates.min())>=20250101
    selected=context.flags!=1; positions=np.flatnonzero(selected)
    prepared=prepare(teacher,context.dates,context.flags,context.valid,spec['universe'])
    pct=np.zeros(len(teacher),dtype=np.float64)
    for day,pos,p,knots,ordered in prepared: pct[pos]=p
    independent_pct=pd.Series(teacher).groupby(context.dates,sort=False).rank(method='average',pct=True).to_numpy()
    assert np.array_equal(pct[selected].view('u8'),independent_pct[selected].view('u8'))
    native_sum=np.zeros(len(teacher),dtype=np.float64); decoded_sum=np.zeros_like(native_sum); controls=[]
    with threadpool_limits(limits=2):
        for c in components:
            info=c['training_info']; assert info['year']==2025
            assert info['last_training_label_date']<info['exclusive_cutoff']<int(context.dates.min()) and info['last_training_label_end']<=info['exclusive_cutoff']
            assert info['features']==[*context._nonflag_raw_feature_names,'qualified106_current_forecast_average_rank_over_N']
            assert ns.sha(c['path'])==c['sha256'] and ns.sha(c['independent_state_path'])==c['independent_state_sha256']
            native=joblib.load(c['path']); reloaded=joblib.load(c['path']); state=ns.read(c['independent_state_path'])
            projection=native['model'].named_steps['rbf'];linear=native['model'].named_steps['ridge']
            assert linear.solver=='cholesky' and linear.alpha==info['parameters']['alpha']
            assert projection.gamma==info['parameters']['gamma'] and projection.n_components==info['parameters']['n_components']
            assert projection.random_state==info['parameters']['random_state'] and state['features']==info['features']
            for left in range(0,len(positions),65536):
                pos=positions[left:left+65536]
                x=np.column_stack([context._nonflag_raw_features[pos],pct[pos]])
                independent_x=np.column_stack([context._nonflag_raw_features[pos],independent_pct[pos]])
                assert np.array_equal(x.view('u8'),independent_x.view('u8'))
                value=predict_native(native,x); repeat=predict_native(reloaded,x); decoded=predict_decoded(state,independent_x)
                assert np.array_equal(value.view('u8'),repeat.view('u8')) and np.array_equal(value.view('u8'),decoded.view('u8'))
                native_sum[pos]+=value; decoded_sum[pos]+=decoded
            controls.append({'name':'nonflag_cpu_rffridge_'+c['name'],'sha256':c['sha256'],'reload_exact':True,'independent_NumPy_decoder_exact':True,
                'actual_nonflag_rows':len(positions),'features':info['features'],'fixed8192_padded_inference_recipe':True})
    native_sum/=len(components); decoded_sum/=len(components)
    assert np.array_equal(native_sum.view('u8'),decoded_sum.view('u8'))
    values=apply_prepared(parent,teacher,context.flags,native_sum,spec['weight'],prepared)
    independent=np.asarray(parent).copy()
    for day,pos,p,knots,ordered in prepared:
        independent[pos]=np.interp(np.minimum(np.maximum(independent_pct[pos]-spec['weight']*decoded_sum[pos],knots[0]),knots[-1]),knots,ordered)
    assert np.array_equal(values.view('u8'),independent.view('u8'))
    assert np.array_equal(values[~selected].view('u8'),np.asarray(parent)[~selected].view('u8'))
    return values,{'residual_sign':-1,'rows':len(values),'actual_nonflag_rows':len(positions),'controls':controls,
        'native_reload_decoder_and_independent_Pandas_CDF_bits_exact':True,'complete_parent_flag_raw_bits_preserved':True,
        'teacher106_before_original_flag_stage_used':True,'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()}
