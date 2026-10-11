"""Retain v5 evidence, retire three verified idle helpers, admit exact native dependencies."""
from pathlib import Path
import sys,ast,subprocess,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 old=A/'prepare_StockRank60Direct200_complete35_pipeline_v5_20261011.py'
 s=old.read_text(encoding='utf8').replace('_v5_20261011','_v6_20261011')
 needle=' return s\n\ndef artifact(n):'
 assert s.count(needle)==1
 patch=""" s=s.replace('actual_stock_rank60_direct_embedding_six_state_native42','actual_stock_rank60_embedding_six_state_native42').replace('StockRank60DirectEmbeddingSmall512_independent_full5','StockRank60EmbeddingSmall512_independent_full5').replace('stock_rank60_direct_embedding_small512_BF16_bank6','stock_rank60_embedding_small512_BF16_bank6')
 s=s.replace('actual_stock_rank60_direct_embedding35_after199_normalization_queue_v1_20261011','actual_stock_rank60_direct_embedding35_after199_normalization_queue_v6_20261011').replace('StockRank60DirectEmbedding35_selected_native14_v1_20261011','StockRank60DirectEmbedding35_selected_native14_v6_20261011')
 return s

def artifact(n):"""
 s=s.replace(needle,patch)
 s=s.replace("'actual_stock_rank60_direct35_after199_normalization_v6_20261011'","'actual_stock_rank60_direct_embedding35_after199_normalization_queue_v6_20261011'")
 marker=' pins={str(p):sha(p) for p in [Path(__file__)'
 assert s.count(marker)==1
 audit=""" # Verify all literal wait gates refer to actual existing services or this family's future jobs.
 planned={'actual_stock_rank60_direct_embedding35_after199_normalization_queue_v6_20261011','StockRank60DirectEmbedding35_selected_native14_v6_20261011','StockRank60DirectEmbedding200_selected_candidate_preparation_v6_20261011','StockRank60DirectEmbedding200_selected_candidate_sealing_v6_20261011'}
 for p in outputs:
  for node in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
   if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='closed' and node.args and isinstance(node.args[0],ast.Constant) and isinstance(node.args[0].value,str):
    gate=node.args[0].value;assert gate in planned or (A/'service_owned_workflows_20261006'/gate/'native_launch.json').exists(),(p.name,gate)
 assert "'stock_rank60_embedding_small512_BF16_bank6_v1_20261011'" in normal
"""
 s=s.replace(marker,audit+marker)
 target=A/'prepare_StockRank60Direct200_complete35_pipeline_v6_20261011.py';ast.parse(s);assert not target.exists();target.write_text(s,encoding='utf8')
 names=['actual_stock_rank60_direct35_after199_normalization_v5_20261011','StockRank60DirectEmbedding35_selected_native14_v1_20261011','StockRank60DirectEmbedding200_complete35_family_v5_20261011'];rows=[]
 spy=ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
 for name in names:
  folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json');assert owned(row)
  w=psutil.Process(row['owned_worker_pid']);p=psutil.Process(row['pid']);assert not w.children() and p.create_time()==row['owned_parent_creation_time'] and p.cmdline()[1:]==w.cmdline()[1:]
  r=subprocess.run([str(spy),'dump','--pid',str(w.pid)],capture_output=True,text=True,encoding='utf8',check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  assert '(idle)' in r.stdout and 'closed (' in r.stdout and 'main (' in r.stdout
  rows.append((folder,row,w,p,r.stdout))
 proof={'status':'verified_three_idle200_helpers_before_any_native_or_future_output','input_sha256':{str(old):sha(old),str(target):sha(target),str(Path(__file__)):sha(__file__)},'retirements':[{'identity':r,'actual_stack':stack} for _,r,_,_,stack in rows],'scientific_jobs_terminated':0,'new_fits_or_scores':0}
 create(A/'complete200_dependencies_actual_idle_retirement_v6_20261011.json',proof)
 for folder,row,w,p,stack in rows:
  assert allowed() and owned(row) and not w.children();w.terminate();w.wait(15);p.terminate();p.wait(15)
  create(folder/'administrative_supersession_before_any_future200_v6_20261011.json',proof)
 import importlib;assert allowed();importlib.import_module(target.stem).main()
 print({'actual200_dependencies_corrected_before_future':True,'three_idle_helpers_only_retired':True},flush=True)
if __name__=='__main__':main()
