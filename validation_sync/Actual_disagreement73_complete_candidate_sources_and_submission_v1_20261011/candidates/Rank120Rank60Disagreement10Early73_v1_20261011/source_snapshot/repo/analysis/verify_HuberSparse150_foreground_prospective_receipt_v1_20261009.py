"""Verify the completed foreground prospective execution; do not repeat its tests or claim inference."""
from pathlib import Path
import sys,hashlib,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    proof=A/'HuberSparse59_prospective_routes_v1_20261009.json';p=read(proof)
    assert p['status']=='passed_actual32_prospective150_sources_fixed_stage_graphs_baselines_status_paths_model_counts_signed_ties_and_cross_volume_bytes'
    assert p['actual_prospective_sources']==32 and p['actual_graph_controls']==440
    assert len(p['baseline_controls'])==12 and len(p['same_score_sort_controls'])==8 and len(p['collector_controls'])==4
    assert str(A/'verify_HuberSparse59_prospective_routes_v2_20261009.py') in p['input_sha256']
    for path,digest in p['input_sha256'].items():assert sha(path)==digest,path
    import prepare_HuberSparse59_round150_sources_v2_20261009 as generator
    actual={str(n):{name:hashlib.sha256(text.encode()).hexdigest() for name,text in generator.generate(n).items()} for n in (146,147,148,149)}
    assert actual==p['generated_source_sha256']
    create(A/'HuberSparse150_foreground_prospective_receipt_v1_20261009.json',{'status':'passed_rehash_of_completed_foreground32_sources440_graphs_and_contract_checks','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':{str(Path(__file__)):sha(__file__),str(proof):sha(proof)},'actual_prior_foreground_prospective_execution_reverified':True,'tests_rerun':False,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
    print('Completed foreground prospective proof rehashed and32 source bytes verified.',flush=True)
if __name__=='__main__':main()
