"""Only replace an idle unlaunched future dispatcher after measured exact caching passes."""
from pathlib import Path
import sys,importlib,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed();closed('actual_feature120_verified_memoization_TRAIN344_v1_20261010')
    pointer=A/'actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json';benchmark=Path(read(pointer)['output'])/'verification.json';proof=read(benchmark)
    if not proof['adopt']:
        create(A/'stock_forward5_embedding178_feature_cache_not_adopted_v3_20261010.json',{'status':'actual_benchmark_did_not_improve_keep_original178_dispatcher','benchmark_sha256':sha(benchmark),'no_workers_changed':True});return
    assert proof['rows']==1599600 and proof['days']==344 and len(proof['actual_controls'])==4
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    source=A/'run_StockForward5Embedding178_complete_family_v2_20261010.py';target=A/'run_StockForward5Embedding178_complete_family_v3_20261010.py';wrapper=A/'run_StockForward5Embedding178_selected_candidate_feature_cache_v3_20261010.py'
    runtime=A/'exact_verified_feature120_memoization_runtime_v1_20261010.py';text=source.read_text(encoding='utf8')
    old="'prepare_StockForward5Embedding178_selected_candidate_v2_20261010.py'";assert text.count(old)==1;text=text.replace(old,repr(wrapper.name))
    needle='    pins={str(p):sha(p) for p in dict.fromkeys([*source_paths(),*extra])}'
    assert text.count(needle)==1
    admission=A/'stock_forward5_embedding178_feature_cache_sources_admission_v3_20261010.json'
    text=text.replace(needle,"    extra += [A/'"+wrapper.name+"',A/'"+runtime.name+"',A/'"+pointer.name+"',Path("+repr(str(benchmark))+"),A/'"+admission.name+"']\n"+needle)
    assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');importlib.import_module(target.stem)
    assert not (A/'StockForward5Embedding178_complete_family_v1_20261010').exists()
    assert not (A/'StockForward5Embedding178_selected_release_v1_20261010').exists()
    oldfolder=A/'service_owned_workflows_20261006/StockForward5Embedding178_complete48_family_v2_20261010';launch=read(oldfolder/'native_launch.json');assert owned(launch)
    import psutil
    worker=psutil.Process(launch['owned_worker_pid']);assert worker.create_time()==launch['owned_worker_creation_time'] and not worker.children()
    assert not (A/'service_owned_workflows_20261006/StockForward5Embedding178_selected_candidate_preparation_v1_20261010').exists()
    pins={str(p):sha(p) for p in [Path(__file__),source,target,wrapper,runtime,pointer,benchmark]}
    create(admission,{'status':'passed_actual_full1599600_TRAIN344_and_cold80_feature_cache_benchmark_sources_only_idle_future_dispatcher_changed','input_sha256':pins,'actual_benchmark':proof,'models_losses_weights_official_scoring_native_predictions_and_all_selected_checks_unchanged':True,'no_started_scientific_task_restarted':True,'actual_future_X_read':False,'new_quality_scores':0,'test_labels_read':False})
    retire(launch,'Actual full1599600 feature120 benchmark passed; replace childless178 dispatcher before any output/future task; no model or scoring changes')
    assert allowed();row=start_service('StockForward5Embedding178_complete48_family_v3_20261010',target.name,[],{str(target):sha(target),str(admission):sha(admission)})
    create(A/'actual_StockForward5Embedding178_complete48_family_feature_cache_activation_v3_20261010.json',row)
    print({'actual_full178_future_dispatcher_v3_started':True,'model_and_scoring_math_unchanged':True,'steady_state_feature_speedup':proof['steady_state_speedup']},flush=True)
if __name__=='__main__':main()
