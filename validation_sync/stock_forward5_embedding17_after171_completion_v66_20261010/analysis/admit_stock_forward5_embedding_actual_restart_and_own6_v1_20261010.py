"""Dispatch independently controlled own64 stock-identity forward5-return training."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def route(text):
    return text.replace('stock_rank5_embedding','stock_forward5_embedding').replace('StockRank5Embedding','StockForward5Embedding').replace('recent252_rank5_mature','recent252_forward5_mature').replace('past_rank5_targets','past_forward5_targets').replace('y_rank_5mean','y_ret_5mean').replace('passed7_independent_mean5_tied_daily_rank_and_recent252_maturity_CPU_controls','passed7_joint_recent252_calendar_and_mean5_strict_maturity_independent_CPU_cases')
def main():
    assert allowed();closed('StockForward5Embedding_actual_mature_fixture_CPU_v1_20261010')
    pairs=[('verify_stock_rank5_embedding_small512_restart_v1_20261010.py','verify_stock_forward5_embedding_small512_restart_v1_20261010.py'),('verify_stock_rank5_embedding_small512_small_CPU_v1_20261010.py','verify_stock_forward5_embedding_small512_small_CPU_v1_20261010.py'),('train_stock_rank5_embedding_small512_BF16_bank6_own64_v1_20261010.py','train_stock_forward5_embedding_small512_BF16_bank6_own64_v1_20261010.py')];inputs=[];outputs=[]
    for old,new in pairs:
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        if new.startswith('verify_stock_forward5_embedding_small512_restart'):
            text=text.replace('rng.uniform(.0001,1.,1024).astype(np.float64)','np.clip(rng.normal(0.,.03,1024),-.1,.1).astype(np.float64)')
        if new.startswith('train_'):
            text=text.replace('assert np.min(y)>0. and np.max(y)<=1.','assert np.isfinite(y).all()')
        outputs.append(save(new,text))
    for p in outputs:importlib.import_module(p.stem)
    proof=A/'stock_forward5_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json'
    create(proof,{'status':'compiled_actual_forward5_mean_returns_fixture_restart_smallCPU_own64_six_training_sources','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_forward5_embedding_own64_native_sources_preparation_v1_20261010.json',A/'actual_stock_forward5_embedding_mature_fixture_location_v1_20261010.json']},'fixed_epochs':64,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    original=A/'run_stock_rank5_embedding_own_training_queue_v1_20261010.py';text=route(original.read_text(encoding='utf8'))
    queue=save('run_stock_forward5_embedding_own_training_queue_v1_20261010.py',text)
    row=start_service('actual_stock_forward5_embedding_own_training_queue_v1_20261010',queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)});create(A/'actual_stock_forward5_embedding_own_training_queue_activation_v1_20261010.json',row)
    print({'actual_forward5_own64_six_fit_queue_started':True,'actual_restart_then_independentCPU_required':True,'new_quality_scores':0},flush=True)
if __name__=='__main__':main()
