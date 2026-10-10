"""Explore identity/cross120/20-day daily rank without taking GPU from qualified delivery."""
from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def route(text):
    text=text.replace('stock_rank5','stock_rank20').replace('StockRank5','StockRank20').replace('rank5','rank20').replace('Rank5','Rank20').replace('y_rank_5mean','y_rank_20mean').replace('y_ret_5mean','y_ret_20mean').replace('label_end_5d','label_end_20d').replace('forward5_mature','forward20_mature').replace('mean5','mean20').replace('five_day','twenty_day').replace('five-day','twenty-day').replace('five_day','twenty_day')
    text=re.sub(r"(label_horizon_trading_days'\]\s*==\s*|label_horizon_trading_days'\s*:\s*)5\b",r'\g<1>20',text)
    return text
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();inputs=[];outputs=[]
    pairs=[('recent252_rank5_mature_training_population_v1_20261010.py','recent252_rank20_mature_training_population_v1_20261010.py'),('stock_rank5_embedding_small512_BF16_native_v1_20261010.py','stock_rank20_embedding_small512_BF16_native_v1_20261010.py'),('stock_rank5_embedding_saved_tensor_decoder_v1_20261010.py','stock_rank20_embedding_saved_tensor_decoder_v1_20261010.py'),('verify_stock_rank5_embedding_small512_restart_v1_20261010.py','verify_stock_rank20_embedding_small512_restart_v1_20261010.py'),('verify_stock_rank5_embedding_small512_small_CPU_v1_20261010.py','verify_stock_rank20_embedding_small512_small_CPU_v1_20261010.py'),('train_stock_rank5_embedding_small512_BF16_bank6_own64_v1_20261010.py','train_stock_rank20_embedding_small512_BF16_bank6_own64_v1_20261010.py')]
    for old,new in pairs:
        source=A/old;inputs.append(source);text=route(source.read_text(encoding='utf8'))
        outputs.append(save(new,text))
    source=A/'verify_recent252_rank5_mature_population_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8'))
    text=re.sub(r'\b5\b','20',text).replace('(1,4,20,6,253,301,401)','(1,19,20,21,253,301,401)')
    controls=save('verify_recent252_rank20_mature_population_v1_20261010.py',text);outputs.append(controls)
    importlib.import_module(controls.stem).main()
    native=importlib.import_module(outputs[1].stem);assert native.CONFIG['epochs']==64 and native.CONFIG['label_horizon_trading_days']==20 and native.CONFIG['target']=='y_rank_20mean'
    for p in outputs:importlib.import_module(p.stem)
    proof=A/'stock_rank20_embedding_own64_native_sources_preparation_v1_20261010.json'
    create(proof,{'status':'compiled_own64_rank20_identity_cross120_with7_independent_scalar_mean_tied_rank_poison_controls_GPU_pending','configuration':native.CONFIG,'input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'recent252_rank20_mature_population_actual_CPU_controls_v1_20261010.json',A/'forward20_mature_training_labels_v1_20261010.py']},'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    admission=A/'stock_rank20_embedding_actual_restart_and_own6_sources_admission_v1_20261010.json'
    create(admission,{'status':'compiled_actual_rank20_mature_fixture_restart_CPU_own6_sources_training_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),*outputs,proof,A/'verify_stock_rank20_embedding_actual_mature_fixture_v1_20261010.py']},'fixed_epochs':64,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    queue=route((A/'run_stock_rank5_embedding_own_training_queue_v1_20261010.py').read_text(encoding='utf8'))
    queue=queue.replace("    assert allowed();closed('StockRank20Embedding_actual_mature_fixture_CPU_v1_20261010')","    assert allowed();closed('StockRank20Embedding_actual_mature_fixture_CPU_v1_20261010')\n    closed('StockRankDual174_selected_candidate_sealing_v1_20261010')")
    driver=save('run_stock_rank20_embedding_own_training_queue_v1_20261010.py',queue)
    for name,p in [('StockRank20Embedding_actual_mature_fixture_CPU_v1_20261010',A/'verify_stock_rank20_embedding_actual_mature_fixture_v1_20261010.py'),('actual_stock_rank20_embedding_own_training_queue_v1_20261010',driver)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(admission):sha(admission)});create(A/(name+'_activation.json'),row)
    print({'rank20_maturity_CPU7_passed':True,'own64_queue_prioritizes_actual174_seal':True,'official_scores_pending':True},flush=True)
if __name__=='__main__':main()
