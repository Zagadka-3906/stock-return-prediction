"""Run7 quantile native hooks on historical603 features and synthetic dates."""
from pathlib import Path
from types import SimpleNamespace
import ast
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import numpy as np
    import polars as pl
    import predict_quantile_HGB_residual_CDF_scheme_v2_20261007 as hook
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    source=Path(hook.__file__);tree=ast.parse(source.read_text(encoding='utf8'))
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='predict')
    end=next(i for i,n in enumerate(function.body) if isinstance(n,ast.Assign) and ast.unparse(n.targets[0])=='(original_read, original_dump)')
    code=ast.fix_missing_locations(ast.Module(body=function.body[:end],type_ignores=[]))
    out=A/'quantile_HGB_native_hook7_preflight_20261007';assert not out.exists();out.mkdir()
    plan_path=A/'quantile_HGB88_plan_20261007.json';plan=read(plan_path)
    features=read(ROOT/'data/feature_manifest.json')['features'];assert len(features)==63
    bank=A/plan['existing_native_bank'];infos={name:read(bank/name/'info_2025.json') for name in plan['single_native_heads']}
    sources=[Path(__file__),source,plan_path,ROOT/'data/feature_manifest.json',ROOT/'data/features.parquet',A/'quantile_HGB_large_batch_codec_20261007.py',A/'predict_lower_pool_after_quantile_HGB_scheme_v2_20261007.py']
    sources += [bank/name/'info_2025.json' for name in infos]
    pins={str(p):sha(p) for p in sources}
    for info in infos.values():
        pins[info['native_model_path']]=info['native_model_sha256'];pins[info['independent_hist_tree_state_path']]=info['independent_hist_tree_state_sha256']
    create(out/'frozen_before_actual_historical_hook.json',{'input_sha256':pins,'new_native_fits':0,'future_features_not_read':True})
    records=[]
    with LockedReadHashCache(pins) as scope:
        frame=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')&(pl.col('trade_date')<20250101)).select(features).head(603).collect()
        x=frame.to_numpy().astype(np.float64);assert x.shape==(603,63)
        dates=np.repeat(np.array([20250102,20250103,20250106]),201)
        flags=np.zeros(603,dtype=np.int8);flags[::7]=1;valid=np.ones(603,dtype=bool);valid[::31]=False
        parent=np.random.default_rng(20261007).normal(size=603);parent[~valid]=-1e6
        groups={n:[n] for n in plan['single_native_heads']};groups.update(plan['ensembles'])
        for name,ordered in groups.items():
            names=list(dict.fromkeys(ordered));components=[{'name':n,'source_path':infos[n]['native_model_path'],'sha256':infos[n]['native_model_sha256'],
                'independent_state_source_path':infos[n]['independent_hist_tree_state_path'],'independent_state_sha256':infos[n]['independent_hist_tree_state_sha256'],'training_info':infos[n]} for n in names]
            spec={'weight':.0125,'universe':plan['universe'],'native_components':components,'ordered_equal_mean_components':ordered}
            graph={'conditional_flag_CPU_HGB_residual_CDF':spec};ns=SimpleNamespace(ROOT=ROOT,GRAPH_FIELD='graph',sha=sha,read=read)
            local={**vars(hook),'ns':ns,'record':{'winner':{'graph':graph}},'candidate':out/'diagnostic_native_links','parent_curve_source':None,'mapping_path':None}
            exec(compile(code,str(source),'exec'),local)
            context=SimpleNamespace(_whole_graph=graph,_CPU_HGB_raw_features=x,_CPU_HGB_raw_feature_names=features,dates=dates,flags=flags,valid=valid)
            full=local['after_parent'](context,parent.copy())
            for rows in (201,402):
                cold=SimpleNamespace(**vars(context));cold.dates=dates[:rows];cold.flags=flags[:rows];cold.valid=valid[:rows];cold._CPU_HGB_raw_features=x[:rows]
                replay=local['after_parent'](cold,parent[:rows].copy());assert np.array_equal(full[:rows].view('u8'),replay.view('u8'))
            assert len(local['calls'])==3
            assert all(len(c['controls'])==len(names) and len({t['sha256'] for t in c['controls']})==len(names) for c in local['calls'])
            assert np.array_equal(full[flags!=1].view('u8'),parent[flags!=1].view('u8'))
            records.append({'name':name,'ordered_heads':ordered,'unique_native_heads':names,'actual_unique_native_controls':len(names),
                'actual_rows':603,'native_reload_independent_decoder_Pandas_CDF_and_whole_day201_402_bits_exact':True})
        scope.reverify()
    lower= A/'predict_lower_pool_after_quantile_HGB_scheme_v2_20261007.py'
    import predict_lower_pool_after_quantile_HGB_scheme_v2_20261007 as lower_hook
    assert lower_hook.parent_source(graph)==source.name
    modified=source.read_text(encoding='utf8');assert modified.count('        return values\n')==1
    compile(modified.replace('        return values\n','        return LOWER_AFTER_COMPLETE_PARENT(context, values)\n'),str(source),'exec')
    create(out/'verification.json',{'status':'passed_actual7_historical603_quantile_HGB_native_independent_and_whole_day_prefix_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'native1_2_4_component_controls_count_matches_declared_mean':True,
        'lower_after_quantile_parent_source_route_compiled':True,'complete_parent15_and_lower_native_execution_not_claimed':True,
        'historical_rows':603,'synthetic_dates':dates[[0,201,402]].tolist(),'actual_future1599600_or80days_not_claimed':True,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'passed','actual_native_hook_cases':7,'historical_rows':603},flush=True)

if __name__=='__main__':main()
