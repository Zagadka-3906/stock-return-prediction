"""Delete only unadopted, closed, main-published scratch prediction CSVs."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    import psutil
    now=datetime.now(timezone(timedelta(hours=8)))
    for name in ('current_user_runtime_control_20261009.json','current_user_runtime_control_20261010.json'):
        c=read(A/name);assert c['status']=='optimization_active_after_explicit_manual_resume' and now<datetime.fromisoformat(c['stop_at_local'])
    out=A/'completed165166_transient_score_csv_cleanup_v1_20261010';out.mkdir(exist_ok=False)
    forbidden=set()
    for p in A.glob('optimization_20261003_r*/protocol.json'):
        forbidden.update(read(p).get('input_sha256',{}))
    rows=[]
    for n in (165,166):
        count=23 if n==158 else 19
        folder=A/'service_owned_workflows_20261006'/f'ReusedNN{n}Quality{count}_official_comparison_v3_20261009'
        assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='passed'
        proofpath=A/f'ReusedNN{n}Quality{count}_official_comparison_v1_20261009/verification.json'
        proof=read(proofpath);assert len(proof['records'])==count and proof['best']['configuration']['model'] is None
        receipt=read(A/f'github_validation_sync_main_20261005/round{n}_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main' and receipt['scored_records']==count
        forbidden.update(proof['input_sha256'])
        for row in proof['records']:
            p=Path(row['official_score_cache']['official_metrics_source']);assert sha(p)==row['official_metric_capsule_sha256']
        target=(A/f'ReusedNN{n}Stage_D_scoring_v1_20261009/comparison/scoring_validation_only/submission.csv').resolve()
        assert target.is_relative_to(A.resolve()) and target.drive.upper()=='D:' and str(target) not in forbidden
        rows.append({'round':n,'target':str(target),'bytes':target.stat().st_size,'sha256':sha(target),'main_commit':receipt['commit'],'records_retained':count,'proof_sha256':sha(proofpath)})
    create(out/'frozen_before_exact_file_deletion.json',{'files':rows,'available_D_before':psutil.disk_usage('D:/').free,'no_models_labels_features_scores_controls_or_current_submission_deleted':True})
    for row in rows:
        target=Path(row['target']);assert sha(target)==row['sha256'];target.unlink()
    create(out/'verification.json',{'status':'passed_two_closed_main_published_unadopted_transient_CSVs_deleted','files':rows,'freed_bytes':sum(row['bytes'] for row in rows),'available_D_after':psutil.disk_usage('D:/').free,'at_local':now.isoformat()})
    print({'freed_bytes':sum(row['bytes'] for row in rows),'D_free_GiB':psutil.disk_usage('D:/').free/2**30},flush=True)
if __name__=='__main__':main()
