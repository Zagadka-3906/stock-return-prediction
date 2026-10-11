"""Prospective39: actual37 mature60/120 protected mixtures plus complete183/202 anchors."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
import prepare_Rank60Rank20Mixed199_complete51_pipeline_v1_20261011 as template
FACTORY=Path(__file__).stem
PROOF='rank120_rank60_protected203_full_execution_sources_admission_v1_20261011.json'
PARENT='StockRank60FractionEmbedding202_complete40_family_v2_20261011'
def changed(s):
 s=s.replace('recovery37_StockRank60Embedding198_complete48_family_v1_20261011','__ACTUAL203_PARENT__')
 for old,new in [('Rank60Rank20Mixed','Rank120Rank60Protected'),('rank60_rank20_mixed','rank120_rank60_protected'),('rank60_weight','rank120_weight'),('complete51','complete39'),('full51','full39'),('pilot51','pilot39'),('protected51','protected39'),('actual51','actual39'),('normalized51','normalized39'),('anchor51','anchor39'),('qa_v110','qa_v114'),('qa110','qa114'),('QA110','QA114')]:s=s.replace(old,new)
 s=re.sub(r'(?<!\d)(199|198|482|110|18114)(?!\d)',lambda m:{'199':'203','198':'202','482':'486','110':'114','18114':'18263'}[m.group()],s)
 s=re.sub(r'(?<![A-Za-z0-9_])(51|49|48|144)(?![A-Za-z0-9_])',lambda m:{'51':'39','49':'37','48':'36','144':'108'}[m.group()],s)
 s=s.replace('_v4_20261011','_v1_20261011').replace('__ACTUAL203_PARENT__',PARENT)
 s=s.replace('owned_idle_publication_wait_runtime_v1_20261010','owned_idle_publication_wait_reboot_identity_v2_20261011').replace('main_publisher_v11_20261010','main_publisher_reboot_v12_20261011')
 s=s.replace('maintain_best_fully_qualified_submission_delivery_v3_20261010','maintain_best_fully_qualified_submission_delivery_v4_20261011')
 return s
NAMES=[changed(n) for n in template.NAMES]
EXTRAS=[changed(n) for n in template.EXTRAS[:19]]+template.EXTRAS[19:]
EXTRAS[12]='predict_rank120_rank60_protected_complete_qualified183_scheme_v1_20261011.py'
EXTRAS[13]='rank120_rank60_protected_actual_twelve_parent_callbacks_CPU_controls_v1_20261011.json'
EXTRAS[14]='rank120_rank60_protected_after_qualified183_native_stage_v1_20261011.py'
EXTRAS[16]='rank120_rank60_protected37_early_sources_admission_v2_20261011.json'
EXTRAS[17:19]=template.EXTRAS[17:19]
EXTRAS += ['shared_live_ranking_report_runtime_v3_20261011.py','shared_live_report_scope203_tuple_controls_v1_20261011.json','maintain_best_fully_qualified_submission_delivery_v4_20261011.py']
def source_paths():return list(dict.fromkeys([Path(__file__),A/PROOF,*[A/n for n in NAMES+EXTRAS]]))
def save(p,t):assert not p.exists(),p;ast.parse(t);p.write_text(t,encoding='utf8');return p
def main():
 assert allowed()
 for p,d in read(A/template.PROOF)['input_sha256'].items():assert sha(p)==d,p
 aliases=dict(zip(template.NAMES+template.EXTRAS[:19],NAMES+EXTRAS[:19]));aliases[Path(template.__file__).name]=Path(__file__).name
 aliases.update({Path(k).stem:Path(v).stem for k,v in list(aliases.items()) if k.endswith('.py')})
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(aliases,key=len,reverse=True)));tokens={k:'__PROTECTED203_ALIAS_'+str(i)+'__' for i,k in enumerate(aliases)}
 inputs=[];outputs=[]
 for name in template.NAMES+template.EXTRAS[:9]:
  p=A/name;inputs.append(p);text=changed(pattern.sub(lambda m:tokens[m.group()],p.read_text(encoding='utf8')))
  for k,v in tokens.items():text=text.replace(v,aliases[k])
  text=text.replace('rank120_rank60_protected_raw_average','rank120_rank60_protected_raw_average')
  if name==template.EXTRAS[0]:text=text.replace("cfg['kind']=='CDF'","cfg['kind']=='valid_pool_protection_v1'")
  if name==template.EXTRAS[3]:
   text=text.replace("'stock_rank20long_embedding_small512_BF16_bank6_v1_20261010':'actual_StockRank20LongEmbeddingSmall512_full5_independent_location_v1_20261009.json'","'stock_rank120_embedding_small512_BF16_bank6_v1_20261011':'actual_StockRank120EmbeddingSmall512_full5_independent_location_v1_20261011.json'")
   text=text.replace('per-day CDF perturbation of whole qualified183 by independently matured Rank20/Rank5 raw average','per-day protected-tail permutation of whole qualified183 by independently matured60/120 raw average')
  if name==template.EXTRAS[6]:
   text=text.replace('from byte_exact_ranking_stream_runtime_v1_20261010 import installed as stream_writer','from byte_exact_ranking_stream_runtime_v1_20261010 import installed as original_stream_writer\n    from shared_live_ranking_report_runtime_v3_20261011 import installed as shared_reader\n    from contextlib import contextmanager\n    @contextmanager\n    def stream_writer():\n        control=read(A/"shared_live_report_scope203_tuple_controls_v1_20261011.json")\n        for p,d in control["input_sha256"].items():assert sha(p)==d,p\n        with original_stream_writer(),shared_reader(203,"'+Path(NAMES[5]).stem+'","'+Path(NAMES[6]).stem+'"):yield')
  outputs.append(save(A/aliases[name],text))
 plan={'status':'predeclared39_complete183202_anchors_plus_actual37_mature60_120_protected_mixtures','expected_records':39,'fully_qualified_anchors':[183,202],'actual_previous_complete_family':PARENT,'families':[{'name':'mixed60_120_after183_protected37','actual_service':'actual_rank120_rank60_after183_protected37_screen_v2_20261011','output':'E:/赛题五_本机临时/StockRank120Rank60_after183_protected37_screen_v1_20261011','main_receipt':'Actual_rank120_rank60_protected37_completed_TRAIN_records_main_receipt_v1_20261011.json','native_stage_module':Path(EXTRAS[14]).stem,'component_weight_field':'rank120_weight','component_weights':[.125,.5,.875],'banks':['stock_rank60_embedding_small512_BF16_bank6_v1_20261011','stock_rank120_embedding_small512_BF16_bank6_v1_20261011'],'label_horizons':[60,120],'training_windows':[252,252],'stage_kind':'rank120_rank60_protected_raw_average','signal_name':'Rank60_Rank120_Protected_ID16_Cross120_e64','member_names':['Rank60_ID16_Cross120_seed20261009_e64','Rank120_ID16_Cross120_seed20261009_e64']}],'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False}
 create(A/EXTRAS[11],plan)
 for i,name in [(2,'optimize_training_round203.py'),(3,'finalize_training_round203.py')]:outputs.append(save(A/name,'from '+Path(NAMES[i]).stem+' import *\n'))
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(203,202,(486,))
 normal=(A/EXTRAS[0]).read_text(encoding='utf8');assert 'for number in (183,202):' in normal and '(39,36,108)' in normal
 storage=importlib.import_module(Path(EXTRAS[2]).stem);assert len(storage.OUTPUTS)==6 and all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
 fixture=A/'verify_shared_live_report_exact15_tuple_scope_controls_v4_20261011.py';text=fixture.read_text(encoding='utf8').replace('共享榜对象精确15作用域控制_v4_20261011','共享榜对象203精确作用域_v1_20261011');namespace={'__name__':'prospective203_scope_fixture','__file__':str(fixture)};exec(compile(text,str(fixture),'exec'),namespace)
 row={'number':203,'codec_name':Path(NAMES[5]).stem,'verifier_name':Path(NAMES[6]).stem};result=namespace['run_variant'](row)
 create(A/'shared_live_report_scope203_tuple_controls_v1_20261011.json',{'status':'passed_actual203_private_readers_tuple_native_bytes_and_restoration_fixture','variant':row,'execution':result,'input_sha256':{str(p):sha(p) for p in [A/NAMES[5],A/NAMES[6],A/'shared_live_ranking_report_runtime_v3_20261011.py',Path(result['execution'])]},'actual_scientific_round_not_executed':True})
 pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/EXTRAS[11],A/EXTRAS[12],A/EXTRAS[13],A/EXTRAS[14],A/EXTRAS[16],*[A/n for n in EXTRAS[17:]]]}
 for name in [*EXTRAS[9:11],EXTRAS[15]]:create(A/name,{'status':'compiled_actual39_203_QA114_18263_W486_before_selected_native_or_future','input_sha256':pins,'expected_records':39,'actual_native14_checks_not_yet_performed':True,'new_fits':0,'new_scores':0,'actual_future_X_read':False})
 create(A/PROOF,{'status':'compiled_complete203_actual39_QA114_18263_W486_actual183202_and_mature60_120_sources_before_future','input_sha256':pins,'expected_records':39,'expected_board':18263,'new_fits':0,'new_scores':0,'actual_future_X_read':False,'test_labels_read':False})
 assert all(p.is_file() for p in source_paths())
 for name,driver in [('actual_rank120_rank60_protected39_after202_normalization_v1_20261011',EXTRAS[0]),('actual_rank120_rank60_protected39_selected_native14_v1_20261011',EXTRAS[1]),('Rank120Rank60Protected203_complete39_family_v1_20261011',EXTRAS[5])]:
  assert allowed();row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),row)
 print({'actual203_future_helpers_queued':3,'new_fits_or_scores':0,'complete_connected_registration_pending':True},flush=True)
if __name__=='__main__':main()
