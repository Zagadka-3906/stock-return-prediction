"""Exercise actual new native HGB hook on historical features with synthetic dates, not future qualification."""
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
    import predict_protected_upper_pool_CPU_HGB_scheme_20261007 as hook
    from protected_upper_pool_HGB_CDF_transform_20261007 import transform
    source=Path(hook.__file__)
    tree=ast.parse(source.read_text(encoding='utf8'))
    f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='predict')
    end=next(i for i,n in enumerate(f.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Tuple) for t in n.targets) and ast.unparse(n.targets[0])=='(original_read, original_dump)')
    code=ast.fix_missing_locations(ast.Module(body=f.body[:end],type_ignores=[]))
    out=A/'protected_upper_pool_HGB_selected_hook_preflight_20261007';assert not out.exists();out.mkdir()
    features=read(ROOT/'data/feature_manifest.json')['features'];assert len(features)==63
    frame=pl.scan_parquet(ROOT/'data/features.parquet').filter(pl.col('is_train')&(pl.col('trade_date')<20250101)).select(features).head(603).collect()
    x=frame.to_numpy().astype(np.float64);assert x.shape==(603,63)
    dates=np.repeat(np.array([20250102,20250103,20250106]),201)
    flags=np.zeros(603,dtype=np.int8);flags[::17]=1
    valid=np.ones(603,dtype=bool);valid[::31]=False
    rng=np.random.default_rng(20261007);parent=rng.normal(size=603);parent[~valid]=-1e6
    plan=read(A/'protected_upper_pool_HGB_CDF_plan_20261007.json')
    heads=plan['single_native_heads'];groups={**{n:[n] for n in heads},**plan['ensembles']}
    infos={n:read(A/'cpu_full_universe_HGB_bank24_recovery_v2_20261007'/n/'info_2025.json') for n in heads}
    records=[]
    for name,names in groups.items():
        for fraction in (.5,.7,.8):
            for weight in (.25,.5,1.):
                components=[{'name':n,'source_path':infos[n]['native_model_path'],'sha256':infos[n]['native_model_sha256'],
                    'independent_state_source_path':infos[n]['independent_hist_tree_state_path'],
                    'independent_state_sha256':infos[n]['independent_hist_tree_state_sha256'],'training_info':infos[n]} for n in names]
                spec={'weight':weight,'lower_fraction':fraction,'native_components':components,'ordered_native_components':names}
                graph={'protected_upper_pool_CPU_HGB_CDF':spec}
                ns=SimpleNamespace(ROOT=ROOT,GRAPH_FIELD='graph',sha=sha,read=read)
                local={**vars(hook),'ns':ns,'record':{'winner':{'graph':graph}},'candidate':out/'diagnostic_native_links',
                    'parent_curve_source':None,'mapping_path':None}
                exec(compile(code,str(source),'exec'),local)
                context=SimpleNamespace(_whole_graph=graph,_lower_HGB_raw_features=x,_lower_HGB_feature_names=features,dates=dates,flags=flags,valid=valid)
                full=local['after_complete_parent'](context,parent.copy())
                for rows in (201,402):
                    cold=SimpleNamespace(**vars(context));cold.dates=dates[:rows];cold.flags=flags[:rows];cold.valid=valid[:rows];cold._lower_HGB_raw_features=x[:rows]
                    replay=local['after_complete_parent'](cold,parent[:rows].copy())
                    assert np.array_equal(full[:rows].view('u8'),replay.view('u8'))
                assert len(local['calls'])==3
                records.append({'head':name,'fraction':fraction,'weight':weight,'actual_rows':603,
                    'actual_native_reload_independent_Pandas_and201_402_whole_day_prefix_bits_exact':True})
    assert len(records)==63
    routes={}
    for key in (None,'conditional_flag_CPU_HGB_residual_CDF','full_universe_CPU_HGB_rank_CDF','full_universe_CPU_ElasticNet_rank_CDF'):
        selected=hook.parent_source({} if key is None else {key:{}})
        text=(A/selected).read_text(encoding='utf8');assert text.count('        return values\n')==1
        modified=text.replace('        return values\n','        return LOWER_AFTER_COMPLETE_PARENT(context, values)\n')
        compile(modified,str(A/selected),'exec');routes[str(key)]=selected
    create(out/'verification.json',{'status':'passed_actual_historical603_features_native_HGB_lower_pool_hook_and_whole_day_prefix_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [source,Path(__file__),A/'protected_upper_pool_HGB_CDF_transform_20261007.py',ROOT/'data/feature_manifest.json']},
        'records':records,'four_complete_parent_dispatch_source_injections_compiled':routes,
        'complete_parent_native_execution_not_tested_by_this_diagnostic':True,
        'actual_future_features_read':False,'actual1599600_or80day_qualification_claimed':False,
        'historical_rows':603,'synthetic_future_dates':dates[[0,201,402]].tolist(),'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'passed','actual_native_hook_cases':63,'historical_rows':603},flush=True)


if __name__=='__main__':main()
