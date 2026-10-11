"""Remove only completed Return65 scratch CSV after qualified167 delivery."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import sys
A=Path(__file__).resolve().parent; ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def strings(x):
    if isinstance(x,str):yield x
    elif isinstance(x,dict):
        for k,v in x.items():yield k;yield from strings(v)
    elif isinstance(x,list):
        for v in x:yield from strings(v)

def main():
    import psutil
    now=datetime.now(timezone(timedelta(hours=8)))
    for n in ('09','10'):
        c=read(A/f'current_user_runtime_control_202610{n}.json')
        assert c['status']=='optimization_active_after_explicit_manual_resume' and now<datetime.fromisoformat(c['stop_at_local'])
    name='actual_Forward20_after163_high_impact65_screen_v1_20261010'
    f=A/'service_owned_workflows_20261006'/name
    assert not owned(read(f/'native_launch.json')) and read(f/'service_execution.json')['status']=='passed'
    receipt=read(A/'high_impact_priority_huber65_main_receipt_v18_20261010.json')
    assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
    delivered=read(A/'latest_verified_submission_delivery_v2_20261008.json')
    assert delivered['selected_round']==167 and sha(Path(delivered['output'])/'submission.csv')==delivered['csv_sha256']
    release=read(A/'github_validation_sync_main_20261005/round167_receipt.json')
    assert release['status']=='pushed_and_remote_head_verified' and release['scored_records']==67 and release['commit']==delivered['main_commit']
    candidate=ROOT/'candidates/RecentReturn252Protected168_v1_20261010'
    assert read(candidate/'verification.json')['status']=='passed'
    proofpath=Path(read(A/'actual_Forward20_after163_high_impact65_screen_location_v1_20261010.json')['output'])/'verification.json'
    proof=read(proofpath);assert len(proof['records'])==65
    for row in proof['records']:
        p=Path(row['official_score_cache']['official_metrics_source']);assert sha(p)==row['official_metric_capsule_sha256']
    target=(A/'Forward20_after163_high_impact65_D_scoring_v1_20261010/scoring_validation_only/submission.csv').resolve()
    assert target.is_relative_to(A.resolve()) and target.drive.upper()=='D:'
    pinsets=[proof['input_sha256']]
    scanned=[]
    for p in A.glob('optimization_20261003_r*/protocol.json'):
        pinsets.append(read(p).get('input_sha256',{}));scanned.append(str(p))
    for directory in (candidate,A/'ReturnProtected167_selected_release_v1_20261010',A/'RecentReturn252Protected168_selected_release_v1_20261010',A/'optimization_20261003_r167',A/'optimization_20261003_r168'):
        for p in directory.glob('*.json'):
            obj=read(p)
            for key in ('input_sha256','source_sha256','source_pins','frozen_source_sha256'):
                if key in obj:pinsets.append(obj[key])
            scanned.append(str(p))
    for pins in pinsets:
        assert str(target) not in set(strings(pins)), 'Scratch CSV is a pinned scientific input'
    out=A/'completed_Forward20_after163_score_csv_cleanup_v1_20261010';out.mkdir(exist_ok=False)
    row={'target':str(target),'bytes':target.stat().st_size,'sha256':sha(target),'completed_screen_main':receipt['commit'],'qualified167_main':release['commit'],'proof_sha256':sha(proofpath),'input_pin_documents_checked':scanned}
    create(out/'frozen_before_exact_file_deletion.json',row)
    assert sha(target)==row['sha256'];target.unlink()
    create(out/'verification.json',{'status':'passed_only_completed_validation_scratch_CSV_deleted','file':row,'freed_bytes':row['bytes'],'D_free_GiB':psutil.disk_usage('D:/').free/2**30,'models_scores_controls_raw_OOF_and_final_submission_preserved':True,'at_local':now.isoformat()})
    print({'freed_bytes':row['bytes'],'D_free_GiB':psutil.disk_usage('D:/').free/2**30},flush=True)
if __name__=='__main__':main()
