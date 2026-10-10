from pathlib import Path
import sys,runpy
from contextlib import contextmanager
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from run_dependency_queue_v3_20261006 import read,sha
if __name__=='__main__':
 assert allowed()
 from route_verified_canonical_publication_and_failed_chain38_v1_20261011 import installed
 closed,start,data=installed()
 for name in ['actual_failed_chain40_preserving186_resume39_admission_v1_20261011.json','actual_completed186_finally_collision_and_shared_report41_admission_v1_20261011.json','actual_scratch_only_and_sealing_sources42_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases43_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases44_admission_v1_20261011.json']:
  data['service_aliases'].update(read(A/name)['service_alias_updates'])
 import byte_exact_ranking_stream_runtime_v1_20261010 as stream
 from shared_live_ranking_report_runtime_v3_20261011 import admitted_installed
 original=stream.installed
 @contextmanager
 def bound():
  with original(),admitted_installed(187,'build_lossless_ranking_display_round187_v2_20261011','verify_lossless_ranking_display_round187_v2_20261011'):yield
 stream.installed=bound
 try:runpy.run_path(str(A/'run_Rank20TwoSeed187_registered_QA_main_resume45_v1_20261011.py'),run_name='__main__')
 finally:stream.installed=original
