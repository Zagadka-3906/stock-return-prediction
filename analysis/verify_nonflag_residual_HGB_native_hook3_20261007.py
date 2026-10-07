"""Actual three native nonflag component routes on603 historical rows and two day prefixes."""
from pathlib import Path
from types import SimpleNamespace
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    import numpy as np,polars as pl
    from run import fold_cutoff
    from nonflag_residual_HGB_native_stage_20261007 import after_parent
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    bank=A/'nonflag_residual_HGB_bank10_20261007';proof=read(bank/'verification.json')
    assert proof['actual_native_fits']==10
    out=A/'nonflag_residual_HGB_native_hook3_preflight_20261007';assert not out.exists();out.mkdir()
    plan=read(A/'nonflag_residual_HGB10_plan_20261007.json');head=list(plan['configurations'])
    paths=[Path(__file__),A/'nonflag_residual_HGB_native_stage_20261007.py',A/'predict_nonflag_residual_HGB_complete_scheme_20261007.py',
      A/'nonflag_residual_HGB_CDF_transform_20261007.py',bank/'verification.json',ROOT/'data/features.parquet',ROOT/'data/feature_manifest.json',
      A/'optimization_20261003_r106/selected_validation.npy']
    components={}
    for name in head:
        info_path=bank/name/'info_2025.json';info=read(info_path);paths += [info_path,Path(info['native_model_path']),Path(info['independent_hist_tree_state_path'])]
        components[name]={'name':name,'source_path':info['native_model_path'],'path':info['native_model_path'],'sha256':info['native_model_sha256'],
          'independent_state_source_path':info['independent_hist_tree_state_path'],'independent_state_path':info['independent_hist_tree_state_path'],
          'independent_state_sha256':info['independent_hist_tree_state_sha256'],'training_info':info}
    pins={str(p):sha(p) for p in paths};create(out/'frozen_before_actual_controls.json',{'input_sha256':pins,'new_native_fits':0,'new_quality_scores':0})
    with LockedReadHashCache(pins) as scope:
        features=read(ROOT/'data/feature_manifest.json')['features']
        frame=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')&(pl.col('trade_date')>=20200101)&(pl.col('trade_date')<fold_cutoff(2021))).sort('trade_date','ts_code').select(features).head(603).collect()
        assert len(frame)==603;x=frame.to_numpy().astype(np.float64)
        teacher=np.asarray(np.load(A/'optimization_20261003_r106/selected_validation.npy',mmap_mode='r')[:603]).copy()
        dates=np.repeat(np.array([20250102,20250103,20250106],dtype=np.int32),201);flags=(np.arange(603)%7==0).astype(np.int8);valid=np.ones(603,dtype=bool)
        parent=teacher.copy();parent[flags==1]+=.125
        ns=SimpleNamespace(sha=sha,read=read);records=[]
        for name,names in [(n,[n]) for n in head]+[('equal_mean_two',head)]:
            spec={'weight':.01,'universe':'all_current_raw_forecasts','ordered_equal_mean_components':names}
            ctx=SimpleNamespace(dates=dates,flags=flags,valid=valid,_whole_graph={'nonflag_CPU_HGB_residual_CDF':spec},_nonflag_raw_features=x,_nonflag_raw_feature_names=features)
            values,report=after_parent(ns,ctx,teacher,parent,spec,[components[n] for n in names])
            assert len(report['controls'])==len(names) and np.array_equal(values[flags==1].view('u8'),parent[flags==1].view('u8'))
            for n in (201,402):
                cold=SimpleNamespace(dates=dates[:n],flags=flags[:n],valid=valid[:n],_whole_graph=ctx._whole_graph,_nonflag_raw_features=x[:n],_nonflag_raw_feature_names=features)
                v,c=after_parent(ns,cold,teacher[:n],parent[:n],spec,[components[k] for k in names]);assert np.array_equal(v.view('u8'),values[:n].view('u8'))
            records.append({'head':name,'actual_native_components':names,'actual_rows':603,'whole_day_prefix_rows':[201,402],'native_reload_independent_Pandas_CDF_and_prefix_bits_exact':True})
        for module in ['predict_conditional_CPU_HGB_residual_CDF_scheme_20261007','predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007','predict_quantile_HGB_residual_CDF_scheme_v2_20261007']:
            text=(A/(module+'.py')).read_text(encoding='utf8');needle="    text = text.replace(needle, '        values = CPU_HGB_AFTER_PARENT(context, values)\\n' + needle)";assert text.count(needle)==1
            assert text.count("'CPU_HGB_AFTER_PARENT': after_parent}")==1
        text=(A/'predict_simplex_residual47_native_scheme_20261006.py').read_text(encoding='utf8');assert text.count('        return values\n')==1
        scope.reverify()
    create(out/'verification.json',{'status':'passed_actual3_historical603_nonflag_HGB_native_reload_decoder_CDF_and_whole_day_prefix_controls',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'native_component_counts':[1,1,2],
      'original_parent15_and_flag_backend_injection_points_checked_not_executed_by_this_diagnostic':True,
      'synthetic_dates':[20250102,20250103,20250106],'actual_future1599600_two_replays_and_cold80_not_claimed':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'passed','native_hook_cases':3},flush=True)
if __name__=='__main__':main()
