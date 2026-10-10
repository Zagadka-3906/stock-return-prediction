from pathlib import Path
import sys,runpy,importlib,re
from contextlib import contextmanager
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
PROOF=A/'actual_completed186_finally_collision_and_shared_report41_admission_v1_20261011.json'

def execute(driver):
 assert allowed()
 import route_verified_canonical_publication_and_failed_chain38_v1_20261011 as prior
 closed,start,data=prior.installed();p40=read(A/'actual_failed_chain40_preserving186_resume39_admission_v1_20261011.json');proof=read(PROOF)
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 data['service_aliases'].update(p40['service_alias_updates']);data['service_aliases'].update(proof['service_alias_updates'])
 data['driver_wrappers'].update(proof['driver_wrappers'])
 for f in proof['source_factories']:
  if f not in data['source_factories']:data['source_factories'].append(f)
  m=importlib.import_module(f);old=m.source_paths
  m.source_paths=lambda old=old:list(dict.fromkeys([*old(),PROOF,Path(__file__),*[Path(p) for p in proof['input_sha256']]]))
 source=A/data['actual_source_overrides'].get(driver,driver)
 contract=proof['full_driver_contracts'].get(driver)
 if contract:
  import byte_exact_ranking_stream_runtime_v1_20261010 as stream
  from shared_live_ranking_report_runtime_v2_20261011 import admitted_installed
  original=stream.installed
  @contextmanager
  def bound():
   with original(),admitted_installed(contract['number'],contract['codec_name'],contract['verifier_name']):yield
  stream.installed=bound
  try:runpy.run_path(str(source),run_name='__main__')
  finally:
   assert stream.installed is bound;stream.installed=original
  return
 if driver.startswith('seal_') or '_full_registration_' in driver:runpy.run_path(str(source),run_name='__main__');return
 m=importlib.import_module(source.stem)
 if hasattr(m,'closed'):m.closed=closed
 if hasattr(m,'start_service'):m.start_service=start
 m.main()
