"""Freeze all complete155 receivers and launch the actual prospective/audit/dispatch gates."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    prospective=A/'BF16Seed10_80_prospective_routes_v1_20261009.json';p=read(prospective)
    assert p['prospective_sources']==56 and len(p['graph_controls'])==2100
    for f,d in p['input_sha256'].items():assert sha(f)==d,f
    specs=[('BF16Seed10_80_round155_source_admission_v1_20261009','verify_BF16Seed10_80_round155_sources_v1_20261009.py',[]),
        ('BF16Seed10_80_controls_main_publication_v1_20261009','publish_BF16Seed10_80_evidence_v1_20261009.py',['controls']),
        ('BF16Seed10_80_official_comparison_v1_20261009','run_BF16Seed10_80_official_comparison_v1_20261009.py',[]),
        ('BF16Seed10_80_scores_main_publication_v1_20261009','publish_BF16Seed10_80_evidence_v1_20261009.py',['scores']),
        ('BF16Seed10_80_selected_candidate_preparation_v1_20261009','prepare_BF16Seed10_80_selected_candidate_v1_20261009.py',[]),
        ('BF16Seed10_80_selected_candidate_sealing_v1_20261009','seal_BF16Seed10_80_selected_candidate_v1_20261009.py',[]),
        ('BF16Seed10_80_round155_full_registration_v1_20261009','run_BF16Seed10_155_safe_registration_v1_20261009.py',[])]
    sources=[Path(__file__),prospective,A/'dispatch_BF16Seed10_155_complete_pipeline_v1_20261009.py',
        A/'run_BF16Seed10_80_round155_full_registration_v1_20261009.py',A/'verify_BF16Seed10_155_prospective_service_v1_20261009.py',
        A/'verify_BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009.py',
        A/'lossless_chunked_safe_main_runtime_v1_20261009.py',A/'serial_main_publication_mutex_v1_20261009.py',*(A/d for _,d,_ in specs)]
    for f in sources:
        assert f.is_file(),f
        if f.suffix=='.py':compile(f.read_text(encoding='utf8'),str(f),'exec')
    meta=A/'BF16Seed10_155_complete_pipeline_preparation_v1_20261009.json'
    create(meta,{'status':'prepared_complete155_seven_receivers_with56_prospective_routes_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(f):sha(f) for f in dict.fromkeys(sources)},
        'receiver_specs':specs,'fixed_stage_base_round':148,'comparison_anchor_rounds':list(range(148,155)),
        'expected_quality_cases':80,'native_saved_annual_states':6,'QA_version':66,'wave':438,
        'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={}
    for name,driver in [('BF16Seed10_155_complete_prospective_controls_v1_20261009','verify_BF16Seed10_155_prospective_service_v1_20261009.py'),
        ('BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009','verify_BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009.py'),
        ('BF16Seed10_155_complete_chronological_dispatch_v1_20261009','dispatch_BF16Seed10_155_complete_pipeline_v1_20261009.py')]:
        rows[name]=start(name,driver,[],{str(meta):sha(meta),str(A/driver):sha(A/driver)})
    create(A/'BF16Seed10_155_complete_prospective_audit_dispatch_hidden_launches_v1_20261009.json',rows)
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
