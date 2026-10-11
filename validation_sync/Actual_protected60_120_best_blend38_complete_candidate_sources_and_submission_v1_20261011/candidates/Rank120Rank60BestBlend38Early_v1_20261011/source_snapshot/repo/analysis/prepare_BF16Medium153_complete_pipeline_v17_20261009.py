"""Freeze actual receiver versions,40 prospective routes and publication-only runtime before quality."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    prospective=A/'BF16Medium78_prospective_routes_v1_20261009.json';p=read(prospective)
    assert p['prospective_sources']==40 and len(p['graph_controls'])==1500
    for f,d in p['input_sha256'].items():assert sha(f)==d,f
    specs=[('BF16Medium78_round153_source_admission_v1_20261009','verify_BF16Medium78_round153_sources_v1_20261009.py',[]),
      ('BF16Medium78_controls_main_publication_v1_20261009','publish_BF16Medium78_evidence_v2_20261009.py',['controls']),
      ('BF16Medium78_official_comparison_v1_20261009','run_BF16Medium78_official_comparison_v2_20261009.py',[]),
      ('BF16Medium78_scores_main_publication_v1_20261009','publish_BF16Medium78_evidence_v2_20261009.py',['scores']),
      ('BF16Medium78_selected_candidate_preparation_v1_20261009','prepare_BF16Medium78_selected_candidate_v1_20261009.py',[]),
      ('BF16Medium78_selected_candidate_sealing_v1_20261009','seal_BF16Medium78_selected_candidate_v1_20261009.py',[]),
      ('BF16Medium78_round153_full_registration_v1_20261009','run_BF16Medium153_safe_registration_v17_20261009.py',[])]
    sources=[Path(__file__),prospective,A/'dispatch_BF16Medium153_complete_pipeline_v17_20261009.py',
      A/'run_BF16Medium78_round153_full_registration_v3_20261009.py',A/'lossless_chunked_safe_main_runtime_v1_20261009.py',
      A/'lossless_chunked_safe_main_runtime_v1_20261009.json',*(A/d for _,d,_ in specs)]
    for f in sources:
        assert f.is_file(),f
        if f.suffix=='.py':compile(f.read_text(encoding='utf8'),str(f),'exec')
    meta=A/'BF16Medium153_complete_pipeline_preparation_v17_20261009.json'
    create(meta,{'status':'prepared_actual_complete153_seven_receivers_with40_prospective_routes_before_quality',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(f):sha(f) for f in dict.fromkeys(sources)},
      'receiver_specs':specs,'fixed_stage_base_round':148,'comparison_anchor_rounds':[148,149,150,151,152],
      'expected_quality_cases':78,'QA_version':64,'wave':436,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={}
    for name,driver in [('BF16Medium153_complete_prospective_controls_v1_20261009','verify_BF16Medium78_prospective_routes_service_v1_20261009.py'),
      ('BF16Medium153_complete_chronological_dispatch_v17_20261009','dispatch_BF16Medium153_complete_pipeline_v17_20261009.py')]:
        rows[name]=start(name,driver,[],{str(meta):sha(meta),str(A/driver):sha(A/driver)})
    create(A/'BF16Medium153_complete_prospective_and_dispatch_hidden_launches_v17_20261009.json',rows)
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)

if __name__=='__main__':main()
