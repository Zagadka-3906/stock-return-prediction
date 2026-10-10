"""Recover actual pre-scoring failures with explicit generator dependency modules."""
from pathlib import Path
import ast,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from handoff_ready_goss_full_execution_20261006 import start_service

def wrapper(old,new,mapping):
    original=(A/old).read_text(encoding='utf8');node=next(n for n in ast.parse(original).body if isinstance(n,ast.FunctionDef) and n.name=='main')
    main_text='\n'.join(original.splitlines()[node.lineno-1:node.end_lineno])
    return f'''from pathlib import Path
import hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
import {Path(old).stem} as original_generator
NAMES=original_generator.NAMES
RECOVERY_MAP={mapping!r}
def generate(parent):
    return {{name:substitute(text,RECOVERY_MAP) for name,text in original_generator.generate(parent).items()}}
'''+substitute(main_text,mapping)+"\nif __name__=='__main__':main()\n"

def main():
    q_services=['quantile_HGB88_round119_source_admission_v5','quantile_HGB88_official_comparison_v5',
      'quantile_HGB88_scores_main_publication_v5','quantile_HGB88_selected_candidate_preparation_v5',
      'quantile_HGB88_selected_candidate_sealing_v5','quantile_HGB88_round119_full_registration_v5']
    n_services=list(read(A/'nonflag_HGB40_complete_pipeline_actual_hidden_launches_v3_20261007.json')['launches'])
    rows={};definitions={}
    for name in [*q_services,*n_services]:
        folder=A/'service_owned_workflows_20261006'/name
        row=read(folder/'native_launch.json');assert not owned(row),name
        assert read(folder/'service_execution.json')['status']=='failed',name
        rows[name]=row;definitions[name]=read(folder/'job_definition.json')
    q_files={Path(definitions[n]['driver']).name for n in q_services}|{
      'run_quantile_HGB88_official_comparison_v5_20261007.py','prepare_quantile_HGB88_round119_sources_v5_20261007.py'}
    n_files={Path(definitions[n]['driver']).name for n in n_services}|{
      'run_nonflag_HGB40_official_comparison_v3_20261007.py','prepare_nonflag_HGB40_round120_sources_v3_20261007.py'}
    filemap={**{n:n.replace('_v5_20261007','_v6_20261007') for n in q_files},
      **{n:n.replace('_v3_20261007','_v4_20261007') for n in n_files}}
    servicemap={**{n:n.removesuffix('_v5')+'_v6' for n in q_services},
      **{n:n.removesuffix('_v3')+'_v4' for n in n_services}}
    mapping={**{o[:-3]:n[:-3] for o,n in filemap.items()},**servicemap,
      'nonflag_HGB40_complete_pipeline_actual_hidden_launches_v3_20261007':'nonflag_HGB40_complete_pipeline_actual_hidden_launches_v4_20261007'}
    for stem,old_version,new_version,number in [('quantile_HGB88',5,6,119),('nonflag_HGB40',3,4,120)]:
        for suffix in ['selected_release','pre_inference_source_freeze','official_comparison',f'round{number}_source_admission',f'round{number}_source_preparation',f'round{number}_actual_registration']:
            mapping[f'{stem}_{suffix}_v{old_version}_20261007']=f'{stem}_{suffix}_v{new_version}_20261007'
        mapping[f'candidates/{stem}_v{old_version}_20261007']=f'candidates/{stem}_v{new_version}_20261007'
    mapping['quantile_HGB88_scores_github_v5_20261007']='quantile_HGB88_scores_github_v6_20261007'
    mapping['quantile_HGB88_{phase}_github_v5_20261007']='quantile_HGB88_{phase}_github_v6_20261007'
    generated={}
    for old,new in filemap.items():
        text=wrapper(old,new,mapping) if old.startswith('prepare_') and '_round' in old else substitute((A/old).read_text(encoding='utf8'),mapping)
        if old.startswith('verify_quantile_'):
            needle='    import prepare_quantile_HGB88_round119_sources_v6_20261007 as generator';assert text.count(needle)==1
            text=text.replace(needle,needle+"\n    import prepare_HGB_quarter_numeric28_round118_sources_v2_20261007 as source_base")
            text=text.replace('generator.base.base','source_base.base').replace('generator.base','source_base')
        compile(text,str(A/new),'exec');generated[new]=text
    for name in generated:assert not (A/name).exists(),name
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    proof_path=A/'quantile119_nonflag120_closed_dependency_recovery_source_v6_20261007.json'
    pins={str(A/n):sha(A/n) for n in generated};pins[str(Path(__file__))]=sha(__file__)
    create(proof_path,{'status':'compiled_fresh_explicit_generator_dependencies_all13_predecessors_actual_failed',
      'input_sha256':pins,'actual_failed_services':rows,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    # Execute the full real119 admission NOW, before launching any new scorer.
    import runpy
    runpy.run_path(str(A/'verify_quantile_HGB88_round119_sources_v6_20261007.py'),run_name='__main__')
    actual_admission=A/'quantile_HGB88_round119_source_admission_v6_20261007.json'
    pins.update({str(proof_path):sha(proof_path),str(actual_admission):sha(actual_admission)})
    launches={}
    for name in [*q_services,*n_services]:
        definition=definitions[name];driver=filemap[Path(definition['driver']).name]
        if name==q_services[0]:
            driver='verify_quantile_HGB88_actual_existing_admission_v6_20261007.py'
        try:row=start_service(servicemap[name],driver,definition['arguments'],pins)
        except AssertionError:
            folder=A/'service_owned_workflows_20261006'/servicemap[name];row=read(folder/'native_launch.json')
            assert not owned(row) and read(folder/'service_execution.json')['status']=='passed',name
        launches[servicemap[name]]=row
    create(A/'quantile119_nonflag120_closed_dependency_recovery_actual_launches_v6_20261007.json',{
      'status':'started_actual13_consoleless_recovered_stages_after_actual119_full_admission',
      'input_sha256':pins,'launches':launches,'new_quality_scores_by_launcher':0,'scientific_workers_stopped':0,'test_labels_read':False})
    create(A/'nonflag_HGB40_complete_pipeline_actual_hidden_launches_v4_20261007.json',{
      'status':'started_actual7_recovered120_consoleless_stages','input_sha256':pins,
      'launches':{n:row for n,row in launches.items() if n.startswith('nonflag_')}})
    print({'status':'actual119_admission_passed_and13_stages_started'},flush=True)

if __name__=='__main__':main()
