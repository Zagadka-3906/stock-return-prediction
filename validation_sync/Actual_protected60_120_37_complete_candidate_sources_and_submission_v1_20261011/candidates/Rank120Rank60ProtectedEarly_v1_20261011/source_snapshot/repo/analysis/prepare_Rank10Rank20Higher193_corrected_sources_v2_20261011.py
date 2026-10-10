from pathlib import Path
import sys,re,subprocess,psutil,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
from handoff_ready_goss_full_execution_20261006 import retire
import prepare_Rank10Rank20Higher193_complete51_pipeline_v1_20261011 as previous
def main():
 assert allowed()
 files=[A/n for n in previous.NAMES+previous.EXTRAS[2:9]]
 mapping={p.name:p.name.replace('_v1_20261011.py','_v2_20261011.py') for p in files}
 mapping.update({Path(k).stem:Path(v).stem for k,v in list(mapping.items())})
 mapping['prepare_Rank10Rank20Higher193_complete51_pipeline_v1_20261011']='prepare_Rank10Rank20Higher193_complete51_pipeline_v2_20261011'
 mapping['rank10_rank20_higher193_candidate_sources_preparation_v1_20261011.json']='rank10_rank20_higher193_candidate_sources_preparation_v2_20261011.json'
 mapping['rank10_rank20_higher193_full_registry_sources_preparation_v1_20261011.json']='rank10_rank20_higher193_full_registry_sources_preparation_v2_20261011.json'
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)));outputs=[]
 for p in files:
  text=pattern.sub(lambda m:mapping[m.group()],p.read_text(encoding='utf8'))
  # Apply the actual51 record count to every embedded status and artifact token too.
  text=re.sub(r'([A-Za-z_]+)27\b',lambda m:m.group(1)+'51',text)
  text=text.replace('stock_rank5_embedding_small512_BF16_bank6_v1_20261010','stock_rank10_embedding_small512_BF16_bank6_v1_20261011').replace('actual_StockRank5EmbeddingSmall512_full5_independent_location_v1_20261009.json','actual_StockRank10EmbeddingSmall512_full5_independent_location_v1_20261011.json')
  q=A/mapping[p.name];assert not q.exists();compile(text,str(q),'exec');q.write_text(text,encoding='utf8',newline='\n');outputs.append(q)
 names=[mapping.get(n,n) for n in previous.NAMES];extras=[mapping.get(n,n) for n in previous.EXTRAS]
 proof=A/'rank10_rank20_higher193_full_execution_sources_admission_v2_20261011.json'
 factory=A/'prepare_Rank10Rank20Higher193_complete51_pipeline_v2_20261011.py'
 body="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nNAMES="+repr(names)+"\nEXTRAS="+repr(extras)+"\nPROOF="+repr(proof.name)+"\ndef source_paths():return list(dict.fromkeys([Path(__file__),A/PROOF,*[A/n for n in NAMES+EXTRAS],A/'prepare_Rank10Rank20Higher193_corrected_sources_v2_20261011.py']))\n"
 assert not factory.exists();compile(body,str(factory),'exec');factory.write_text(body,encoding='utf8',newline='\n');outputs.append(factory)
 candidate=A/mapping[previous.EXTRAS[3]];text=candidate.read_text(encoding='utf8')
 assert "pilot51.json" in text and 'passed_normalized51_actual_TRAIN' in text and 'stock_rank10_embedding_small512_BF16_bank6_v1_20261011' in text
 assert 'stock_rank5_embedding_small512_BF16_bank6_v1_20261010' not in text
 register=A/mapping[previous.NAMES[0]];assert 'pilot51.json' in register.read_text(encoding='utf8')
 for p in outputs:
  if p.suffix=='.py':
   for node in ast_nodes(p):
    if isinstance(node,str) and ('Rank10Rank20Higher193' in node or 'rank10_rank20' in node):assert (A/(node+'.py')).exists(),(p.name,node)
 pins={str(p):sha(p) for p in [Path(__file__),Path(previous.__file__),A/previous.PROOF,*files,*outputs,A/'rank10_rank20_higher51_normalization_native14_sources_admission_v1_20261011.json']}
 for key in previous.EXTRAS[9:11]:create(A/mapping[key],{'status':'compiled_corrected51_status_and_pilot_tokens_and_own_rank10_full5_bank_mapping_before_future','input_sha256':pins,'new_fits':0,'new_scores':0,'future_X_read':False})
 create(proof,{'status':'compiled_193_corrected_complete51_QA104_17852_W476_before_any_future_inference','input_sha256':pins,'original_source1_preserved':True,'corrected_pilot_record_count':51,'corrected_own_new_bank_horizon':10,'new_scores':0,'new_fits':0,'future_X_read':False})
 old=A/'service_owned_workflows_20261006/Rank10Rank20Higher193_complete51_family_v1_20261011/native_launch.json';row=read(old);stack=None
 if owned(row):
  p=psutil.Process(row['owned_worker_pid']);assert not p.children();stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,timeout=30).stdout
  assert 'closed (' in stack,(row,stack);retire(row,'Replace exact idle193 source1 before any scientific dispatch; corrected embedded51 artifact/status guards and new Rank10 own bank full5 pointer, original source1 retained')
 create(A/'rank10_rank20_higher193_actual_source1_idle_supersession_v2_20261011.json',{'prior_identity':row,'stack':stack,'new_fits':0,'new_scores':0})
 driver=A/mapping[previous.EXTRAS[5]];r=start_service('Rank10Rank20Higher193_complete51_family_v2_20261011',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/'Rank10Rank20Higher193_complete51_family_v2_activation_20261011.json',r)
 print({'193_actual_corrected51_sources_v2_dispatched':True,'new_fits_or_scores':0},flush=True)
def ast_nodes(p):
 import ast
 for node in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
  if isinstance(node,ast.ImportFrom) and node.module:yield node.module
if __name__=='__main__':main()
