"""Replay each saved Huber head from raw provided features and the original teacher106."""
import hashlib
import numpy as np
from HuberIRLS64_complete_parent_CDF_v1_20261008 import required_heads,mixture,independent_mixture,prepare,apply_prepared,pandas_oracle
GRAPH_KEY='nonflag_CPU_HuberIRLS64_complete_parent_CDF'


def exact(a,b):
    assert a.dtype==b.dtype==np.float64 and a.shape==b.shape
    assert np.array_equal(a.view('u8'),b.view('u8'))


def after_parent(ns,context,teacher,parent,spec,components):
    import pandas as pd,joblib
    from threadpoolctl import threadpool_limits
    from nonflag_HuberIRLS64_streamed_v1_20261008 import CONFIGS,predict_native,predict_decoded
    assert 0.<spec['amplitude']<=.1 and spec['group'] in range(6)
    assert spec['position']=='after_complete_qualified_parent' and spec['universe']=='all_current_raw_forecasts'
    assert spec['teacher_feature']=='qualified106_current_forecast_average_rank_over_N' and context._whole_graph[GRAPH_KEY]==spec
    assert [item['head'] for item in components]==required_heads(spec['group'])
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
    oracle_pct=pd.Series(teacher).groupby(context.dates,sort=False).rank(method='average',pct=True).to_numpy();exact(pct,oracle_pct)
    raw={};independent_raw={};controls=[];metadata=None
    with threadpool_limits(limits=2):
        for component in components:
            info=component['training_info'];assert info['year']==year and component['state_kind']=='HuberIRLS64_linear'
            assert info['last_training_label_date']<info['exclusive_cutoff']<int(context.dates.min())
            assert info['last_training_label_end']<=info['exclusive_cutoff']
            current={key:info[key] for key in ('features','training_rows','exclusive_cutoff','last_training_label_date','last_training_label_end','training_matrix_numeric_sha256','training_target_numeric_sha256')}
            if metadata is None:metadata=current
            assert metadata==current and info['features']==[*context._nonflag_raw_feature_names,spec['teacher_feature']]
            assert ns.sha(component['path'])==component['sha256'] and ns.sha(component['independent_state_path'])==component['independent_state_sha256']
            bundle=joblib.load(component['path']);saved=joblib.load(component['path']);state=ns.read(component['independent_state_path'])
            assert bundle['features']==state['features']==info['features'] and bundle['preprocessing']==state['preprocessing']
            params=bundle['model'].get_params();assert params==info['parameters']==state['training_configuration']
            assert params['solver']=='fixed8192_Huber_IRLS65_normal_equations' and params['alpha']==info['training_rows']*.01
            cfg=CONFIGS[info['name']];assert all(params[key]==value for key,value in cfg.items())
            value=np.zeros(len(parent),dtype=np.float64);other=np.zeros_like(value)
            for left in range(0,len(positions),65536):
                pos=positions[left:left+65536]
                x=np.column_stack([context._nonflag_raw_features[pos],pct[pos]])
                ox=np.column_stack([context._nonflag_raw_features[pos],oracle_pct[pos]]);exact(x,ox)
                primary=predict_native(bundle,x);exact(primary,predict_native(saved,x));decoded=predict_decoded(state,ox);exact(primary,decoded)
                value[pos]=primary;other[pos]=decoded
            raw[component['head']]=value;independent_raw[component['head']]=other
            controls.append({'head':component['head'],'name':component['name'],'sha256':component['sha256'],
                'independent_state_sha256':component['independent_state_sha256'],'reload_exact':True,'independent_decoder_exact':True,
                'actual_nonflag_rows':len(positions),'fixed8192_padded_recipe':True,'year':year})
    residual=mixture(raw,spec['group']);oracle=independent_mixture(independent_raw,spec['group']);exact(residual,oracle)
    value=apply_prepared(parent,residual,context.dates,context.flags,context.valid,spec['amplitude'],prepare(parent,context.dates))
    exact(value,pandas_oracle(parent,oracle,context.dates,context.flags,context.valid,spec['amplitude']))
    preserved=(context.dates<20210101)|(context.flags==1)|~context.valid;exact(value[preserved],np.asarray(parent,dtype=np.float64)[preserved])
    return value,{'rows':len(parent),'year':year,'prediction_calendar_years':[int(y) for y in years],
        'saved_fit_year_fixed_for_all_prediction_dates':True,'controls':controls,'actual_nonflag_rows':len(positions),
        'native_reload_independent_arithmetic_and_Pandas_complete_parent_CDF_bits_exact':True,
        'complete_parent_flag1_invalid_and2020_bits_preserved':True,'original_teacher106_feature_used':True,
        'predicted_all_nonflags_including_invalid_to_preserve_fixed_batch_alignment':True,
        'prediction_numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()}
