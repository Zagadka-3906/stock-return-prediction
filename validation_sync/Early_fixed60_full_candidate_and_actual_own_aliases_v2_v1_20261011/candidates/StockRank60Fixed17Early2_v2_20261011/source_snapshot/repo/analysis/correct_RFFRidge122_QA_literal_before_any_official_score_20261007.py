"""Correct the real admission's QA string, preserve failures and re-admit fresh sources."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
def main():
    original_service=A/'service_owned_workflows_20261006/nonflag_RFFRidge40_round122_source_admission_v1'
    assert not owned(read(original_service/'native_launch.json')) and read(original_service/'service_execution.json')['status']=='failed'
    assert not (A/'nonflag_RFFRidge40_official_comparison_v1_20261007').exists()
    assert not (A/'nonflag_RFFRidge40_round122_source_admission_v1_20261007.json').exists()
    names=['prepare_nonflag_RFFRidge40_round122_sources','verify_nonflag_RFFRidge40_round122_sources',
        'publish_nonflag_RFFRidge40_evidence','run_nonflag_RFFRidge40_round122_full_registration','run_nonflag_RFFRidge40_admitted_comparison']
    m={n+'_v1_20261007':n+'_v2_20261007' for n in names}
    base=A/'prepare_nonflag_RFFRidge40_round122_sources_v1_20261007.py'
    generator=A/'prepare_nonflag_RFFRidge40_round122_sources_v2_20261007.py';assert not generator.exists()
    code=base.read_text(encoding='utf8')
    # Keep the original generator as immutable scientific template; replace concrete route source references.
    code=code.replace("name=NAMES[old];text=substitute(convert(text),extra)","name=NAMES[old];text=substitute(substitute(convert(text),CORRECTION_MAP),extra)")
    needle="NAMES={name:convert(name) for name in base.NAMES.values()}";assert code.count(needle)==1
    code=code.replace(needle,needle+'\nCORRECTION_MAP='+repr(m))
    compile(code,str(generator),'exec');generator.write_text(code,encoding='utf8',newline='\n')
    new_sources=[generator]
    for stem in names[1:]:
        old=A/(stem+'_v1_20261007.py');new=A/(stem+'_v2_20261007.py');assert not new.exists()
        code=substitute(old.read_text(encoding='utf8'),m)
        if stem.startswith('verify_'):
            assert code.count('assert "actual_full_QA_version\': 32"')==1
            code=code.replace('assert "actual_full_QA_version\': 32"','assert "actual_full_QA_version\': 33"')
        if stem.startswith('run_nonflag_RFFRidge40_admitted'):
            code=code.replace("'nonflag_RFFRidge40_round122_source_admission_v1'","'nonflag_RFFRidge40_round122_source_admission_v2'")
        compile(code,str(new),'exec');new.write_text(code,encoding='utf8',newline='\n');new_sources.append(new)
    old=A/'verify_nonflag_RFFRidge40_prospective_routes_v1_20261007.py'
    new=A/'verify_nonflag_RFFRidge40_prospective_routes_v2_20261007.py';assert not new.exists()
    code=substitute(old.read_text(encoding='utf8'),m).replace('nonflag_RFFRidge40_prospective_routes_v1','nonflag_RFFRidge40_prospective_routes_v2')
    compile(code,str(new),'exec');new.write_text(code,encoding='utf8',newline='\n');new_sources.append(new)
    old=A/'continue_nonflag_RFFRidge40_after_actual_admission_20261007.py'
    new=A/'continue_nonflag_RFFRidge40_after_actual_admission_v2_20261007.py';assert not new.exists()
    code=substitute(old.read_text(encoding='utf8'),m).replace("'nonflag_RFFRidge40_round122_source_admission_v1'","'nonflag_RFFRidge40_round122_source_admission_v2'")
    compile(code,str(new),'exec');new.write_text(code,encoding='utf8',newline='\n');new_sources.append(new)
    proof=A/'RFFRidge122_zero_score_QA_literal_correction_20261007.json'
    pins={str(p):sha(p) for p in [Path(__file__),*new_sources,original_service/'service_execution.json',original_service/'stderr.log']}
    create(proof,{'status':'corrected_only_expected_QA33_literal_and_fresh_route_source_references_before_any_official_score',
        'input_sha256':pins,'prior_actual_failure_retained':True,'actual_prior_official_scores':0,
        'native_models_features_weights_training_windows_and_scoring_math_unchanged':True})
    import verify_nonflag_RFFRidge40_prospective_routes_v2_20261007 as verifier
    verifier.main()
    prospective=A/'nonflag_RFFRidge40_prospective_routes_v2_20261007.json';p=read(prospective)
    assert p['status']=='passed_actual24_prospective_sources_and12_graph_controls' and not p['issues']
    pins.update({str(proof):sha(proof),str(prospective):sha(prospective)})
    from handoff_ready_goss_full_execution_20261006 import start_service
    rows={}
    for name,driver in [('nonflag_RFFRidge40_round122_source_admission_v2','verify_nonflag_RFFRidge40_round122_sources_v2_20261007.py'),
        ('nonflag_RFFRidge40_continue_after_actual_admission_v2','continue_nonflag_RFFRidge40_after_actual_admission_v2_20261007.py')]:
        rows[name]=start_service(name,driver,[],pins)
    create(A/'nonflag_RFFRidge40_corrected_admission_hidden_launches_v2_20261007.json',{'status':'started_corrected_real_admission_and_guarded_continuation_before_any_official_scores','launches':rows,'input_sha256':pins})
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
