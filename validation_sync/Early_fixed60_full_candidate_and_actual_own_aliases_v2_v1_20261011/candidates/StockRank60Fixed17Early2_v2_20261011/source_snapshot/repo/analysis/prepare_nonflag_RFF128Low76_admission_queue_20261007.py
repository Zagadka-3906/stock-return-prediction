"""Create an actual dependency-gated126 admission and six-stage local execution queue."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from nonflag_RFF128Low126_route_mapping_20261007 import convert

def main():
    pairs=[('verify_nonflag_RFF12876_prospective_routes_v1_20261007.py','verify_nonflag_RFF128Low76_prospective_routes_v2_20261007.py'),
        ('start_nonflag_RFF12876_actual_admission_20261007.py','start_nonflag_RFF128Low76_actual_admission_20261007.py'),
        ('continue_nonflag_RFF12876_after_actual_admission_v2_20261007.py','continue_nonflag_RFF128Low76_after_actual_admission_v1_20261007.py')]
    paths=[]
    for before,after in pairs:
        old=A/before;new=A/after;assert not new.exists()
        text=convert(old.read_text(encoding='utf8'))
        if before.startswith('verify_'):
            # Re-evaluate the same concrete paths after controls exist; preserve the earlier waiting-state failure.
            original=A/'verify_nonflag_RFF128Low76_prospective_routes_v1_20261007.py'
            text=original.read_text(encoding='utf8').replace('prospective_routes_v1_20261007.json','prospective_routes_v2_20261007.json')
            paths.append(original)
        if before.startswith('start_'):
            text=text.replace('science_route_preparation_v2_20261007.json','science_route_preparation_v1_20261007.json')
        compile(text,str(new),'exec');new.write_text(text,encoding='utf8',newline='\n');paths.extend((old,new))
    queue=A/'queue_nonflag_RFF128Low76_actual_admission_and_pipeline_20261007.py';assert not queue.exists()
    text='''"""Execute126 only after real10 native fits,6/73/219 controls,125main and local history."""
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
'''
    compile(text,str(queue),'exec');queue.write_text(text,encoding='utf8',newline='\n');paths.append(queue)
    prep=A/'nonflag_RFF128Low76_science_route_preparation_v1_20261007.json'
    pins={**read(prep)['input_sha256'],**{str(p):sha(p) for p in [Path(__file__),*paths,prep,
        A/'nonflag_RFF128Low76_plan_20261007.json']}}
    create(A/'nonflag_RFF128Low76_admission_queue_source_preparation_20261007.json',
        {'status':'compiled_future_dependency_gated126_admission_and_pipeline','input_sha256':pins,
         'actual_official_scores':0,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    pub=A/'publish_RFF128Low_actual_history_after125_20261007.py'
    publisher=start_service('RFF128Low_actual_history_main_after125',pub.name,[],{str(pub):sha(pub)})
    launch=start_service('nonflag_RFF128Low76_actual_admission_dependency_queue',queue.name,[],pins)
    create(A/'nonflag_RFF128Low76_actual_dependency_queue_hidden_launch_20261007.json',
        {'publisher':publisher,'admission_queue':launch,'input_sha256':pins,'actual_official_scores_by_launcher':0})
if __name__=='__main__':main()
