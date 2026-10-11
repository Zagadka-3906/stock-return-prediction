"""Recover a duplicate inherited selection alias and its never-scored dependants."""
from pathlib import Path
import ast
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
import prepare_protected_upper_pool_HGB66_round115_sources_20261007 as substitution

def write_new(name,text):
    p=A/name;assert not p.exists();ast.parse(text)
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    return p

def main():
    old_names=['protected_upper_pool_HGB66_round115_full_registration','flagged_HGB_small_amplitude88_official_comparison',
        'flagged_HGB_small_amplitude88_scores_main_publication','flagged_HGB_small_amplitude88_selected_candidate_preparation',
        'flagged_HGB_small_amplitude88_selected_candidate_sealing']
    evidence=[]
    for name in old_names:
        folder=A/'service_owned_workflows_20261006'/name
        assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='failed'
        evidence.extend(folder/n for n in ('job_definition.json','native_launch.json','service_execution.json','stderr.log'))
    old_registry=A/'register_protected_upper_pool_HGB66_round115_artifacts_20261007.py'
    text=old_registry.read_text(encoding='utf8')
    text=text.replace('    assert not OUT.exists() and not CANDIDATE.exists()',"    assert not (OUT/'selection.json').exists() and not (CANDIDATE/'selection.json').exists()\n    assert OUT.exists() and CANDIDATE.exists()")
    text=text.replace('    OUT.mkdir()\n    CANDIDATE.mkdir()','    OUT.mkdir(exist_ok=True)\n    CANDIDATE.mkdir(exist_ok=True)')
    text=text.replace("'original_inference_selection.json' if relative == 'selection.json' else relative","'source_registration_selection.json' if relative == 'selection.json' else relative")
    before='        os.link(SOURCE_CANDIDATE / relative, target)';assert text.count(before)==1
    text=text.replace(before,"        if target.exists():\n            assert sha(target)==sha(SOURCE_CANDIDATE / relative),target\n        else:\n            os.link(SOURCE_CANDIDATE / relative, target)")
    needle="    pins = {**read(RELEASE / 'protocol.json')['input_sha256']"
    assert text.count(needle)==1
    text=text.replace(needle,"    sources += [A/'prepare_local115_alias_and116_dependency_recovery_20261007.py', A/'run_protected_upper_pool_HGB66_round115_full_registration_v2_20261007.py', *list((A/'service_owned_workflows_20261006/protected_upper_pool_HGB66_round115_full_registration').glob('*.json')), A/'service_owned_workflows_20261006/protected_upper_pool_HGB66_round115_full_registration/stderr.log']\n"+needle)
    reg=write_new('register_protected_upper_pool_HGB66_round115_artifacts_v2_20261007.py',text)
    old_driver=A/'run_protected_upper_pool_HGB66_round115_full_registration_20261007.py'
    text=old_driver.read_text(encoding='utf8')
    text=text.replace('protected_upper_pool_HGB66_round115_actual_registration_20261007','protected_upper_pool_HGB66_round115_actual_registration_v2_20261007')
    text=text.replace('    prepare_sources()',"    assert read(A/'protected_upper_pool_HGB66_round115_source_preparation_20261007.json')['status']=='passed_actual66_sealed_candidate_registry_and_original_QA26_source_routes'\n    admission=read(A/'protected_upper_pool_HGB66_candidate_source_admission_20261007.json')\n    for path,digest in admission['input_sha256'].items():assert sha(path)==digest,path\n    for name,digest in admission['generated_source_sha256']['112'].items():assert sha(A/name)==digest,name")
    text=text.replace('from register_protected_upper_pool_HGB66_round115_artifacts_20261007 import main as register','from register_protected_upper_pool_HGB66_round115_artifacts_v2_20261007 import main as register')
    driver=write_new('run_protected_upper_pool_HGB66_round115_full_registration_v2_20261007.py',text)
    routes={
        'protected_upper_pool_HGB66_round115_full_registration':'protected_upper_pool_HGB66_round115_full_registration_v2',
        'flagged_HGB_small_amplitude88_official_comparison_20261007':'flagged_HGB_small_amplitude88_official_comparison_v2_20261007',
        'flagged_HGB_small_amplitude88_official_comparison':'flagged_HGB_small_amplitude88_official_comparison_v2',
        'flagged_HGB_small_amplitude88_scores_main_publication':'flagged_HGB_small_amplitude88_scores_main_publication_v2',
        'flagged_HGB_small_amplitude88_selected_candidate_preparation':'flagged_HGB_small_amplitude88_selected_candidate_preparation_v2',
        'flagged_HGB_small_amplitude88_selected_candidate_sealing':'flagged_HGB_small_amplitude88_selected_candidate_sealing_v2',
        'flagged_HGB_small_amplitude88_scores_github_20261007':'flagged_HGB_small_amplitude88_scores_v2_github_20261007',
        'flagged_HGB_small_amplitude88_selected_release_20261007':'flagged_HGB_small_amplitude88_selected_release_v2_20261007',
        'flagged_HGB_small_amplitude88_pre_inference_source_freeze_20261007':'flagged_HGB_small_amplitude88_pre_inference_source_freeze_v2_20261007',
        'run_flagged_HGB_small_amplitude88_official_comparison_20261007':'run_flagged_HGB_small_amplitude88_official_comparison_v2_20261007',
        'prepare_flagged_HGB_small_amplitude88_selected_candidate_v2_20261007':'prepare_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007',
        'seal_flagged_HGB_small_amplitude88_selected_candidate_v2_20261007':'seal_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007',
    }
    jobs=[('protected_upper_pool_HGB66_round115_full_registration_v2',driver,[])]
    prototypes=[('run_flagged_HGB_small_amplitude88_official_comparison_20261007.py','run_flagged_HGB_small_amplitude88_official_comparison_v2_20261007.py',old_names[1]+'_v2',[]),
        ('publish_flagged_HGB_small_amplitude88_evidence_20261007.py','publish_flagged_HGB_small_amplitude88_evidence_v2_20261007.py',old_names[2]+'_v2',['scores']),
        ('prepare_flagged_HGB_small_amplitude88_selected_candidate_v2_20261007.py','prepare_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007.py',old_names[3]+'_v2',[]),
        ('seal_flagged_HGB_small_amplitude88_selected_candidate_v2_20261007.py','seal_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007.py',old_names[4]+'_v2',[])]
    for old,new,name,args in prototypes:
        text=substitution.substitute((A/old).read_text(encoding='utf8'),routes)
        if old.startswith('publish_'):
            text=text.replace("f'flagged_HGB_small_amplitude88_{phase}_github_20261007'","f'flagged_HGB_small_amplitude88_{phase}_v2_github_20261007'")
            text=text.replace('validation_sync/flagged_HGB_small_amplitude88_{phase}_20261007','validation_sync/flagged_HGB_small_amplitude88_{phase}_v2_20261007')
            text=text.replace("    sources=list(dict.fromkeys(sources));", "    sources += [A/'prepare_local115_alias_and116_dependency_recovery_20261007.py', *[p for name in " +repr(old_names)+" for p in (A/'service_owned_workflows_20261006'/name).glob('*.json')]]\n    sources=list(dict.fromkeys(sources));")
        p=write_new(new,text);jobs.append((name,p,args));evidence.append(A/old)
    # These files failed before any case/scientific fit/future inference.
    assert not list((A/'flagged_HGB_small_amplitude88_official_comparison_20261007').glob('case*_official.json'))
    proof=A/'local115_alias_and116_dependency_recovery_admission_20261007.json'
    pins={str(p):sha(p) for p in [Path(__file__),reg,old_registry,old_driver,*evidence,*[p for n,p,a in jobs]]}
    create(proof,{'status':'compiled_fresh_alias_and_five_closed_dependency_recovery_routes','input_sha256':pins,
        'failed_scientific_jobs_restarted':0,'original66_scores_reused':True,'original88_actual_scored_cases':0,
        'partial115_aliases_reused_only_if_SHA_exact':True,'inherited_original_and_source_registration_selection_both_retained':True,
        'old_failures_preserved':old_names,'routes':routes,'new_quality_scores':0,'test_labels_read':False})
    pins[str(proof)]=sha(proof)
    launched=[]
    for name,p,args in jobs:
        row=start_service(name,p.name,args,pins);launched.append({'name':name,'native_launch':row})
    create(A/'local115_alias_and116_dependency_recovery_actual_hidden_launches_20261007.json',{'input_sha256':pins,'services':launched,'new_native_fits':0,'new_quality_scores_by_launch':0,'scientific_workers_stopped':0})
    print({'status':'launched_five_fresh_services','workers':[r['native_launch']['owned_worker_pid'] for r in launched]},flush=True)

if __name__=='__main__':main()
