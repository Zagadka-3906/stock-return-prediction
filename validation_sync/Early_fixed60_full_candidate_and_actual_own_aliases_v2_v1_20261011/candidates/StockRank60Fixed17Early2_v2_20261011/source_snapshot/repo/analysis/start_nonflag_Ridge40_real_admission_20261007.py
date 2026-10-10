"""Start only admission and its continuation; no official scorer starts before full admission."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    preflight=A/'nonflag_Ridge40_prospective_routes_v2_20261007.json'; proof=read(preflight)
    assert proof['status']=='passed_actual24_prospective_sources_and12_graph_controls' and not proof['issues']
    native=A/'nonflag_residual_Ridge_bank10_20261007/verification.json';assert read(native)['actual_native_fits']==10
    controls=A/'nonflag_residual_Ridge37_transform_preflight_20261007/verification.json';assert read(controls)['actual_full_cases']==37
    paths=[Path(__file__),preflight,native,controls,A/'nonflag_residual_Ridge_native_hook3_preflight_20261007/verification.json',
        A/'verify_nonflag_Ridge40_round121_sources_v2_20261007.py',A/'continue_nonflag_Ridge40_after_actual_admission_20261007.py',
        A/'run_nonflag_Ridge40_admitted_comparison_v2_20261007.py',A/'nonflag_Ridge40_plan_20261007.json',
        A/'prepare_nonflag_Ridge40_round121_sources_v2_20261007.py']
    pins={str(p):sha(p) for p in paths}
    for p in paths:
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    from handoff_ready_goss_full_execution_20261006 import start_service
    rows={}
    for name,driver in [('nonflag_Ridge40_round121_source_admission_v1','verify_nonflag_Ridge40_round121_sources_v2_20261007.py'),
        ('nonflag_Ridge40_continue_after_actual_admission','continue_nonflag_Ridge40_after_actual_admission_20261007.py')]:
        rows[name]=start_service(name,driver,[],pins)
    create(A/'nonflag_Ridge40_admission_actual_hidden_launches_20261007.json',{'status':'started_actual_complete_admission_and_guarded_continuation_only',
        'launches':rows,'input_sha256':pins,'official_scorer_not_launched_until_actual_admission_passes':True,'new_quality_scores':0,'test_labels_read':False})
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
