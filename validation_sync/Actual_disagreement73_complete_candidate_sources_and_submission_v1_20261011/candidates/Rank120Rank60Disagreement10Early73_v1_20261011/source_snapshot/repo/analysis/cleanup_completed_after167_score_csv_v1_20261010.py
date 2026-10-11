"""Delete two closed, published TRAIN scoring scratch CSVs after qualified168 delivery."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,json,shutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def strings(value):
    if isinstance(value,str):yield value
    elif isinstance(value,dict):
        for key,item in value.items():yield key;yield from strings(item)
    elif isinstance(value,list):
        for item in value:yield from strings(item)

def main():
    assert allowed()
    delivery=read(A/'latest_verified_submission_delivery_v2_20261008.json')
    assert delivery['selected_round']==168
    assert sha(Path(delivery['output'])/'submission.csv')==delivery['csv_sha256']
    receipt=read(A/'github_validation_sync_main_20261005/round168_receipt.json')
    assert receipt['commit']==delivery['main_commit'] and receipt['status']=='pushed_and_remote_head_verified'
    rows=[];documents=[];targets=[]
    for stem,publication in [('Forward20_after167_high_impact65',20),('RecentReturn252_after167_high_impact65',19)]:
        service=A/'service_owned_workflows_20261006'/('actual_'+stem+'_screen_v1_20261010')
        assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='passed'
        main=read(A/f'high_impact_priority_huber65_main_receipt_v{publication}_20261010.json')
        assert main['status']=='pushed_and_remote_head_verified' and main['branch']=='main'
        proofpath=Path('E:/赛题五_本机临时')/(stem+'_screen_v1_20261010')/'verification.json'
        proof=read(proofpath);assert len(proof['records'])==65
        for row in proof['records']:
            capsule=Path(row['official_score_cache']['official_metrics_source']);assert sha(capsule)==row['official_metric_capsule_sha256']
        target=(A/(stem+'_D_scoring_v1_20261010')/'scoring_validation_only/submission.csv').resolve()
        assert target.is_relative_to(A.resolve()) and target.drive.upper()=='D:' and target.name=='submission.csv'
        targets.append(target)
        documents.append(proofpath)
        rows.append({'path':str(target),'bytes':target.stat().st_size,'sha256':sha(target),'completed_official_records':65,'main_commit':main['commit'],'verification_sha256':sha(proofpath)})
    documents.extend(A.glob('optimization_20261003_r*/protocol.json'))
    documents.extend(A.glob('service_owned_workflows_20261006/*/job_definition.json'))
    documents.extend(Path('E:/赛题五_本机临时').glob('*/frozen_before_any_new_controls_or_scores.json'))
    for directory in [ROOT/'candidates/RecentReturn252Protected168_v1_20261010',A/'optimization_20261003_r168',A/'RecentReturn252Protected168_selected_release_v1_20261010']:
        documents.extend(directory.glob('*.json'))
    checked=[]
    for document in dict.fromkeys(documents):
        obj=read(document)
        pins={key:obj[key] for key in ['input_sha256','source_sha256','source_pins','frozen_source_sha256'] if key in obj}
        values=set(strings(pins))
        for target in targets:assert str(target) not in values,'Scratch CSV pinned by '+str(document)
        checked.append({'path':str(document),'sha256':sha(document)})
    out=A/'completed_after167_score_csv_cleanup_v1_20261010';out.mkdir(exist_ok=False)
    create(out/'frozen_before_exact_file_deletion.json',{'rows':rows,'pin_documents_checked':checked,'qualified168_receipt_sha256':sha(A/'github_validation_sync_main_20261005/round168_receipt.json')})
    for row,target in zip(rows,targets):
        assert allowed() and sha(target)==row['sha256'];target.unlink()
    create(out/'verification.json',{'status':'passed_only_two_closed_main_published_TRAIN_scratch_CSVs_removed','rows':rows,'freed_bytes':sum(row['bytes'] for row in rows),'models_OOF_labels_scores_controls_final_csv_preserved':True,'D_free_GiB':shutil.disk_usage('D:/').free/2**30,'at_local':datetime.now(timezone(timedelta(hours=8))).isoformat()})
    print({'freed_bytes':sum(row['bytes'] for row in rows),'D_free_GiB':shutil.disk_usage('D:/').free/2**30},flush=True)
if __name__=='__main__':main()
