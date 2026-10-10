"""Correct a pre-publication path/data mixup and preserve all real failed zero-score gates."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    assert not (A/'nonflag_RFF128Low76_round126_source_admission_v1_20261007.json').exists()
    assert not (A/'nonflag_RFF128Low76_official_comparison_v1_20261007').exists()
    old=A/'publish_RFF128Low_actual_history_after125_v2_20261007.py'
    pub=A/'publish_RFF128Low_actual_history_after125_v3_20261007.py';assert not pub.exists()
    text=old.read_text(encoding='utf8')
    text=text.replace("A/'local_optimization_boundary_audit_v3_20261007/运行范围说明.md',receipt]",
        "A/'local_optimization_boundary_audit_v3_20261007/运行范围说明.md',\n        A/'github_validation_sync_main_20261005/round125_receipt.json',\n        A/'audit_local_optimization_boundaries_v3_20261007.py',\n        A/'handoff_local_only_monitor_v24_20261007.py']")
    text=text.replace("'nonflag_RFF12876_round125_source_admission_v1','nonflag_RFF12876_continue_after_actual_admission_v2']:",
        "'nonflag_RFF12876_round125_source_admission_v1','nonflag_RFF12876_continue_after_actual_admission_v2',\n        'RFF128Low_actual_history_main_after125','RFF128Low_actual_history_main_after125_v2',\n        'nonflag_RFF128Low76_actual_admission_dependency_queue','nonflag_RFF128Low76_actual_admission_dependency_queue_v2']:")
    text=text.replace("sources=list(dict.fromkeys(p for p in sources if p.is_file()))",
        "assert all(isinstance(p,Path) for p in sources)\n    sources=list(dict.fromkeys(p for p in sources if p.is_file()))")
    compile(text,str(pub),'exec');pub.write_text(text,encoding='utf8',newline='\n')
    out=A/'RFF128Low126_unadmitted_publication_path_correction_20261007';assert not out.exists();out.mkdir()
    phase=A/'publish_nonflag_RFF128Low76_evidence_v1_20261007.py';(out/phase.name).write_bytes(phase.read_bytes())
    text=phase.read_text(encoding='utf8').replace('RFF128Low_actual_history_main_after125_v2','RFF128Low_actual_history_main_after125_v3')
    compile(text,str(phase),'exec');phase.write_text(text,encoding='utf8',newline='\n')
    pairs=[('start_nonflag_RFF128Low76_actual_admission_v2_20261007.py','start_nonflag_RFF128Low76_actual_admission_v3_20261007.py'),
        ('continue_nonflag_RFF128Low76_after_actual_admission_v2_20261007.py','continue_nonflag_RFF128Low76_after_actual_admission_v3_20261007.py'),
        ('queue_nonflag_RFF128Low76_actual_admission_and_pipeline_v2_20261007.py','queue_nonflag_RFF128Low76_actual_admission_and_pipeline_v3_20261007.py')]
    generated=[]
    for before,after in pairs:
        p=A/before;q=A/after;assert not q.exists()
        text=p.read_text(encoding='utf8').replace('science_route_preparation_v2_20261007.json','science_route_preparation_v3_20261007.json')
        text=text.replace('RFF128Low_actual_history_main_after125_v2','RFF128Low_actual_history_main_after125_v3')
        text=text.replace('start_nonflag_RFF128Low76_actual_admission_v2_20261007','start_nonflag_RFF128Low76_actual_admission_v3_20261007')
        text=text.replace('continue_nonflag_RFF128Low76_after_actual_admission_v2_20261007','continue_nonflag_RFF128Low76_after_actual_admission_v3_20261007')
        compile(text,str(q),'exec');q.write_text(text,encoding='utf8',newline='\n');generated.extend((p,q))
    previous=A/'nonflag_RFF128Low76_science_route_preparation_v2_20261007.json'
    paths=list(dict.fromkeys([Path(p) for p in read(previous)['input_sha256']]+[Path(__file__),pub,previous,*generated,out/phase.name]))
    pins={str(p):sha(p) for p in paths}
    prep=A/'nonflag_RFF128Low76_science_route_preparation_v3_20261007.json'
    create(prep,{'status':'compiled_concrete_publication_path_types_corrected_before126_admission_or_scores',
        'input_sha256':pins,'actual_official_scores':0,'test_labels_read':False})
    create(out/'correction_record.json',{'status':'preserved_real_zero_score_publication_failures_and_corrected_concrete_path',
        'incorrect_prior_value':'parsed125receipt_dict_instead_of_receipt_file_path',
        'input_sha256':pins,'native_models_and_official_math_changed':False,'actual_official_scores':0})
    # Validate concrete collection and every completed dependency before starting publication again.
    for name in ('nonflag_RFF12876_round125_full_registration_v1','nonflag_RFF128Low_actual_hook6_and_full73_controls_v2',
        'nonflag_residual_RFF128Low_native_bank10_v2'):
        assert read(A/'service_owned_workflows_20261006'/name/'service_execution.json')['status']=='passed'
    from handoff_ready_goss_full_execution_20261006 import start_service
    publisher=start_service('RFF128Low_actual_history_main_after125_v3',pub.name,[],{str(pub):sha(pub)})
    queue=start_service('nonflag_RFF128Low76_actual_admission_dependency_queue_v3',
        'queue_nonflag_RFF128Low76_actual_admission_and_pipeline_v3_20261007.py',[],{**pins,str(prep):sha(prep)})
    create(A/'nonflag_RFF128Low76_corrected_path_dependency_queue_hidden_launch_20261007.json',
        {'publisher':publisher,'admission_queue':queue,'actual_official_scores_by_launcher':0})
if __name__=='__main__':main()
