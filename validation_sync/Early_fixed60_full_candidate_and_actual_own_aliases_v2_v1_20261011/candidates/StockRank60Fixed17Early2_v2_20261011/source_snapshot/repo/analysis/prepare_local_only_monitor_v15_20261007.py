"""Extend actual single-host observations to118/119 and new nonflag training."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    old=A/'monitor_local_only_runtime_v14_20261007.py';s=old.read_text(encoding='utf8')
    s=s.replace('single_host_optimization_live_status_v14_20261007','single_host_optimization_live_status_v15_20261007').replace('local_only_v14','local_only_v15')
    needle="        'weighted_HGB340_round117_full_registration')";assert s.count(needle)==1
    extra=['HGB_quarter_numeric_audit_main_publication_after117','HGB_quarter_numeric28_full25_transform_preflight','HGB_quarter_numeric28_round118_source_admission',
      'HGB_quarter_numeric28_full25_controls_main_publication','HGB_quarter_numeric28_official_comparison','HGB_quarter_numeric28_scores_main_publication',
      'HGB_quarter_numeric28_selected_candidate_preparation','HGB_quarter_numeric28_selected_candidate_sealing','HGB_quarter_numeric28_round118_full_registration',
      'quantile_HGB_native_bank20_training_v2','quantile_HGB_large_batch20_benchmark','quantile_HGB_native_hook7_preflight','quantile_HGB_bank20_main_publication_after118',
      'cached_official_spearman_full12_benchmark','quantile_HGB_full85_transform_preflight','local_speed_and_quantile85_controls_main_publication',
      'quantile_HGB88_round119_source_admission','quantile_HGB88_full85_controls_main_publication','quantile_HGB88_official_comparison',
      'quantile_HGB88_scores_main_publication','quantile_HGB88_selected_candidate_preparation','quantile_HGB88_selected_candidate_sealing','quantile_HGB88_round119_full_registration',
      'nonflag_residual_HGB_codec2_preflight','nonflag_residual_HGB10_training_admission','nonflag_residual_HGB10_training']
    s=s.replace(needle,"        'weighted_HGB340_round117_full_registration',\n        "+',\n        '.join(repr(n) for n in extra)+')')
    needle='(116, 27), (117, 28)):';assert needle in s;s=s.replace(needle,'(116, 27), (117, 28), (118, 29), (119, 30)):')
    needle="117:'weighted_HGB340_round117_full_registration'}[n]";assert needle in s
    s=s.replace(needle,"117:'weighted_HGB340_round117_full_registration',118:'HGB_quarter_numeric28_round118_full_registration',119:'quantile_HGB88_round119_full_registration'}[n]")
    needle="    value['no_full_qualification_claim_from_partial_case_counts']=True";assert needle in s
    s=s.replace(needle,"""    for family,folder,expected in (
        ('numeric28','HGB_quarter_numeric28_official_comparison_20261007',28),
        ('quantile88','quantile_HGB88_official_comparison_20261007',88)):
        directory=A/folder
        value[family+'_official_cases_completed']=len(list(directory.glob('case*_official.json')))
        value[family+'_expected_official_cases']=expected
        stage=directory/'actual_stage.json'
        if stage.exists():value[family+'_actual_stage']=read(stage)
    for family,folder,expected in (
        ('quantile_HGB20','quantile_HGB_native_bank20_v2_20261007',20),
        ('nonflag_residual_HGB10','nonflag_residual_HGB_bank10_20261007',10)):
        directory=A/folder;proof=directory/'verification.json'
        value[family+'_actual_native_fits']=read(proof)['actual_native_fits'] if proof.exists() else len(list(directory.glob('*/info_*.json')))
        value[family+'_expected_native_fits']=expected
        stage=directory/'actual_stage.json'
        if stage.exists():value[family+'_actual_stage']=read(stage)
        value[family+'_native_fits_do_not_prove_official_score_or_candidate_qualification']=True
    for key,folder in (
        ('actual_scoring_only_SciPy_cache_benchmark','cached_official_spearman_full_scoring_benchmark_20261007'),
        ('actual_quantile20_batch_benchmark','quantile_HGB_large_batch20_benchmark_20261007')):
        path=A/folder/'verification.json'
        if path.exists():
            proof=read(path);value[key]={k:v for k,v in proof.items() if k in ('status','actual_uncached_official_evaluation_calls','median_full_mapping_and_official_score_phase_speedup','native_phase_speedup','independent_decoder_phase_speedup')}
    receipt=A/'local_speed_and_quantile85_controls_github_20261007/receipt.json'
    if receipt.exists():value['local_speed_and_quantile85_actual_main_receipt']=read(receipt)
"""+needle)
    target=A/'monitor_local_only_runtime_v15_20261007.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8')
    old_handoff=A/'handoff_local_only_monitor_v14_20261007.py';h=old_handoff.read_text(encoding='utf8')
    h=substitute(h,{'local_only_monitor_v14_actual_handoff_20261007':'local_only_monitor_v15_actual_handoff_20261007',
      'local_only_progress_monitor_v13':'local_only_progress_monitor_v14','local_only_progress_monitor_v14':'local_only_progress_monitor_v15',
      'monitor_local_only_runtime_v13_20261007.py':'monitor_local_only_runtime_v14_20261007.py','monitor_local_only_runtime_v14_20261007.py':'monitor_local_only_runtime_v15_20261007.py',
      'local_only_v14':'local_only_v15','administrative_supersession_local_v14_20261007':'administrative_supersession_local_v15_20261007',
      'passed_actual_idle_observer13_complete115_116_routes_and_R90_gate':'passed_actual_idle_observer14_complete118_119_and_nonflag_training_routes_and_R90_gate'})
    h=h.replace('Observer13','Observer15')
    target_h=A/'handoff_local_only_monitor_v15_20261007.py';assert not target_h.exists();compile(h,str(target_h),'exec');target_h.write_text(h,encoding='utf8')
    create(A/'local_only_monitor_v15_source_preparation_20261007.json',{'status':'compiled_actual118_119_nonflag_source_routes_and_exact_idle_observer_handoff',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target,old_handoff,target_h]},'scientific_workers_stopped':0,'new_quality_scores':0})
if __name__=='__main__':main()
