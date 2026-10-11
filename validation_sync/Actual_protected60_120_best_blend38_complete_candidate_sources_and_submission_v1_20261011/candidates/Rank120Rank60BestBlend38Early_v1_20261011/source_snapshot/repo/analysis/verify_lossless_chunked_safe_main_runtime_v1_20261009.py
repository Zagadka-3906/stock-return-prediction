from pathlib import Path
import sys,hashlib,json,types,subprocess
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
import lossless_chunked_safe_main_runtime_v1_20261009 as runtime
folder=Path('E:/赛题五_本机临时/lossless_chunked_safe_main_runtime_probe_v1_20261009');folder.mkdir(exist_ok=False)
data=bytes(range(256))*12001;name='validation_sync/round999/display/probe.gz'
payload={name:data,'validation_sync/round999/display/small.json':b'{}'}
evidence={'exported_files':{n:{'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()} for n,d in payload.items()},'original_full_ranking_sha256':'unused_for_non_report_probe'}
module=types.ModuleType('collect_full_lossless_round_transport_probe');module.collect=lambda *args:(dict(payload),json.loads(json.dumps(evidence)))
sys.modules[module.__name__]=module
old_limit,old_chunk=runtime.LIMIT,runtime.CHUNK;runtime.LIMIT=1024**2;runtime.CHUNK=256*1024
try:
 with runtime.installed(folder/'runtime_execution'):
  imported=__import__(module.__name__);transport,proof=imported.collect()
  assert name not in transport and name not in proof['exported_files']
  target=folder/'display';target.mkdir()
  for n,d in transport.items():
   assert hashlib.sha256(d).hexdigest()==proof['exported_files'][n]['sha256']
   (target/Path(n).name).write_bytes(d)
  script=target/'reconstruct_chunked_reports.py'
  r=subprocess.run([sys.executable,'-B','-X','utf8',str(script)],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
  assert r.returncode==0,r.stderr
  assert (target/'probe.gz').read_bytes()==data
  import publish_classifier_consensus_workflows_20261006 as helpers
  encoded=helpers.sync.encoded({'status':'validated_local_snapshot'})
  assert name in json.loads(encoded)['chunked_original_artifacts']
  commit=helpers.sync.git('rev-parse','HEAD',cwd=ROOT);helpers.watcher.advance_source_index(commit)
finally:
 runtime.LIMIT=old_limit;runtime.CHUNK=old_chunk;del sys.modules[module.__name__]
assert module.collect()==(payload,evidence)
record=json.loads((folder/'runtime_execution/execution.json').read_text(encoding='utf8'))
assert record['research_index_bytes_unchanged'] and len(record['main_ref_updates'])==1
create(A/'lossless_chunked_safe_main_runtime_v1_20261009.json',{'status':'passed_independent_reconstruction_import_collector_manifest_and_research_index_guards',
 'input_sha256':{str(p):sha(p) for p in (Path(__file__),Path(runtime.__file__),script,folder/'runtime_execution/execution.json')},
 'original_bytes':len(data),'original_sha256':hashlib.sha256(data).hexdigest(),'chunk_count':len(record['chunked_original_artifacts'][name]['parts']),
 'exact_reconstruction_executed':True,'research_index_bytes_unchanged':True,'large_production_file_threshold_MiB':95,'production_chunk_MiB':16,'scientific_math_changed':False,'new_quality_scores':0})
print('Independent reconstruction, collector hook, manifest and index guards passed.')
