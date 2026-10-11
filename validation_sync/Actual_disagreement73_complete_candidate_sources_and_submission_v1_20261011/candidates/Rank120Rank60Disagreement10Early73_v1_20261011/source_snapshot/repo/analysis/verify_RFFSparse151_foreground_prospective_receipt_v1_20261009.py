"""Rehash the completed151 foreground32/440 proof before chronological admission; no tests repeated."""
from pathlib import Path
import sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    proof_path=A/'RFFSparse59_prospective_routes_v1_20261009.json';proof=read(proof_path)
    assert proof['status']=='passed_actual32_prospective151_sources_fixed_stage_graphs_baselines_status_paths_model_counts_signed_ties_and_cross_volume_bytes'
    assert proof['actual_prospective_sources']==32 and proof['actual_graph_controls']==440
    assert len(proof['baseline_controls'])==12 and len(proof['same_score_sort_controls'])==8 and len(proof['collector_controls'])==4
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    import prepare_RFFSparse59_round151_sources_v1_20261009 as generator
    actual={str(n):{name:hashlib.sha256(text.encode()).hexdigest() for name,text in generator.generate(n).items()} for n in (147,148,149,150)}
    assert actual==proof['generated_source_sha256']
    coverage_path=A/'sparse150151_all20_annual_native_coverage_v1_20261009.json';coverage=read(coverage_path)
    row=next(r for r in coverage['records'] if r['round']==151)
    assert row['actual_head_year_states']==20 and row['actual_native_cases']==row['actual_cold_cases']==90
    create(A/'RFFSparse151_foreground_prospective_receipt_v1_20261009.json',{'status':'passed_rehash_of_completed_foreground32_sources440_graphs_and_all20_annual_state_coverage',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in (Path(__file__),proof_path,coverage_path)},
        'actual_prior_foreground_prospective_execution_reverified':True,'tests_rerun':False,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
    print('Actual15132-source440-graph foreground proof and20 annual states reverified.',flush=True)
if __name__=='__main__':main()
