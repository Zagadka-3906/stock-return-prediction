"""Replace only the exact idle188 dispatcher; keep actual504 training/scoring queue and all outputs intact."""
from pathlib import Path
import sys,subprocess,psutil,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire

def main():
    assert allowed()
    original='StockRank20LongEmbedding188_complete48_family_v1_20261011'
    actual='StockRank20LongEmbedding188_complete48_family_actual_queue_v2_20261011'
    bad='actual_run_stock_rank20long_embedding_504_own64_controls46_queue_v1_20261011'
    correct='actual_stock_rank20long_embedding_504_own64_controls46_queue_v1_20261011'
    row=read(A/'service_owned_workflows_20261006'/original/'native_launch.json')
    queue=read(A/'service_owned_workflows_20261006'/correct/'native_launch.json');assert owned(queue)
    assert not (A/'service_owned_workflows_20261006'/bad).exists()
    assert not (A/'optimization_20261003_r188').exists() and not (A.parent/'candidates/optimization_20261003_r188').exists()
    assert not (A/'StockRank20LongEmbedding188_complete_family_v1_20261010').exists()
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    for attempt in range(10):
        assert allowed() and owned(row) and not psutil.Process(row['owned_worker_pid']).children()
        stack=subprocess.run([str(spy),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True).stdout
        if '(idle)' in stack and 'main (run_StockRank20LongEmbedding188_complete_family_v1_20261011.py:' in stack:break
        time.sleep(2)
    else:raise RuntimeError('Dispatcher not verified idle; no retirement performed')
    driver=A/'route_long188_actual_scientific_queue_v2_20261011.py';compile(driver.read_text(encoding='utf8'),str(driver),'exec')
    paths=[Path(__file__),driver,A/'prepare_StockRank20LongEmbedding188_complete48_pipeline_v1_20261011.py',
        A/'run_StockRank20LongEmbedding188_complete_family_v1_20261011.py',
        A/'stock_rank20long_embedding188_full_execution_sources_admission_v1_20261011.json',
        A/'prepare_stock_rank20long_504_own64_controls46_v1_20261011.py']
    proof=A/'long188_actual_scientific_queue_routes_v2_20261011.json'
    create(proof,{'status':'verified_actual504_queue_exact_dependency_before_any188_future_dispatch',
        'input_sha256':{str(p):sha(p) for p in paths},'dependency_aliases':{bad:correct},'service_aliases':{original:actual},
        'actual_live_scientific_queue':queue,'idle_dispatcher':row,'idle_stack':stack,
        'expected_records':48,'expected_full_board':17538,'QA':99,'training_calendar_window':504,
        'legacy_source_status_text_and_stdout_board_literal_not_actual_qualification_evidence':True,
        'scientific_workers_stopped_or_restarted':0,'actual_future_X_read':False,'test_labels_read':False})
    retire(row,'Verified idle188 dispatcher routed to actual504 own64 scientific queue; no training, scoring, native or candidate worker stopped')
    assert allowed();new=start_service(actual,driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/(actual+'_activation.json'),new)
    print({'actual188_dependency_routed':correct,'scientific_workers_stopped_or_restarted':0},flush=True)

if __name__=='__main__':main()
