from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
def main():
 from run_dependency_queue_v3_20261006 import read,sha
 from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
 assert allowed();proof=read(A/'actual191_original27_registration_metadata_only_recovery70_admission_v1_20261011.json');assert sha(A/'run_MixedRefined191_full_registration_v1_20261011_actual_parent190_metadata_recovery70.py')==proof['new_source_sha256']
 import route_verified_canonical_publication_and_failed_chain38_v1_20261011 as prior
 original=prior.installed
 def patched():
  closed,start,data=original();data['actual_source_overrides']['run_MixedRefined191_full_registration_v1_20261011.py']='run_MixedRefined191_full_registration_v1_20261011_actual_parent190_metadata_recovery70.py';return closed,start,data
 prior.installed=patched
 try:runpy.run_path(str(A/'run_MixedRefined191_full_registration_v1_20261011_current_main_parent69_wrapper.py'),run_name='__main__')
 finally:prior.installed=original
if __name__=='__main__':main()
