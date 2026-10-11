from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 import prepare_Rank10Rank20Higher193_complete51_pipeline_v4_20261011 as factory
 from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
 opt=literal_assignments(A/factory.NAMES[2]);assert(opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(193,192,(476,))
 assert '(193, 104, 51)' in (A/factory.NAMES[-1]).read_text(encoding='utf8')
 records=[]
 for name in factory.NAMES+factory.EXTRAS:
  p=A/name;assert p.exists(),p
  if p.suffix!='.py':continue
  text=p.read_text(encoding='utf8');tree=ast.parse(text);compile(text,str(p),'exec')
  if '193' in name:
   for bad in ('pilot27.json','normalized27','anchor27','actual27_selected','80*4660'):assert bad not in text,(name,bad)
  for node in ast.walk(tree):
   if isinstance(node,ast.ImportFrom) and node.module and ('193' in node.module or 'rank10_rank20' in node.module):assert (A/(node.module+'.py')).exists(),(name,node.module)
   if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.endswith('.py') and '/' not in node.value and '\\' not in node.value and ('193' in node.value or 'rank10_rank20' in node.value):assert (A/node.value).exists(),(name,node.value)
  records.append({'source':name,'sha256':sha(p),'compiled_direct_import_and_literal_dependency_controls':True})
 candidate=(A/factory.EXTRAS[3]).read_text(encoding='utf8')
 assert '(1599600,344,4650)' in candidate and 'cfg["anchor_round"]' not in ''
 assert 'stock_rank10_embedding_small512_BF16_bank6_v1_20261011' in candidate and 'actual_StockRank10EmbeddingSmall512_full5_independent_location_v1_20261011.json' in candidate
 assert "mix_field='rank10_weight'" in candidate and "cfg['stage_kind']=='rank10_rank20_mixed_raw_average'" in candidate
 assert 'stock_rank5_embedding_small512_BF16_bank6_v1_20261010' not in candidate
 seal=(A/factory.EXTRAS[4]).read_text(encoding='utf8');assert 'closed(service.name)' in seal and 'pilot51.json' in seal
 registry=(A/factory.NAMES[0]).read_text(encoding='utf8');assert 'pilot51.json' in registry and 'passed_normalized51_actual_TRAIN' in registry
 plan=read(A/'rank10_rank20_higher_complete51_after192_plan_v1_20261011.json');assert plan['fully_qualified_anchors']==[175,192] and plan['families'][0]['label_horizons']==[20,10]
 create(A/'rank10_rank20_higher193_corrected_materialized_source_controls_v4_20261011.json',{'status':'passed_actual_corrected193_51_QA104_17852_W476_guards_new_own10_bank_pointers_and_frozen_recipe','records':records,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(factory.__file__),A/factory.PROOF,A/'rank10_rank20_mixed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json']},'new_fits':0,'new_scores':0,'future_X_read':False,'test_labels_read':False,'original_unadmitted_drafts_preserved':True})
 print({'actual193_v4_materialized_source_checks':len(records)},flush=True)
if __name__=='__main__':main()
