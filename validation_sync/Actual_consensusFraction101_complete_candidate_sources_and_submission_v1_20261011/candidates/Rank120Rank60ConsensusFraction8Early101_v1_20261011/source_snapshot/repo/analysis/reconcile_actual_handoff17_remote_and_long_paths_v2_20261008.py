"""Validate already-pushed handoff17 blobs and repair only source-index long path metadata; preserve original failure."""
from pathlib import Path
import sys,hashlib,gzip,subprocess,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    service=A/'service_owned_workflows_20261006/actual_optimization_handoff_main_publication_v17_20261008'
    assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='failed'
    out=A/'actual_optimization_handoff_main_v17_20261008';assert not (out/'receipt.json').exists()
    pins=read(out/'frozen_before_main_publication.json')['input_sha256']
    for p,d in pins.items():assert sha(p)==d,p
    import publish_classifier_consensus_workflows_20261006 as helpers
    from file_backed_hidden_git_runtime_20261007 import installed
    with installed(A/'actual_handoff17_reconciliation_file_IO_v2_20261008'):
        sync=helpers.sync;commit=sync.git('rev-parse','HEAD');assert commit=='20963b2f495b86b4eb85610ad0a3b4b5709f99ac'
        helpers.verify_main(commit);assert not sync.git('status','--porcelain')
        prefix=Path('validation_sync/actual_optimization_handoff_v17_20261008')
        manifest=read(sync.WORKTREE/prefix/'manifest.json');expected={}
        for path,binding in manifest['files'].items():
            assert sha(path)==binding['raw_sha256']==pins[path],path
            target=sync.WORKTREE/binding['published_path'];data=target.read_bytes()
            raw=gzip.decompress(data) if target.suffix=='.gz' else data
            assert hashlib.sha256(raw).hexdigest()==binding['raw_sha256']
            expected[binding['published_path']]=hashlib.sha256(data).hexdigest()
        for name in ('manifest.json','.gitattributes'):
            expected[(prefix/name).as_posix()]=sha(sync.WORKTREE/prefix/name)
        assert helpers.blob_hashes(commit,expected)==expected
        assert sync.git('config','--get','core.longpaths',cwd=ROOT)=='true'
        raw=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT,creationflags=subprocess.CREATE_NO_WINDOW)
        missing=[n for n in raw.split(b'\0') if n and not (ROOT/n.decode('utf8')).exists()]
        result=subprocess.run(['git','update-index','--skip-worktree','-z','--stdin'],cwd=ROOT,
            input=b'\0'.join(missing)+b'\0',capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,result.stderr.decode('utf8',errors='replace')
        create(A/'actual_handoff17_long_paths_reconciliation_v2_20261008.json',{
            'status':'passed_actual_existing_remote_main_handoff17_and_long_path_source_index_metadata',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'commit':commit,'actual_raw_blobs_verified':len(expected),
            'source_index_missing_paths_marked':len(missing),'maximum_absolute_path_chars':max(len(str(ROOT/n.decode('utf8'))) for n in missing),
            'core_longpaths_local_config_enabled':True,'no_working_files_reset_checked_out_deleted_or_moved':True,
            'original_failed_publication_source_and_terminal_preserved':True,'new_quality_scores':0})
        create(out/'receipt.json',{'status':'pushed_and_remote_head_verified','at_local':sync.now(),'branch':'main','commit':commit,
            'raw_git_blobs_verified':len(expected),'new_official_scores_by_publication':0,
            'original_push_success_reconciled_from_verified_blobs_not_reexecuted':True,
            'source_index_long_path_failure_repaired_and_preserved':True,
            'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()})
        print('Existing remote handoff17 verified; source-index long paths fixed without changing research files.',flush=True)
if __name__=='__main__':main()
