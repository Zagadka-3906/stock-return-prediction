"""Delete exact completed unadopted scratch CSVs only, retaining all score evidence."""
from pathlib import Path
import sys,shutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed();out=A/'completed_top65_stock33_csv_cleanup_v2_20261010';out.mkdir(exist_ok=False)
    forbidden=set()
    for p in A.glob('optimization_20261003_r*/protocol.json'):forbidden.update(read(p).get('input_sha256',{}))
    items=[('TopWeighted_after163_high_impact65',65,'v1','high_impact_priority_huber65_main_receipt_v12_20261010.json'),('stock_identity_prior_after163_screen33',33,'v4','high_impact_priority_huber65_main_receipt_v14_20261010.json')]
    rows=[]
    for family,count,version,receipt_name in items:
        service=A/'service_owned_workflows_20261006'/f'actual_{family}{"_screen" if family.startswith("Top") else ""}_{version}_20261010'
        assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='passed'
        proofpath=Path('E:/赛题五_本机临时')/f'{family}{"_screen" if family.startswith("Top") else ""}_{version}_20261010'/'verification.json'
        proof=read(proofpath);assert len(proof['records'])==count and proof['best']['case']==0
        receipt=read(A/receipt_name);assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
        forbidden.update(proof['input_sha256'])
        for row in proof['records']:assert sha(Path(row['official_score_cache']['official_metrics_source']))==row['official_metric_capsule_sha256']
        scoring_family=family if family.startswith('Top') else 'stock_identity_prior_after163_screen33'
        target=(A/f'{scoring_family}_D_scoring_{version}_20261010/scoring_validation_only/submission.csv').resolve()
        assert target.is_relative_to(A.resolve()) and str(target) not in forbidden and target.name=='submission.csv'
        rows.append({'target':str(target),'bytes':target.stat().st_size,'sha256':sha(target),'main_commit':receipt['commit'],'records_retained':count,'proof_sha256':sha(proofpath)})
    create(out/'frozen_before_exact_file_deletion.json',{'files':rows,'D_free_before':shutil.disk_usage('D:/').free})
    for row in rows:
        p=Path(row['target']);assert sha(p)==row['sha256'];p.unlink()
    create(out/'verification.json',{'status':'passed_two_closed_published_unadopted_scratch_CSVs_deleted','files':rows,'freed_bytes':sum(r['bytes'] for r in rows),'D_free_after':shutil.disk_usage('D:/').free,'models_data_scores_and_current_submission_preserved':True})
    print('PASS cleaned only two unadopted scratch CSVs',flush=True)
if __name__=='__main__':main()
