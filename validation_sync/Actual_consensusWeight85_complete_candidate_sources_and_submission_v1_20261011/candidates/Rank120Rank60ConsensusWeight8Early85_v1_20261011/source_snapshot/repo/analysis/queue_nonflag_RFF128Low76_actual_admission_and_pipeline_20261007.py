"""Execute126 only after real10 native fits,6/73/219 controls,125main and local history."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned,sha,create
def closed(name):
    f=A/'service_owned_workflows_20261006'/name
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(10)
    assert read(f/'service_execution.json')['status']=='passed',name
def main():
    for name in ('nonflag_residual_RFF128Low_native_bank10_v2','nonflag_RFF128Low_actual_hook6_and_full73_controls_v2',
        'nonflag_RFF12876_round125_full_registration_v1','RFF128Low_actual_history_main_after125'):closed(name)
    import verify_nonflag_RFF128Low76_prospective_routes_v2_20261007 as prospective
    prospective.main()
    proof=read(A/'nonflag_RFF128Low76_prospective_routes_v2_20261007.json')
    assert proof['status']=='passed_actual24_prospective_sources_and24_graph_controls' and not proof['issues']
    from start_nonflag_RFF128Low76_actual_admission_20261007 import main as admit
    admit()
    closed('nonflag_RFF128Low76_round126_source_admission_v1')
    from continue_nonflag_RFF128Low76_after_actual_admission_v1_20261007 import main as execute
    execute()
    create(A/'nonflag_RFF128Low76_actual_dependency_queue_execution_20261007.json',
        {'status':'passed_actual126_admission_and6_real_stages_launched_after_closed_dependencies',
         'new_quality_scores_by_queue':0,'new_native_fits_by_queue':0,'test_labels_read':False})
if __name__=='__main__':main()
