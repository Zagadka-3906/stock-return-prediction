"""Refresh the retained E copy at a proved idle publication boundary; preserve nine raw legacy files."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
 old=A/'reconcile_nine_Git_worktree_line_endings_and_relocate_v6_20261008.py';s=old.read_text(encoding='utf8')
 s=s.replace('_v6_20261008','_v7_20261008')
 s=s.replace("    failure = A / 'service_owned_workflows_20261006/Git_publisher_original_D_path_verified_E_relocation_v4_20261008/service_execution.json'", "    failure = A / 'service_owned_workflows_20261006/Git_publisher_exact_nine_line_endings_and_E_relocation_v6_20261008/service_execution.json'")
 needle='    held, switched, deleted = [], False, False\n'
 gate='''    gate=A/'service_owned_workflows_20261006/KrylovGram52_controls_main_publication_v18_20261008'
    while not (gate/'service_execution.json').exists():time.sleep(10)
    while owned(read(gate/'native_launch.json')):time.sleep(1)
    assert read(gate/'service_execution.json')['status']=='passed'
'''
 assert s.count(needle)==1;s=s.replace(needle,gate+needle)
 s=s.replace("('SpectralGram52_scores_main_publication_v18_20261008', '    closed (publish_SpectralGram52_evidence_v18_20261008.py:')", "('KrylovGram52_scores_main_publication_v18_20261008', '    closed (publish_KrylovGram52_evidence_v19_20261008.py:')")
 begin=s.index('        assert manifest(TARGET) == original,');end=s.index('        corrections = {}',begin)
 replacement='''        names = [
            'validation_sync/authorized_cleanup_20261005/deletions.jsonl',
            'validation_sync/authorized_cleanup_20261005/plan.json',
            'validation_sync/authorized_cleanup_20261005/verification.json',
            'validation_sync/compute_storage_controls_20261005/capability.json',
            'validation_sync/compute_storage_controls_20261005/frozen_before_actual_control.json',
            'validation_sync/compute_storage_controls_20261005/placement_frozen_before_creation.json',
            'validation_sync/compute_storage_controls_20261005/placement_verification.json',
            'validation_sync/compute_storage_controls_20261005/placement_withdrawal_20261005.json',
            'validation_sync/compute_storage_controls_20261005/verification.json']
        stale = manifest(TARGET)
        assert set(stale)<=set(original), 'Unexpected E files require investigation, not deletion.'
        refreshed=[]
        for name,record in original.items():
            if name in names:continue
            if stale.get(name)!=record:
                target=TARGET/name;target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(SOURCE/name,target)
                assert sha(target)==record['sha256'] and target.stat().st_size==record['bytes'],name
                refreshed.append(name)
        create(OUT/'actual_current_main_E_copy_refresh.json',{'current_main_HEAD':head,'refreshed_files':refreshed,'new_commits_created':0})
'''
 s=s[:begin]+replacement+s[end:]
 needle='            preserved.write_bytes(raw)\n'
 assert s.count(needle)==1
 s=s.replace(needle,"            prior_raw=Path('E:/赛题五_本机临时/Git_publisher_E_relocation_v6_20261008/original_raw_legacy_records')/name\n            assert prior_raw.read_bytes()==raw,name\n"+needle)
 needle="        assert not git(TARGET, 'status', '--porcelain'), 'Every E worktree file must now match its committed tree.'\n"
 assert s.count(needle)==1
 s=s.replace(needle,"        for name in names:assert not git(TARGET,'diff','--raw','--',name),name\n        status=git(TARGET,'status','--porcelain')\n        create(OUT/'actual_refreshed_E_status_before_access_switch.json',{'status_porcelain':status,'HEAD':head})\n        assert not status, 'Every refreshed E worktree file must now match its committed tree.'\n")
 target=A/'reconcile_refreshed_current_Git_publisher_and_relocate_v7_20261008.py';compile(s,str(target),'exec')
 with target.open('x',encoding='utf8',newline='') as f:f.write(s)
 pins={str(p):sha(p) for p in [Path(__file__),old,target]}
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('Git_publisher_refreshed_current_main_and_E_relocation_v7_20261008',target.name,[],pins)
 create(A/'Git_publisher_refreshed_E_relocation_hidden_launch_v7_20261008.json',{'launch':row,'input_sha256':pins,'gate':'actual141_controls_main_passed_and_scores_publisher_and_main8_proved_idle','no_D_deletion_before_all_E_raw_records_and_clean_original_access_verified':True})
 print(json.dumps({'worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
