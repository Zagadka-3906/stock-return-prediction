"""Replace only the still idle candidate controller; Win32 directory guard correction precedes all inference."""
from pathlib import Path
import sys,ast,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from run_protected167_complete_family_v1_20261010 import junction

def main():
 assert allowed()
 name='actual_rank60_flag17_gain_selected_full_candidate_queue_v1_20261011';folder=A/'service_owned_workflows_20261006'/name;identity=read(folder/'native_launch.json');assert owned(identity)
 def idle():
  assert owned(identity);p=psutil.Process(identity['owned_worker_pid']);assert not p.children(recursive=True)
  dump=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,encoding='utf8',check=True).stdout
  assert '(idle)' in dump and 'closed (' in dump,dump;return dump
 dump=idle()
 assert not (A/'rank60_flag17_best17_gain_decision_v1_20261011.json').exists()
 original=A/'stock_rank60_flag17_early_storage_v2_20261011.py';text=original.read_text(encoding='utf8');assert text.count('kernel16')==1 and 'float16' not in text
 # Actual Windows API control: the corrected function is byte-for-byte the proven original guard body.
 previous=A/'stock_rank60medium_best33_early_storage_v2_20261011.py'
 def body(s):return ast.dump(next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name=='empty'),include_attributes=False)
 assert body(text.replace('kernel16','kernel32'))==body(previous.read_text(encoding='utf8'))
 import ctypes
 attributes=ctypes.windll.kernel32.GetFileAttributesW(str(A));assert attributes!=0xFFFFFFFF and attributes&0x10
 proof=A/'flag17_actual_Win32_storage_guard_recovery_admission_v1_20261011.json'
 wrapper=A/'run_StockRank60FlagOnlyBest17Early_selected_candidate_feature_cache_v3_20261011.py'
 source='''from pathlib import Path
import sys,runpy,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed();p=A/'flag17_actual_Win32_storage_guard_recovery_admission_v1_20261011.json';proof=read(p)
 for source,digest in proof['input_sha256'].items():assert sha(source)==digest,source
 import stock_rank60_flag17_early_storage_v2_20261011 as storage
 old=storage.empty;tree=ast.parse(Path(storage.__file__).read_text(encoding='utf8'))
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='empty')
 node_source=ast.unparse(node).replace('kernel16','kernel32');namespace=dict(vars(storage));exec(compile(node_source,str(Path(__file__)),'exec'),namespace);new=namespace['empty'];storage.empty=new
 import importlib
 prepare=importlib.import_module('prepare_StockRank60FlagOnlyBest17Early_selected_candidate_v2_20261011')
 original_create=prepare.create
 def frozen_create(path,value):
  if isinstance(value,dict) and 'input_sha256' in value:value['input_sha256'].update({str(p):sha(p),str(Path(__file__)):sha(__file__)})
  return original_create(path,value)
 prepare.create=frozen_create
 try:runpy.run_path(str(A/'run_StockRank60FlagOnlyBest17Early_selected_candidate_feature_cache_v2_20261011.py'),run_name='__main__')
 finally:
  assert storage.empty is new;storage.empty=old;prepare.create=original_create
if __name__=='__main__':main()
'''
 ast.parse(source);assert not wrapper.exists();wrapper.write_text(source,encoding='utf8',newline='\n')
 queue=A/'run_rank60_flag17_gain_selected_full_candidate_queue_v2_20261011.py';s=(A/'run_rank60_flag17_gain_selected_full_candidate_queue_v1_20261011.py').read_text(encoding='utf8')
 old='run_StockRank60FlagOnlyBest17Early_selected_candidate_feature_cache_v2_20261011.py';assert s.count(old)==1;s=s.replace(old,wrapper.name)
 ast.parse(s);assert not queue.exists();queue.write_text(s,encoding='utf8',newline='\n')
 create(proof,{'status':'passed_actual_original_storage_empty_guard_AST_exact_after_kernel32_typo_correction_actual_Win32_directory_attribute_call','input_sha256':{str(p):sha(p) for p in [Path(__file__),original,previous,wrapper,queue]},'original_idle_controller_identity':identity,'actual_idle_stack':dump,'actual_directory_attributes':attributes,'scientific_workers_restarted_or_terminated':0,'new_fits':0,'new_scores':0,'native_checks_and_all_candidate_assertions_retained':True})
 idle();assert not (A/'rank60_flag17_best17_gain_decision_v1_20261011.json').exists()
 p=psutil.Process(identity['owned_worker_pid']);assert owned(identity);p.terminate();p.wait(timeout=10)
 archive=folder.with_name(name+'_original_idle_storage_API_evidence');assert not archive.exists();folder.rename(archive)
 actual='actual_rank60_flag17_gain_selected_full_candidate_queue_v2_20261011';i=start_service(actual,queue.name,[],{str(queue):sha(queue),str(proof):sha(proof)})
 junction(folder,A/'service_owned_workflows_20261006'/actual)
 create(A/'actual_flag17_Win32_storage_controller_recovery_activation_v1_20261011.json',{'identity':i,'original_controller_evidence':str(archive),'original_logical_service_alias':str(folder),'scientific_workers_restarted_or_terminated':0})
 print('Only actual idle flag candidate controller corrected; raw17 scores and all model jobs untouched',flush=True)

if __name__=='__main__':main()
