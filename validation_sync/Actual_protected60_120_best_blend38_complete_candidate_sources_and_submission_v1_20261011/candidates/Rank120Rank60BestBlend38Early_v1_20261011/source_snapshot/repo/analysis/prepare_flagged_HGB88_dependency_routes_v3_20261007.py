"""Recover four never-scored88 dependants; retain original plan, fits and controls."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def main():
    pairs=[('run_flagged_HGB_small_amplitude88_official_comparison_v2_20261007.py','run_flagged_HGB_small_amplitude88_official_comparison_v3_20261007.py','flagged_HGB_small_amplitude88_official_comparison_v2',[]),
        ('publish_flagged_HGB_small_amplitude88_evidence_v2_20261007.py','publish_flagged_HGB_small_amplitude88_evidence_v3_20261007.py','flagged_HGB_small_amplitude88_scores_main_publication_v2',['scores']),
        ('prepare_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007.py','prepare_flagged_HGB_small_amplitude88_selected_candidate_v4_20261007.py','flagged_HGB_small_amplitude88_selected_candidate_preparation_v2',[]),
        ('seal_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007.py','seal_flagged_HGB_small_amplitude88_selected_candidate_v4_20261007.py','flagged_HGB_small_amplitude88_selected_candidate_sealing_v2',[])]
    routes={
        'protected_upper_pool_HGB66_round115_full_registration_v2':'protected_upper_pool_HGB66_round115_full_registration_v3',
        'flagged_HGB_small_amplitude88_official_comparison_v2_20261007':'flagged_HGB_small_amplitude88_official_comparison_v3_20261007',
        'flagged_HGB_small_amplitude88_official_comparison_v2':'flagged_HGB_small_amplitude88_official_comparison_v3',
        'flagged_HGB_small_amplitude88_scores_main_publication_v2':'flagged_HGB_small_amplitude88_scores_main_publication_v3',
        'flagged_HGB_small_amplitude88_selected_candidate_preparation_v2':'flagged_HGB_small_amplitude88_selected_candidate_preparation_v3',
        'flagged_HGB_small_amplitude88_selected_candidate_sealing_v2':'flagged_HGB_small_amplitude88_selected_candidate_sealing_v3',
        'flagged_HGB_small_amplitude88_scores_v2_github_20261007':'flagged_HGB_small_amplitude88_scores_v3_github_20261007',
        'flagged_HGB_small_amplitude88_selected_release_v2_20261007':'flagged_HGB_small_amplitude88_selected_release_v3_20261007',
        'flagged_HGB_small_amplitude88_pre_inference_source_freeze_v2_20261007':'flagged_HGB_small_amplitude88_pre_inference_source_freeze_v3_20261007',
        'run_flagged_HGB_small_amplitude88_official_comparison_v2_20261007':'run_flagged_HGB_small_amplitude88_official_comparison_v3_20261007',
        'prepare_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007':'prepare_flagged_HGB_small_amplitude88_selected_candidate_v4_20261007',
        'seal_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007':'seal_flagged_HGB_small_amplitude88_selected_candidate_v4_20261007'}
    evidence=[Path(__file__)];jobs=[]
    for old,new,name,args in pairs:
        f=A/'service_owned_workflows_20261006'/name
        assert not owned(read(f/'native_launch.json')) and read(f/'service_execution.json')['status']=='failed'
        evidence += [f/n for n in ('job_definition.json','native_launch.json','service_execution.json','stderr.log')]
        source=A/old;p=A/new;assert not p.exists();text=substitute(source.read_text(encoding='utf8'),routes)
        if old.startswith('publish_'):
            text=text.replace('_{phase}_v2_github_20261007','_{phase}_v3_github_20261007').replace('_{phase}_v2_20261007','_{phase}_v3_20261007')
        compile(text,str(p),'exec')
        with p.open('x',encoding='utf8',newline='\n') as stream:stream.write(text)
        jobs.append((routes[name],p,args));evidence += [source,p]
    assert not list((A/'flagged_HGB_small_amplitude88_official_comparison_v2_20261007').glob('case*_official.json'))
    pins={str(p):sha(p) for p in evidence};proof=A/'flagged_HGB88_dependency_routes_v3_admission_20261007.json'
    create(proof,{'status':'compiled_four_fresh_closed_dependency_routes_without_repeating_science','input_sha256':pins,
        'routes':routes,'old_actual_scored_cases':0,'old_failures_preserved':True,'new_quality_scores':0,'new_native_fits':0})
    pins[str(proof)]=sha(proof);rows=[]
    for name,p,args in jobs:rows.append({'name':name,'native_launch':start_service(name,p.name,args,pins)})
    create(A/'flagged_HGB88_dependency_routes_v3_actual_hidden_launches_20261007.json',{'input_sha256':pins,'services':rows,'console_windows':0,'scientific_workers_stopped':0})
    print({'status':'launched_four_fresh_dependants','workers':[r['native_launch']['owned_worker_pid'] for r in rows]},flush=True)

if __name__=='__main__':main()
