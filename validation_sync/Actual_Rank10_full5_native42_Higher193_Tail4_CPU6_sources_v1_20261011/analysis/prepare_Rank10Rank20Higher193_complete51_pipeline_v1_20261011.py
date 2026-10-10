from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
import prepare_MixedRefined191_complete27_pipeline_v1_20261011 as previous
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
FACTORY=Path(__file__).stem
PROOF='rank10_rank20_higher193_full_execution_sources_admission_v1_20261011.json'
NORMAL='normalize_completed_rank10_rank20_higher51_after192_v1_20261011'
QUAL='qualify_rank10_rank20_higher51_selected_native14_v1_20261011'
PRED='predict_rank10_rank20_mixed_complete_qualified_parent_scheme_v1_20261011'
PLAN='rank10_rank20_higher_complete51_after192_plan_v1_20261011.json'
CALL='rank10_rank20_mixed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json'
STAGE='rank10_rank20_mixed_after_qualified_parent_native_stage_v1_20261011'
def base(text):
 mapping={'MixedRefined191':'Rank10Rank20Higher193','mixed_refined191':'rank10_rank20_higher193',
 'MixedProtected190_complete39_family_v1_20261011':'StockRank10Embedding192_complete48_family_v1_20261011',
 'mixed_protected190_full_execution_sources_admission_v1_20261011.json':'stock_rank10_embedding192_full_execution_sources_admission_v1_20261011.json',
 'round191':'round193','round190':'round192','_r191':'_r193','_r190':'_r192','第191轮':'第193轮','qualified190':'qualified192','qa102':'qa104','QA102':'QA104','qa_v102':'qa_v104','wave474':'wave476','17753':'17852','17726':'17801',
 'near_refined27':'rank10_rank20_higher51','near_refined_complete27':'rank10_rank20_higher_complete51','near_refined25':'rank10_rank20_higher49',
 'rank5_rank20_near_pure_after_qualified_parent_native_stage_v1_20261011':STAGE,
 'rank5_rank20_mixed':'rank10_rank20_mixed','rank5_weight':'rank10_weight'}
 pat=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)));text=pat.sub(lambda m:mapping[m.group()],text)
 return re.sub(r'(?<![.A-Za-z0-9_])(191|190|474|102|27|24|72)(?![A-Za-z0-9_])',lambda m:{'191':'193','190':'192','474':'476','102':'104','27':'51','24':'48','72':'144'}[m.group()],text)
NAMES=[base(n) for n in previous.NAMES]
EXTRAS=[NORMAL+'.py',QUAL+'.py',*[base(n) for n in previous.EXTRAS[2:11]],PLAN,PRED+'.py',CALL,STAGE+'.py',
 'rank10_rank20_higher51_normalization_native14_sources_admission_v1_20261011.json',
 'rank10_rank20_higher49_actual_native14_and_predictor_sources_admission_v1_20261011.json',
 *[n for n in previous.EXTRAS[17:] if 'near_refined' not in n]]
def source_paths():return list(dict.fromkeys([Path(__file__),A/PROOF,*[A/n for n in NAMES+EXTRAS]]))
def route(text):
 mapping={previous.EXTRAS[0]:NORMAL+'.py',previous.EXTRAS[1]:QUAL+'.py',previous.EXTRAS[11]:PLAN,previous.EXTRAS[12]:PRED+'.py',previous.EXTRAS[13]:CALL,Path(previous.__file__).name:FACTORY+'.py',previous.STAGE:STAGE}
 mapping.update({Path(k).stem:Path(v).stem for k,v in list(mapping.items()) if k.endswith('.py')})
 placeholders={k:'__SOURCE193_'+str(i)+'__' for i,k in enumerate(mapping)};pat=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
 text=pat.sub(lambda m:placeholders[m.group()],text);text=base(text)
 for k,v in placeholders.items():text=text.replace(v,mapping[k])
 text=text.replace('main_publisher_v11_20261010','main_publisher_reboot_v12_20261011')
 text=text.replace("while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)","from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed\n    closed(service.name)")
 return text
def main():
 assert allowed();assert read(A/PLAN)['expected_records']==51 and len(read(A/CALL)['records'])==11
 admission=A/'rank10_rank20_higher51_normalization_native14_sources_admission_v1_20261011.json'
 for p,d in read(admission)['input_sha256'].items():assert sha(p)==d,p
 inputs=[A/n for n in previous.NAMES+previous.EXTRAS[2:9]];texts={}
 for source in inputs:
  target=A/base(source.name);assert not target.exists(),target;text=route(source.read_text(encoding='utf8'));compile(text,str(target),'exec');texts[target]=text
 assert 'wave476_results.json' in texts[A/NAMES[0]]
 assert '(193, 104, 51)' in texts[A/NAMES[-1]]
 assert "closed('StockRank10Embedding192_complete48_family_v1_20261011')" in texts[A/EXTRAS[6]]
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 for target,text in texts.items():target.write_text(text,encoding='utf8',newline='\n')
 opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(193,192,(476,))
 assert 'len(report["connected"])' in texts[A/NAMES[5]]
 aliases=[]
 for name in NAMES[2:4]:
  p=A/name;q=A/name.replace('_v1_20261011.py','.py');assert not q.exists();q.write_bytes(p.read_bytes());aliases.append(q)
 import_rows=[]
 for target,text in texts.items():
  for node in ast.walk(ast.parse(text)):
   if isinstance(node,ast.ImportFrom) and node.module and ('193' in node.module or 'rank10_rank20' in node.module):assert (A/(node.module+'.py')).is_file(),(target.name,node.module);import_rows.append({'source':target.name,'module':node.module})
   if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.endswith('.py') and '/' not in node.value and '\\' not in node.value and ('193' in node.value or 'rank10_rank20' in node.value):assert (A/node.value).is_file(),(target.name,node.value)
 for name in EXTRAS:
  if name not in EXTRAS[9:11]:assert (A/name).is_file(),name
 pins={str(p):sha(p) for p in [Path(__file__),*inputs,*texts,*aliases,*[A/n for n in EXTRAS if n not in EXTRAS[9:11]]]}
 for name in EXTRAS[9:11]:create(A/name,{'status':'compiled_complete51_rank10_rank20_higher49_actual_sources_before_future','input_sha256':pins,'expected_records':51,'expected_full_board':17852,'new_scores':0,'new_fits':0,'future_X_read':False})
 create(A/PROOF,{'status':'compiled_full193_complete51_QA104_17852_W476_new_rank10_rank20_higher_allocation_before_future','input_sha256':pins,'source_import_checks':import_rows,'expected_records':51,'expected_full_board':17852,'anchor_rounds':[175,192],'new_scores':0,'new_fits':0,'future_X_read':False,'test_labels_read':False})
 assert all(p.is_file() for p in source_paths())
 driver=A/EXTRAS[5];name='Rank10Rank20Higher193_complete51_family_v1_20261011';r=start_service(name,driver.name,[],{str(driver):sha(driver),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),r)
 print({'full193_complete51_queued':True,'QA':104,'board':17852,'new_scores':0},flush=True)
if __name__=='__main__':main()
