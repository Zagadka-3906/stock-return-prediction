"""Exercise the actual selected full-pool hook using four real96-tree diagnostic models."""
from pathlib import Path
from types import SimpleNamespace
import ast,os,sys,time
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import numpy as np,pandas as pd,polars as pl,joblib
    from sklearn.linear_model import ElasticNet
    import warnings
    from threadpoolctl import threadpool_limits
    from run import fold_cutoff
    from full_universe_HGB_percentile_CDF_transform_20261007 import prepare,apply_prepared,centered_daily_forecast,transform
    from cpu_ElasticNet_independent_linear_codec_20261007 import target_scale,export,predict_native,predict_decoded
    from ElasticNet_memory_bounded_preprocessing_20261007 import fit_preprocessing,prepare_training_fortran as feature_prepare
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out=A/'ElasticNet_selected_hook_preflight_20261007';assert not out.exists();out.mkdir()
    source=A/'predict_full_universe_CPU_ElasticNet_rank_CDF_scheme_20261007.py'
    sources=[Path(__file__),source,A/'cpu_full_universe_ElasticNet_bank24_plan_20261007.json',A/'full_universe_HGB_percentile_CDF_transform_20261007.py',A/'cpu_ElasticNet_independent_linear_codec_20261007.py',A/'ElasticNet_memory_bounded_preprocessing_20261007.py',ROOT/'data/features.parquet',ROOT/'data/feature_manifest.json',ROOT/'run.py',ROOT/'后续选模标准.md']
    pins={str(p.resolve()):sha(p) for p in sources};create(out/'frozen_before_actual_controls.json',{'input_sha256':pins,'actual_declared_diagnostic_fits':4,'max_iterations':2000,'synthetic_future_context_dates_with_actual_historical_prediction_features':True,'actual_selection_fits':0,'actual_official_scores':0,'actual_future_features_not_read':True,'test_labels_read':False})
    with LockedReadHashCache(pins) as scope,threadpool_limits(limits=2):
        features=read(ROOT/'data/feature_manifest.json')['features'];plan=read(A/'cpu_full_universe_ElasticNet_bank24_plan_20261007.json');cutoff=fold_cutoff(2025)
        lazy=pl.scan_parquet(ROOT/'data/features.parquet');components=[]
        all_days=lazy.filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
        for name,cfg in plan['configurations'].items():
            target=cfg['target'];f=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)&pl.col('price_valid')&pl.col(target).is_finite()).select(list(dict.fromkeys(['trade_date',*features,target]))).sort('trade_date').head(1113).collect()
            x=f.select(features).to_numpy().astype(np.float64);y=f[target].to_numpy().astype(np.float64);prep=fit_preprocessing(x[:512]);ty=y[:512]
            if target=='y_ret_1d':ty=np.clip(ty,*np.quantile(ty,[.005,.995]))
            scaling=target_scale(ty);params={**plan['fixed_parameters'],'alpha':cfg['alpha']}
            with warnings.catch_warnings(record=True) as actual_warnings:
                warnings.simplefilter('always');m=ElasticNet(**params).fit(feature_prepare(x[:512],prep),(ty-scaling['center'])/scaling['scale'])
            bundle={'model':m,'preprocessing':prep,'features':features,'target_scaling':scaling}
            native=out/(name+'.joblib');joblib.dump(bundle,native)
            state=out/(name+'.json');create(state,export(bundle))
            components.append({'name':name,'path':str(native),'sha256':sha(native),'independent_state_path':str(state),'independent_state_sha256':sha(state),'diagnostic_training_rows':512,'actual_native_parameters':params,'actual_warnings':[str(w.message) for w in actual_warnings],'actual_dual_gap':float(m.dual_gap_),'training_info':{'year':2025,'actual_iterations':int(m.n_iter_),'features':features,'training_metadata':{'last_training_label_date':int(f['trade_date'][:512].max()),'exclusive_cutoff':cutoff,'last_training_label_end':int(all_days[np.searchsorted(all_days,int(f['trade_date'][:512].max()))+1])}}})
        test=x[512:];dates=np.repeat([20250102,20250103,20250106],[201,200,200]);valid=np.ones(601,dtype=bool);valid[::29]=False
        raw=np.round(np.sin(np.arange(601)/19),2);flags=(np.arange(601)%7==0).astype(np.int8)
        tree=ast.parse(source.read_text(encoding='utf-8'));function=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='after_parent')
        heads={**{c['name']:[c] for c in components},'rank_pair':components[:2],'return_pair':components[2:],'all_four':components}
        controls=[]
        for name,cs in heads.items():
            ranks=[]
            for c in cs:
                pred=predict_native(joblib.load(c['path']),test);pred[~valid]=-1e6
                ranks.append(pd.Series(pred).groupby(dates,sort=False).rank(method='average',pct=True).to_numpy()-.5)
            mean=np.zeros(601)
            for p in ranks:mean+=p
            mean/=len(cs)
            for weight in plan['planned_official_comparison']['weights']:
                spec={'weight':weight,'universe':'all_current_raw_forecasts','ordered_equal_mean_components':[c['name'] for c in cs]};calls=[]
                ns=SimpleNamespace(sha=sha,read=read)
                namespace={'np':np,'pd':pd,'joblib':joblib,'Path':Path,'threadpool_limits':threadpool_limits,'hashlib':__import__('hashlib'),'ns':ns,'spec':spec,'components':cs,'calls':calls,'prepare':prepare,'apply_prepared':apply_prepared,'centered_daily_forecast':centered_daily_forecast,'predict_native':predict_native,'predict_decoded':predict_decoded}
                exec(compile(ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[])),str(source),'exec'),namespace)
                def context(n):return SimpleNamespace(_whole_graph={'full_universe_CPU_ElasticNet_rank_CDF':spec},_CPU_ELASTIC_raw_features=test[:n],_CPU_ELASTIC_raw_feature_names=features,dates=dates[:n],flags=flags[:n],valid=valid[:n])
                actual=namespace['after_parent'](context(601),raw)
                expected=transform(raw,dates,flags,valid,mean,weight,spec['universe']);assert np.array_equal(actual.view('u8'),expected.view('u8'))
                for n in (201,401):assert np.array_equal(namespace['after_parent'](context(n),raw[:n]).view('u8'),actual[:n].view('u8'))
                controls.append({'head':name,'weight':weight,'actual_native_and_independent_decoder_pandas_rank_CDF_full_and_two_day_prefix_bits_exact':True})
        assert len(controls)==42;scope.reverify()
        create(out/'verification.json',{'status':'passed_actual_four_ElasticNet_diagnostic_models_and42_selected_hook_rank_CDF_full_prefix_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_diagnostic_fits':4,'actual_diagnostic_iteration_cap':2000,'actual_saved_diagnostic_components':components,'actual_hook_heads':7,'actual_weight_configurations':42,'controls':controls,'actual_selection_fits':0,'actual_official_scores':0,'actual1599600_future_or24_full_training_not_claimed':True,'synthetic_dates_actual_historical_features_explicit':True,'test_labels_read':False})
if __name__=='__main__':main()
