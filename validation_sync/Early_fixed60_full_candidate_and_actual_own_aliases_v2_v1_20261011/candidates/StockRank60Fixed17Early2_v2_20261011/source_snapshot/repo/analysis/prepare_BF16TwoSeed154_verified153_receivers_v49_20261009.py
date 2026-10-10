"""Resume154 only after actual153 complete595? blob reconciliation, with no scientific rerun."""
from pathlib import Path
from copy import deepcopy
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    proof=A/'BF16Medium153_committed_full_QA_main_reconciliation_v48_20261009.json';p=read(proof)
    assert p['status']=='passed_all_committed153_blobs_QA64_original_report_stream_remote_main_and_frozen_sources'
    assert p['actual_scored_records']==78 and p['actual_connected_records']==15310
    service=A/'service_owned_workflows_20261006/BF16Medium78_round153_full_registration_v5_20261009/service_execution.json'
    assert read(service)['status']=='passed'
    oldmeta=A/'BF16TwoSeed154_complete_pipeline_preparation_v3_20261009.json';newmeta=A/'BF16TwoSeed154_complete_pipeline_preparation_v4_20261009.json'
    pairs=[('verify_BF16TwoSeed79_round154_sources_current153_v3_20261009.py','verify_BF16TwoSeed79_round154_sources_current153_v4_20261009.py'),
        ('publish_BF16TwoSeed79_evidence_v2_20261009.py','publish_BF16TwoSeed79_evidence_v3_20261009.py'),
        ('run_BF16TwoSeed79_round154_full_registration_v3_20261009.py','run_BF16TwoSeed79_round154_full_registration_v4_20261009.py'),
        ('run_BF16TwoSeed154_safe_registration_v3_20261009.py','run_BF16TwoSeed154_safe_registration_v4_20261009.py'),
        ('verify_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v2_20261009.py','verify_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v3_20261009.py'),
        ('dispatch_BF16TwoSeed154_complete_pipeline_v3_20261009.py','dispatch_BF16TwoSeed154_complete_pipeline_v4_20261009.py')]
    files=[Path(__file__),proof,service,oldmeta];mapping={}
    for old,new in pairs:
        src,dst=A/old,A/new;s=src.read_text(encoding='utf8')
        s=s.replace('BF16Medium78_round153_full_registration_v4_20261009','BF16Medium78_round153_full_registration_v5_20261009')
        s=s.replace(oldmeta.name,newmeta.name)
        s=s.replace('BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v2_20261009','BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v3_20261009')
        if 'safe_registration' in new:
            s=s.replace('run_BF16TwoSeed79_round154_full_registration_v3_20261009','run_BF16TwoSeed79_round154_full_registration_v4_20261009')
            s=s.replace('/safe_full_main_v3','/safe_full_main_v4')
        if new.startswith('publish_'):s=s.replace("'safe_'+phase+'_main_v2'","'safe_'+phase+'_main_v3'")
        if new.startswith('dispatch_'):s=s.replace('BF16TwoSeed154_complete_hidden_launches_v3_20261009','BF16TwoSeed154_complete_hidden_launches_v4_20261009')
        compile(s,str(dst),'exec')
        with dst.open('x',encoding='utf8') as f:f.write(s)
        files.extend((src,dst));mapping[old]=new
    m=deepcopy(read(oldmeta));m['receiver_specs']=[[sid,mapping.get(driver,driver),args] for sid,driver,args in m['receiver_specs']]
    m['input_sha256'].update({str(f):sha(f) for f in files});m.update(status='prepared154_after_actual153_full5_independently_reverified_main',
        at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),new_quality_scores=0,test_labels_read=False)
    create(newmeta,m)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={}
    for name,driver in [('BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v3_20261009','verify_BF16TwoSeed154_prior_complete_forecast_duplicate_audit_v3_20261009.py'),
        ('BF16TwoSeed154_complete_chronological_dispatch_v4_20261009','dispatch_BF16TwoSeed154_complete_pipeline_v4_20261009.py')]:
        rows[name]=start(name,driver,[],{str(newmeta):sha(newmeta),str(A/driver):sha(A/driver)})
    create(A/'BF16TwoSeed154_verified153_receivers_hidden_launches_v49_20261009.json',{'launches':rows,
        'input_sha256':{str(newmeta):sha(newmeta)},'all_original_scores_and_failed_admin_attempts_preserved':True,
        'scientific_jobs_stopped_or_restarted':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)
if __name__=='__main__':main()
