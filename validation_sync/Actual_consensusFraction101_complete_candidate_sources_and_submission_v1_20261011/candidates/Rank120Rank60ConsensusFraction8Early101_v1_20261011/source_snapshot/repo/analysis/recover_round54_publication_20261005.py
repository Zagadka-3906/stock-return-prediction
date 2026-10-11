"""Rehash all frozen science/artifacts andrestore ranking-only R54 completion.

Keep the failed original scope. No training, scoring orcandidate inference rerun.
"""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'analysis'),str(ROOT)]
OUT=ROOT/'analysis/round54_publication_recovery_20261005'
ROUND=ROOT/'analysis/optimization_20261003_r54'
RUN=ROOT/'analysis/round54_publication_recovery_run_20261005.json'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def create(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2);stream.write('\n')


def main():
    while not RUN.exists():time.sleep(1)
    job=read(RUN);assert job['source_sha256']==sha(__file__)
    original=ROUND/'provenance_scope_execution.json';old_scope=read(original)
    expected_error="NameError: name 'provenance_ref' is not defined"
    assert old_scope['status']=='failed' and old_scope['failure']==expected_error
    assert old_scope['all_sha_bindings_restored'] and old_scope['scope_started']
    import psutil
    registry=read(ROOT/'analysis/resumed_rounds_nystrom_locked_20261004.json')
    old_job=next(item for item in registry if item['round']==54)
    if psutil.pid_exists(old_job['pid']):assert old_job['script'] not in psutil.Process(old_job['pid']).cmdline()
    prototype=ROUND/'protocol.json';protocol=read(prototype);selection=ROUND/'selection.json'
    selected=read(selection);published=ROOT/'results/optimization_20261003_r54.json';result=read(published)
    assert result['status']=='complete' and result['round']==54
    assert result['scored_records']==protocol['expected_scored_records']==178
    assert result['winner']==selected['winner']
    for key in ('component_audit','calibrated_written_csv','method_causal_checks','prediction'):
        assert result[key]['status']=='passed',key
    official=ROUND/'calibrated_csv_official.json';scores=read(official)
    assert scores['status']=='passed' and scores['metrics']==result['winner']['metrics']
    metrics=scores['metrics']
    assert metrics['final_score']==.4*metrics['ic_mean']+.3*metrics['annual_excess']+.3*(1-metrics['mean_turnover'])
    candidate=Path(result['candidate_submission']);verification=candidate.parent/'verification.json';value=read(verification)
    assert value['status']=='passed' and not value['test_labels_read']
    assert (value['rows'],value['days'],value['codes'])==(1599600,344,4650)
    assert value['model_reload_bit_identical'] and value['cold80_day_prefix_bit_identical'] and value['csv_replay_byte_identical']
    assert sha(candidate)==value['csv_sha256']
    state=ROOT/'analysis/ongoing_optimization_r54_state.json';failed_state=read(state)
    assert failed_state['status']=='failed' and expected_error in failed_state['traceback']
    create(OUT/'original_failed_state.json',failed_state)
    inputs={str(Path(path).resolve()):digest for path,digest in protocol['input_sha256'].items()}
    frozen_input_count=len(inputs)
    for relative,digest in selected['frozen_sha256'].items():
        path=Path(relative);path=path if path.is_absolute() else ROOT/path
        key=str(path.resolve());assert key not in inputs or inputs[key]==digest,key
        inputs[key]=digest
    scientific=[prototype,selection,published,original,official,verification,candidate,
        ROUND/'component_audit.json',ROUND/'no_dropout_seed_scheme_causal_checks.json',ROUND/'causal_validation.json',
        *ROUND.glob('wave*_results.json'),*[path for path in candidate.parent.glob('model*') if path.is_file()]]
    for model in value['models'].values():
        model_path=Path(model['path']);assert sha(model_path)==model['sha256'],model_path
        scientific.append(model_path)
    report_sources=[Path(__file__),RUN,ROOT/'analysis/locked_read_hash_cache_20261004.py',
        ROOT/'analysis/build_all_model_rankings_20261003.py',ROOT/'analysis/verify_all_model_rankings_20261003.py',
        Path(old_job['stderr']),OUT/'original_failed_state.json']
    for path in [*scientific,*report_sources]:
        key=str(path.resolve());digest=sha(path);assert key not in inputs or inputs[key]==digest,key
        inputs[key]=digest
    assert 'provenance_ref(recovery)' not in report_sources[3].read_text(encoding='utf-8')
    create(OUT/'frozen_before_rehash_andranking.json',{'status':'frozen_before_independent_full_rehash_andranking',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'original_failure':expected_error,
        'input_sha256':inputs,'original_protocol_frozen_input_files':frozen_input_count,
        'original_failed_scope_retained':True,'recovery_only_for_post_science_ranking_error':True,
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print('Independent full rehash andread locks: '+str(len(inputs))+' frozen source/artifact files.',flush=True)
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    with LockedReadHashCache(inputs) as locked:
        print('All frozen input andselected artifact SHA values matched; rebuilding ranking.',flush=True)
        import build_all_model_rankings_20261003 as ranking
        import verify_all_model_rankings_20261003 as qa
        ranking.main();qa.main()
        qa_path=ROOT/'analysis/all_model_ranking_qa/interaction_result.json';quality=read(qa_path)
        assert quality['status']=='passed'
        assert quality['connected_records']>=8276
        board=read(ROOT/'results/all_model_rankings_20261003.json')
        assert board['summary']['later_round_records']['54']==178
        create(OUT/'ranking_qa_snapshot.json',quality)
    # Successful context exit performed another full rehash before releasing all handles.
    assert locked.closed
    for path in scientific:assert sha(path)==inputs[str(path.resolve())],path
    recovery={'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'original_failure':expected_error,'original_failed_scope_retained':True,
        'original_protocol_frozen_input_files':frozen_input_count,
        'all_original_frozen_inputs_fully_rehashed_andmatched':True,
        'all_selected_scientific_artifacts_andcandidate_bytes_rehashed_andmatched':True,
        'Windows_read_share_only_locks_held_during_actual_ranking_andQA':True,
        'final_full_rehash_before_read_lock_release_passed':True,'all_read_handles_closed':True,
        'actual_ranking_QA_passed':True,'ranking_qa_snapshot':str((OUT/'ranking_qa_snapshot.json').resolve()),
        'ranking_qa_snapshot_sha256':sha(OUT/'ranking_qa_snapshot.json'),
        'published_result_sha256':sha(published),'protocol_sha256':sha(prototype),
        'original_failed_scope_sha256':sha(original),'candidate_verification_sha256':sha(verification),
        'official_written_CSV_verification_sha256':sha(official),'candidate_csv_sha256':sha(candidate),
        'effective_recovery_script_sha256':sha(__file__),'input_sha256':inputs,
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False,
        'scope':'Recovery completes missing final full-input rehash andranking QA after the retained ranking-only NameError. Existing178 official results andall scientific parameters/artifacts remain unchanged.'}
    create(OUT/'verification.json',recovery)
    create(ROUND/'publication_recovery_execution_20261005.json',recovery)
    completed={key:val for key,val in failed_state.items() if key!='traceback'}
    completed.update(status='completed',stage='round_complete_after_ranking_only_recovery',
        updated_at_local=time.strftime('%Y-%m-%dT%H:%M:%S'),
        retained_failure_state=str((OUT/'original_failed_state.json').resolve()),
        publication_recovery_evidence=str((ROUND/'publication_recovery_execution_20261005.json').resolve()),
        score=metrics['final_score'],gain=result['score_gain'],continuous_goal_complete=False)
    state.write_text(json.dumps(completed,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('R54 full source/artifact rehash andranking QA recovery passed; original failed scope retained.',flush=True)


if __name__=='__main__':main()
