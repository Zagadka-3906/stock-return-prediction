"""Own five-day ranking recipe and strictly mature embedding fixture, all storage on E."""
from pathlib import Path
import sys,importlib,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
RECIPE='own_mature_stock_rank5_embedding16_cross120_rank5mean_recent252_small512_BF16_e64_v1_20261010'
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    source=A/'stock_rank_embedding_small512_BF16_native_v1_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace("'target': 'y_rank'","'target': 'y_rank_5mean'").replace("cfg['target'] == 'y_rank'","cfg['target'] == 'y_rank_5mean'").replace("'epochs': 24","'epochs': 64").replace("'training_calendar_window':252","'label_horizon_trading_days':5,'training_calendar_window':252").replace('own_mature_stock_rank_embedding16_cross120_rank1d_recent252_small512_BF16_e24_v1_20261010',RECIPE)
    start=text.index('def prepare_rank_targets(y,cfg):')
    text=text[:start]+"""def prepare_rank_targets(y,cfg):
    import numpy as np
    y=np.asarray(y);assert y.ndim==1 and len(y) and np.isfinite(y).all()
    assert cfg['target']=='y_rank_5mean' and cfg['label_horizon_trading_days']==5
    assert np.min(y)>0. and np.max(y)<=1.
    centered=y-.5
    low,high=np.quantile(centered,cfg['return_winsor_quantiles'])
    target=(np.clip(centered,low,high)*cfg['return_target_scale']).astype(np.float32)
    return target,[float(low),float(high)]
"""
    native=save('stock_rank5_embedding_small512_BF16_native_v1_20261010.py',text)
    decoder_source=A/'stock_rank_embedding_saved_tensor_decoder_v1_20261010.py';text=decoder_source.read_text(encoding='utf8').replace('own_mature_stock_rank_embedding16_cross120_rank1d_recent252_small512_BF16_e24_v1_20261010',RECIPE).replace("cfg['target']=='y_rank'","cfg['target']=='y_rank_5mean'")
    decoder=save('stock_rank5_embedding_saved_tensor_decoder_v1_20261010.py',text)
    module=importlib.import_module(native.stem);assert module.CONFIG['epochs']==64 and module.CONFIG['label_horizon_trading_days']==5
    importlib.import_module(decoder.stem)
    proof=A/'stock_rank5_embedding_own64_native_sources_preparation_v1_20261010.json'
    create(proof,{'status':'compiled_new_rank5_embedding_recipe_raw_positive_rank_centered_exactly_once_GPU_and_actual_mature_fixture_pending','recipe':RECIPE,'configuration':module.CONFIG,'input_sha256':{str(p):sha(p)for p in [Path(__file__),source,native,decoder_source,decoder,A/'stock_identity_rank5_own64_prospective_direction_plan_v1_20261010.json',A/'recent252_rank5_mature_training_population_v1_20261010.py',A/'recent252_rank5_mature_population_actual_CPU_controls_v1_20261010.json']},'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    driver=A/'verify_stock_rank5_embedding_actual_mature_fixture_v1_20261010.py'
    row=start_service('StockRank5Embedding_actual_mature_fixture_CPU_v1_20261010',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/'actual_StockRank5Embedding_mature_fixture_activation_v1_20261010.json',row)
    print({'actual_rank5_own64_sources':'compiled','actual_fixture_worker':row['owned_worker_pid'],'memory_guard_GiB':11,'new_model_fits':0},flush=True)
if __name__=='__main__':main()
