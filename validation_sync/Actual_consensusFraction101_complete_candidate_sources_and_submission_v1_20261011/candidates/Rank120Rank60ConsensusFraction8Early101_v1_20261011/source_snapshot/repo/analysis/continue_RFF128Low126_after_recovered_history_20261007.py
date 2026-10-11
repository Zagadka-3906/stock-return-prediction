"""After a real main recovery, freeze corrected unadmitted dependencies and launch actual126."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    folder=A/'service_owned_workflows_20261006/RFF128Low_history_batched_main_recovery'
    while owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    assert not (A/'nonflag_RFF128Low76_round126_source_admission_v1_20261007.json').exists()
    assert not (A/'nonflag_RFF128Low76_official_comparison_v1_20261007').exists()
    out=A/'RFF128Low126_after_history_recovery_source_preparation_20261007';assert not out.exists();out.mkdir()
    phase=A/'publish_nonflag_RFF128Low76_evidence_v1_20261007.py';(out/phase.name).write_bytes(phase.read_bytes())
    text=phase.read_text(encoding='utf8');assert text.count('RFF128Low_actual_history_main_after125_v3')==1
    text=text.replace('RFF128Low_actual_history_main_after125_v3','RFF128Low_history_batched_main_recovery')
    compile(text,str(phase),'exec');phase.write_text(text,encoding='utf8',newline='\n')
    pairs=[('start_nonflag_RFF128Low76_actual_admission_v3_20261007.py','start_nonflag_RFF128Low76_actual_admission_v4_20261007.py'),
        ('continue_nonflag_RFF128Low76_after_actual_admission_v3_20261007.py','continue_nonflag_RFF128Low76_after_actual_admission_v4_20261007.py')]
    generated=[]
    for before,after in pairs:
        p=A/before;q=A/after;assert not q.exists()
        text=p.read_text(encoding='utf8').replace('science_route_preparation_v3_20261007.json','science_route_preparation_v4_20261007.json')
        text=text.replace('start_nonflag_RFF128Low76_actual_admission_v3_20261007','start_nonflag_RFF128Low76_actual_admission_v4_20261007')
        compile(text,str(q),'exec');q.write_text(text,encoding='utf8',newline='\n');generated.extend((p,q))
    previous=A/'nonflag_RFF128Low76_science_route_preparation_v3_20261007.json'
    paths=list(dict.fromkeys([Path(p) for p in read(previous)['input_sha256']]+[Path(__file__),previous,*generated,out/phase.name,
        A/'RFF128Low_actual_history_github_20261007/receipt.json']))
    pins={str(p):sha(p) for p in paths}
    prep=A/'nonflag_RFF128Low76_science_route_preparation_v4_20261007.json'
    create(prep,{'status':'compiled_actual_main_recovery_dependency_before126_admission_or_scores',
        'input_sha256':pins,'actual_official_scores':0,'test_labels_read':False})
    import verify_nonflag_RFF128Low76_prospective_routes_v2_20261007 as prospective
    prospective.main()
    proof=read(A/'nonflag_RFF128Low76_prospective_routes_v2_20261007.json')
    assert proof['status']=='passed_actual24_prospective_sources_and24_graph_controls' and not proof['issues']
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import main as admit
    admit()
    f=A/'service_owned_workflows_20261006/nonflag_RFF128Low76_round126_source_admission_v1'
    while owned(read(f/'native_launch.json')):time.sleep(10)
    assert read(f/'service_execution.json')['status']=='passed'
    from continue_nonflag_RFF128Low76_after_actual_admission_v4_20261007 import main as execute
    execute()
    create(out/'execution.json',{'status':'passed_actual126_source_admission_and6_stages_after_real_recovered_main_history',
        'new_native_fits_by_launcher':0,'new_official_scores_by_launcher':0,'test_labels_read':False})
if __name__=='__main__':main()
