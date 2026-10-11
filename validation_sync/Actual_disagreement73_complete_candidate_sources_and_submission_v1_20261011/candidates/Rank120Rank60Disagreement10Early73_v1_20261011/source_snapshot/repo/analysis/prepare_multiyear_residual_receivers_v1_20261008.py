"""Repair calendar admission before quality, without altering fitted models or immutable evidence."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute


def main():
    originals=[];generated=[]
    native_pairs=(('CrossFamily_complete_parent_native_stage_v1_20261008','CrossFamily_complete_parent_native_stage_v2_20261008'),
        ('HuberIRLS64_complete_parent_native_stage_v2_20261008','HuberIRLS64_complete_parent_native_stage_v3_20261008'))
    mapping=dict(native_pairs)
    mapping.update({'predict_CrossFamily_complete_parent_scheme_v1_20261008':'predict_CrossFamily_complete_parent_scheme_v2_20261008',
        'predict_HuberIRLS64_complete_parent_scheme_v2_20261008':'predict_HuberIRLS64_complete_parent_scheme_v3_20261008',
        'verify_CrossFamily15_native_historical_hooks_v1_20261008':'verify_CrossFamily15_native_historical_hooks_v2_20261008',
        'CrossFamily15_native_historical_hooks_v1_20261008':'CrossFamily15_native_historical_hooks_v2_20261008',
        'actual_CrossFamily15_native_hooks_location_v1_20261008':'actual_CrossFamily15_native_hooks_location_v2_20261008',
        'verify_HuberIRLS64_18_native_historical_hooks_v2_20261008':'verify_HuberIRLS64_18_native_historical_hooks_v3_20261008',
        'HuberIRLS64_18_native_historical_hooks_v2_20261008':'HuberIRLS64_18_native_historical_hooks_v3_20261008',
        'actual_HuberIRLS64_18_native_hooks_location_v2_20261008':'actual_HuberIRLS64_18_native_hooks_location_v3_20261008'})
    for old,new in native_pairs:
        source=A/(old+'.py');text=source.read_text(encoding='utf8');originals.append(source)
        if old.startswith('Cross'):
            before="years=np.unique(context.dates//10000);assert len(years)==1 and int(years[0])>=2021\n    year=int(years[0]);positions=np.flatnonzero(context.flags!=1)"
        else:
            before="years=np.unique(context.dates//10000);assert len(years)==1 and years[0]>=2021\n    year=int(years[0]);positions=np.flatnonzero(context.flags!=1)"
        assert text.count(before)==1
        after="""years=np.unique(context.dates//10000)
    fit_years={int(component['training_info']['year']) for component in components}
    assert len(fit_years)==1 and len(years)>0
    year=next(iter(fit_years))
    assert year>=2021 and int(years.min())>=year
    # Historical folds use their own model; all multi-year future rows use the final frozen2025 model.
    assert len(years)==1 and int(years[0])==year or year==2025
    positions=np.flatnonzero(context.flags!=1)"""
        text=text.replace(before,after)
        text=text.replace("'rows':len(parent),'year':year,","'rows':len(parent),'year':year,'prediction_calendar_years':[int(y) for y in years],\n        'saved_fit_year_fixed_for_all_prediction_dates':True,")
        target=A/(new+'.py');assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');generated.append(target)
    for old,new in mapping.items():
        if old in dict(native_pairs) or not old.startswith(('predict_','verify_')):continue
        source=A/(old+'.py');assert source.is_file();originals.append(source)
        text=substitute(source.read_text(encoding='utf8'),mapping);target=A/(new+'.py');assert not target.exists()
        compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');generated.append(target)
    create(A/'multiyear_residual_native_preparation_v1_20261008.json',{
        'status':'fresh_fixed_saved_fit_year_receivers_prepared_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'old_source_sha256':{str(p):sha(p) for p in originals},
        'new_source_sha256':{str(p):sha(p) for p in generated},'mapping':mapping,
        'all_original_fitted_models_and_CDF_math_unchanged':True,'new_official_scores':0,'new_fits':0,
        'historical_native_and_synthetic_calendar_controls_still_required':True,'test_labels_read':False})


if __name__=='__main__':main()
