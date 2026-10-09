"""Predict ordered saved residual heads using teacher106, then alter the complete parent's CDF."""
import hashlib
import numpy as np
from RFFSparse_complete_parent_CDF_v3_20261009 import GROUPS,prepare,mixture,independent_mixture,apply_prepared,pandas_oracle

GRAPH_KEY='nonflag_CPU_RFFSparse_complete_parent_CDF'


def exact(a,b):
    assert a.dtype==b.dtype==np.float64 and a.shape==b.shape
    assert np.array_equal(a.view('u8'),b.view('u8'))


def after_parent(ns,context,teacher,parent,spec,components):
    import pandas as pd,joblib
    from nonflag_sparse_Gram64_codec_20261007 import predict_native as sparse_native,predict_decoded as sparse_decoded
    from nonflag_residual_RFF128_codec_20261007 import predict_native as rff_native,predict_decoded as rff_decoded
    from threadpoolctl import threadpool_limits
    assert spec['amplitude']>0. and spec['amplitude']<=.1 and spec['share'] in (.25,.5,.75)
    assert spec['universe']=='all_current_raw_forecasts' and spec['position']=='after_complete_qualified_parent'
    assert spec['teacher_feature']=='qualified106_current_forecast_average_rank_over_N'
    assert context._whole_graph[GRAPH_KEY]==spec
    required=list(dict.fromkeys(h for names,sign in GROUPS[spec['group']] for h in names))
    assert [c['head'] for c in components]==required
    years=np.unique(context.dates//10000)
    fit_years={int(component['training_info']['year']) for component in components}
    assert len(fit_years)==1 and len(years)>0
    year=next(iter(fit_years))
    assert year>=2021 and int(years.min())>=year
    # Historical folds use their own model; all multi-year future rows use the final frozen2025 model.
    assert len(years)==1 and int(years[0])==year or year==2025
    positions=np.flatnonzero(context.flags!=1)
    pct=np.empty(len(teacher),dtype=np.float64)
    for left,right,p,knots,ordered in prepare(teacher,context.dates):pct[left:right]=p
    oracle_pct=pd.Series(teacher).groupby(context.dates,sort=False).rank(method='average',pct=True).to_numpy()
    exact(pct,oracle_pct)
    raw={};decoded_raw={};controls=[];reference_metadata=None
    with threadpool_limits(limits=2):
        for component in components:
            head=component['head'];info=component['training_info'];kind=component['state_kind']
            assert info['year']==year
            assert info['last_training_label_date']<info['exclusive_cutoff']<int(context.dates.min())
            assert info['last_training_label_end']<=info['exclusive_cutoff']
            metadata={key:info[key] for key in ('features','training_rows','exclusive_cutoff','last_training_label_date','last_training_label_end','training_matrix_numeric_sha256','training_target_numeric_sha256')}
            if reference_metadata is None:reference_metadata=metadata
            assert metadata==reference_metadata
            assert info['features']==[*context._nonflag_raw_feature_names,spec['teacher_feature']]
            assert ns.sha(component['path'])==component['sha256'] and ns.sha(component['independent_state_path'])==component['independent_state_sha256']
            bundle=joblib.load(component['path']);reloaded=joblib.load(component['path']);state=ns.read(component['independent_state_path'])
            assert bundle['features']==state['features']==info['features'] and bundle['preprocessing']==state['preprocessing']
            native,decoded=(rff_native,rff_decoded) if kind=='random_fourier_linear' else (sparse_native,sparse_decoded)
            assert kind in ('random_fourier_linear','SparseGram64_linear')
            if head.startswith('rff_'):
                assert kind=='random_fourier_linear' and state['kind']=='nonflag_residual_RFF128'
                projection=bundle['model'].named_steps['rbf'];linear=bundle['model'].named_steps['ridge']
                assert projection.gamma==info['parameters']['gamma'] and projection.n_components==128
                assert linear.alpha==info['parameters']['alpha']
                assert projection.random_state==info['parameters']['random_state'] and linear.solver=='cholesky'
            else:
                assert head in ('sparse_l1','sparse_elastic') and kind=='SparseGram64_linear'
                assert bundle['model'].get_params()==info['parameters']
                assert info['parameters']['solver']=='own_centered_Gram64_cyclic_coordinate_descent'
                assert state['kind']=='nonflag_residual_SparseGram64'
                assert bundle['model'].alpha_==info['parameters']['alpha']
            values=np.zeros(len(parent),dtype=np.float64);independent=np.zeros_like(values)
            for left in range(0,len(positions),65536):
                pos=positions[left:left+65536]
                x=np.column_stack([context._nonflag_raw_features[pos],pct[pos]])
                oracle_x=np.column_stack([context._nonflag_raw_features[pos],oracle_pct[pos]])
                exact(x,oracle_x)
                value=native(bundle,x);exact(value,native(reloaded,x));other=decoded(state,oracle_x);exact(value,other)
                values[pos]=value;independent[pos]=other
            raw[head]=values;decoded_raw[head]=independent
            controls.append({'head':head,'name':component['name'],'sha256':component['sha256'],'independent_state_sha256':component['independent_state_sha256'],
                'reload_exact':True,'independent_decoder_exact':True,'actual_nonflag_rows':len(positions),'fixed8192_padded_recipe':True,'year':year})
    residual=mixture(raw,spec['group'],spec['share']);oracle_residual=independent_mixture(decoded_raw,spec['group'],spec['share']);exact(residual,oracle_residual)
    values=apply_prepared(parent,residual,context.dates,context.flags,context.valid,spec['amplitude'],prepare(parent,context.dates))
    exact(values,pandas_oracle(parent,oracle_residual,context.dates,context.flags,context.valid,spec['amplitude']))
    preserved=(context.dates<20210101)|(context.flags==1)|~context.valid;exact(values[preserved],np.asarray(parent,dtype=np.float64)[preserved])
    return values,{'rows':len(parent),'year':year,'prediction_calendar_years':[int(y) for y in years],
        'saved_fit_year_fixed_for_all_prediction_dates':True,'actual_nonflag_rows':len(positions),'controls':controls,
        'native_reload_independent_arithmetic_and_Pandas_complete_parent_CDF_bits_exact':True,
        'complete_parent_flag1_invalid_and2020_bits_preserved':True,'original_teacher106_feature_used':True,
        'predicted_all_nonflags_including_invalid_to_preserve_fixed_batch_alignment':True,
        'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()}
