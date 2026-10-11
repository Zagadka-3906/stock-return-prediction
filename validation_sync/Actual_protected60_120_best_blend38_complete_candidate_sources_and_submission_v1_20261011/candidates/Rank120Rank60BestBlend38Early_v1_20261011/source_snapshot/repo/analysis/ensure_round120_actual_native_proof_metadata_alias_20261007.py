"""Keep a legacy generic registry proof filename tied to the actual whole nonflag replay."""
from pathlib import Path
import sys,time,os
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle,stack

def main():
    out=A/'round120_actual_native_proof_metadata_alias_20261007';assert not out.exists();out.mkdir()
    release=A/'nonflag_HGB40_selected_release_v4_20261007';candidate=ROOT/'candidates/nonflag_HGB40_v4_20261007'
    assert not (release/'inference_ready.json').exists() and not candidate.exists(), 'Only install this guard before selected future inference'
    import prepare_nonflag_HGB40_round120_sources_v4_20261007 as generator
    text=generator.generate(119)['register_nonflag_HGB40_round120_artifacts_20261007.py']
    assert "SOURCE_CANDIDATE / ('refined_quantile_HGB_native_replay_verification.json' if READY['new_inference_claimed'] else 'verification.json')" in text
    sealer=A/'service_owned_workflows_20261006/nonflag_HGB40_selected_candidate_sealing_v4'
    identity=read(sealer/'native_launch.json');assert owned(identity)
    driver=Path(read(sealer/'job_definition.json')['driver']);lines=driver.read_text(encoding='utf8').splitlines();before=stack(identity['owned_worker_pid'])
    possible=[f'({driver.name}:{i+1})' for i,line in enumerate(lines) if 'time.sleep(' in line and f'({driver.name}:{i+1})' in before]
    assert len(possible)==1,(identity['owned_worker_pid'],before)
    parent,worker,idle=suspended_idle(identity,possible[0]);held=True
    create(out/'actual_original_sealer_exact_idle_guard.json',{'status':'held_only_original_idle_sealing_helper_before_manifest','identity':identity,'actual_idle':idle,
        'native_training_and_future_inference_workers_suspended':0,'generic_legacy_metadata_literal':"refined_quantile_HGB_native_replay_verification.json"})
    try:
        prep=A/'service_owned_workflows_20261006/nonflag_HGB40_selected_candidate_preparation_v4'
        while owned(read(prep/'native_launch.json')):time.sleep(10)
        assert read(prep/'service_execution.json')['status']=='passed'
        ready=read(release/'inference_ready.json')
        if not ready['new_inference_claimed']:
            create(out/'verification.json',{'status':'passed_exact_anchor_reuse_no_new_metadata_alias_required','actual_source_candidate':ready['source_candidate'],
                'new_inference_claimed':False,'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False})
        else:
            assert Path(ready['source_candidate']).resolve()==candidate.resolve() and not (candidate/'manifest.json').exists()
            source=candidate/'nonflag_residual_HGB_native_replay_verification.json'; proof=read(source)
            assert proof['status']=='passed_actual_complete_parent_and_nonflag_HGB_two_full_replays_independent_and_cold80'
            assert len([c for c in proof['calls'] if c['rows']==1599600])>=2 and len([c for c in proof['calls'] if c['rows']==80*4650])>=1
            actual=read(candidate/'verification.json');assert actual['status']=='passed' and len(actual['models'])==proof['actual_models']==ready['actual_saved_native_models']
            for k in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert actual[k]
            assert sha(candidate/'submission.csv')==actual['csv_sha256']
            snapshot=read(Path(ready['pre_inference_source_snapshot'])/'manifest.json'); relative=Path(__file__).relative_to(ROOT).as_posix()
            assert snapshot['files'][relative]['sha256']==sha(__file__), 'Guard source must be frozen before selected future inference'
            alias=candidate/'refined_quantile_HGB_native_replay_verification.json'
            assert alias.resolve().is_relative_to(candidate.resolve()) and not alias.exists()
            source_sha=sha(source);os.link(source,alias);assert os.path.samefile(source,alias) and sha(alias)==source_sha
            record={'status':'passed_byte_exact_alias_of_actual_complete_nonflag_HGB_replay_for_legacy_generic_registry_pointer',
                'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'actual_verification_source':str(source),'actual_source_status':proof['status'],
                'actual_verification_sha256':source_sha,'legacy_metadata_alias':str(alias),'legacy_alias_sha256':sha(alias),
                'actual_saved_native_models':proof['actual_models'],'same_physical_file':True,'created_before_candidate_manifest':True,
                'guard_source_in_original_pre_inference_snapshot':True,'separate_quantile_inference_not_claimed':True,
                'original_inference_freeze_timestamp_unchanged':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False}
            create(candidate/'legacy_generic_native_proof_filename_alias_verification.json',record);create(out/'verification.json',record)
        worker.resume();parent.resume();held=False
        create(out/'original_sealer_resumed_after_actual_proof_guard.json',{'status':'resumed_same_original_sealing_identity','identity':identity,
            'scientific_workers_restarted_or_terminated':0,'new_quality_scores':0,'test_labels_read':False})
        print({'status':'passed_actual_metadata_guard','new_inference':ready['new_inference_claimed']},flush=True)
    finally:
        if held:
            for p in (worker,parent):
                if p.is_running():p.resume()
if __name__=='__main__':main()
