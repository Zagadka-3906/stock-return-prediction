"""Use exact imported module identifiers, not filename-only routing; replace only audited idle144 receivers."""
from pathlib import Path
import sys,time,subprocess,hashlib,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from complete_ConeRidgeAlpha144_metadata_and_queue_v2_20261008 import FILES
STEMS={}
for file in FILES:
    for version in (1,2):STEMS[Path(file).stem.replace('_v1_',f'_v{version}_')]=Path(file).stem.replace('_v1_','_v3_')
META={}
for name in ('ConeRidgeAlpha100_round144_source_admission','ConeRidgeAlpha100_round144_source_preparation',
             'ConeRidgeAlpha100_prospective_routes','ConeRidgeAlpha144_receiver_preparation'):
    for version in (1,2):META[f'{name}_v{version}_20261008.json']=f'{name}_v3_20261008.json'
SERVICES={name:name.replace('_v1_','_v3_') for name in (
    'ConeRidgeAlpha100_round144_source_admission_v1_20261008',
    'ConeRidgeAlpha100_controls_main_publication_v1_20261008',
    'ConeRidgeAlpha100_official_comparison_v1_20261008',
    'ConeRidgeAlpha100_scores_main_publication_v1_20261008',
    'ConeRidgeAlpha100_selected_candidate_preparation_v1_20261008',
    'ConeRidgeAlpha100_selected_candidate_sealing_v1_20261008',
    'ConeRidgeAlpha100_round144_full_registration_v1_20261008')}
def corrected(text):
    # Long service identifiers first. Keep declared science output directories and native versions intact.
    for before,after in [*SERVICES.items(),*META.items(),*STEMS.items()]:text=text.replace(before,after)
    return text
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    sources=[Path(__file__)];outputs=[]
    for filename in FILES:
        source=A/filename.replace('_v1_','_v2_');sources.append(source);text=corrected(source.read_text(encoding='utf8'))
        text=text.replace('from complete_ConeRidgeAlpha144_metadata_and_queue_v2_20261008 import corrected',
                          'from recover_ConeRidgeAlpha144_module_routing_and_dispatch_v3_20261008 import corrected')
        outputs.append(save(filename.replace('_v1_','_v3_'),text))
    source=A/'verify_ConeRidgeAlpha100_prospective_routes_v4_20261008.py';sources.append(source)
    text=corrected(source.read_text(encoding='utf8')).replace('cross_volume_byte_probe_v4','cross_volume_byte_probe_v5')
    outputs.append(save('verify_ConeRidgeAlpha100_prospective_routes_v5_20261008.py',text))
    pins={str(p):sha(p) for p in [*sources,*outputs]}
    create(A/'ConeRidgeAlpha144_module_receiver_preparation_v3_20261008.json',{
        'status':'frozen_module_and_filename_and_service_routing3_before_any144_quality',
        'input_sha256':pins,'module_mapping':STEMS,'metadata_mapping':META,'service_mapping':SERVICES,
        'original_failures_and_previous_drafts_preserved':True,'native_math_grid_unchanged':True,'new_quality_scores':0})
    from verify_ConeRidgeAlpha100_prospective_routes_v5_20261008 import main as prospective
    prospective()
    proof_path=A/'ConeRidgeAlpha100_prospective_routes_v3_20261008.json';proof=read(proof_path)
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==2619
    import prepare_ConeRidgeAlpha100_round144_sources_v3_20261008 as generator
    for parent in (132,134,143):
        generated=generator.generate(parent)
        assert {n:hashlib.sha256(t.encode()).hexdigest() for n,t in generated.items()}==proof['generated_source_sha256'][str(parent)]
        for text in generated.values():
            for stem in STEMS:assert stem not in text,(parent,stem)
    # Diagnose each exact waiting service, suspend them only after all seven prove idle/no science output.
    import psutil
    audit=[];held=[]
    try:
        assert not (A/'ConeRidgeAlpha100_official_comparison_v1_20261008/verification.json').exists()
        assert not any((A/'ConeRidgeAlpha100_official_comparison_v1_20261008').glob('case*_official.json'))
        for name in SERVICES:
            folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json');assert owned(row),name
            worker=psutil.Process(row['owned_worker_pid']);parent=psutil.Process(row['pid'])
            assert parent.create_time()==row['owned_parent_creation_time'] and worker.memory_info().rss<256*2**20
            dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(worker.pid)],
                capture_output=True,text=True,encoding='utf8',creationflags=subprocess.CREATE_NO_WINDOW,check=True).stdout
            assert 'closed (' in dump and '(idle)' in dump,(name,dump)
            worker.suspend();parent.suspend();held.extend((worker,parent))
            audit.append({'service':name,'native_launch':row,'actual_idle_stack':dump,'RSS':worker.memory_info().rss})
        create(A/'ConeRidgeAlpha144_exact_idle_retirement_audit_v3_20261008.json',{
            'status':'passed_exact_seven_idle144_receivers_before_any_quality','records':audit,
            'neural_fitter_and_current_parent_and_auxiliary_workers_untouched':True})
        for record in audit:
            row=record['native_launch'];folder=A/'service_owned_workflows_20261006'/record['service']
            create(folder/'service_execution.json',{'status':'superseded_before_quality_by_module_routing3',
                'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'new_quality_scores':0,
                'original_driver_and_launch_and_logs_preserved':True,'replacement_service':SERVICES[record['service']]})
            psutil.Process(row['owned_worker_pid']).terminate();psutil.Process(row['pid']).terminate()
        held=[]
    finally:
        for process in reversed(held):
            if process.is_running():process.resume()
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    jobs=read(A/'ConeRidgeAlpha144_complete_dependency_plan_v2_20261008.json')['jobs']
    jobs=[(SERVICES[name],corrected(driver),args) for name,driver,args in jobs]
    pins.update({str(proof_path):sha(proof_path)})
    create(A/'ConeRidgeAlpha144_complete_dependency_plan_v3_20261008.json',{
        'status':'frozen_exact_module_imports_and100_QA55_complete_pipeline','jobs':jobs,'input_sha256':pins,
        'existing_actual_current_parent_service':'ConeRidgeAlpha97_current_parent_controls_v2_20261008',
        'expected_scored_cases':100,'QA_version':55,'new_quality_scores':0})
    launches={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'ConeRidgeAlpha144_complete_hidden_launches_v3_20261008.json',{
        'status':'started_exact_corrected_seven144_services_after_actual24_sources2619_graph_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'launches':launches,'input_sha256':pins,
        'new_native_fits':0,'quality_scores_by_dispatch':0,'100_scoring_candidate_QA55_main_still_required':True})
    print('Exact module-routed seven144 services dispatched; only proven idle receivers replaced.',flush=True)
if __name__=='__main__':main()
