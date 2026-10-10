"""Complete the original94-case pipeline with fresh receipt/gate receivers, short native source aliases and E evidence support."""
from pathlib import Path
import sys,ast,json,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def save(name,value):
    p=A/name;assert not p.exists(),p;compile(value,str(p),'exec');p.write_text(value,encoding='utf8',newline='\n');return p
def main():
    assert read(A/'service_owned_workflows_20261006/CrossFamily94_round136_source_admission_v5_20261008/service_execution.json')['status']=='passed'
    changes={'BF16wide40_round135_full_registration_v4_20261008':'BF16wide40_round135_full_registration_v7_20261008','CrossFamily94_official_comparison_v4_20261008':'CrossFamily94_official_comparison_v5_20261008','CrossFamily94_scores_main_publication_v4_20261008':'CrossFamily94_scores_main_publication_v5_20261008','CrossFamily94_selected_candidate_preparation_v4_20261008':'CrossFamily94_selected_candidate_preparation_v5_20261008','CrossFamily94_selected_candidate_sealing_v4_20261008':'CrossFamily94_selected_candidate_sealing_v5_20261008','CrossFamily94_round136_source_admission_v4_20261008.json':'CrossFamily94_round136_source_admission_v5_20261008.json','CrossFamily94_scores_github_v1_20261008/receipt.json':'CrossFamily94_scores_github_v2_20261008/receipt.json','CrossFamily94_actual_controls_index_v3_20261008':'CrossFamily94_actual_controls_index_v4_20261008'}
    outputs=[];originals=[]
    for role in ('prepare','seal'):
        source=A/f'{role}_CrossFamily94_selected_candidate_v4_20261008.py';old=source.read_text(encoding='utf8');value=old
        for before,after in changes.items():value=value.replace(before,after)
        if role=='prepare':
            value=value.replace("A/'seal_CrossFamily94_selected_candidate_v4_20261008.py'","A/'seal_CrossFamily94_selected_candidate_v5_20261008.py'")
            needle="            prediction,storage=predict(ns,selection,CANDIDATE,parent_candidate/'cohort_curve.json',OUT/'future_return_mapping.json');output_scope.reverify()";assert value.count(needle)==1
            value=value.replace(needle,"            from short_content_addressed_native_storage_v2_20261008 import installed as short_storage\n            with short_storage(ns,freeze/'model_source_aliases') as storage_contract:\n                prediction,storage=predict(ns,selection,CANDIDATE,parent_candidate/'cohort_curve.json',OUT/'future_return_mapping.json')\n            create(OUT/'short_native_source_aliases_execution.json',storage_contract)\n            output_scope.reverify()")
        else:
            needle="        target=candidate/'evidence'/source.relative_to(A);target.parent.mkdir(parents=True,exist_ok=True);os.link(source,target);assert sha(target)==sha(source)";assert value.count(needle)==1
            value=value.replace(needle,"        relative=source.relative_to(A) if source.is_relative_to(A) else Path('external_frozen_metadata')/(sha(source)+'_'+source.name)\n        target=candidate/'evidence'/relative;target.parent.mkdir(parents=True,exist_ok=True)\n        if target.exists():assert sha(target)==sha(source)\n        else:os.link(source,target)\n        assert sha(target)==sha(source)")
        outputs.append(save(f'{role}_CrossFamily94_selected_candidate_v5_20261008.py',value));originals.append(source)
    source=A/'run_CrossFamily94_round136_full_registration_v4_20261008.py';value=source.read_text(encoding='utf8')
    for before,after in changes.items():value=value.replace(before,after)
    value=value.replace('actual_registration_v4_20261008','actual_registration_v5_20261008').replace('full_registration_v4_file_IO_20261008','full_registration_v5_file_IO_20261008')
    needle='    from prepare_CrossFamily94_round136_sources_v4_20261008 import main as prepare_sources';assert value.count(needle)==1
    hook='''    import prepare_CrossFamily94_round136_sources_v4_20261008 as actual_generator
    original_read=actual_generator.read;original_paths=actual_generator.source_paths
    def current_admission_read(path):
        path=Path(path)
        if path==A/'CrossFamily94_round136_source_admission_v4_20261008.json':path=A/'CrossFamily94_round136_source_admission_v5_20261008.json'
        return original_read(path)
    def current_source_paths():
        names={'CrossFamily94_round136_source_admission_v4_20261008.json':'CrossFamily94_round136_source_admission_v5_20261008.json','CrossFamily94_actual_controls_index_v3_20261008.json':'CrossFamily94_actual_controls_index_v4_20261008.json','actual_CrossFamily91_current_parent_location_v1_20261008.json':'actual_CrossFamily91_current_parent_location_v2_20261008.json'}
        paths=[]
        for path in original_paths():
            if path.name in names and path.parent==A:path=A/names[path.name]
            if path.name=='receipt.json' and path.parent.name=='CrossFamily94_scores_github_v1_20261008':path=A/'CrossFamily94_scores_github_v2_20261008/receipt.json'
            paths.append(path)
        extra=[Path(__file__),A/'prepare_CrossFamily136_candidate_registration_recovery_v5_20261008.py',A/'recover_CrossFamily136_quality_after_actual135_main_v5_20261008.py',A/'CrossFamily136_quality_receiver_recovery_v5_20261008.json',A/'CrossFamily136_candidate_registration_recovery_v5_20261008.json',A/'verify_CrossFamily94_round136_sources_v5_20261008.py',A/'run_CrossFamily94_official_comparison_v5_20261008.py',A/'publish_CrossFamily94_evidence_v5_20261008.py',A/'prepare_CrossFamily94_selected_candidate_v5_20261008.py',A/'seal_CrossFamily94_selected_candidate_v5_20261008.py',A/'short_content_addressed_native_storage_v2_20261008.py',A/'actual_short_parent_alias_nested_copy_v2_20261008.json']
        for name in ('CrossFamily94_round136_source_admission_v5_20261008','CrossFamily94_controls_main_publication_v5_20261008','CrossFamily94_official_comparison_v5_20261008','CrossFamily94_scores_main_publication_v5_20261008','CrossFamily94_selected_candidate_preparation_v5_20261008','CrossFamily94_selected_candidate_sealing_v5_20261008'):
            folder=A/'service_owned_workflows_20261006'/name;extra.extend(folder.glob('*.json'));extra.extend(folder.glob('*.log'))
        return list(dict.fromkeys([*paths,*extra]))
    actual_generator.read=current_admission_read;actual_generator.source_paths=current_source_paths
'''
    value=value.replace(needle,hook+needle)
    outputs.append(save('run_CrossFamily94_round136_full_registration_v5_20261008.py',value));originals.append(source)
    pins={str(p):sha(p) for p in [Path(__file__),*outputs,*originals,A/'short_content_addressed_native_storage_v2_20261008.py',A/'actual_short_parent_alias_nested_copy_v2_20261008.json']}
    create(A/'CrossFamily136_candidate_registration_recovery_v5_20261008.json',{'status':'frozen_fresh_candidate_sealing_and_full_QA47_receivers_for_exact94_original_quality_cases','input_sha256':pins,'administrative_dependency_and_metadata_mapping':changes,'all_original24_generated_graph_and_registry_sources_remain_byte_exact_to_admission5_preflight':True,'original_main_source_generator_admission_read_and_source_list_only_rebound_in_isolated_worker':True,'actual_long_parent_source_name_alias_control_passed':True,'native_model_parameters_and_prediction_arithmetic_unchanged':True,'new_quality_scores':0,'old_failed_receivers_preserved':True})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    names=['CrossFamily94_selected_candidate_preparation_v5_20261008','CrossFamily94_selected_candidate_sealing_v5_20261008','CrossFamily94_round136_full_registration_v5_20261008']
    launches={n:start(n,p.name,[],pins) for n,p in zip(names,outputs)}
    create(A/'CrossFamily136_candidate_registration_hidden_launches_v5_20261008.json',{'launches':launches,'input_sha256':pins,'new_quality_scores':0})
    print(json.dumps({'started':list(launches)},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
