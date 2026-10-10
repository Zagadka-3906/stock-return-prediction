"""Register38 independently controlled refinements plus actual183/201 anchors, preserving every gate."""
from pathlib import Path
import sys,re,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
import prepare_StockRank60Direct200_complete35_pipeline_v6_20261011 as template
FACTORY=Path(__file__).stem
PROOF='stock_rank60window504_direct206_complete35_sources_admission_v2_20261011.json'
PARENT='Rank60TwoSeedProtected205_complete39_family_v2_20261011'
def changed(s):
 s=s.replace('Rank60Rank20Mixed199_complete51_family_v4_20261011','__ACTUAL206_PARENT__')
 for old,new in [('StockRank60Direct','StockRank60Window504Direct'),('stock_rank60_direct','stock_rank60window504_direct'),('StockRank60Embedding','StockRank60Window504Embedding'),('stock_rank60_embedding','stock_rank60window504_embedding'),('seed09_e64','seed09_e64'),('qa_v111','qa_v117'),('qa111','qa117'),('QA111','QA117')]:s=s.replace(old,new)
 s=re.sub(r'(?<!\d)(200|199|483|111|18149)(?!\d)',lambda m:{'200':'206','199':'205','483':'489','111':'117','18149':'18372'}[m.group()],s)
 s=s.replace('_v6_20261011','_v1_20261011').replace('__ACTUAL206_PARENT__',PARENT)
 s=s.replace("CONFIG['seed']==20261009","CONFIG['seed']==20261009")
 s=s.replace('recent252','recent504').replace('Recent252','Recent504')
 s=s.replace('owned_idle_publication_wait_runtime_v1_20261010','owned_idle_publication_wait_reboot_identity_v2_20261011').replace('main_publisher_v11_20261010','main_publisher_reboot_v12_20261011')
 s=s.replace('publish_explicit_parent_training_round_v2_20261005','publish_explicit_parent_training_round_external_frozen_v3_20261011')
 s=s.replace('stock_rank60window504_direct_embedding_complete_parent_native_replay_verification.json','stock_rank60window504_embedding_complete_parent_native_replay_verification.json')
 s=s.replace('passed_actual_complete_qualified_parent_stock_rank60window504_direct_embedding_two_full_native_independent_replays_and_cold80','passed_actual_complete_qualified_parent_stock_rank60window504_embedding_two_full_native_independent_replays_and_cold80')
 return s

NAMES=[changed(n) for n in template.NAMES]
EXTRAS=[changed(n) for n in template.EXTRAS[:19]]+template.EXTRAS[19:]
EXTRAS[13]='stock_rank60window504_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json'
EXTRAS[17]=template.EXTRAS[17]
EXTRAS[22]='stock_rank60window504_own6_full5_native42_direct33_predeclared_sources_v1_20261011.json'
EXTRAS += ['stock_rank60window504_own6_full5_native42_direct33_predeclared_sources_v1_20261011.json','shared_live_ranking_report_runtime_v3_20261011.py','shared_live_report_scope206_tuple_controls_v1_20261011.json','maintain_best_fully_qualified_submission_delivery_v4_20261011.py']
def source_paths():return list(dict.fromkeys([Path(__file__),A/PROOF,*[A/n for n in NAMES+EXTRAS]]))
def save(p,text):
 assert not p.exists(),p;ast.parse(text);p.write_text(text,encoding='utf8');return p
def main():
 assert allowed()
 for p,d in read(A/template.PROOF)['input_sha256'].items():assert sha(p)==d,p
 aliases=dict(zip(template.NAMES+template.EXTRAS[:12],NAMES+EXTRAS[:12]))
 aliases[template.EXTRAS[18]]=EXTRAS[18]
 aliases['prepare_StockRank60Direct200_complete35_pipeline_v6_20261011.py']=FACTORY+'.py'
 aliases.update({Path(k).stem:Path(v).stem for k,v in list(aliases.items()) if k.endswith('.py')})
 pattern=re.compile('|'.join(re.escape(k) for k in sorted(aliases,key=len,reverse=True)))
 tokens={k:'__FRACTION202_ALIAS_'+str(i)+'__' for i,k in enumerate(aliases)};inputs=[];outputs=[]
 for name in template.NAMES+template.EXTRAS[:9]:
  p=A/name;inputs.append(p);text=changed(pattern.sub(lambda m:tokens[m.group()],p.read_text(encoding='utf8')))
  for k,v in tokens.items():text=text.replace(v,aliases[k])
  text=text.replace('actual_stock_rank60_mature_objective_own6_full5_queue_v1_20261011','actual_stock_rank60window504_embedding_small512_bank6_v1_20261011')
  if name==template.EXTRAS[5]:text=text.replace('maintain_best_fully_qualified_submission_delivery_v3_20261010','maintain_best_fully_qualified_submission_delivery_v4_20261011')
  if name==template.EXTRAS[6]:
   text=text.replace('    from types import SimpleNamespace','    from types import SimpleNamespace\n    import importlib\n    sys.modules["optimize_training_round206"]=importlib.import_module("'+Path(NAMES[2]).stem+'")\n    sys.modules["finalize_training_round206"]=importlib.import_module("'+Path(NAMES[3]).stem+'")')
   text=text.replace('from byte_exact_ranking_stream_runtime_v1_20261010 import installed as stream_writer','from byte_exact_ranking_stream_runtime_v1_20261010 import installed as original_stream_writer\n    from shared_live_ranking_report_runtime_v3_20261011 import installed as shared_reader\n    from contextlib import contextmanager\n    @contextmanager\n    def stream_writer():\n        control=read(A/"shared_live_report_scope206_tuple_controls_v1_20261011.json")\n        for p,d in control["input_sha256"].items():assert sha(p)==d,p\n        with original_stream_writer(),shared_reader(206,"'+Path(NAMES[5]).stem+'","'+Path(NAMES[6]).stem+'"):yield')
  text=text.replace('stock_rank60_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json','stock_rank60window504_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json')
  outputs.append(save(A/aliases[name],text))
 plan=read(A/template.EXTRAS[11]);plan.update(status='predeclared35_actual33_window504_records_and_complete183203_anchors',expected_records=35,fully_qualified_anchors=[183,205],families=[{'name':'StockRank60Window504EmbeddingSmall512_after183_direct_allocation33','actual_service':'actual_stock_rank60window504_embedding_after183_direct_allocation33_v1_20261011','records':33,'base_round':183,'stage_kind':'stock_rank60window504_embedding_rank60mean_direct','main_receipt':'Actual_rank60_window504_pure33_completed_TRAIN_records_main_receipt_v1_20261011.json'}])
 create(A/EXTRAS[11],plan)
 for i,canonical in [(2,'optimize_training_round206.py'),(3,'finalize_training_round206.py')]:outputs.append(save(A/canonical,'from '+Path(NAMES[i]).stem+' import *\n'))
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 opt=literal_assignments(A/NAMES[2]);assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(206,205,(489,))
 normal=(A/EXTRAS[0]).read_text(encoding='utf8');assert 'for number in (183,205):' in normal and '(35,32,96)' in normal
 stage=importlib.import_module(Path(EXTRAS[14]).stem);normalizer=importlib.import_module(Path(EXTRAS[0]).stem);assert set(stage.BACKENDS)==set(normalizer.RECIPES)
 storage=importlib.import_module(Path(EXTRAS[2]).stem);assert len(storage.OUTPUTS)==6 and all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
 fixture_source=A/'verify_shared_live_report_exact15_tuple_scope_controls_v4_20261011.py'
 fixture_text=fixture_source.read_text(encoding='utf8').replace('共享榜对象精确15作用域控制_v4_20261011','共享榜对象206精确作用域_v1_20261011')
 fixture_namespace={'__name__':'prospective202_scoped_control_recovery','__file__':str(fixture_source)}
 exec(compile(fixture_text,str(fixture_source),'exec'),fixture_namespace);run_variant=fixture_namespace['run_variant']
 row={'number':206,'codec_name':Path(NAMES[5]).stem,'verifier_name':Path(NAMES[6]).stem};scope=run_variant(row)
 scopepins={str(p):sha(p) for p in [A/NAMES[5],A/NAMES[6],A/'shared_live_ranking_report_runtime_v3_20261011.py',Path(scope['execution'])]}
 create(A/'shared_live_report_scope206_tuple_controls_v1_20261011.json',{'status':'passed_actual202_private_readers_tuple_native_bytes_and_restoration_fixture','variant':row,'execution':scope,'input_sha256':scopepins,'actual_scientific_round_not_executed':True})
 pins={str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/EXTRAS[11],*[A/n for n in EXTRAS[12:18]],*[A/n for n in EXTRAS[19:]]]}
 for name in (EXTRAS[9],EXTRAS[10],EXTRAS[18]):create(A/name,{'status':'compiled202_actual40_QA113_18224_W485_before_selected_native_or_future','input_sha256':pins,'expected_records':35,'actual_future_X_read':False,'new_fits':0,'new_scores':0})
 create(A/PROOF,{'status':'compiled202_actual38_plus183201_actual_complete_anchors_all_original_scientific_candidate_QA_main_gates_retained','input_sha256':pins,'expected_records':35,'expected_board':18372,'new_fits':0,'new_scores':0,'test_labels_read':False})
 assert all(p.is_file() for p in source_paths())
 jobs=[('actual_stock_rank60window504_direct_embedding35_after205_normalization_queue_v1_20261011',EXTRAS[0]),('StockRank60Window504DirectEmbedding35_selected_native14_v1_20261011',EXTRAS[1]),('StockRank60Window504DirectEmbedding206_complete35_family_v1_20261011',EXTRAS[5])]
 for name,driver in jobs:
  assert allowed();row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(A/PROOF):sha(A/PROOF)});create(A/(name+'_activation.json'),row)
 print({'actual202_future_helpers_queued':3,'new_fits_or_scores':0,'future_qualification_pending':True},flush=True)
if __name__=='__main__':main()
