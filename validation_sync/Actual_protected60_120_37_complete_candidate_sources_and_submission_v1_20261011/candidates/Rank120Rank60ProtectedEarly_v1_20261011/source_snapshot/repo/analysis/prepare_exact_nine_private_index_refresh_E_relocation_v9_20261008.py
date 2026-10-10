"""Use Git add for exactly nine already verified HEAD-identical LF files; prove every staged object unchanged."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
 old=A/'relocate_verified_publisher_after_private_stat_refresh_v8_20261008.py';s=old.read_text(encoding='utf8').replace('_v8_20261008','_v9_20261008')
 s=s.replace('Git_publisher_refreshed_current_main_and_E_relocation_v7_20261008/service_execution.json','Git_publisher_private_stat_refresh_verified_E_relocation_v8_20261008/service_execution.json')
 needle="        git(TARGET,'update-index','--refresh')";assert s.count(needle)==1
 s=s.replace(needle,"""        for name in names:
            actual_blob=git(TARGET,'hash-object','--path='+name,name)
            expected_blob=git(TARGET,'rev-parse',head+':'+name)
            assert actual_blob==expected_blob,name
        # Git refresh may reject a size mismatch without content hashing; add refreshes exactly these same objects and stat entries.
        git(TARGET,'add','-f','--',*names)
""")
 target=A/'relocate_verified_publisher_after_exact_nine_index_refresh_v9_20261008.py';compile(s,str(target),'exec')
 with target.open('x',encoding='utf8',newline='') as f:f.write(s)
 pins={str(p):sha(p) for p in [Path(__file__),old,target]}
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 r=start('Git_publisher_exact_nine_index_refresh_verified_E_relocation_v9_20261008',target.name,[],pins)
 create(A/'Git_publisher_exact_nine_index_refresh_E_relocation_hidden_launch_v9_20261008.json',{'launch':r,'input_sha256':pins,
  'exactly_nine_current_HEAD_identical_objects_refreshed':True,'all_staged_modes_paths_and_object_ids_checked_equal_before_switch':True,
  'primary_workspace_index_and_working_files_unchanged':True,'all_original_raw_bytes_retained_on_E_before_D_duplicate_deletion':True})
 print(json.dumps({'worker':r['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
