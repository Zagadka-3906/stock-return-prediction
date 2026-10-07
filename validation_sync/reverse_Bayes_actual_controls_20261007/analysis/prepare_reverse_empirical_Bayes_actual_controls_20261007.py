"""Prepare explicitly signed native3/full37 controls; no official scoring or automatic tomorrow dispatch."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def save(old,new,text):
    path=A/new;assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return [A/old,path]

def main():
    sources=[Path(__file__)];bank=A/'nonflag_residual_EmpiricalBayes64_bank10_20261007/verification.json';assert read(bank)['actual_native_fits']==10
    old='nonflag_residual_EmpiricalBayes64_native_stage_20261007.py';new='nonflag_residual_ReverseBayes64_native_stage_20261007.py'
    text=(A/old).read_text(encoding='utf8').replace('nonflag_CPU_EmpiricalBayes64_residual_CDF','nonflag_CPU_ReverseBayes64_residual_CDF').replace('nonflag_cpu_empirical_bayes64_','nonflag_cpu_reverse_bayes64_')
    needle="    assert spec['weight']>0. and spec['universe']=='all_current_raw_forecasts'";assert text.count(needle)==1
    text=text.replace(needle,needle+"\n    assert spec['residual_sign']==-1")
    needle='    native_sum/=len(components); decoded_sum/=len(components)';assert text.count(needle)==1
    text=text.replace(needle,needle+'\n    native_sum*=-1.; decoded_sum*=-1.')
    sources.extend(save(old,new,text))
    old='run_nonflag_residual_EmpiricalBayes64_hook3_after_bank_v2_20261007.py';new='run_nonflag_residual_ReverseBayes64_hook3_after_bank_20261007.py'
    text=(A/old).read_text(encoding='utf8')
    text=text.replace('nonflag_residual_EmpiricalBayes64_native_stage_20261007','nonflag_residual_ReverseBayes64_native_stage_20261007').replace('nonflag_residual_EmpiricalBayes64_native_hook3_preflight_20261007','nonflag_residual_ReverseBayes64_native_hook3_preflight_20261007').replace('nonflag_CPU_EmpiricalBayes64_residual_CDF','nonflag_CPU_ReverseBayes64_residual_CDF')
    text=text.replace("spec={'weight':.01,'universe'", "spec={'weight':.01,'residual_sign':-1,'universe'")
    text=text.replace('passed_actual3_historical603_nonflag_EmpiricalBayes64','passed_actual3_historical603_nonflag_ReverseBayes64')
    sources.extend(save(old,new,text))
    plan=read(A/'nonflag_EmpiricalBayes40_plan_20261007.json')
    plan={k:v for k,v in plan.items() if k not in ['input_sha256','at_local','round','wave','after_round','qualified_anchor_rounds','selection','full_future_candidate_native_replays_and_QA41_required','parent_nonflag_HGB_replaced_by_Ridge_complete_flag_graph_retained']}
    plan.update(status='frozen_negative_empirical_Bayes_control_plan_before_any_actual_controls_or_quality_scores',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
      proposed_round=132,residual_sign=-1,new_branch='nonflag_CPU_ReverseBayes64_residual_CDF',proposed_future_qualified_anchor_rounds=[112,130,131],
      actual_qualified_preflight_parent=112,actual_current_forecast_teacher=106,
      original_native_bank_and_linear_decoder_reused_without_new_fit_claims=True,original_full_future_source_schema_not_yet_admitted=True,
      official40_quality_scores_not_yet_started=True,automatic_morning_restart_enabled=False,
      selection='no_selection_by_preflight;actual_whole_official_comparison_and_frozen_full_candidate_required')
    path=A/'nonflag_ReverseBayes40_control_plan_20261007.json';create(path,plan);sources.append(path)
    old='verify_nonflag_residual_EmpiricalBayes37_transform_v3_20261007.py';new='verify_nonflag_residual_ReverseBayes37_transform_20261007.py'
    text=(A/old).read_text(encoding='utf8').replace('nonflag_residual_EmpiricalBayes37_transform_preflight_20261007','nonflag_residual_ReverseBayes37_transform_preflight_20261007').replace('nonflag_EmpiricalBayes40_plan_20261007.json','nonflag_ReverseBayes40_control_plan_20261007.json').replace('remove_nonflag_EmpiricalBayes64','remove_nonflag_ReverseBayes64')
    needle="        ensemble=np.zeros(len(parent),dtype=np.float64)";assert text.count(needle)==1
    # Negation and ordered averaging are explicitly part of the fresh recipe.
    text=text.replace(needle,needle)
    needle="        prepared=prepare(reference,dates,flags,valid,'all_current_raw_forecasts')";assert text.count(needle)==1
    text=text.replace(needle,"        assert plan['residual_sign']==-1\n        head={n:-np.asarray(v) for n,v in head.items()}\n"+needle)
    text=text.replace('passed_actual37_full5635800_nonflag_residual_Ridge_independent_CDF_and111_cold_controls','passed_actual37_full5635800_nonflag_ReverseBayes64_independent_CDF_and111_cold_controls')
    text=text.replace("'official40_comparisons_and_round130_candidate_QA41_not_claimed':True", "'official40_comparisons_and_full132_candidate_not_claimed':True,'residual_sign':-1")
    text=text.replace("print({'status':'passed','full_cases':49,'cold_controls':147}","print({'status':'passed','full_cases':37,'cold_controls':111,'residual_sign':-1}")
    text=text.replace('Actual full49 independent CDF oracles and147', 'Actual full37 signed independent CDF oracles and111')
    sources.extend(save(old,new,text))
    create(A/'nonflag_ReverseBayes40_control_source_preparation_20261007.json',{
      'status':'compiled_fresh_negative_native3_and_full37_cold111_routes_before_any_quality_scores','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
      'input_sha256':{str(p):sha(p) for p in [*sources,bank]},'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
