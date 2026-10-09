"""Create fresh Ridge scopes without changing any admitted or running HGB source."""
from pathlib import Path
import ast,sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute

def mapping():
    own=['run_nonflag_HGB40_official_comparison','run_nonflag_HGB40_admitted_comparison',
        'prepare_nonflag_HGB40_selected_candidate','seal_nonflag_HGB40_selected_candidate',
        'prepare_nonflag_HGB40_round120_sources','verify_nonflag_HGB40_round120_sources',
        'run_nonflag_HGB40_round120_full_registration','publish_nonflag_HGB40_evidence']
    m={n+'_v4_20261007':n.replace('nonflag_HGB40','nonflag_Ridge40').replace('round120','round121')+'_v1_20261007' for n in own}
    for suffix in ('official_comparison','selected_release','pre_inference_source_freeze','round120_source_admission','round120_source_preparation','round120_actual_registration'):
        m['nonflag_HGB40_'+suffix+'_v4_20261007']='nonflag_Ridge40_'+suffix.replace('round120','round121')+'_v1_20261007'
    for suffix in ('round120_source_admission','full37_controls_main_publication','official_comparison','scores_main_publication','selected_candidate_preparation','selected_candidate_sealing','round120_full_registration'):
        m['nonflag_HGB40_'+suffix+'_v4']='nonflag_Ridge40_'+suffix.replace('round120','round121')+'_v1'
    m.update({'nonflag_HGB40_plan_20261007':'nonflag_Ridge40_plan_20261007',
        'nonflag_HGB40_scores_github_20261007':'nonflag_Ridge40_scores_github_v1_20261007',
        'nonflag_HGB40_controls_github_20261007':'nonflag_Ridge40_controls_github_v1_20261007',
        'nonflag_HGB40_{phase}_github_20261007':'nonflag_Ridge40_{phase}_github_v1_20261007',
        'candidates/nonflag_HGB40_v4_20261007':'candidates/nonflag_Ridge40_v1_20261007',
        'nonflag_residual_HGB_bank10_20261007':'nonflag_residual_Ridge_bank10_20261007',
        'nonflag_residual_HGB37_transform_preflight_20261007':'nonflag_residual_Ridge37_transform_preflight_20261007',
        'nonflag_residual_HGB37_transform_preflight':'nonflag_residual_Ridge37_transform_preflight',
        'nonflag_residual_HGB_native_hook3_preflight_20261007':'nonflag_residual_Ridge_native_hook3_preflight_20261007',
        'nonflag_residual_HGB_native_stage_20261007':'nonflag_residual_Ridge_native_stage_20261007',
        'predict_nonflag_residual_HGB_complete_scheme_20261007':'predict_nonflag_residual_Ridge_complete_scheme_20261007',
        'refine_flagged_HGB_compatible_parent_transform_20261007':'nonflag_residual_Ridge_compatible_parent_20261007',
        'remove_nonflag_HGB':'remove_nonflag_Ridge',
        'nonflag_CPU_HGB_residual_CDF':'nonflag_CPU_Ridge_residual_CDF',
        'independent_hist_tree_state':'independent_linear_state',
        'nonflag_residual_HGB_native_replay_verification.json':'nonflag_residual_Ridge_native_replay_verification.json',
        'refined_quantile_HGB_native_replay_verification.json':'nonflag_residual_Ridge_native_replay_verification.json',
        'passed_actual37_full5635800_nonflag_residual_HGB_independent_CDF_and111_cold_controls':'passed_actual37_full5635800_nonflag_residual_Ridge_independent_CDF_and111_cold_controls',
        'passed_actual40_nonflag_HGB_full_official_comparisons':'passed_actual40_nonflag_Ridge_full_official_comparisons',
        'passed_actual3_historical603_nonflag_HGB_native_reload_decoder_CDF_and_whole_day_prefix_controls':'passed_actual3_historical603_nonflag_Ridge_native_reload_decoder_CDF_and_whole_day_prefix_controls',
        'passed_actual_complete_parent_and_nonflag_HGB_two_full_replays_independent_and_cold80':'passed_actual_complete_parent_and_nonflag_Ridge_two_full_replays_independent_and_cold80',
        'passed_actual_selected_new_nonflag_HGB40_candidate_inference':'passed_actual_selected_new_nonflag_Ridge40_candidate_inference',
        'passed_frozen_nonflag_HGB40_complete_native_parent_independent_and_cold80':'passed_frozen_nonflag_Ridge40_complete_native_parent_independent_and_cold80',
        'passed_actual_pre_inference_source_snapshot_and_nonflag_HGB40_native_candidate':'passed_actual_pre_inference_source_snapshot_and_nonflag_Ridge40_native_candidate',
        'frozen_selected_nonflag_HGB40_before_future_inference':'frozen_selected_nonflag_Ridge40_before_future_inference',
        'nonflag_HGB40_complete_pipeline_actual_hidden_launches_v4_20261007':'nonflag_Ridge40_complete_pipeline_actual_hidden_launches_v1_20261007',
        'nonflag_HGB40_actual_source_paths_before_registration_20261007':'nonflag_Ridge40_actual_source_paths_before_registration_20261007'})
    return m

def main():
    m=mapping(); generated={}
    base_names=['run_nonflag_HGB40_official_comparison','run_nonflag_HGB40_admitted_comparison',
        'prepare_nonflag_HGB40_selected_candidate','seal_nonflag_HGB40_selected_candidate','run_nonflag_HGB40_round120_full_registration']
    for stem in base_names:
        old=stem+'_v4_20261007'; new=m[old]; text=substitute((A/(old+'.py')).read_text(encoding='utf8'),m)
        text=text.replace('(112,118,119)','(112,119,120)').replace('((112,23),(118,29),(119,30))','((112,23),(119,30),(120,31))')
        text=text.replace('candidate_full_future_freeze_native_replays_QA31','candidate_full_future_freeze_native_replays_QA32').replace('future_candidate_and_full120_qualification','future_candidate_and_full121_qualification')
        if stem.startswith('run_nonflag_HGB40_official'):
            text=text.replace("'HGB_quarter_numeric28_round118_full_registration_v5','quantile_HGB88_round119_full_registration_v6'","'quantile_HGB88_round119_full_registration_v6','nonflag_HGB40_round120_full_registration_v4'")
        elif stem.startswith('prepare_'):
            text=text.replace("        assert info['year']==2025 and info['actual_iterations']==96\n        assert info['parameters']['loss'] in ('squared_error','absolute_error')", "        assert info['year']==2025 and info['parameters']['solver']=='cholesky'\n        assert info['parameters']['alpha']>0.")
            needle="        if names:\n            graph['nonflag_CPU_Ridge_residual_CDF']"
            assert text.count(needle)==1
            text=text.replace(needle,"        graph.pop('nonflag_CPU_HGB_residual_CDF',None)\n"+needle)
            text=text.replace("if not key.startswith('nonflag_cpu_hgb_')", "if not key.startswith(('nonflag_cpu_hgb_','nonflag_cpu_ridge_'))")
            text=text.replace("if not n.startswith('nonflag_residual_hgb')", "if not n.startswith(('nonflag_residual_hgb','nonflag_residual_ridge'))")
            text=text.replace('new_HGB_component_names','new_Ridge_component_names')
        elif 'full_registration' in stem:
            text=text.replace("'quantile_HGB88_round119_full_registration_v6',","'nonflag_HGB40_round120_full_registration_v4',")
            text=text.replace('optimization_20261003_r120','optimization_20261003_r121').replace('round120_artifacts','round121_artifacts').replace('round120_full_validation','round121_full_validation').replace('adapter_round120','adapter_round121')
            text=text.replace('publish(120,','publish(121,').replace('lossless(120)','lossless(121)').replace('nonflag_HGB40_full120','nonflag_Ridge40_full121')
            text=text.replace('full120_QA31','full121_QA32').replace('actual120_registry','actual121_registry')
            text=text.replace('非涨停残差HGB','非涨停残差Ridge')
        generated[new+'.py']=text
    wrapper=(A/'predict_nonflag_residual_HGB_complete_scheme_20261007.py').read_text(encoding='utf8')
    wrapper=substitute(wrapper,{k:v for k,v in m.items() if k in ('nonflag_residual_HGB_native_stage_20261007','nonflag_CPU_HGB_residual_CDF','nonflag_residual_HGB_native_replay_verification.json','passed_actual_complete_parent_and_nonflag_HGB_two_full_replays_independent_and_cold80')})
    wrapper=wrapper.replace('nonflag_cpu_hgb_','nonflag_cpu_ridge_').replace('actual_nonflag_residual_HGB_native_independent','actual_nonflag_residual_Ridge_native_independent')
    generated['predict_nonflag_residual_Ridge_complete_scheme_20261007.py']=wrapper
    for name,text in generated.items():
        compile(text,str(A/name),'exec'); assert not (A/name).exists(),name
    plan=read(A/'nonflag_HGB40_plan_20261007.json')
    plan.update(status='frozen_Ridge40_before_full_controls_and_official_scores',at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),round=121,wave=404,
        existing_native_bank='nonflag_residual_Ridge_bank10_20261007',qualified_anchor_rounds=[112,119,120],
        single_native_heads=['nonflag_residual_ridge_l001','nonflag_residual_ridge_l025'],ensembles={'nonflag_residual_ridge_equal_mean_two':['nonflag_residual_ridge_l001','nonflag_residual_ridge_l025']},
        parent_nonflag_HGB_replaced_by_Ridge_complete_flag_graph_retained=True,full_future_source_admission_required_before_official_scoring=True)
    # Older descriptive fields are rewritten explicitly; shared CDF numerical recipe stays identical.
    for key in list(plan):
        if isinstance(plan[key],str):plan[key]=plan[key].replace('nonflag_HGB','nonflag_Ridge').replace('nonflag_residual_HGB','nonflag_residual_Ridge')
    create(A/'nonflag_Ridge40_plan_20261007.json',plan)
    for name,text in generated.items():
        with (A/name).open('x',encoding='utf8',newline='\n') as f:f.write(text)
    create(A/'nonflag_Ridge40_science_route_preparation_20261007.json',{'status':'compiled_fresh_Ridge40_scoring_freeze_native_wrapper_and_full_registration_prototypes',
        'input_sha256':{str(A/n):sha(A/n) for n in generated},'original_HGB_sources_unchanged':True,
        'actual_new_official_scores':0,'complete_round121_source_admission_not_yet_claimed':True,'test_labels_read':False})
    print({'status':'compiled','fresh_science_sources':len(generated)},flush=True)
if __name__=='__main__':main()
