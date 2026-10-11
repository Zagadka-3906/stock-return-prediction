"""Audit only obsolete scratch predictions from qualified and published local rounds108–118."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from cleanup_closed_round_worker_submissions_20261006 import identities
from bounded_frozen_SHA_bindings_20261007 import scan as bounded_scan
def scan_bindings(targets):
    proof=bounded_scan(ROOT,targets)
    if proof['blocked']:raise AssertionError('Frozen input: '+proof['blocked'][0])
    return proof['fingerprints']
OUT=A/'closed_local_score_scratch_cleanup_v2_20261007'
ROUNDS={108:('direct_flag_rank92_official_comparison_20261007','direct_flag_rank92_official_comparison'),
    109:('direct_flag_rank_micro74_official_comparison_20261007','direct_flag_rank_micro74_official_comparison'),
    110:('conditional_residual_mlp44_official_comparison_20261007','conditional_residual_mlp44_official_comparison'),
    111:('compact_conditional_residual_mlp44_official_comparison_20261007','compact_conditional_residual_mlp44_official_comparison'),
    112:('conditional_residual_hgb44_official_comparison_20261007','conditional_residual_hgb44_official_comparison'),
    113:('full_universe_HGB44_official_comparison_v3_20261007','full_universe_HGB44_official_comparison_v3'),
    114:('full_universe_ElasticNet44_official_comparison_v3_20261007','full_universe_ElasticNet44_official_comparison_v3'),
    115:('protected_upper_pool_HGB66_official_comparison_v2_20261007','protected_upper_pool_HGB66_official_comparison_v2'),
    116:('flagged_HGB_small_amplitude88_official_comparison_v4_20261007','flagged_HGB_small_amplitude88_official_comparison_v4'),
    117:('flagged_HGB_weighted_quarters340_official_comparison_20261007','flagged_HGB_weighted_quarters340_official_comparison'),
    118:('HGB_quarter_numeric28_official_comparison_v5_20261007','HGB_quarter_numeric28_official_comparison_v5')}

def live_direct_bindings():
    protected={}; services=[]
    for folder in (A/'service_owned_workflows_20261006').iterdir():
        launch=folder/'native_launch.json'; definition=folder/'job_definition.json'
        if not (launch.exists() and definition.exists()):continue
        row=read(launch)
        if not owned(row):continue
        data=read(definition);services.append({'name':folder.name,'pid':row['owned_worker_pid'],'birth':row['owned_worker_creation_time']})
        for key,value in data.get('input_sha256',{}).items():protected[Path(key).resolve()]=value
    return protected,services

def main():
    assert not OUT.exists();OUT.mkdir(); candidates=[];retained={};skipped=[]
    for number,(folder_name,service_name) in ROUNDS.items():
        folder=A/folder_name; target=(folder/'scoring_validation_only/submission.csv').resolve()
        if not target.is_file():continue
        assert target.is_relative_to(ROOT.resolve()) and target.drive.upper()=='D:' and not target.is_symlink() and not target.is_junction()
        for parent in target.parents:
            if parent.is_relative_to(ROOT):assert not parent.is_symlink() and not parent.is_junction()
        service=A/'service_owned_workflows_20261006'/service_name
        launch=read(service/'native_launch.json');assert not owned(launch)
        assert read(service/'service_execution.json')['status']=='passed'
        receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'; publication=read(receipt)
        assert publication['status']=='pushed_and_remote_head_verified' and publication['branch']=='main'
        assert publication['full_immutable_ranking_and_all_original_QA_preserved']
        assert read(A/f'optimization_20261003_r{number}/full_registration_execution.json')['status']=='passed'
        evidence=[receipt,service/'native_launch.json',service/'service_execution.json',folder/'verification.json',*folder.glob('case*_official.json'),
            A/f'optimization_20261003_r{number}/calibrated_csv_official.json',A/f'optimization_20261003_r{number}/selection.json']
        retained.update({str(p.resolve()):sha(p) for p in evidence})
        candidates.append({'round':number,'path':str(target),'sha256':sha(target),**identities(target),'qualified_main_commit':publication['commit']})
    direct,services=live_direct_bindings()
    remaining={Path(row['path']) for row in candidates if Path(row['path']) not in direct}
    skipped += [{'path':r['path'],'reason':'actual_live_job_direct_input'} for r in candidates if Path(r['path']) in direct]
    binding_proof=bounded_scan(ROOT,remaining)
    bindings=binding_proof['fingerprints']
    for item in binding_proof['blocked']:
        remaining.remove(Path(item));skipped.append({'path':item,'reason':'conservative_existing_SHA_map_binding'})
    deletions=[r for r in candidates if Path(r['path']) in remaining]
    create(OUT/'plan.json',{'status':'audited_user_authorized_closed_scoring_scratch_only','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'authorization':'清理历史副本与弃用缓存，仅保留记录和分数等信息','allowed_absolute_root':str(ROOT.resolve()),
        'deletions':deletions,'skipped':skipped,'retained_records_sha256':retained,'frozen_documents_sha256':bindings,
        'live_jobs_at_observation':services,'source_sha256':{str(Path(__file__)):sha(__file__),str(A/'bounded_frozen_SHA_bindings_20261007.py'):sha(A/'bounded_frozen_SHA_bindings_20261007.py')},'bounded_scan':{k:v for k,v in binding_proof.items() if k!='fingerprints'},
        'reclaimable_single_link_bytes':sum(r['bytes'] for r in deletions if r['hardlinks']==1),
        'source_inputs_models_test_labels_candidates_and_active_scoring_outputs_retained':True,'test_labels_read':False})
    print({'status':'audited','eligible_files':len(deletions),'skipped':len(skipped),'single_link_GiB':sum(r['bytes'] for r in deletions if r['hardlinks']==1)/2**30},flush=True)

def revalidate():
    plan=read(OUT/'plan.json');targets={Path(r['path']) for r in plan['deletions']}
    direct,services=live_direct_bindings();assert not targets&set(direct)
    scan_bindings(targets)
    for row in plan['deletions']:
        path=Path(row['path']);assert path.resolve()==path and path.is_relative_to(ROOT.resolve())
        assert identities(path)=={k:row[k] for k in identities(path)} and sha(path)==row['sha256']
    for p,d in plan['retained_records_sha256'].items():assert sha(p)==d
    create(OUT/'revalidated_immediately_before_native_single_file_deletion.json',{'status':'passed_current_bindings_identities_and_full_hashes','plan_sha256':sha(OUT/'plan.json'),
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'live_jobs':services,'eligible_files':len(targets),'test_labels_read':False})
    print({'status':'passed_revalidation','files':len(targets)},flush=True)

def verify():
    plan=read(OUT/'plan.json');assert (OUT/'revalidated_immediately_before_native_single_file_deletion.json').exists()
    for r in plan['deletions']:assert not Path(r['path']).exists(),r['path']
    for p,d in plan['retained_records_sha256'].items():assert sha(p)==d,p
    for p,d in plan['frozen_documents_sha256'].items():assert sha(p)==d,p
    create(OUT/'verification.json',{'status':'passed_authorized_closed_scoring_scratch_cleanup_all_records_and_frozen_inputs_preserved',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'deleted_files':len(plan['deletions']),'deleted_logical_bytes':sum(r['bytes'] for r in plan['deletions']),
        'single_link_reclaimed_bytes':plan['reclaimable_single_link_bytes'],'retained_records_verified':len(plan['retained_records_sha256']),
        'existing_frozen_documents_verified':len(plan['frozen_documents_sha256']),'models_deleted':0,'candidate_submissions_deleted':0,
        'source_inputs_and_original_test_data_retained':True,'scientific_workers_stopped_or_restarted':0,'test_labels_read':False})
    print({'status':'passed_cleanup','deleted_files':len(plan['deletions']),'GiB':plan['reclaimable_single_link_bytes']/2**30},flush=True)
if __name__=='__main__': {'plan':main,'revalidate':revalidate,'verify':verify}[sys.argv[1]]()
