from pathlib import Path
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
