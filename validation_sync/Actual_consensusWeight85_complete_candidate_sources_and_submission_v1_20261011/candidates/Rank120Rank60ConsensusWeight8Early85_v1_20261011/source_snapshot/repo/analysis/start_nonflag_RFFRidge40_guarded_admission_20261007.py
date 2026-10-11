"""Admit the next complete scheme before launching any of its quality comparisons."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from nonflag_RFFRidge122_route_mapping_20261007 import convert
def main():
    old=A/'continue_nonflag_Ridge40_after_actual_admission_20261007.py'
    new=A/'continue_nonflag_RFFRidge40_after_actual_admission_20261007.py';assert not new.exists()
    source=convert(old.read_text(encoding='utf8'));compile(source,str(new),'exec');new.write_text(source,encoding='utf8',newline='\n')
    prospective=A/'nonflag_RFFRidge40_prospective_routes_v1_20261007.json';p=read(prospective)
    assert p['status']=='passed_actual24_prospective_sources_and12_graph_controls' and not p['issues']
    native=A/'nonflag_residual_RFFRidge_bank10_20261007/verification.json';assert read(native)['actual_native_fits']==10
    controls=A/'nonflag_residual_RFFRidge37_transform_preflight_20261007/verification.json';c=read(controls)
    assert c['actual_full_cases']==37 and c['actual_cold_cases']==111
    hooks=A/'nonflag_residual_RFFRidge_native_hook3_preflight_20261007/verification.json';assert len(read(hooks)['records'])==3
    paths=[Path(__file__),new,prospective,native,controls,hooks,
        A/'nonflag_RFFRidge122_route_mapping_20261007.py',A/'nonflag_RFFRidge40_plan_20261007.json',
        A/'prepare_nonflag_RFFRidge40_complete_routes_20261007.py',
        A/'prepare_nonflag_RFFRidge40_round122_sources_v1_20261007.py',
        A/'verify_nonflag_RFFRidge40_round122_sources_v1_20261007.py',
        A/'run_nonflag_RFFRidge40_admitted_comparison_v1_20261007.py']
    pins={str(p):sha(p) for p in paths}
    for p in paths:
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    from handoff_ready_goss_full_execution_20261006 import start_service
    rows={}
    for name,driver in [('nonflag_RFFRidge40_round122_source_admission_v1','verify_nonflag_RFFRidge40_round122_sources_v1_20261007.py'),
        ('nonflag_RFFRidge40_continue_after_actual_admission',new.name)]:
        rows[name]=start_service(name,driver,[],pins)
    create(A/'nonflag_RFFRidge40_admission_actual_hidden_launches_20261007.json',{'status':'started_real122_admission_and_guarded_continuation_after_actual10_3_37_111_controls',
        'launches':rows,'input_sha256':pins,'official_scorer_not_launched_until_real_qualified121_and_actual24_9_12_admission_passes':True,
        'actual_quality_scores':0,'test_labels_read':False})
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
