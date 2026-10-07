"""Start real round124 admission and launch science only after its genuine success."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_ready_goss_full_execution_20261006 import start_service
def start(name,driver,args,pins):
    try:return start_service(name,driver,args,pins)
    except AssertionError:
        folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json')
        assert not owned(row) and read(folder/'service_execution.json')['status']=='passed'
        assert row['actual_native_console_handle']==0 and not row['independent_launch_root_in_any_job']
        return row
def main():
    prospective=A/'nonflag_reverse_Ridge40_prospective_routes_v1_20261007.json';p=read(prospective)
    assert p['status']=='passed_actual24_prospective_sources_and12_graph_controls' and not p['issues']
    controls=A/'nonflag_reverse_Ridge37_transform_preflight_20261007/verification.json';c=read(controls)
    assert c['actual_full_cases']==37 and c['actual_cold_cases']==111
    hooks=A/'nonflag_reverse_Ridge_native_hook3_preflight_20261007/verification.json';assert len(read(hooks)['records'])==3
    native=A/'nonflag_residual_Ridge_bank10_20261007/verification.json';assert read(native)['actual_native_fits']==10
    original_cdf=A/'nonflag_residual_HGB_CDF_transform_20261007.py'
    historical=read(A/'nonflag_residual_HGB37_transform_preflight_20261007/verification.json')
    assert historical['input_sha256'][str(original_cdf)]==sha(original_cdf)
    sources=[Path(__file__),prospective,controls,hooks,native,original_cdf,
      A/'nonflag_reverse_Ridge40_plan_20261007.json',A/'nonflag_reverse_Ridge40_science_route_preparation_20261007.json',
      A/'nonflag_reverse_Ridge124_route_mapping_20261007.py',
      A/'prepare_nonflag_reverse_Ridge40_round124_sources_v1_20261007.py',
      A/'verify_nonflag_reverse_Ridge40_round124_sources_v1_20261007.py']
    pins={**read(A/'nonflag_reverse_Ridge40_science_route_preparation_20261007.json')['input_sha256'],
      **{str(p):sha(p) for p in sources}}
    for p,d in pins.items():assert sha(p)==d,p
    row=start('nonflag_reverse_Ridge40_round124_source_admission_v1','verify_nonflag_reverse_Ridge40_round124_sources_v1_20261007.py',[],pins)
    create(A/'nonflag_reverse_Ridge40_actual_admission_hidden_launch_20261007.json',
      {'status':'started_actual124_source_admission_after_real10_3_37_111_controls','identity':row,
       'input_sha256':pins,'original_delegated_CDF_matches_qualified120_control_source':True,
       'actual_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
