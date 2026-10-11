"""Prepare strict20-day own64 training; actual fixture and both replay controls gate fitting."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def route(text):
    return text.replace('stock_forward5_embedding','stock_forward20_embedding').replace('StockForward5Embedding','StockForward20Embedding').replace('recent252_forward5','recent252_forward20').replace('forward5_mature_training_labels','forward20_mature_training_labels').replace('past_forward5_targets','past_forward20_targets').replace('y_ret_5mean','y_ret_20mean').replace('label_end_5d','label_end_20d').replace('mean5_strict_maturity','mean20_strict_maturity').replace("native.CONFIG['label_horizon_trading_days']==5","native.CONFIG['label_horizon_trading_days']==20").replace("'label_horizon_trading_days':5","'label_horizon_trading_days':20").replace('five_day_','twenty_day_')
def main():
    assert allowed();inputs=[];outputs=[]
    for old,new in [('verify_stock_forward5_embedding_small512_restart_v1_20261010.py','verify_stock_forward20_embedding_small512_restart_v1_20261010.py'),('verify_stock_forward5_embedding_small512_small_CPU_v1_20261010.py','verify_stock_forward20_embedding_small512_small_CPU_v1_20261010.py'),('train_stock_forward5_embedding_small512_BF16_bank6_own64_v1_20261010.py','train_stock_forward20_embedding_small512_BF16_bank6_own64_v1_20261010.py')]:
        p=A/old;inputs.append(p);outputs.append(save(new,route(p.read_text(encoding='utf8'))))
    for p in outputs:importlib.import_module(p.stem)
    assert 'label_end_5d' not in outputs[2].read_text(encoding='utf8') and "label_horizon_trading_days']==20" in outputs[2].read_text(encoding='utf8')
    proof=A/'stock_forward20_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json'
    create(proof,{'status':'compiled_actual_forward20_mature_fixture_small32_wide2_restart_CPU_decoder_and_six_own64_sources_no_fit_completion_claimed','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_forward20_embedding_own64_native_sources_preparation_v1_20261010.json']},'fixed_epochs':64,'label_horizon_trading_days':20,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    old=A/'run_stock_forward5_embedding_own_training_queue_v1_20261010.py';queue=save('run_stock_forward20_embedding_own_training_queue_v1_20261010.py',route(old.read_text(encoding='utf8')))
    row=start_service('actual_stock_forward20_embedding_own_training_queue_v1_20261010',queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)});create(A/'actual_stock_forward20_embedding_own_training_queue_activation_v1_20261010.json',row)
    print({'actual_forward20_own64_queue_started':True,'actual_fixture_restart_and_independentCPU_required_before_fitting':True,'new_quality_scores':0},flush=True)
if __name__=='__main__':main()
