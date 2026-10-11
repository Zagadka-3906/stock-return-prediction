"""Recover only administrative stages; all forty original official scores stay immutable."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def save(old_name,new_name,changes):
    old=A/old_name;new=A/new_name;text=old.read_text(encoding='utf8')
    for before,after,count in changes:
        assert text.count(before)==count,(old_name,before,text.count(before));text=text.replace(before,after)
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n');return [old,new]

def main():
    assert len(read(A/'nonflag_RidgeMicro40_official_comparison_v1_20261007/verification.json')['records'])==40
    paths=[Path(__file__),A/'file_backed_hidden_git_runtime_20261007.py']
    failed=[]
    for name in ['nonflag_RidgeMicro40_scores_main_publication_v1','nonflag_RidgeMicro40_selected_candidate_preparation_v1','nonflag_RidgeMicro40_selected_candidate_sealing_v1','nonflag_RidgeMicro40_round131_full_registration_v1']:
        folder=A/'service_owned_workflows_20261006'/name;assert read(folder/'service_execution.json')['status']=='failed'
        failed.extend([*folder.glob('*.json'),*folder.glob('*.log')])
    paths+=failed
    extra="    sources += [A/'recover_nonflag_RidgeMicro131_after_actual_API_main_v2_20261007.py',A/'nonflag_RidgeMicro131_administrative_publication_recovery_v2_20261007.json',A/'file_backed_hidden_git_runtime_20261007.py',A/'publish_nonflag_RidgeMicro40_evidence_v2_20261007.py',A/'prepare_nonflag_RidgeMicro40_selected_candidate_v2_20261007.py',A/'seal_nonflag_RidgeMicro40_selected_candidate_v2_20261007.py',A/'run_nonflag_RidgeMicro40_round131_full_registration_v2_20261007.py']\n"
    extra+='    sources += ['+','.join('A/'+repr(p.relative_to(A).as_posix()) for p in failed)+']\n'
    paths+=save('publish_nonflag_RidgeMicro40_evidence_v1_20261007.py','publish_nonflag_RidgeMicro40_evidence_v2_20261007.py',[
      ('def main(phase):','def actual_main(phase):',1),
      ('    sources=list(dict.fromkeys(sources));',extra+'    sources=list(dict.fromkeys(sources));',1),
      ("out=A/f'nonflag_RidgeMicro40_{phase}_github_v1_20261007'","out=A/f'nonflag_RidgeMicro40_{phase}_github_recovery_v2_20261007'",1),
      ('共52项。','共40项。',1),
      ("if __name__=='__main__':main(sys.argv[1])","""def main(phase):
    proof=A/'sparse_main_API_transport_recovery_20261007/receipt.json'
    while not proof.exists():time.sleep(2)
    assert read(proof)['status']=='pushed_and_remote_head_verified'
    from file_backed_hidden_git_runtime_20261007 import installed
    with installed(A/'RidgeMicro131_scores_file_IO_git_v2_20261007'):actual_main(phase)
    receipt=A/f'nonflag_RidgeMicro40_{phase}_github_recovery_v2_20261007/receipt.json'
    canonical=A/f'nonflag_RidgeMicro40_{phase}_github_v1_20261007/receipt.json'
    assert not canonical.exists()
    create(canonical,{**read(receipt),'actual_publication_recovery_driver':str(Path(__file__)),'original_failed_service_execution_retained':True})

if __name__=='__main__':main(sys.argv[1])""",1)])
    paths+=save('prepare_nonflag_RidgeMicro40_selected_candidate_v1_20261007.py','prepare_nonflag_RidgeMicro40_selected_candidate_v2_20261007.py',[
      ('    assert not OUT.exists()\n    OUT.mkdir()','    assert not OUT.exists() or not any(OUT.iterdir())\n    OUT.mkdir(exist_ok=True)',1),
      ("closed('nonflag_RidgeMicro40_scores_main_publication_v1')","closed('nonflag_RidgeMicro40_scores_main_publication_v2')",1)])
    paths+=save('seal_nonflag_RidgeMicro40_selected_candidate_v1_20261007.py','seal_nonflag_RidgeMicro40_selected_candidate_v2_20261007.py',[
      ('service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_preparation_v1','service_owned_workflows_20261006/nonflag_RidgeMicro40_selected_candidate_preparation_v2',1)])
    paths+=save('run_nonflag_RidgeMicro40_round131_full_registration_v1_20261007.py','run_nonflag_RidgeMicro40_round131_full_registration_v2_20261007.py',[
      ('nonflag_RidgeMicro40_round131_actual_registration_v1_20261007','nonflag_RidgeMicro40_round131_actual_registration_v2_20261007',1),
      ("'nonflag_RidgeMicro40_scores_main_publication_v1'","'nonflag_RidgeMicro40_scores_main_publication_v2'",1),
      ("'nonflag_RidgeMicro40_selected_candidate_sealing_v1'","'nonflag_RidgeMicro40_selected_candidate_sealing_v2'",1),
      ("protocol=register();folder=A/'optimization_20261003_r131';pins=protocol['input_sha256']","protocol=register();folder=A/'optimization_20261003_r131';pins={**protocol['input_sha256']}\n    recovery=A/'nonflag_RidgeMicro131_administrative_publication_recovery_v2_20261007.json'\n    pins.update({**read(recovery)['input_sha256'],str(recovery):sha(recovery)})",1),
      ("if __name__=='__main__':main()","""if __name__=='__main__':
    from file_backed_hidden_git_runtime_20261007 import installed
    with installed(A/'RidgeMicro131_full42_file_IO_git_v2_20261007'):main()""",1)])
    proof=A/'nonflag_RidgeMicro131_administrative_publication_recovery_v2_20261007.json'
    create(proof,{'status':'fresh_actual131_publication_preparation_sealing_and_full42_receivers_preserving40_original_scores',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in paths},
      'original_failed_V1_source_bytes_and_statuses_retained':True,'mathematical_scoring_candidate_and_generated_metadata_recipes_not_changed':True,
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    pins={**read(proof)['input_sha256'],str(proof):sha(proof)}
    jobs=[('nonflag_RidgeMicro40_scores_main_publication_v2','publish_nonflag_RidgeMicro40_evidence_v2_20261007.py',['scores']),
      ('nonflag_RidgeMicro40_selected_candidate_preparation_v2','prepare_nonflag_RidgeMicro40_selected_candidate_v2_20261007.py',[]),
      ('nonflag_RidgeMicro40_selected_candidate_sealing_v2','seal_nonflag_RidgeMicro40_selected_candidate_v2_20261007.py',[]),
      ('nonflag_RidgeMicro40_round131_full_registration_v2','run_nonflag_RidgeMicro40_round131_full_registration_v2_20261007.py',[])]
    rows={name:start(name,driver,args,pins) for name,driver,args in jobs}
    create(A/'nonflag_RidgeMicro131_actual4_recovered_hidden_launches_v2_20261007.json',{'status':'started_actual131_recovery_without_new_official_scoring','launches':rows,'input_sha256':pins})

if __name__=='__main__':main()
