"""Publish the actual11 CPU callbacks and joint predictor source; do not claim future inference."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    assert allowed()
    source=A/'publish_rank20_two_seed88_source_and_controls_stages_main_v1_20261011.py';text=source.read_text(encoding='utf8')
    old="[('sources',()),('normalized_selected14',('actual_rank20_two_seed88_after186_normalization_v1_20261011','actual_rank20_two_seed88_selected_native14_v1_20261011'))]"
    assert text.count(old)==1;text=text.replace(old,"[('parent_callbacks11',())]")
    text=text.replace('rank20_two_seed_complete88_normalization_native14_sources_admission_v1_20261011.json','rank20_two_seed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json')
    text=text.replace('Rank20_two_seed88_{stage}','Rank20_two_seed88_callbacks_{stage}')
    marker='        assert all(p.is_file() for p in paths)';assert text.count(marker)==1
    text=text.replace(marker,"        assert data['status']=='passed_actual_eleven_complete_parent_callback_expressions_for_two_seed' and len(data['records'])==11\n        paths += [A/r['parent'] for r in data['records']]\n        paths += [A/'prepare_two_seed_parent_callbacks11_main_v1_20261011.py',A/'rank20_two_seed_after_qualified_parent_native_stage_v1_20261010.py',A/'rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011.py']\n"+marker)
    text=text.replace("'full187_candidate_registry_pipeline_pending':True","'full187_candidate_registry_pipeline_pending':True,'actual_parent_callback_CPU_checks':11,'actual_GPU_or_future_inference_by_CPU_callbacks':False")
    driver=A/'publish_rank20_two_seed88_actual_parent_callbacks11_main_v1_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    assert allowed();name='actual_Rank20_two_seed88_actual_parent_callbacks11_main_v1_20261011'
    row=start_service(name,driver.name,[],{str(driver):sha(driver),str(Path(__file__)):sha(__file__)})
    create(A/(name+'_activation.json'),row)
    print({'actual11_CPU_callbacks_and_predictor_main_queued':True},flush=True)

if __name__=='__main__':main()
