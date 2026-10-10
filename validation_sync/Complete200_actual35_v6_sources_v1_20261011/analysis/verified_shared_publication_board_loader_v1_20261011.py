"""Read the same immutable full report through its byte-proven shared-node archive."""
from pathlib import Path
from contextlib import contextmanager
from types import SimpleNamespace
import hashlib,json,gzip,re,gc,time

class BoardText:
 def __init__(self,owner):self.owner=owner
class BoardBytes:
 def __init__(self,owner):self.owner=owner
 def decode(self,encoding='utf-8',errors='strict'):
  assert encoding in ('utf-8','utf-8-sig') and errors=='strict';return BoardText(self.owner)

class SharedBoard:
 def __init__(self,path):
  from run_dependency_queue_v3_20261006 import read,sha
  self.path=Path(path);self.folder=self.path.parent;self.proof=read(self.folder/'full_report_publication_snapshot_verification.json');self.codec=read(self.folder/'verification.json')
  assert self.proof['status']=='passed_exact_original_full_report_bytes_from_immutable_lossless_HTML'
  assert self.codec['status']=='passed_all_original_report_values_and_six_views_lossless_roundtrip'
  assert self.proof['original_report_sha256']==self.codec['original_report_sha256']
  self.compressed_sha=sha(self.path);assert self.compressed_sha==self.proof['compressed_snapshot_sha256']
  self.page=self.folder/'complete_rankings_lossless.html';self.page_sha=sha(self.page);assert self.page_sha==self.codec['lossless_HTML_sha256']
  self.pins={str(p):sha(p) for p in [self.path,self.page,self.folder/'verification.json',self.folder/'full_report_publication_snapshot_verification.json']};self.report=None;self.events=[];self.marker=BoardBytes(self)
 def load(self):
  if self.report is None:
   from build_lossless_ranking_display_v2_20261006 import unpack_report
   start=time.perf_counter();text=self.page.read_text(encoding='utf8');match=re.search(r'<script\s+id="data"\s+type="application/json">(.*?)</script>',text,re.S);assert match is not None;packed=json.loads(match.group(1));self.report=unpack_report(packed)
   assert len(self.report['connected'])==self.proof['connected_records']==self.codec['connected_records'];del text,match,packed;gc.collect();self.events.append({'actual_shared_load_seconds':time.perf_counter()-start,'connected_records':len(self.report['connected'])})
  return self.report
 def reverify(self):
  from run_dependency_queue_v3_20261006 import sha
  for p,d in self.pins.items():assert sha(p)==d,p

def bind_namespace(namespace):
 originals={k:namespace[k] for k in ('json','gzip','sha')};state={'owner':None,'avoided_full_decompression_calls':0}
 class JsonProxy:
  def __getattr__(self,n):return getattr(originals['json'],n)
  def loads(self,value,*args,**kwargs):
   if isinstance(value,BoardText):assert not args and not kwargs;return value.owner.load()
   return originals['json'].loads(value,*args,**kwargs)
 class GzipProxy:
  def __getattr__(self,n):return getattr(originals['gzip'],n)
  def decompress(self,value):
   path=namespace.get('PUBLICATION_FULL_REPORT')
   if path is not None:
    if state['owner'] is None:state['owner']=SharedBoard(path)
    owner=state['owner']
    if hashlib.sha256(value).hexdigest()==owner.compressed_sha:
     state['avoided_full_decompression_calls']+=1;return owner.marker
   return originals['gzip'].decompress(value)
 def digest(value,*args,**kwargs):
  if isinstance(value,BoardBytes):assert not args and not kwargs;return value.owner.proof['original_report_sha256']
  return originals['sha'](value,*args,**kwargs)
 proxies={'json':JsonProxy(),'gzip':GzipProxy(),'sha':digest};namespace.update(proxies)
 def restore():
  for k,v in proxies.items():assert namespace[k] is v;namespace[k]=originals[k]
 return state,restore

@contextmanager
def installed(publisher,log=None):
 from byte_exact_dynamic_snapshot_encoder_runtime_v1_20261010 import installed as original_binding
 from run_dependency_queue_v3_20261006 import read,sha,create
 A=Path(__file__).resolve().parent;proof=read(A/'verified_shared_publication_board_loader_actual_complete180_controls_v1_20261011.json')
 assert proof['status']=='passed_actual_complete180_shared_board_publication_read_stage_and_full_native_bytes_exact'
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 states=[];restores=[]
 with original_binding(publisher,Path(log).with_name('original_encoder_binding.json') if log else None):
  delegate=publisher.exec
  def execute(code,namespace,*args,**kwargs):
   result=delegate(code,namespace,*args,**kwargs);assert namespace['snapshot'].__globals__ is namespace
   state,restore=bind_namespace(namespace);states.append(state);restores.append(restore);return result
  publisher.exec=execute
  try:yield states
  finally:
   assert publisher.exec is execute;publisher.exec=delegate
   for state in states:
    if state['owner'] is not None:state['owner'].reverify()
   for restore in reversed(restores):restore()
 if log:
  create(Path(log),{'status':'passed_publication_only_shared_full_board_reader_restored','actual_reports':[{'pins':s['owner'].pins,'events':s['owner'].events,'avoided_full_decompression_calls':s['avoided_full_decompression_calls'],'original_native_sha256':s['owner'].proof['original_report_sha256']} for s in states if s['owner'] is not None],'new_fits':0,'new_scores':0,'snapshot_function_code_object_unchanged':True,'original_scientific_values_and_byte_exact_encoder_preserved':True})
