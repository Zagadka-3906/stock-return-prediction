"""Compile QA/main continuation after a stale watcher identity rejection; no duplicate registration."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed();old=A/'run_StockPairRankEmbedding184_full_registration_v8_20261010.py';new=A/'run_StockPairRankEmbedding184_registered_QA_main_resume26_v1_20261011.py';assert not new.exists()
 failure=A/'service_owned_workflows_20261006/recovery24_StockPairRankEmbedding184_round184_full_registration_v1_20261010/service_execution.json';assert read(failure)['status']=='failed'
 folder=A/'optimization_20261003_r184';protocol=read(folder/'protocol.json');assert protocol['expected_scored_records']==48 and protocol['explicit_parent_round']==183
 assert not (folder/'full_registration_execution.json').exists() and not (A/'github_validation_sync_main_20261005/round184_receipt.json').exists()
 s=old.read_text(encoding='utf8').replace('main_publisher_v11_20261010/native_launch.json','main_publisher_reboot_v12_20261011/native_launch.json').replace('from owned_idle_publication_wait_runtime_v1_20261010 import hold','from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold')
 needle="protocol=register();folder=A/'optimization_20261003_r184'";assert s.count(needle)==1;s=s.replace(needle,"folder=A/'optimization_20261003_r184';protocol=read(folder/'protocol.json')")
 s=s.replace("pins=protocol['input_sha256']","pins={**protocol['input_sha256'],str(Path(__file__)):sha(Path(__file__)),str(A/'owned_idle_publication_wait_reboot_identity_v2_20261011.py'):sha(A/'owned_idle_publication_wait_reboot_identity_v2_20261011.py')}\n    for path,digest in pins.items():assert sha(path)==digest,path")
 s=s.replace('frozen_before_actual_full_registration.json','frozen_before_actual_registered_QA_main_resume26.json').replace('full_registration_failure.json','full_registration_resume26_failure.json')
 compile(s,str(new),'exec');new.write_text(s,encoding='utf8',newline='\n')
 create(A/'actual184_registered_QA_main_resume26_source_admission_v1_20261011.json',{'status':'compiled_already_registered48_protocol_reuse_and_actual_reboot12_watcher_full_identity_before_QA_main_dispatch','input_sha256':{str(p):sha(p) for p in [Path(__file__),old,new,failure,folder/'protocol.json',folder/'frozen_before_actual_full_registration.json',A/'owned_idle_publication_wait_reboot_identity_v2_20261011.py']},'new_scores':0,'new_registration_claimed':False,'actual_QA95_and_main_not_yet_complete':True,'original_identity_rejection_preserved':True,'test_labels_read':False})
 print({'actual184_registered_protocol_reuse_QA_main_sources_ready':True,'new_fits_or_scores':0},flush=True)
if __name__=='__main__':main()
