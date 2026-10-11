"""Freeze and dispatch actual complete154 receivers, preserving all comparison and publication gates."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    prospective=A/'BF16TwoSeed79_prospective_routes_v1_20261009.json';p=read(prospective)
    assert p['prospective_sources']==48 and len(p['graph_controls'])==1800
    for f,d in p['input_sha256'].items():assert sha(f)==d,f
    specs=[('BF16TwoSeed79_round154_source_admission_v1_20261009','verify_BF16TwoSeed79_round154_sources_v1_20261009.py',[]),
        ('BF16TwoSeed79_controls_main_publication_v1_20261009','publish_BF16TwoSeed79_evidence_v1_20261009.py',['controls']),
        ('BF16TwoSeed79_official_comparison_v1_20261009','run_BF16TwoSeed79_official_comparison_v1_20261009.py',[]),
        ('BF16TwoSeed79_scores_main_publication_v1_20261009','publish_BF16TwoSeed79_evidence_v1_20261009.py',['scores']),
        ('BF16TwoSeed79_selected_candidate_preparation_v1_20261009','prepare_BF16TwoSeed79_selected_candidate_v1_20261009.py',[]),
        ('BF16TwoSeed79_selected_candidate_sealing_v1_20261009','seal_BF16TwoSeed79_selected_candidate_v1_20261009.py',[]),
        ('BF16TwoSeed79_round154_full_registration_v1_20261009','run_BF16TwoSeed154_safe_registration_v1_20261009.py',[])]
    sources=[Path(__file__),prospective,A/'dispatch_BF16TwoSeed154_complete_pipeline_v1_20261009.py',
        A/'run_BF16TwoSeed79_round154_full_registration_v1_20261009.py',A/'verify_BF16TwoSeed154_prospective_service_v1_20261009.py',
        A/'verify_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009.py',
        A/'lossless_chunked_safe_main_runtime_v1_20261009.py',A/'serial_main_publication_mutex_v1_20261009.py',*(A/d for _,d,_ in specs)]
    for f in sources:
        assert f.is_file(),f
        if f.suffix=='.py':compile(f.read_text(encoding='utf8'),str(f),'exec')
    meta=A/'BF16TwoSeed154_complete_pipeline_preparation_v1_20261009.json'
    create(meta,{'status':'prepared_complete154_seven_receivers_with48_prospective_routes_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(f):sha(f) for f in dict.fromkeys(sources)},
        'receiver_specs':specs,'fixed_stage_base_round':148,'comparison_anchor_rounds':list(range(148,154)),
        'expected_quality_cases':79,'native_saved_annual_states':12,'QA_version':65,'wave':437,
        'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={}
    for name,driver in [('BF16TwoSeed154_complete_prospective_controls_v1_20261009','verify_BF16TwoSeed154_prospective_service_v1_20261009.py'),
        ('BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009','verify_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v1_20261009.py'),
        ('BF16TwoSeed154_complete_chronological_dispatch_v1_20261009','dispatch_BF16TwoSeed154_complete_pipeline_v1_20261009.py')]:
        rows[name]=start(name,driver,[],{str(meta):sha(meta),str(A/driver):sha(A/driver)})
    create(A/'BF16TwoSeed154_complete_prospective_audit_dispatch_hidden_launches_v1_20261009.json',rows)
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
