"""Keep actual scores and candidate bytes; delete two verified complete transient OOF CSVs."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();import psutil
    out=A/'completed164_temporal73_transient_csv_cleanup_v1_20261010';out.mkdir(exist_ok=False)
    forbidden=set()
    for n in (157,162,163,164,165):
        path=A/f'optimization_20261003_r{n}/protocol.json'
        if path.exists():forbidden.update(read(path).get('input_sha256',{}))
    rows=[]
    specs=[('ReusedNN164Quality19_official_comparison_v3_20261009',A/'ReusedNN164Quality19_official_comparison_v1_20261009/verification.json',A/'github_validation_sync_main_20261005/round164_receipt.json',A/'ReusedNN164Stage_D_scoring_v1_20261009/comparison/scoring_validation_only/submission.csv',19),('actual_causal_neural_smoothing73_screen_v1_20261010',Path('E:/赛题五_本机临时/causal_neural_smoothing73_screen_v1_20261010/verification.json'),A/'high_impact_priority_temporal73_main_receipt_v10_20261010.json',A/'causal_neural_smoothing73_D_scoring_v1_20261010/scoring_validation_only/submission.csv',73)]
    for service,proofpath,receiptpath,target,count in specs:
        folder=A/'service_owned_workflows_20261006'/service;assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='passed'
        proof=read(proofpath);assert len(proof['records'])==count
        receipt=read(receiptpath);assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
        forbidden.update(proof['input_sha256'])
        for row in proof['records']:
            capsule=Path(row['official_score_cache']['official_metrics_source']);assert sha(capsule)==row['official_metric_capsule_sha256']
        if count==73:assert proof['best']['case']==0
        else:assert proof['best']['configuration']['anchor_round']==163 and proof['best']['configuration']['model'] is None
        target=target.resolve();assert target.is_relative_to(A.resolve()) and target.drive.upper()=='D:' and str(target) not in forbidden
        rows.append({'target':str(target),'bytes':target.stat().st_size,'sha256':sha(target),'score_records_retained':count,'main_commit':receipt['commit'],'proof':str(proofpath)})
    create(out/'frozen_before_exact_file_deletion.json',{'files':rows,'available_D_before':psutil.disk_usage('D:/').free,'no_models_datasets_scores_controls_or_final_submission_removed':True})
    for row in rows:
        path=Path(row['target']);assert sha(path)==row['sha256'];path.unlink()
    create(out/'verification.json',{'status':'passed_two_complete_main_published_transient_CSVs_deleted_all_records_and_final163_preserved','files':rows,'freed_bytes':sum(r['bytes'] for r in rows),'available_D_after':psutil.disk_usage('D:/').free,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    print({'freed_bytes':sum(r['bytes'] for r in rows),'available_D_GiB':psutil.disk_usage('D:/').free/2**30},flush=True)
if __name__=='__main__':main()
