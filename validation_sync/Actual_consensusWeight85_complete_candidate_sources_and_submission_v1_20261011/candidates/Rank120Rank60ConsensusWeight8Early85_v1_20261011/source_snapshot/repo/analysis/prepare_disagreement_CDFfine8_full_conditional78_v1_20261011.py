"""Freeze CDF native callbacks and full candidate helpers before any new Test inference."""
from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def renamed(s):
 for before,after in [('disagreement10_early73','disagreement_CDFfine8_early78'),('Disagreement10Early73','DisagreementCdfFine8Early78'),('60与120日分歧10项完整候选73','60与120日分歧CDF细调8项完整候选78'),('disagreement_after_qualified183_native_stage73','disagreement_CDFfine_after_qualified183_native_stage78'),('disagreement_complete_qualified183_scheme73','disagreement_CDFfine_complete_qualified183_scheme78'),('disagreement_after_complete_qualified_parent73','disagreement_CDFfine_after_complete_qualified_parent78'),('stock_rank120_rank60_disagreement_label_horizon_ID16_cross120_recent252_e64','stock_rank120_rank60_disagreement_CDFfine_label_horizon_ID16_cross120_recent252_e64'),('rank120_rank60_disagreement_raw_fusion','rank120_rank60_disagreement_CDFfine_fusion'),('pilot10.json','pilot8.json'),('passed_normalized10_actual','passed_normalized8_actual'),('selected_by_all10','selected_by_all8'),('actual_all10_official_controls','actual_all8_official_controls'),('len(pilot[\'records\'])==10','len(pilot[\'records\'])==8'),("len(proof['records'])==proof['new_quality_score_records']==10","len(proof['records'])==proof['new_quality_score_records']==8"),('(9,27)','(7,21)'),("'expected_scored_records':10","'expected_scored_records':8"),('expected_scored_records=10','expected_scored_records=8'),("'scored_records':10","'scored_records':8"),("'actual_nonidentity_full_controls':9","'actual_nonidentity_full_controls':7"),("'actual_nonidentity_prefix_controls':27","'actual_nonidentity_prefix_controls':21")]:s=s.replace(before,after)
 return s
def main():
 assert allowed()
 names=['normalize_rank120_rank60_disagreement10_early73_v1_20261011.py','qualify_rank120_rank60_disagreement10_early73_selected_native14_v2_20261011.py','prepare_Rank120Rank60Disagreement10Early73_selected_candidate_v2_20261011.py','run_Rank120Rank60Disagreement10Early73_selected_candidate_feature_cache_v2_20261011.py','seal_Rank120Rank60Disagreement10Early73_selected_candidate_v2_20261011.py','rank120_rank60_disagreement10_early73_storage_v1_20261011.py','rank120_rank60_disagreement_after_qualified183_native_stage73_v1_20261011.py','predict_rank120_rank60_disagreement_complete_qualified183_scheme73_v1_20261011.py']
 outputs=[]
 for name in names:
  s=renamed((A/name).read_text(encoding='utf8'))
  if name.startswith('normalize_'):
   s=s.replace('actual_completed_disagreement10_pointer_namespace_bridge72_v1_20261011','actual_rank120_rank60_after183_disagreement_CDFfine8_screen77_v1_20261011').replace('StockRank120Rank60_after183_disagreement10_screen_v1_20261011','StockRank120Rank60_after183_disagreement_CDFfine8_screen77_v1_20261011')
  if name.startswith('rank120_rank60_disagreement_after_qualified183_native_stage73'):
   s=s.replace('import protected_upper_tail_rank_permutation_v1_20261010 as codec','import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec')
   s=s.replace("spec['codec']=='valid_pool_protection_v1' and .1<=spec['protect_fraction']<=.5","spec['codec']=='CDF' and spec['protect_fraction'] is None and spec['role']=='nonflag_valid'")
   s=s.replace("args=(context.dates,context.flags,context.valid,spec['weight'],spec['protect_fraction'],spec['sign'])","args=(context.dates,context.flags,context.valid,spec['role'],spec['weight'],spec['sign'])")
   s=s.replace("codec.assert_invariants(parent,value,context.dates,context.flags,context.valid,spec['protect_fraction'])","mask=codec.selected(context.flags,context.valid,spec['role']);assert np.array_equal(value[~mask].view('u8'),np.asarray(parent)[~mask].view('u8'))")
   s=s.replace("'codec':'valid_pool_protection_v1'","'codec':'CDF'")
  if name.startswith('normalize_'):
   # The shared reference case uses the original protected codec. Preserve that exact reference honestly;
   # only a CDF record exceeding all completed/raw incumbents can enter the new inference pipeline.
   s=s.replace("stage_kind='anchor' if identity else 'rank120_rank60_disagreement_CDFfine_fusion'","stage_kind='anchor' if identity else 'rank120_rank60_disagreement_CDFfine_fusion'")
  q=A/renamed(name);ast.parse(s);assert not q.exists();q.write_text(s,encoding='utf8');outputs.append(q)
 # Reference38 must never be dispatched through the CDF-specific stage.
 prep=next(p for p in outputs if p.name.startswith('prepare_'));s=prep.read_text(encoding='utf8');needle="    assert parent_number == 183 and 0.<cfg['weight']<=1. and cfg['sign'] in (-1.,1.)"
 assert needle in s;s=s.replace(needle,needle+"\n    assert cfg['codec']=='CDF' and cfg['role']=='nonflag_valid'");prep.write_text(s,encoding='utf8')
 oldpub=A/'publish_actual_disagreement73_complete_candidate_main_v1_20261011.py';olddelivery=A/'prepare_verified_disagreement73_alternate_submission_delivery_v1_20261011.py'
 extra=[]
 for original in (oldpub,olddelivery):
  s=renamed(original.read_text(encoding='utf8')).replace('disagreement73_complete_candidate','disagreement_CDFfine78_complete_candidate').replace('alternate_verified_disagreement73','alternate_verified_disagreement_CDFfine78').replace('verified_disagreement73_alternate','verified_disagreement_CDFfine78_alternate').replace('已核验候选_60与120日分歧10项73','已核验候选_60与120日分歧CDF细调8项78').replace("pilot['expected_scored_records']==len(pilot['records'])==10","pilot['expected_scored_records']==len(pilot['records'])==8").replace('10项TRAIN官方评分','8项TRAIN官方评分').replace('actual10_record_selected','actual8_record_selected')
  q=A/renamed(original.name).replace('disagreement73_complete_candidate','disagreement_CDFfine78_complete_candidate').replace('verified_disagreement73_alternate','verified_disagreement_CDFfine78_alternate');ast.parse(s);assert not q.exists();q.write_text(s,encoding='utf8');extra.append(q)
 protocol=A/'rank120_rank60_disagreement_CDFfine8_early78_sources_admission_v2_20261011.json'
 create(protocol,{'status':'frozen_conditional_CDF_only_actual_S_gain_vs_all8_CDF_and_all10_protected_records_then14_native14_cold7_prefit_full37_native_independent_reload_CSV_cold80_main_E_delivery_required','input_sha256':{str(p):sha(p) for p in [Path(__file__),*[A/n for n in names],*outputs,oldpub,olddelivery,*extra,A/'rank120_rank60_disagreement_CDFfine8_predeclared_sources77_v1_20261011.json']},'new_scores_or_Test_inference_not_yet_claimed':True})
 # The runner supplies the actual selection, publication and conditional full inference sequentially.
 runner=A/'run_disagreement_CDFfine8_results_selection_main_and_conditional78_v1_20261011.py';assert runner.is_file()
 assert allowed();r=start_service('actual_disagreement_CDFfine8_results_selection_main77_v1_20261011',runner.name,[],{str(runner):sha(runner),str(protocol):sha(protocol)});create(A/'actual_disagreement_CDFfine8_results_selection_main77_activation_v1_20261011.json',r)
 print({'conditional_CDF8_full_native_helpers':len(outputs),'future_inference_only_after_actual_S_gain':True},flush=True)
if __name__=='__main__':main()
