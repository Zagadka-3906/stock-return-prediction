"""Prepare88 scorer and full116 routes after actual alias recovery, without repeating20 fits."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def write_new(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec')
    with p.open('x',encoding='utf8',newline='\n') as f:f.write(text)
    return p

def main():
    routes={
        'protected_upper_pool_HGB66_round115_full_registration_v2':'protected_upper_pool_HGB66_round115_full_registration_v5',
        'flagged_HGB_small_amplitude88_official_comparison_v2_20261007':'flagged_HGB_small_amplitude88_official_comparison_v4_20261007',
        'flagged_HGB_small_amplitude88_official_comparison_v2':'flagged_HGB_small_amplitude88_official_comparison_v4',
        'flagged_HGB_small_amplitude88_scores_main_publication_v2':'flagged_HGB_small_amplitude88_scores_main_publication_v4',
        'flagged_HGB_small_amplitude88_selected_candidate_preparation_v2':'flagged_HGB_small_amplitude88_selected_candidate_preparation_v4',
        'flagged_HGB_small_amplitude88_selected_candidate_sealing_v2':'flagged_HGB_small_amplitude88_selected_candidate_sealing_v4',
        'flagged_HGB_small_amplitude88_scores_v2_github_20261007':'flagged_HGB_small_amplitude88_scores_v4_github_20261007',
        'flagged_HGB_small_amplitude88_selected_release_v2_20261007':'flagged_HGB_small_amplitude88_selected_release_v4_20261007',
        'flagged_HGB_small_amplitude88_pre_inference_source_freeze_v2_20261007':'flagged_HGB_small_amplitude88_pre_inference_source_freeze_v4_20261007',
        'run_flagged_HGB_small_amplitude88_official_comparison_v2_20261007':'run_flagged_HGB_small_amplitude88_official_comparison_v4_20261007',
        'prepare_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007':'prepare_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007',
        'seal_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007':'seal_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007',
        'prepare_flagged_HGB88_round116_sources_v2_20261007':'prepare_flagged_HGB88_round116_sources_v3_20261007',
        'run_flagged_HGB88_round116_full_registration_v2_20261007':'run_flagged_HGB88_round116_full_registration_v3_20261007',
        'flagged_HGB88_round116_actual_registration_v2_20261007':'flagged_HGB88_round116_actual_registration_v3_20261007',
        'flagged_HGB88_round116_source_preparation_v2_20261007':'flagged_HGB88_round116_source_preparation_v3_20261007'}
    prototypes=[('run_flagged_HGB_small_amplitude88_official_comparison_v2_20261007.py','run_flagged_HGB_small_amplitude88_official_comparison_v4_20261007.py','flagged_HGB_small_amplitude88_official_comparison_v4',[]),
        ('publish_flagged_HGB_small_amplitude88_evidence_v2_20261007.py','publish_flagged_HGB_small_amplitude88_evidence_v4_20261007.py','flagged_HGB_small_amplitude88_scores_main_publication_v4',['scores']),
        ('prepare_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007.py','prepare_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007.py','flagged_HGB_small_amplitude88_selected_candidate_preparation_v4',[]),
        ('seal_flagged_HGB_small_amplitude88_selected_candidate_v3_20261007.py','seal_flagged_HGB_small_amplitude88_selected_candidate_v5_20261007.py','flagged_HGB_small_amplitude88_selected_candidate_sealing_v4',[])]
    paths=[Path(__file__)];jobs=[]
    for old,new,name,args in prototypes:
        text=substitute((A/old).read_text(encoding='utf8'),routes)
        if old.startswith('publish_'):
            text=text.replace('_{phase}_v2_github_20261007','_{phase}_v4_github_20261007').replace('_{phase}_v2_20261007','_{phase}_v4_20261007')
        p=write_new(new,text);paths.extend([A/old,p]);jobs.append({'name':name,'driver':p.name,'arguments':args})
    text=substitute((A/'prepare_flagged_HGB88_round116_sources_v2_20261007.py').read_text(encoding='utf8'),routes)
    text=text.replace('def generate(parent):','def generate_before_alias_controls(parent):')
    insert='''
def generate(parent):
    generated=generate_before_alias_controls(parent)
    for name,text in generated.items():
        if name.startswith('register_'):
            text=text.replace("'original_inference_selection_round116.json' if relative == 'selection.json' else relative", "'original_inference_selection_round116.json' if relative == 'selection.json' else ('original_registry_alias_round116.json' if relative == 'registry_alias_verification.json' else relative)")
            text=text.replace("target = CANDIDATE / 'registration_sources' / source.name", "target = CANDIDATE / 'registration_sources' / 'round116_full_scope' / source.relative_to(ROOT)")
        compile(text,str(A/name),'exec');generated[name]=text
    return generated

'''
    assert text.count("if __name__=='__main__':main()")==1
    text=text.replace("if __name__=='__main__':main()",insert+"if __name__=='__main__':main()")
    gen=write_new('prepare_flagged_HGB88_round116_sources_v3_20261007.py',text);paths.append(gen)
    driver=write_new('run_flagged_HGB88_round116_full_registration_v3_20261007.py',substitute((A/'run_flagged_HGB88_round116_full_registration_v2_20261007.py').read_text(encoding='utf8'),routes));paths.append(driver)
    jobs.append({'name':'flagged_HGB88_round116_full_registration','driver':driver.name,'arguments':[]})
    text=substitute((A/'verify_flagged_HGB88_round116_sources_v3_20261007.py').read_text(encoding='utf8'),routes)
    before="namespace={'A':A,'ROOT':ROOT,'read':mock_read";assert text.count(before)==1
    text=text.replace(before,"namespace={'pilot':{'actual_scheme_base_round':112},'A':A,'ROOT':ROOT,'read':mock_read")
    needle="        required={n.slice.value";assert text.count(needle)==1
    text=text.replace(needle,"        registry_source=generated['register_flagged_HGB88_round116_artifacts_20261007.py']\n        assert \"'original_registry_alias_round116.json'\" in registry_source\n        assert \"'round116_full_scope' / source.relative_to(ROOT)\" in registry_source\n"+needle)
    check=write_new('verify_flagged_HGB88_round116_sources_v4_20261007.py',text);paths.append(check)
    create(A/'flagged_HGB88_complete_pipeline_preparation_v4_20261007.json',{'status':'compiled_seven_sources_before_full_prospective_admission',
        'input_sha256':{str(p):sha(p) for p in paths},'jobs':jobs,'routes':routes,'canonical116_sources_written':0,'new_native_fits':0,'new_quality_scores':0})
    print({'status':'compiled_fresh_pipeline','jobs':len(jobs)},flush=True)

if __name__=='__main__':main()
