"""Refresh only private publisher index stat entries, prove staged objects unchanged, then verify original D access on E."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
 old=A/'reconcile_refreshed_current_Git_publisher_and_relocate_v7_20261008.py';s=old.read_text(encoding='utf8').replace('_v7_20261008','_v8_20261008')
 s=s.replace('Git_publisher_exact_nine_line_endings_and_E_relocation_v6_20261008/service_execution.json','Git_publisher_refreshed_current_main_and_E_relocation_v7_20261008/service_execution.json')
 s=s.replace('    held, switched, deleted = [], False, False','    held, switched, deleted = [], False, False\n    private_index=private_original=root_index_sha=None')
 needle="        assert not git(SOURCE, 'status', '--porcelain')\n        assert git(TARGET, 'rev-parse', 'HEAD') == head"
 assert s.count(needle)==1
 s=s.replace(needle,"""        assert not git(SOURCE, 'status', '--porcelain')
        private_path=Path(git(SOURCE,'rev-parse','--git-path','index'))
        private_index=(private_path if private_path.is_absolute() else SOURCE/private_path).resolve()
        assert private_index.is_relative_to((ROOT/'.git/worktrees').resolve()) and private_index!=(ROOT/'.git/index').resolve()
        private_original=private_index.read_bytes();(OUT/'original_private_publisher_index.bin').write_bytes(private_original)
        root_index_sha=sha(ROOT/'.git/index')
        assert git(TARGET, 'rev-parse', 'HEAD') == head""")
 needle="        status=git(TARGET,'status','--porcelain')\n";assert s.count(needle)==1
 s=s.replace(needle,"""        before_objects=git_bytes(TARGET,'ls-files','--stage','-z')
        git(TARGET,'update-index','--refresh')
        after_objects=git_bytes(TARGET,'ls-files','--stage','-z')
        assert before_objects==after_objects, 'Only stat-cache metadata may change, never staged content.'
        assert sha(ROOT/'.git/index')==root_index_sha, 'Primary workspace dirty index must stay unchanged.'
        create(OUT/'actual_private_index_stat_refresh.json',{'private_index':str(private_index),
            'original_index_sha256':hashlib.sha256(private_original).hexdigest(),'refreshed_index_sha256':sha(private_index),
            'all_staged_modes_objects_and_paths_identical':True,'primary_workspace_index_unchanged':True,
            'primary_index_sha256':root_index_sha,'new_commits_created':0})
        status=git(TARGET,'status','--porcelain')
""")
 needle="        create(OUT / 'failure.json', {'status': 'failed_preserved_original_D_or_verified_E_publisher',"
 assert s.count(needle)==1
 s=s.replace(needle,"""        if not deleted and private_index is not None and private_original is not None:
            assert not SOURCE.is_junction() and private_index.is_relative_to((ROOT/'.git/worktrees').resolve())
            private_index.write_bytes(private_original)
            assert sha(private_index)==hashlib.sha256(private_original).hexdigest()
            assert sha(ROOT/'.git/index')==root_index_sha
            create(OUT/'restored_original_private_index_stat_cache.json',{'original_private_index_restored':True,'primary_workspace_index_unchanged':True})
"""+needle)
 target=A/'relocate_verified_publisher_after_private_stat_refresh_v8_20261008.py';compile(s,str(target),'exec')
 with target.open('x',encoding='utf8',newline='') as f:f.write(s)
 pins={str(p):sha(p) for p in [Path(__file__),old,target]}
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 r=start('Git_publisher_private_stat_refresh_verified_E_relocation_v8_20261008',target.name,[],pins)
 create(A/'Git_publisher_private_stat_refresh_E_relocation_hidden_launch_v8_20261008.json',{'launch':r,'input_sha256':pins,
  'primary_workspace_index_files_and_refs_not_reset':True,'all_original_raw_records_retained_before_checked_duplicate_D_deletion':True})
 print(json.dumps({'worker':r['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
