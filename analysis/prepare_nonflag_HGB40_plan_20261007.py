"""Freeze the previously declared40 comparisons after actual native and CDF controls."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    original=A/'nonflag_residual_HGB10_plan_20261007.json';plan=read(original)
    sources=[Path(__file__),original]
    for name in ('nonflag_residual_HGB10_training','nonflag_residual_HGB37_transform_preflight','nonflag_residual_HGB_native_hook3_preflight'):
        folder=A/'service_owned_workflows_20261006'/name
        assert not owned(read(folder/'native_launch.json'))
        assert read(folder/'service_execution.json')['status']=='passed'
        sources += [folder/'native_launch.json',folder/'service_execution.json']
    sources += [A/'nonflag_residual_HGB_bank10_20261007/verification.json',
      A/'nonflag_residual_HGB37_transform_preflight_20261007/verification.json',
      A/'nonflag_residual_HGB_native_hook3_preflight_20261007/verification.json',
      A/'predict_nonflag_residual_HGB_complete_scheme_20261007.py',A/'nonflag_residual_HGB_native_stage_20261007.py']
    assert plan['later_expected_official_records']==40 and len(plan['later_weights'])==12
    create(A/'nonflag_HGB40_plan_20261007.json',{
      'status':'predeclared_nonflag40_after_actual10_fits37_full111_cold_and3_historical_hooks',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'round':120,'wave':403,
      'qualified_anchor_rounds':plan['later_anchor_rounds'],'after_round':119,
      'single_native_heads':list(plan['configurations']),
      'ensembles':{'equal_mean_two':list(plan['configurations'])},'weights':plan['later_weights'],
      'universe':'all_current_raw_forecasts','existing_native_bank':'nonflag_residual_HGB_bank10_20261007',
      'expected_scored_records':40,'expected_full_transform_controls':37,'expected_cold_prefix_controls':111,
      'teacher_round':106,'preserve_complete_parent_flag_and2020_raw_bits':True,
      'new_branch':'nonflag_CPU_HGB_residual_CDF','new_native_fits_by_comparison':0,
      'selection':'highest_full_connected_official_score_after_actual120_source_admission',
      'full_future_candidate_native_replays_and_QA31_required':True,
      'input_sha256':{str(p):sha(p) for p in sources},'test_labels_read':False,
      'selection_bias_uncorrected':True,'global_resource_exhaustion_established':False})

if __name__=='__main__':main()
