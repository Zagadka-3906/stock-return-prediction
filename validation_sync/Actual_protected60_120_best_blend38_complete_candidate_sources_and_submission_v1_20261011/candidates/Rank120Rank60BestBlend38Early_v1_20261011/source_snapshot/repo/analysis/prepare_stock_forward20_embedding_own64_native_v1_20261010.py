"""Uncovered identity embedding/cross120/mean20-return recipe, strict mature TRAIN only."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();source=A/'stock_forward5_embedding_small512_BF16_native_v1_20261010.py'
    text=source.read_text(encoding='utf8').replace('stock_forward5_embedding','stock_forward20_embedding').replace('return5mean','return20mean').replace('y_ret_5mean','y_ret_20mean').replace("'label_horizon_trading_days':5","'label_horizon_trading_days':20")
    native=save('stock_forward20_embedding_small512_BF16_native_v1_20261010.py',text)
    source_decoder=A/'stock_forward5_embedding_saved_tensor_decoder_v1_20261010.py'
    decoder=save('stock_forward20_embedding_saved_tensor_decoder_v1_20261010.py',source_decoder.read_text(encoding='utf8').replace('stock_forward5_embedding','stock_forward20_embedding').replace('return5mean','return20mean'))
    cfg=importlib.import_module(native.stem).CONFIG;assert cfg['target']=='y_ret_20mean' and cfg['epochs']==64 and cfg['label_horizon_trading_days']==20
    assert read(A/'recent252_forward20_mature_population_actual_CPU_controls_v1_20261010.json')['status']=='passed7_joint_recent252_calendar_and_mean20_strict_maturity_independent_CPU_cases'
    proof=A/'stock_forward20_embedding_own64_native_sources_preparation_v1_20261010.json'
    create(proof,{'status':'prospective_uncovered_identity16_cross120_recent252_forward20_return_Huber_own64_actual_mature_fixture_pending','configuration':cfg,'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,source_decoder,native,decoder,A/'recent252_forward20_mature_training_population_v1_20261010.py',A/'recent252_forward20_mature_population_actual_CPU_controls_v1_20261010.json',A/'forward20_mature_training_labels_v1_20261010.py']},'new_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    driver=A/'verify_stock_forward20_embedding_actual_mature_fixture_v1_20261010.py';assert driver.is_file();compile(driver.read_text(encoding='utf8'),str(driver),'exec')
    row=start_service('StockForward20Embedding_actual_mature_fixture_CPU_v1_20261010',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/'actual_stock_forward20_embedding_mature_fixture_CPU_activation_v1_20261010.json',row)
    print({'forward20_identity_cross120_own64_sources_prepared':True,'actual_mature_CPU_fixture_started':True,'new_fits':0},flush=True)
if __name__=='__main__':main()
