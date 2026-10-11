"""Preserve unlaunched187 source-route failure; protect exact destination filenames from round substitution."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    source=A/'prepare_Rank20TwoSeed187_complete88_pipeline_v1_20261011.py'
    original=importlib.import_module(source.stem)
    assert not (A/original.PROOF).exists()
    assert not (A/'service_owned_workflows_20261006/Rank20TwoSeed187_complete88_family_v1_20261011').exists()
    assert not (A/'optimization_20261003_r187').exists() and not (A.parent/'candidates/optimization_20261003_r187').exists()
    existing=[p for n in original.FILE_MAP.values() if (p:=A/n).exists() and '187' in n]
    text=source.read_text(encoding='utf8')
    old="    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)\n    text=base(text)"
    new="    placeholders={k:'__EXACT_SOURCE_ROUTE_'+str(i)+'__' for i,k in enumerate(mapping)}\n    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:placeholders[m.group()],text)\n    text=base(text)\n    for oldname,placeholder in placeholders.items():text=text.replace(placeholder,mapping[oldname])"
    assert text.count(old)==1;text=text.replace(old,new)
    text=text.replace("'_v1_20261011.py',base(old)","'_v2_20261011.py',base(old)")
    for oldname,newname in [
        ('rank20_two_seed187_full_execution_sources_admission_v1_20261011.json','rank20_two_seed187_full_execution_sources_admission_v2_20261011.json'),
        ('rank20_two_seed187_candidate_sources_preparation_v1_20261011.json','rank20_two_seed187_candidate_sources_preparation_v2_20261011.json'),
        ('rank20_two_seed187_full_registry_sources_preparation_v1_20261011.json','rank20_two_seed187_full_registry_sources_preparation_v2_20261011.json'),
        ('rank20_two_seed187_full_family_preflight_v1_20261011.json','rank20_two_seed187_full_family_preflight_v2_20261011.json'),
        ("name='Rank20TwoSeed187_complete88_family_v1_20261011'","name='Rank20TwoSeed187_complete88_family_v2_20261011'")]:
        assert oldname in text,oldname;text=text.replace(oldname,newname)
    driver=A/'prepare_Rank20TwoSeed187_complete88_pipeline_v2_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    create(A/'two_seed187_exact_destination_route_recovery_v2_20261011.json',{
        'status':'preserved_unlaunched187_source_route_failure_before_any_scientific_output',
        'reason':'Round substitution was applied to exact new normalizer filename after186, incorrectly changing it to after187; protect exact destination routes before generic round substitution',
        'original_error':'ValueError: substring not found before candidate source generation or any future dispatch',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver,*existing]},
        'original_partial_source_files_preserved':True,'fresh_source_version':2,'new_model_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'fresh187_route_factory_v2_created':True,'original_scientific_outputs_unstarted':True},flush=True)

if __name__=='__main__':main()
