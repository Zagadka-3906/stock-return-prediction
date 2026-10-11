"""Correct a publication-only case-insensitive filename collision; preserve the original failure."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    old=A/'service_owned_workflows_20261006/actual_Seed10_complete48_sources_main_v1_20261011'
    assert read(old/'service_execution.json')['status']=='failed' and not owned(read(old/'native_launch.json'))
    source=A/'publish_seed10_complete48_sources_main_v1_20261011.py'
    assert source.name.casefold()=='publish_Seed10_complete48_sources_main_v1_20261011.py'.casefold()
    text=source.read_text(encoding='utf8')
    bad="driver=A/'publish_Seed10_complete48_sources_main_v1_20261011.py'"
    assert text.count(bad)==1
    text=text.replace(bad,"driver=A/'publish_Seed10_complete48_sources_payload_main_v2_20261011.py'")
    text=text.replace('paths=list(dict.fromkeys([Path(__file__),template,admission,',
        "paths=list(dict.fromkeys([Path(__file__),A/'publish_seed10_complete48_sources_main_v1_20261011.py',A/'seed10_source_capsules_case_collision_recovery_v2_20261011.json',template,admission,")
    driver=A/'publish_seed10_complete48_source_capsules_main_v2_20261011.py'
    assert driver.name.casefold()!='publish_Seed10_complete48_sources_payload_main_v2_20261011.py'.casefold()
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    proof=A/'seed10_source_capsules_case_collision_recovery_v2_20261011.json'
    create(proof,{'status':'publication_only_case_insensitive_filename_collision_fixed_before_any_push',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver,old/'service_execution.json',old/'stderr.log']},
        'original_service_failed_preserved':True,'scientific_sources_or_math_changed':False,'new_quality_scores':0,'new_native_fits':0})
    assert allowed();row=start_service('actual_Seed10_complete48_source_capsules_main_v2_20261011',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/'actual_Seed10_complete48_source_capsules_main_v2_20261011_activation.json',row)
    print({'publication_filename_collision_recovery2':'started','scientific_workers_restarted':0},flush=True)
if __name__=='__main__':main()
