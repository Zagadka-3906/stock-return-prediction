"""Admit complete round126 only after real native controls and corrected prospective routes."""
from pathlib import Path
import sys
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
    prospective=A/'nonflag_RFF128Low76_prospective_routes_v2_20261007.json';p=read(prospective)
    assert p['status']=='passed_actual24_prospective_sources_and24_graph_controls' and not p['issues']
    controls=A/'nonflag_residual_RFF128Low73_transform_preflight_20261007/verification.json';c=read(controls)
    assert c['actual_full_cases']==73 and c['actual_cold_cases']==219
    hooks=A/'nonflag_residual_RFF128Low_native_hook6_preflight_20261007/verification.json';assert len(read(hooks)['records'])==6
    native=A/'nonflag_residual_RFF128Low_bank10_20261007/verification.json';assert read(native)['actual_native_fits']==10
    preparation=A/'nonflag_RFF128Low76_science_route_preparation_v4_20261007.json'
    sources=[Path(__file__),prospective,controls,hooks,native,preparation,
      A/'nonflag_RFF128Low126_route_mapping_20261007.py',A/'nonflag_RFF128Low76_plan_20261007.json',
      A/'prepare_nonflag_RFF128Low76_round126_sources_v1_20261007.py',
      A/'verify_nonflag_RFF128Low76_round126_sources_v1_20261007.py']
    pins={**read(preparation)['input_sha256'],**{str(p):sha(p) for p in sources}}
    for path,digest in pins.items():assert sha(path)==digest,path
    row=start('nonflag_RFF128Low76_round126_source_admission_v1','verify_nonflag_RFF128Low76_round126_sources_v1_20261007.py',[],pins)
    create(A/'nonflag_RFF128Low76_actual_admission_hidden_launch_20261007.json',
      {'status':'started_actual126_source_admission_after_real10_6_73_219_controls','identity':row,
       'input_sha256':pins,'actual_quality_scores':0,'test_labels_read':False})
if __name__=='__main__':main()
