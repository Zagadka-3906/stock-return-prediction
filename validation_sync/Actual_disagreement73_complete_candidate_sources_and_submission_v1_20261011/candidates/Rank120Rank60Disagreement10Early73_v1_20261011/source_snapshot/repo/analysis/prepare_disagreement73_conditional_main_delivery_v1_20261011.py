"""Prepare main publication and actual qualified delivery; no score/candidate claims before execution."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,read,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed()
 originals=['publish_actual_protected60_120_best_blend38_complete_candidate_main_v1_20261011.py','prepare_verified_best_blend38_alternate_submission_delivery_v1_20261011.py']
 def renamed(s):
  for before,after in [('Rank120Rank60BestBlend38Early','Rank120Rank60Disagreement10Early73'),('protected60_120_best_blend38_complete_candidate','disagreement73_complete_candidate'),('rank120_rank60_best_blend_fraction38_early','rank120_rank60_disagreement10_early73'),('pilot38.json','pilot10.json'),('alternate_verified_best_blend38','alternate_verified_disagreement73'),('已核验候选_60与120日最佳组合38项','已核验候选_60与120日分歧10项73'),('actual38_record_selected','actual10_record_selected'),("pilot['expected_scored_records']==len(pilot['records'])==38","pilot['expected_scored_records']==len(pilot['records'])==10"),('(37,111)','(9,27)'),('38项TRAIN官方评分','10项TRAIN官方评分')]:s=s.replace(before,after)
  return s.replace('verified_best_blend38_alternate','verified_disagreement73_alternate')
 outputs=[]
 for name in originals:
  s=renamed((A/name).read_text(encoding='utf8'));q=A/renamed(name);ast.parse(s);assert q!=A/name
  if q.exists():assert q.read_text(encoding='utf8')==s
  else:q.write_text(s,encoding='utf8')
  outputs.append(q)
 # Source-only publication is independent of whether the frozen hypotheses ultimately gain.
 original=A/'publish_actual_disagreement10_score_priority72_observer148_sources_main_v1_20261011.py'
 s=original.read_text(encoding='utf8').replace('actual_disagreement10_score_priority72_observer148_sources','actual_disagreement73_full_native_pipeline_sources').replace('冻结10项跨时长预测分歧评分优先队列与实际监控148；保留正在运行191和原48项任务，提分后完整候选核验仍必要','冻结跨时长分歧10项提分后完整候选流程73及实际CPU回调12和Windows存储API核验；当前评分和候选仍待完成')
 paths=[Path(__file__),*outputs,A/'prepare_disagreement10_conditional_full_pipeline73_v1_20261011.py',A/'actual_disagreement10_conditional_full_pipeline73_source_preparation_v1_20261011.json',A/'rank120_rank60_disagreement10_early73_sources_admission_v2_20261011.json',A/'launch_disagreement10_conditional_full_pipeline73_v1_20261011.py',A/'verify_disagreement73_actual_callback_and_storage_CPU_v1_20261011.py',A/'actual_disagreement73_callback12_storage_and_recipe_CPU_controls_v1_20261011.json']
 paths += [Path(p) for p in read(A/'rank120_rank60_disagreement10_early73_sources_admission_v2_20261011.json')['input_sha256'] if 'early73' in Path(p).name or 'scheme73' in Path(p).name or 'stage73' in Path(p).name]
 tree=ast.parse(s);node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
 lines=s.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'];s=''.join(lines)
 sourcepub=A/'publish_actual_disagreement73_full_native_pipeline_sources_main_v1_20261011.py';ast.parse(s);assert not sourcepub.exists();sourcepub.write_text(s,encoding='utf8')
 launcher=A/'launch_disagreement73_conditional_main_delivery_v1_20261011.py'
 code='''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();closed('actual_rank120_rank60_disagreement10_S_only_gain_decision_v2_20261011')
 decision=read(A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json')
 if not decision['adopt']:
  create(A/'actual_disagreement73_main_delivery_not_needed_v1_20261011.json',{'status':'passed_actual_no_S_gain_no_new_delivery_claimed','decision_sha256':sha(A/'rank120_rank60_disagreement10_gain_decision_v1_20261011.json')});return
 closed('actual_disagreement10_conditional_full_pipeline73_v1_20261011')
 for name,driver in [('actual_disagreement73_complete_candidate_main_v1_20261011','publish_actual_disagreement73_complete_candidate_main_v1_20261011.py'),('actual_verified_disagreement73_alternate_submission_delivery_v1_20261011','prepare_verified_disagreement73_alternate_submission_delivery_v1_20261011.py')]:
  assert allowed();p=A/driver;r=start_service(name,driver,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r);closed(name)
 actual=read(A/'alternate_verified_disagreement73_submission_delivery_v1_20261011.json')
 assert actual['all_full_native_independent_reload_csv_and_cold80_checks_passed'] and actual['official_TRAIN_internal_score']==decision['best']['connected_final_score']
 create(A/'rank120_rank60_disagreement10_selected_full_candidate_complete_v1_20261011.json',actual)
if __name__=='__main__':main()
'''
 ast.parse(code);assert not launcher.exists();launcher.write_text(code,encoding='utf8')
 proof=A/'actual_disagreement73_conditional_main_delivery_sources_admission_v1_20261011.json'
 create(proof,{'status':'frozen_conditional_actual_full_candidate_then_main_then_delivery_only_if_actual_TRAIN_S_gain','input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in originals],*outputs,launcher,sourcepub]},'new_scores_or_Test_inference_not_claimed':True})
 for name,p in [('actual_disagreement73_full_native_pipeline_sources_main_v1_20261011',sourcepub),('actual_disagreement73_conditional_main_delivery_v1_20261011',launcher)]:
  assert allowed();r=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),r)
 print({'conditional_delivery_and_sources_prepared':True,'actual_new_scoring_and_native_candidate_still_pending':True},flush=True)
if __name__=='__main__':main()
