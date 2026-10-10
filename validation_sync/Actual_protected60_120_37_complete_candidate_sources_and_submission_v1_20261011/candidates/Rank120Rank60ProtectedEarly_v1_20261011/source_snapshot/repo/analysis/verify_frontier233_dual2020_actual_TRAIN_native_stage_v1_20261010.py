"""Actual CUDA saved-state controls on TRAIN-only2020 features; no candidate selection or future X."""
from pathlib import Path
from types import SimpleNamespace
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    # Do not contend with the next own bank or an actual selected candidate GPU replay.
    for name in ('actual_BF16_medium2048_cross120recent252returnhuber050_seed09_e64_bank6_v1_20261009','Cross120170_selected_candidate_preparation_v1_20261010','Cross120170_selected_native14_v3_20261010'):
        folder=A/'service_owned_workflows_20261006'/name
        if (folder/'native_launch.json').exists() and owned(read(folder/'native_launch.json')):
            if name=='Cross120170_selected_native14_v3_20261010':
                assert not Path('E:/赛题五_本机临时/cross120_two_target132_selected_native14_v1_20261010').exists()
            else:raise RuntimeError('Actual GPU bank or candidate already running; defer this control')
    import numpy as np,polars as pl,importlib
    import frontier233_after_complete_parent_native_stage_v1_20261010 as stage
    from normalize_predeclared_cross120_two_target132_v5_20261010 import RECIPES
    from cross120_after_complete169_native_stage_v2_20261010 import BACKENDS
    from run import FEATURE_FILE,feature_names,to_matrix
    frame=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['ts_code','trade_date','flag_limit_up','price_valid']).head(13950)
    days=frame['trade_date'].unique().to_list();features=feature_names()
    source=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(['ts_code','trade_date',*features]).sort('trade_date','ts_code').collect()
    assert source.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
    components=[];paths=[Path(__file__),Path(stage.__file__),A/'dual_target_daily_rank_consensus_v1_20261010.py',FEATURE_FILE,A/'optimization_20261003_r169/selected_validation.npy']
    for recipe in ('cross120recent252forward5huber050','cross120recent252rank5huber050'):
        name,bankname=RECIPES[recipe];bank=Path('E:/赛题五_本机临时')/bankname;info=read(bank/'2020/info.json');native=importlib.import_module(BACKENDS[recipe][0])
        components.append({'name':name,'recipe':recipe,'path':str(bank/'2020/model.joblib'),'sha256':info['model_sha256'],'configuration':native.CONFIG,'training_info':info})
        paths.extend([bank/'2020/model.joblib',bank/'2020/info.json',Path(native.__file__),A/(BACKENDS[recipe][1]+'.py')])
    pins={str(p):sha(p) for p in paths};parent=np.load(A/'optimization_20261003_r169/selected_validation.npy',mmap_mode='r')[:13950]
    records=[]
    for mean_weight in (.25,.5,.75):
        for kind in ('CDF','valid_pool_protection_v1','official_Top_protection_v2'):
            assert allowed()
            spec={'stage_kind':'dual120_rank_consensus','anchor_round':169,'position':'after_complete_qualified_parent',
                'mean_weight':mean_weight,'kind':kind,'role':'nonflag_valid','weight':.064,'sign':1.,'protect_fraction':None if kind=='CDF' else .25}
            ctx=SimpleNamespace(frame=frame,dates=frame['trade_date'].to_numpy(),flags=frame['flag_limit_up'].to_numpy(),valid=frame['price_valid'].to_numpy(),
                _BF16_raw_features=to_matrix(source,features),_BF16_feature_names=features,_whole_graph={stage.GRAPH_KEY:spec})
            value,full=stage.after_parent(SimpleNamespace(sha=sha),ctx,parent,spec,components)
            cold=SimpleNamespace(**vars(ctx));cold.frame=frame.head(4650)
            for key in ('dates','flags','valid','_BF16_raw_features'):setattr(cold,key,getattr(ctx,key)[:4650])
            prefix,report=stage.after_parent(SimpleNamespace(sha=sha),cold,parent[:4650],spec,components)
            assert np.array_equal(value[:4650].view('u8'),prefix.view('u8')) and len(full['controls'])==len(report['controls'])==2
            records.append({'configuration':spec,'full':full,'cold':report,'whole_date_cold_bits_exact':True})
            print({'actual_dual_saved_state_controls':len(records),'expected':9},flush=True)
    for p,d in pins.items():assert sha(p)==d,p
    create(A/'frontier233_dual2020_actual9_TRAIN_native_and_cold_controls_v1_20261010.json',{'status':'passed_actual_two120_saved2020_states9_TRAIN13950_native_tensor_consensus_Pandas_and9_cold4650_controls',
        'input_sha256':pins,'records':records,'actual_saved_states':2,'full233_selected_all6_pairs_not_claimed':True,
        'new_native_fits':0,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False})

if __name__=='__main__':main()
