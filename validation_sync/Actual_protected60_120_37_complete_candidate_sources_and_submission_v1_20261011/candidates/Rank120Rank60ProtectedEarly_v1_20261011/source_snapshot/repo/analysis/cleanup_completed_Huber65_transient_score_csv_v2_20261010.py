"""Remove only one completed, main-published, transient transient score CSVs."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();import psutil
    out=A/'completed_Huber65_transient_csv_cleanup_v2_20261010';out.mkdir(exist_ok=False)
    plans=[];forbidden=set()
    for n in (157,162,163,164):
        p=A/f'optimization_20261003_r{n}/protocol.json'
        if p.exists():forbidden.update(read(p).get('input_sha256',{}))
    for family,receipt_name in [('Huber010_high_impact65','high_impact_priority_huber65_main_receipt_v7_20261010.json')]:
        receipt=read(A/receipt_name);assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
        service=A/'service_owned_workflows_20261006'/('actual_'+family+'_screen_v1_20261010')
        assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='passed'
        proofpath=Path('E:/赛题五_本机临时')/(family+'_screen_v1_20261010')/'verification.json';proof=read(proofpath)
        assert len(proof['records'])==65 and read(A/'optimization_20261003_r163/full_registration_execution.json')['status']=='passed'
        forbidden.update(proof['input_sha256'])
        for row in proof['records']:
            capsule=Path(row['official_score_cache']['official_metrics_source']);assert sha(capsule)==row['official_metric_capsule_sha256']
        target=(A/(family+'_D_scoring_v1_20261010')/'scoring_validation_only/submission.csv').resolve()
        assert target.is_relative_to(A.resolve()) and target.drive.upper()=='D:' and str(target) not in forbidden and target.name=='submission.csv'
        plans.append({'target':str(target),'bytes':target.stat().st_size,'sha256':sha(target),'published_scores_commit':receipt['commit'],'retained_verification':str(proofpath),'all65_original_score_capsules_rehashed':True})
    create(out/'frozen_before_exact_file_deletion.json',{'files':plans,'available_D_before':psutil.disk_usage('D:/').free,'models_datasets_labels_scores_controls_and_selected_CSV_preserved':True})
    for row in plans:
        target=Path(row['target']);assert sha(target)==row['sha256'];target.unlink()
    create(out/'verification.json',{'status':'passed_only_one_completed_transient_transient_score_CSVs_deleted','files':plans,'freed_bytes':sum(r['bytes'] for r in plans),'available_D_after':psutil.disk_usage('D:/').free,'models_datasets_labels_scores_controls_and_selected_CSV_preserved':True,'at_local':time.strftime('%Y-%m-%dT%H:%M:%S')})
    print({'freed_bytes':sum(r['bytes'] for r in plans),'available_D_GiB':psutil.disk_usage('D:/').free/2**30},flush=True)
if __name__=='__main__':main()
