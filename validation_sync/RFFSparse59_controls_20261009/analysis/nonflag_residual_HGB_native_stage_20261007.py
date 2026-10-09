"""Execute new nonflag native models after preserved parent flag stage, using106 current teacher."""
import hashlib
import numpy as np
def after_parent(ns,context,teacher,parent,spec,components):
    import pandas as pd,joblib
    import cpu_numerical_HGB_large_batch_codec_v2_20261007 as codec
    from memory_bounded_numeric_preparation_20261007 import prepare as bounded_prepare
    from nonflag_residual_HGB_CDF_transform_20261007 import prepare,apply_prepared
    from threadpoolctl import threadpool_limits
    old_prepare=codec.prepare;codec.prepare=bounded_prepare
    assert spec['weight']>0. and spec['universe']=='all_current_raw_forecasts'
    assert [c['name'] for c in components]==spec['ordered_equal_mean_components'] and len(components) in (1,2)
    assert context._whole_graph['nonflag_CPU_HGB_residual_CDF']['weight']==spec['weight']
    selected=context.flags!=1;positions=np.flatnonzero(selected)
    prepared=prepare(teacher,context.dates,context.flags,context.valid,spec['universe'])
    pct=np.zeros(len(teacher),dtype=np.float64)
    for day,pos,p,knots,ordered in prepared:pct[pos]=p
    assert int(context.dates.min())>=20250101
    independent_pct=pd.Series(teacher).groupby(context.dates,sort=False).rank(method='average',pct=True).to_numpy()
    assert np.array_equal(pct[selected].view('u8'),independent_pct[selected].view('u8'))
    native_sum=np.zeros(len(teacher),dtype=np.float64);decoded_sum=np.zeros_like(native_sum);controls=[]
    try:
        with threadpool_limits(limits=4):
            for c in components:
                info=c['training_info'];assert info['year']==2025 and info['actual_iterations']==96
                assert info['last_training_label_date']<info['exclusive_cutoff']<int(context.dates.min()) and info['last_training_label_end']<=info['exclusive_cutoff']
                assert info['features']==[*context._nonflag_raw_feature_names,'qualified106_current_forecast_average_rank_over_N']
                assert ns.sha(c['path'])==c['sha256'] and ns.sha(c['independent_state_path'])==c['independent_state_sha256']
                native=joblib.load(c['path']);reloaded=joblib.load(c['path']);state=ns.read(c['independent_state_path'])
                assert native['model'].n_iter_==96 and native['model'].loss==info['parameters']['loss']
                assert len(state['trees'])==96 and state['loss']==info['parameters']['loss']
                for left in range(0,len(positions),65536):
                    pos=positions[left:left+65536]
                    x=np.column_stack([context._nonflag_raw_features[pos],pct[pos]])
                    independent_x=np.column_stack([context._nonflag_raw_features[pos],independent_pct[pos]])
                    assert np.array_equal(x.view('u8'),independent_x.view('u8'))
                    value=codec.predict_native(native,x);repeat=codec.predict_native(reloaded,x);decoded=codec.predict_decoded(state,independent_x)
                    assert np.array_equal(value.view('u8'),repeat.view('u8')) and np.array_equal(value.view('u8'),decoded.view('u8'))
                    native_sum[pos]+=value;decoded_sum[pos]+=decoded
                controls.append({'name':'nonflag_cpu_hgb_'+c['name'],'sha256':c['sha256'],'reload_exact':True,'independent_NumPy_decoder_exact':True,
                  'actual_nonflag_rows':len(positions),'features':info['features'],'recipe_batch256_runtime8192_outer65536':True})
        native_sum/=len(components);decoded_sum/=len(components)
        assert np.array_equal(native_sum.view('u8'),decoded_sum.view('u8'))
        values=apply_prepared(parent,teacher,context.flags,native_sum,spec['weight'],prepared)
        independent=np.asarray(parent).copy()
        for day,pos,p,knots,ordered in prepared:
            independent[pos]=np.interp(np.minimum(np.maximum(independent_pct[pos]+spec['weight']*decoded_sum[pos],knots[0]),knots[-1]),knots,ordered)
        assert np.array_equal(values.view('u8'),independent.view('u8'))
        assert np.array_equal(values[~selected].view('u8'),np.asarray(parent)[~selected].view('u8'))
        report={'rows':len(values),'actual_nonflag_rows':len(positions),'controls':controls,'native_reload_decoder_and_independent_Pandas_CDF_bits_exact':True,
          'complete_parent_flag_raw_bits_preserved':True,'teacher106_before_original_flag_stage_used':True,
          'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()}
        return values,report
    finally:codec.prepare=old_prepare
