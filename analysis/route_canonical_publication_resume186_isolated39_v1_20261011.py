from pathlib import Path
import sys,runpy,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
PROOF=A/'canonical_publication_resume186_isolated39_admission_v1_20261011.json'
def execute(driver):
 assert allowed()
 import route_verified_canonical_publication_and_failed_chain38_v1_20261011 as prior
 closed,start,data=prior.installed();proof=read(PROOF)
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 data['service_aliases']['actual186_registered_QA_main_resume38_v1_20261011']='actual186_registered_QA_main_resume39_v1_20261011'
 for f in data['source_factories']:
  m=importlib.import_module(f);old=m.source_paths
  m.source_paths=lambda old=old:list(dict.fromkeys([*old(),PROOF,Path(__file__),*[Path(p) for p in proof['input_sha256']]]))
 source=A/data['actual_source_overrides'].get(driver,driver)
 if driver.startswith('seal_') or '_full_registration_' in driver or 'resume39' in driver:runpy.run_path(str(source),run_name='__main__');return
 m=importlib.import_module(source.stem)
 if hasattr(m,'closed'):m.closed=closed
 if hasattr(m,'start_service'):m.start_service=start
 m.main()
