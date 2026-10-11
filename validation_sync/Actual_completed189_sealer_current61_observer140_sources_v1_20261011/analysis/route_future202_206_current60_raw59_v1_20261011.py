"""Route nested frozen scripts through current closures, not superseded wrapper generations."""
from pathlib import Path
import sys,runpy,importlib
from contextlib import contextmanager
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
PROOF=A/'actual_future202_206_current60_raw59_admission_v1_20261011.json'

def execute(driver):
 assert allowed()
 import route_verified_canonical_publication_and_failed_chain38_v1_20261011 as prior
 closed,start,data=prior.installed()
 for name in ['actual_failed_chain40_preserving186_resume39_admission_v1_20261011.json','actual_completed186_finally_collision_and_shared_report41_admission_v1_20261011.json','actual_scratch_only_and_sealing_sources42_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases43_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases44_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases45_admission_v1_20261011.json','actual_fraction38_gate_only_routes46_admission_v1_20261011.json','actual_nested_dispatch_and_complete_aliases48_admission_v1_20261011.json','actual_failed_future202_206_routes49_admission_v1_20261011.json','actual_current_publication_paths_and_prospective50_admission_v1_20261011.json','actual_current_publication_paths_and_prospective53_admission_v1_20261011.json','actual_verified_current55_publication_runtime_admission_v1_20261011.json','actual_verified_current58_after_actual187_bridge_admission_v1_20261011.json']:
  p=read(A/name);data['service_aliases'].update(p['service_alias_updates'])
 proof=read(PROOF)
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 data['service_aliases'].update(proof['service_alias_updates']);data['driver_wrappers'].update(proof['driver_wrappers'])
 import owned_idle_publication_wait_reboot_identity_v2_20261011 as wait_module
 from owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 import hold as actual_hold
 wait_module.hold=actual_hold
 from types import ModuleType
 for name,filename in proof['publication_module_corrections'].items():
  q=A/filename;module=ModuleType(name);module.__file__=str(q);exec(compile(q.read_text(encoding='utf8'),str(q),'exec'),module.__dict__);sys.modules[name]=module
 p41=read(A/'actual_completed186_finally_collision_and_shared_report41_admission_v1_20261011.json')
 p42=read(A/'actual_scratch_only_and_sealing_sources42_admission_v1_20261011.json')
 for f in [*p41['source_factories'],*proof['source_factories']]:
  if f not in data['source_factories']:data['source_factories'].append(f)
  m=importlib.import_module(f);old=m.source_paths
  m.source_paths=lambda old=old:list(dict.fromkeys([*old(),PROOF,Path(__file__),*[Path(p) for p in proof['input_sha256']]]))
 # Load the real stdlib run_path in a private namespace to bypass historical path-wrapper redirects.
 raw_namespace={'__name__':'private_original_stdlib_runpy','__file__':runpy.__file__}
 exec(compile(Path(runpy.__file__).read_text(encoding='utf8'),runpy.__file__,'exec'),raw_namespace)
 raw=raw_namespace['run_path'];previous=runpy.run_path
 def dispatch(name):
  source=A/data['actual_source_overrides'].get(name,name)
  contract=p41['full_driver_contracts'].get(name)
  if contract:
   import byte_exact_ranking_stream_runtime_v1_20261010 as stream
   from shared_live_ranking_report_runtime_v3_20261011 import admitted_installed
   original=stream.installed
   @contextmanager
   def bound():
    with original(),admitted_installed(contract['number'],contract['codec_name'],contract['verifier_name']):yield
   stream.installed=bound
   try:return raw(str(source),run_name='__main__')
   finally:
    assert stream.installed is bound;stream.installed=original
  if name in p42['sealing_corrections']:
   text=source.read_text(encoding='utf8')
   for old,new in p42['sealing_corrections'][name]['replacements'].items():assert text.count(old)==1;text=text.replace(old,new)
   namespace={'__name__':'__main__','__file__':str(source)};exec(compile(text,str(source),'exec'),namespace);return namespace
  if name.startswith('seal_') or '_full_registration_' in name:return raw(str(source),run_name='__main__')
  m=importlib.import_module(source.stem)
  if hasattr(m,'create'):
   prior_create=m.create
   def pinned_create(path,value):
    if isinstance(value,dict) and 'input_sha256' in value:value['input_sha256'].update({str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)})
    return prior_create(path,value)
   m.create=pinned_create
  if hasattr(m,'closed'):m.closed=closed
  if hasattr(m,'start_service'):m.start_service=start
  if name.startswith('qualify_'):
   from native_scratch_only_mkdir_scope_v1_20261011 import installed
   with installed(m.OUT):m.main()
  elif name=='run_Rank20TwoSeed187_complete_family_v2_20261011.py':
   import verify_Rank20TwoSeed187_full88_preflight_v2_20261011 as pre
   old_create=pre.create
   target=A/'rank20_two_seed187_full_family_preflight_v2_20261011.json'
   recovered=A/'rank20_two_seed187_full_family_preflight_recovered44_v1_20261011.json'
   def fresh(path,value):
    assert Path(path)==target
    return old_create(recovered,value)
   pre.create=fresh
   text=source.read_text(encoding='utf8')
   begin=text.index('    for logical,physical in OUTPUTS.items():')
   end=text.index('    from prepare_Rank20TwoSeed187_complete88_pipeline',begin)
   text=text[:begin]+'''    for logical,physical in OUTPUTS.items():
        assert logical.is_relative_to(ROOT) and physical.is_relative_to(Path('E:/赛题五_本机临时/第187轮_20261010'))
        assert logical.exists() and physical.exists()
        empty(logical)
'''+text[end:]
   text=text.replace("out=A/'Rank20TwoSeed187_complete_family_v1_20261010'", "out=A/'Rank20TwoSeed187_complete_family_recovered44_v1_20261011'")
   text=text.replace("A/'rank20_two_seed187_full_family_preflight_v2_20261011.json'", "A/'rank20_two_seed187_full_family_preflight_recovered44_v1_20261011.json'")
   namespace={'__name__':'__main__','__file__':str(source)}
   try:exec(compile(text,str(source),'exec'),namespace)
   finally:pre.create=old_create
  elif name=='run_Rank20TwoSeed187_selected_candidate_feature_cache_v2_20261011.py':
   text=source.read_text(encoding='utf8');old='selected_feature_cache_runtime_v5';assert text.count(old)==1
   text=text.replace(old,'selected_feature_cache_runtime_recovered44')
   namespace={'__name__':'__main__','__file__':str(source)};exec(compile(text,str(source),'exec'),namespace)
  else:m.main()
  return vars(m)
 def routed(path,*args,**kwargs):
  name=Path(path).name
  if name in proof['driver_wrappers']:
   assert not args and kwargs.get('run_name','__main__')=='__main__' and not kwargs.get('init_globals')
   return dispatch(name)
  return raw(path,*args,**kwargs)
 runpy.run_path=routed
 try:dispatch(driver)
 finally:
  assert runpy.run_path is routed;runpy.run_path=previous
