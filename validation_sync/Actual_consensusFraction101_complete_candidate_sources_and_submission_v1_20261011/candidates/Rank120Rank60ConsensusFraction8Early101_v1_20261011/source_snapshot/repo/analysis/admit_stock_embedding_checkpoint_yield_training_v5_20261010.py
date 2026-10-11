"""Use spare GPU now and yield at verified durable boundaries before candidate qualification."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from scheduled_user_pause_20261007 import write
def main():
    assert allowed()
    closed('actual_stock_embedding_small512_restart_v1_20261010');closed('StockEmbeddingSmall512_independent_small_CPU_v1_20261009')
    state=read(A/'stock_embedding_small512_own_training_queue_v1_20261010/state.json')
    assert state['status']=='restart_and_independent_CPU_admission_complete_waiting_actual172_seal_before_six_fits'
    assert not (A/'service_owned_workflows_20261006/actual_stock_embedding_small512_bank6_v1_20261010').exists()
    old=A/'train_stock_embedding_small512_BF16_bank6_v3_20261010.py';text=old.read_text(encoding='utf8')
    before="        bundle = native.fit_arrays(x, y, native.CONFIG, folder / 'checkpoint.joblib')"
    after="""        checkpoint=folder/'checkpoint.joblib'
        completed=joblib.load(checkpoint)['next_epoch'] if checkpoint.exists() else 0
        while True:
            assert allowed()
            #193 normalization+main gates the original native233 workers; at its
            #completion, release our tensors at an actual completed epoch boundary.
            if Path('E:/赛题五_本机临时/Dual120Consensus_after169_high_impact193_screen_v1_20261010/verification.json').exists():
                from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed
                write(OUT/'actual_stage.json',{'status':'durable_stock_embedding_checkpoint_yield_waiting_actual172_candidate_seal','year':year,'completed_epochs':completed,'new_quality_scores':0})
                gc.collect();torch.cuda.empty_cache()
                closed('Frontier133172_selected_candidate_sealing_v1_20261010')
                assert allowed()
            boundary=completed+8
            stop=boundary if boundary<native.CONFIG['epochs'] else None
            bundle=native.fit_arrays(x,y,native.CONFIG,checkpoint,stop_after_epoch=stop)
            if bundle.get('status')=='stopped_after_durable_BF16_micro_epoch_for_control':
                completed=bundle['next_epoch'];del bundle;gc.collect();torch.cuda.empty_cache()
                continue
            break
"""
    assert text.count(before)==1;text=text.replace(before,after)
    #completed==epochs may occur after a clean checkpoint write; fit_arrays loads
    #its exact state and returns the original complete bundle without retraining.
    bank=A/'train_stock_embedding_small512_BF16_bank6_checkpoint_yield_v5_20261010.py';assert not bank.exists();compile(text,str(bank),'exec');bank.write_text(text,encoding='utf8',newline='\n')
    queue=A/'run_stock_embedding_checkpoint_yield_queue_v5_20261010.py'
    source="""from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from scheduled_user_pause_20261007 import write
def main():
    assert allowed()
    proof=read(A/'stock_embedding_checkpoint_yield_training_admission_v5_20261010.json')
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    tasks=[('actual_stock_embedding_small512_bank6_v1_20261010','train_stock_embedding_small512_BF16_bank6_checkpoint_yield_v5_20261010.py'),('StockEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009','verify_stock_embedding_small512_full5_independent_v3_20261010.py')]
    state=A/'stock_embedding_small512_own_training_queue_v1_20261010/state.json'
    for name,driver in tasks:
        assert allowed()
        if name=='StockEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009' and Path('E:/赛题五_本机临时/Dual120Consensus_after169_high_impact193_screen_v1_20261010/verification.json').exists():closed('Frontier133172_selected_candidate_sealing_v1_20261010')
        row=start_service(name,driver,[],{str(A/driver):sha(A/driver)})
        create(A/'stock_embedding_small512_own_training_queue_v1_20261010'/(name+'_launch.json'),row)
        write(state,{'status':'actual_checkpoint_yield_new_stock_embedding_training_or_full5','actual_service':name,'new_quality_scores':0})
        while owned(row):
            if not allowed():return
            time.sleep(15)
        assert read(A/'service_owned_workflows_20261006'/name/'service_execution.json')['status']=='passed'
    write(state,{'status':'actual_stock_embedding_six_fits_and_independent_full5_complete_official_scoring_pending','new_quality_scores':0})
if __name__=='__main__':main()
"""
    assert not queue.exists();compile(source,str(queue),'exec');queue.write_text(source,encoding='utf8',newline='\n')
    restart=Path(read(A/'actual_stock_embedding_small512_restart_location_v1_20261010.json')['output'])
    proof=read(restart/'verification.json');assert proof['status']=='passed_actual_small32_and_wide2_BF16_micro_fresh_process_restart'
    create(A/'stock_embedding_checkpoint_yield_training_admission_v5_20261010.json',{'status':'actual_original_and_resumed_GPU_controls_passed_admit_same_native_fit_at_durable8_epoch_boundaries','input_sha256':{str(p):sha(p) for p in [Path(__file__),old,bank,queue,A/'stock_embedding_small512_BF16_native_v1_20261010.py',restart/'verification.json',A/'verify_stock_embedding_small512_full5_independent_v3_20261010.py']},'restart_all_weight_loss_and_prediction_bits_exact':True,'new_native_training_mutation':False,'new_quality_scores':0,'yield_before_existing233_and133_full_candidate_GPU_work':'at193_complete_stop_after_completed8_epoch_checkpoint_then_wait_actual172_seal','full_epochs':24,'GPU_training_can_use_actual_CPU_score_wait_interval':True})
    row=read(A/'service_owned_workflows_20261006/actual_stock_embedding_own_training_queue_v4_20261010/native_launch.json')
    retire(row,'Actual restart+independent CPU controls passed; replace idle172-waiting dispatcher with verified durable8-epoch GPU yield dispatcher, preserving all scientific processes.')
    actual=start_service('actual_stock_embedding_checkpoint_yield_training_queue_v5_20261010',queue.name,[],{str(queue):sha(queue)})
    create(A/'actual_stock_embedding_checkpoint_yield_training_queue_activation_v5_20261010.json',actual)
    write(A/'stock_embedding_small512_own_training_queue_v1_20261010/state.json',{'status':'actual_checkpoint_yield_dispatcher_started_after_restart_controls','actual_service':'actual_stock_embedding_checkpoint_yield_training_queue_v5_20261010','worker_pid':actual['owned_worker_pid'],'new_quality_scores':0})
    print({'actual_checkpoint_yield_dispatcher_pid':actual['owned_worker_pid'],'restart_controls':'passed','existing_quality_and_candidate_workers_preserved':True},flush=True)
if __name__=='__main__':main()
