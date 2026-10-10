"""Remove a delivery dependency from independent mature-only fits, preserving mathematics."""
from pathlib import Path
import sys, ast, time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire

def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec')
    p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    assert allowed()
    base=A/'service_owned_workflows_20261006'
    phases=('actual_stock_top10_embedding_small512_restart_v1_20261010','StockTop10EmbeddingSmall512_independent_small_CPU_v1_20261009','actual_stock_top10_embedding_small512_bank6_v1_20261010','StockTop10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009')
    assert all(not (base/name).exists() for name in phases)
    oldnames=('actual_stock_top10_embedding_own_training_queue_v2_20261010','actual_stock_top10_embedding_native42_and_after174_fast17_queue_v2_20261010')
    import psutil
    rows=[read(base/name/'native_launch.json') for name in oldnames]
    assert all(owned(row) and not psutil.Process(row['owned_worker_pid']).children() for row in rows)
    native=A/'stock_top10_embedding_small512_BF16_native_v2_20261010.py'
    decoder=A/'stock_top10_embedding_saved_tensor_decoder_v1_20261010.py'
    science={str(p):sha(p) for p in (native,decoder,A/'run_stock_top10_embedding_after174_fast17_screen_v1_20261010.py')}
    restart=A/'verify_stock_top10_embedding_small512_restart_priority174_v2_20261010.py'
    old=restart.read_text(encoding='utf8')
    gate="                if Path('E:/赛题五_本机临时/Dual120Consensus_after169_high_impact193_screen_v1_20261010/verification.json').exists():closed('StockRankDual174_selected_candidate_sealing_v1_20261010')\n"
    assert old.count(gate)==1
    restart3=save('verify_stock_top10_embedding_small512_restart_memory_guard_v3_20261010.py',old.replace(gate,''))
    bank=A/'train_stock_top10_embedding_small512_BF16_bank6_checkpoint_yield_priority174_v2_20261010.py'
    old=bank.read_text(encoding='utf8')
    gate="                closed('StockRankDual174_selected_candidate_sealing_v1_20261010')"
    assert old.count(gate)==1
    bank3=save('train_stock_top10_embedding_small512_BF16_bank6_memory_guard_v3_20261010.py',old.replace(gate,"                assert allowed()  # independent fits need no selected-candidate result"))
    queue=A/'run_stock_top10_embedding_own_training_queue_v2_20261010.py'
    text=queue.read_text(encoding='utf8')
    gate="assert allowed();closed('StockRankDual174_selected_candidate_sealing_v1_20261010')"
    assert text.count(gate)==1
    text=text.replace(gate,'assert allowed()').replace(restart.name,restart3.name).replace(bank.name,bank3.name)
    own3=save('run_stock_top10_embedding_own_training_queue_v3_20261010.py',text)
    queue2=A/'run_stock_top10_embedding_native42_and_after174_fast17_queue_v2_20261010.py'
    native3=save('run_stock_top10_embedding_native42_and_after174_fast17_queue_v3_20261010.py',queue2.read_text(encoding='utf8').replace(oldnames[0],'actual_stock_top10_embedding_own_training_queue_v3_20261010'))
    # Restrict changes to scheduling: model, target conversion, loss, epochs,
    # native replay, case definitions and score inputs remain byte-identical.
    assert '11 * 2**30' in restart3.read_text(encoding='utf8') and '11 * 2**30' in bank3.read_text(encoding='utf8')
    for p,d in science.items():assert sha(p)==d
    paths=[Path(__file__),restart,bank,queue,queue2,restart3,bank3,own3,native3]
    proof=A/'stock_top10_independent_training_schedule_admission_v3_20261010.json'
    create(proof,{'status':'passed_exact_schedule_only_change_before_any_actual_Top10_GPU_output','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in paths},'unchanged_scientific_source_sha256':science,'memory_available_min_GiB':11,'durable_epoch_chunk':8,'fixed_epochs':24,'actual_annual_fits':6,'all_model_and_cache_storage':'E:','final17_comparison_still_requires_actual_full174':True,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    for row in rows:retire(row,'Verified childless before any Top10 GPU output. Independent mature-only training moved ahead of full174 delivery; mathematics and eventual full174 comparison unchanged, 11GiB memory guards retained.')
    launched=[]
    for name,driver in [('actual_stock_top10_embedding_own_training_queue_v3_20261010',own3),('actual_stock_top10_embedding_native42_and_after174_fast17_queue_v3_20261010',native3)]:
        assert allowed();row=start_service(name,driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/(name+'_activation.json'),row);launched.append(row)
    create(A/'actual_stock_top10_independent_training_acceleration_v3_20261010.json',{'status':'actual_hidden_schedule3_started_no_training_completion_claimed','services':launched,'proof':str(proof),'proof_sha256':sha(proof)})
    print({'actual_schedule_version':3,'no_delivery_gate_on_independent_training':True,'actual_services':[(r['owned_worker_pid']) for r in launched]},flush=True)
if __name__=='__main__':main()
