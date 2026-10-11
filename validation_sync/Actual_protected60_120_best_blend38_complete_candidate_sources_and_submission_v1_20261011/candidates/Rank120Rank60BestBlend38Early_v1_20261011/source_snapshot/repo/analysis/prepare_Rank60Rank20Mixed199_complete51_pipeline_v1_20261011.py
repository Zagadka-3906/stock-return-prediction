"""Freeze 183/198 anchors plus49 genuinely new TRAIN comparisons, then qualify and register."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
import prepare_Rank10Rank20Higher193_complete51_pipeline_v4_20261011 as template
FACTORY=Path(__file__).stem
PROOF='rank60_rank20_mixed199_full_execution_sources_admission_v1_20261011.json'

def renamed(s):
 for old,new in [('Rank10Rank20Higher','Rank60Rank20Mixed'),('rank10_rank20_higher','rank60_rank20_mixed'),('RANK10_RANK20','RANK60_RANK20'),('Rank10Rank20','Rank60Rank20'),('rank10_rank20','rank60_rank20'),('StockRank10','StockRank60'),('stock_rank10','stock_rank60'),('rank10_weight','rank60_weight'),('y_rank_10mean','y_rank_60mean'),('qa_v104','qa_v110'),('qa104','qa110'),('QA104','QA110'),('17852','18114')]:s=s.replace(old,new)
 s=re.sub(r'(?<!\d)(193|192|476|104|175)(?!\d)',lambda m:{'193':'199','192':'198','476':'482','104':'110','175':'183'}[m.group()],s)
 return s.replace('(.25,.5,.75)','(.125,.5,.875)').replace('(20,10)','(20,60)')

NAMES=[renamed(n) for n in template.NAMES]
EXTRAS=[renamed(n) for n in template.EXTRAS[:19]]
EXTRAS[0]='normalize_completed_rank60_rank20_mixed51_after198_v1_20261011.py'
EXTRAS[1]='qualify_rank60_rank20_mixed51_selected_native14_v1_20261011.py'
EXTRAS[11]='rank60_rank20_mixed_complete51_after198_plan_v1_20261011.json'
EXTRAS[12]='predict_rank60_rank20_mixed_complete_qualified183_scheme_v1_20261011.py'
EXTRAS[13]='rank60_rank20_mixed_actual_twelve_parent_callbacks_CPU_controls_v1_20261011.json'
EXTRAS[14]='rank60_rank20_mixed_after_qualified183_native_stage_v1_20261011.py'
EXTRAS[15]='rank60_rank20_mixed51_normalization_native14_sources_admission_v1_20261011.json'
EXTRAS[16]='rank60_rank20_mixed49_native14_predictor_sources_admission_v1_20261011.json'
EXTRAS += ['exact_verified_feature120_memoization_runtime_v1_20261010.py','actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json','verified_shared_publication_board_loader_v1_20261011.py','late_bound_shared_snapshot_encoder_runtime_v1_20261011.py','verified_shared_publication_board_loader_actual_complete180_controls_v1_20261011.json','actual_latest183_parent196198_routes37_v1_20261011.json','rank60_rank20_after183_mixed49_predeclared_sources_admission_v1_20261011.json']

def source_paths():return list(dict.fromkeys([Path(__file__),A/PROOF,*[A/n for n in NAMES+EXTRAS]]))

def save(p,s):
 assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n');return p

def main():
 assert allowed();data=read(A/'unified_completed_parent_shared_publication36_routes_v1_20261011.json')
 mapping={old:new for old,new in zip(template.NAMES+template.EXTRAS[:19],NAMES+EXTRAS[:19])}
 mapping[Path(template.__file__).name]=Path(__file__).name
 mapping['prepare_Rank10Rank20Higher193_complete51_pipeline_v1_20261011.py']=Path(__file__).name
 mapping.update({Path(k).stem:Path(v).stem for k,v in list(mapping.items()) if k.endswith('.py')})
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
 paths=[Path(__file__),A/'rank60_rank20_after183_mixed49_predeclared_sources_admission_v1_20261011.json',A/EXTRAS[13]];outputs=[]
 # All renamed source references use the unique actual factory version.
 catalog={re.sub(r'_v\d+_202\d{5}$','',Path(n).stem):Path(n).stem for n in NAMES+EXTRAS if n.endswith('.py')}
 def actual_tokens(s):
  def replace(m):
   token=m.group();suffix='.py' if token.endswith('.py') else '';stem=token[:-3] if suffix else token
   base=re.sub(r'_v\d+_202\d{5}$','',stem)
   if base in catalog:return catalog[base]+suffix
   return token
  return re.sub(r'[A-Za-z0-9_]+_v\d+_202\d{5}(?:\.py)?',replace,s)
 inputs=template.NAMES+template.EXTRAS[:9]
 for old in inputs:
  source=A/data['actual_source_overrides'].get(old,old);paths.append(source)
  s=renamed(pattern.sub(lambda m:mapping[m.group()],source.read_text(encoding='utf8')))
  s=actual_tokens(s)
  s=s.replace('rank60_rank20_mixed_after_qualified_parent_native_stage_v1_20261011','rank60_rank20_mixed_after_qualified183_native_stage_v1_20261011').replace('predict_rank60_rank20_mixed_complete_qualified_parent_scheme_v1_20261011','predict_rank60_rank20_mixed_complete_qualified183_scheme_v1_20261011')
  s=s.replace('rank60_rank20_mixed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json',EXTRAS[13]).replace('three_cached_mixed_actual_eleven_parent_callbacks_CPU_controls_v2_20261011.json',EXTRAS[13])
  s=s.replace('rank60_rank20_mixed49_actual_native14_and_predictor_sources_admission_v1_20261011.json',EXTRAS[16])
  s=s.replace('StockRank60Embedding198_complete48_family_v1_20261011','recovery37_StockRank60Embedding198_complete48_family_v1_20261011')
  s=s.replace('Rank60Rank20Mixed199_complete51_family_v1_20261011','Rank60Rank20Mixed199_complete51_family_v4_20261011')
  s=s.replace('from owned_idle_publication_wait_runtime_v1_20261010 import hold','from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold').replace('from publish_explicit_parent_training_round_v2_20261005 import publish','from publish_explicit_parent_training_round_external_frozen_v3_20261011 import publish')
  if old==template.EXTRAS[4]:
   s=re.sub(r"service=A/'service_owned_workflows_20261006/[^']+'",lambda m:"service=A/'service_owned_workflows_20261006/Rank60Rank20Mixed199_selected_candidate_preparation_v1_20261010'",s)
  if old==template.EXTRAS[6]:assert 'late_bound_shared_snapshot_encoder_runtime_v1_20261011' in s
  outputs.append(save(A/mapping[old],s))
 plan={'status':'predeclared51_complete183198_anchors_plus49_mature20_60_mix_after183_before_new_scores','expected_records':51,'fully_qualified_anchors':[183,198],'actual_previous_complete_family':'recovery37_StockRank60Embedding198_complete48_family_v1_20261011','families':[{'name':'mixed20_60_after183_49','actual_service':'actual_rank60_rank20_after183_mixed49_screen_v1_20261011','output':'E:/赛题五_本机临时/StockRank60Rank20_after183_higher_allocation49_screen_v1_20261011','main_receipt':'Rank60Rank20_after183_completed49_sources_main_receipt_v1_20261011.json','native_stage_module':Path(EXTRAS[14]).stem,'component_weight_field':'rank60_weight','component_weights':[.125,.5,.875],'banks':['stock_rank20_embedding_small512_BF16_bank6_v1_20261010','stock_rank60_embedding_small512_BF16_bank6_v1_20261011'],'label_horizons':[20,60],'training_windows':[252,252],'stage_kind':'rank60_rank20_mixed_raw_average','signal_name':'Rank20_Rank60_Mixed_ID16_Cross120_e64','member_names':['Rank20_ID16_Cross120_seed20261009_e64','Rank60_ID16_Cross120_seed20261009_e64']}],'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False}
 create(A/EXTRAS[11],plan)
 # Ensure all source aliases and explicit parent metadata match the predeclared plan.
 for p in outputs:
  for node in ast.walk(ast.parse(p.read_text(encoding='utf8'))):
   if isinstance(node,ast.ImportFrom) and node.module and ('Rank60Rank20' in node.module or 'rank60_rank20' in node.module):assert (A/(node.module+'.py')).is_file(),(p.name,node.module)
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(199,198,(482,))
 normal=(A/EXTRAS[0]).read_text(encoding='utf8');assert 'for number in (183,198):' in normal and "anchor_round=183" in normal
 candidate=(A/EXTRAS[3]).read_text(encoding='utf8');assert 'parent_number in (183,198)' in candidate and 'stock_rank60_embedding_small512_BF16_bank6_v1_20261011' in candidate
 assert '(199, 110, 51)' in (A/NAMES[-1]).read_text(encoding='utf8')
 storage=importlib.import_module(Path(EXTRAS[2]).stem);assert len(storage.OUTPUTS)==6 and all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
 pins={str(p):sha(p) for p in [*paths,*outputs,A/EXTRAS[11],A/EXTRAS[12],A/EXTRAS[14]]}
 for n in [*EXTRAS[9:11],EXTRAS[15],EXTRAS[16]]:create(A/n,{'status':'compiled_complete51_exact199_QA110_18114_W482_before_selected_native_or_future','input_sha256':pins,'expected_records':51,'actual_native14_checks_not_yet_performed':True,'new_fits':0,'new_scores':0,'actual_future_X_read':False})
 create(A/PROOF,{'status':'compiled_complete199_51_QA110_18114_W482_true183198_and_mature20_60_sources_before_future','input_sha256':pins,'expected_records':51,'expected_board':18114,'new_fits':0,'new_scores':0,'actual_future_X_read':False,'test_labels_read':False})
 assert all(p.is_file() for p in source_paths())
 for name,driver in [('actual_rank60_rank20_mixed51_after198_normalization_v1_20261011',EXTRAS[0]),('actual_rank60_rank20_mixed51_selected_native14_v1_20261011',EXTRAS[1]),('Rank60Rank20Mixed199_complete51_family_v4_20261011',EXTRAS[5])]:
  p=save(A/(Path(driver).stem+'_current37_wrapper.py'),"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_actual_latest183_parent196198_v37_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n")
  assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),r)
 print({'complete199_sources_frozen_queued':True,'new_fits_or_scores':0,'submission_qualification_pending':True},flush=True)
if __name__=='__main__':main()
