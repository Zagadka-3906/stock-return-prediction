"""Recover a terminal location collision; verify all29 already-scored records without rerun."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();folder=A/'service_owned_workflows_20261006/actual_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010'
    assert not owned(read(folder/'native_launch.json'));failure=read(folder/'service_execution.json')
    assert failure['status']=='failed' and failure['failure'].startswith('FileExistsError:') and 'high_impact17_screen_location' in failure['failure']
    out=Path('E:/赛题五_本机临时/StockRank5EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010');proof=read(out/'verification.json')
    assert len(proof['records'])==proof['new_quality_score_records']==29 and (proof['actual_nonidentity_full_controls'],proof['actual_nonidentity_prefix_controls'])==(28,84)
    pins={**proof['input_sha256'],str(out/'verification.json'):sha(out/'verification.json'),str(folder/'service_execution.json'):sha(folder/'service_execution.json'),str(Path(__file__)):sha(__file__)}
    for i,row in enumerate(proof['records']):
        assert row['case']==i and row['recipe']=='stock_rank5_embedding16_cross120_rank5mean_recent252_small512_BF16_e64'
        record=out/f'case{i:03d}_official.json';control=out/f'case{i:03d}_controls.json';capsule=Path(row['official_score_cache']['official_metrics_source'])
        assert read(record)==row and sha(control)==row['control_sha256'] and sha(capsule)==row['official_metric_capsule_sha256']
        assert read(capsule)['metrics']==row['metrics'] and read(control)['numeric_sha256']==row['prediction_numeric_sha256']
        if i:assert read(control)['full_independent_Pandas_exact'] and [r['days'] for r in read(control)['prefix_controls']]==[80,260,975]
        for p in (record,control,capsule):pins[str(p)]=sha(p)
    prior=A/'actual_StockRank5EmbeddingSmall512_after171_high_impact17_screen_location_v1_20261010.json';prior_sha=sha(prior)
    assert read(prior)['output'].endswith('StockRank5EmbeddingSmall512_after171_high_impact17_screen_v1_20261010')
    for p,d in pins.items():assert sha(p)==d,p
    create(A/'actual_StockRank5EmbeddingSmall512_after171_large_allocation29_screen_location_v1_20261010.json',{'output':str(out),'verification_sha256':sha(out/'verification.json'),'actual_terminal_pointer_recovery_no_score_rerun':True})
    assert sha(prior)==prior_sha
    create(A/'stock_rank5_embedding_actual29_terminal_pointer_recovery_v1_20261010.json',{'status':'passed_actual29_completed_official_records28_full84_prefix_rehashed_terminal_pointer_recovered','input_sha256':pins,'original_failed_service_retained':True,'original17_pointer_unchanged':prior_sha,'best':proof['best'],'actual_recipe':'stock_rank5_embedding16_cross120_rank5mean_recent252_small512_BF16_e64','original_Top10_BCE_caption_is_legacy_only':True,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'actual29_recovered_without_rerun':True,'best_S':proof['best']['connected_final_score']},flush=True)
if __name__=='__main__':main()
