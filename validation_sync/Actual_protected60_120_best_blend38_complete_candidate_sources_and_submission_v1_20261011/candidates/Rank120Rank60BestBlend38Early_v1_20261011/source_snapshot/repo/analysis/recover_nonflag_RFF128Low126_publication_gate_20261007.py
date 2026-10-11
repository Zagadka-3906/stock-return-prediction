"""Preserve admitted scientific sources; correct only execution/publication endpoints before any scores."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    original=A/'nonflag_RFF128Low76_round126_source_admission_v1_20261007.json';proof=read(original)
    assert proof['status']=='passed_actual73_controls_and24_prospective126_complete_source_schema_paths_and_graph_routes'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    assert not (A/'nonflag_RFF128Low76_official_comparison_v1_20261007').exists()
    assert not (A/'nonflag_RFF128Low76_selected_release_v1_20261007').exists()
    oldservice=A/'service_owned_workflows_20261006/nonflag_RFF128Low76_full37_controls_main_publication_v1'
    assert not owned(read(oldservice/'native_launch.json'))
    failure=read(oldservice/'service_execution.json');assert failure['status']=='failed' and 'science_route_preparation_20261007.json' in failure['failure']
    # The first publication created its folder, then failed before freezing or writing any payload.
    control_out=A/'nonflag_RFF128Low76_controls_github_v1_20261007'
    assert control_out.is_dir() and not list(control_out.iterdir())
    oldpub=A/'publish_nonflag_RFF128Low76_evidence_v1_20261007.py'
    pub=A/'publish_nonflag_RFF128Low76_evidence_v2_20261007.py';assert not pub.exists()
    text=oldpub.read_text(encoding='utf8').replace('nonflag_RFF128Low76_science_route_preparation_20261007.json',
        'nonflag_RFF128Low76_science_route_preparation_v4_20261007.json')
    text=text.replace('nonflag_RFF128Low76_full37_controls_main_publication_v1','nonflag_RFF128Low76_full73_controls_main_publication_v2')
    text=text.replace("assert not out.exists();out.mkdir()",
        "assert not out.exists() or (phase=='controls' and not list(out.iterdir()));out.mkdir(exist_ok=True)")
    # Publish the real execution sources alongside the immutable originally admitted sources.
    needle="    if phase=='scores':\n        for row in proof['records']:";assert text.count(needle)==1
    text=text.replace(needle,"    sources += [A/'nonflag_RFF128Low126_execution_gate_recovery_admission_20261007.json',\n        A/'run_nonflag_RFF128Low76_admitted_comparison_v2_20261007.py',\n        A/'prepare_nonflag_RFF128Low76_selected_candidate_v2_20261007.py']\n"+needle)
    compile(text,str(pub),'exec');pub.write_text(text,encoding='utf8',newline='\n')
    admitted=A/'run_nonflag_RFF128Low76_admitted_comparison_v2_20261007.py';assert not admitted.exists()
    text=(A/'run_nonflag_RFF128Low76_admitted_comparison_v1_20261007.py').read_text(encoding='utf8')
    text=text.replace('nonflag_RFF128Low76_full37_controls_main_publication_v1','nonflag_RFF128Low76_full73_controls_main_publication_v2')
    needle="    from run_nonflag_RFF128Low76_official_comparison_v1_20261007 import main as actual";assert text.count(needle)==1
    text=text.replace(needle,"    extra=read(A/'nonflag_RFF128Low126_execution_gate_recovery_admission_20261007.json')\n    assert extra['status']=='passed_actual_publication_endpoint_recovery_with_original126_science_bytes_unchanged'\n    for p,d in extra['input_sha256'].items():assert sha(p)==d,p\n"+needle)
    compile(text,str(admitted),'exec');admitted.write_text(text,encoding='utf8',newline='\n')
    prep=A/'prepare_nonflag_RFF128Low76_selected_candidate_v2_20261007.py';assert not prep.exists()
    text=(A/'prepare_nonflag_RFF128Low76_selected_candidate_v1_20261007.py').read_text(encoding='utf8')
    text=text.replace("closed('nonflag_RFF128Low_actual_hook6_and_full73_controls_v2')",
        "closed('nonflag_RFF128Low_actual_hook6_and_full73_controls_v2')\n    closed('nonflag_RFF128Low76_full73_controls_main_publication_v2')")
    compile(text,str(prep),'exec');prep.write_text(text,encoding='utf8',newline='\n')
    paths=[Path(__file__),original,oldpub,pub,admitted,prep,
        A/'nonflag_RFF128Low76_science_route_preparation_v4_20261007.json',
        oldservice/'service_execution.json',oldservice/'stderr.log']
    pins={**proof['input_sha256'],**{str(p):sha(p) for p in paths}}
    gate=A/'nonflag_RFF128Low126_execution_gate_recovery_admission_20261007.json'
    create(gate,{'status':'passed_actual_publication_endpoint_recovery_with_original126_science_bytes_unchanged',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,
        'original_actual24_generated_sources_and24_graph_and9_real_baseline_controls_preserved':True,
        'actual_native10_hooks6_full73_cold219_preserved':True,'previous_real_zero_score_publication_failure':failure,
        'remaining5_science_stages_previously_not_started':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    jobs=[('nonflag_RFF128Low76_full73_controls_main_publication_v2',pub.name,['controls']),
        ('nonflag_RFF128Low76_official_comparison_v1',admitted.name,[]),
        ('nonflag_RFF128Low76_scores_main_publication_v1',pub.name,['scores']),
        ('nonflag_RFF128Low76_selected_candidate_preparation_v1',prep.name,[]),
        ('nonflag_RFF128Low76_selected_candidate_sealing_v1','seal_nonflag_RFF128Low76_selected_candidate_v1_20261007.py',[]),
        ('nonflag_RFF128Low76_round126_full_registration_v1','run_nonflag_RFF128Low76_round126_full_registration_v1_20261007.py',[])]
    assert all(not (A/'service_owned_workflows_20261006'/name).exists() for name,_,_ in jobs)
    pins.update({str(gate):sha(gate),**{str(A/driver):sha(A/driver) for _,driver,_ in jobs}})
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'nonflag_RFF128Low76_recovered6_complete_pipeline_actual_hidden_launches_20261007.json',
        {'status':'started_actual6_stages_with_complete126_original_science_admission_and_corrected_execution_endpoints',
         'input_sha256':pins,'launches':launches,'new_quality_scores_by_launcher':0,'test_labels_read':False})
if __name__=='__main__':main()
