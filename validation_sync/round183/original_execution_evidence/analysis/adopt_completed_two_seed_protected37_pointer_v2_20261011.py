"""Revalidate all completed scientific records before adding the missing unique pointer."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();out=Path('E:/赛题五_本机临时/StockRank20TwoSeed_after175_protected_tail37_screen_v1_20261011')
    proof=read(out/'verification.json');assert len(proof['records'])==37 and proof['actual_nonidentity_full_controls']==36 and proof['actual_nonidentity_prefix_controls']==108
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    for i,r in enumerate(proof['records']):
        assert read(out/f'case{i:03d}_official.json')==r
        assert sha(out/f'case{i:03d}_controls.json')==r['control_sha256']
        capsule=Path(r['official_score_cache']['official_metrics_source']);assert sha(capsule)==r['official_metric_capsule_sha256'] and read(capsule)['metrics']==r['metrics']
        c=read(out/f'case{i:03d}_controls.json');assert c['numeric_sha256']==r['prediction_numeric_sha256']
        if i:assert c['full_independent_Pandas_exact'] and len(c['prefix_controls'])==3
    create(A/'actual_StockRank20TwoSeed_after175_protected_tail37_screen_location_v1_20261011.json',{'output':str(out),'verification_sha256':sha(out/'verification.json'),'recovery':'Original score loop completed; only inherited49 pointer collision repaired without re-scoring'})
    create(A/'two_seed_protected37_completed_pointer_recovery_v2_20261011.json',{'status':'passed_actual37_capsules_and36_full108_prefix_controls_reverified','input_sha256':{str(out/'verification.json'):sha(out/'verification.json')},'new_quality_scores':0,'new_model_fits':0,'original_failed_service_preserved':True})
if __name__=='__main__':main()
