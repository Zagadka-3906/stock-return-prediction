"""Replace only an exactly idle checkpointed CPU trainer and its unstarted control waiter."""
from pathlib import Path
import sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    import numpy as np,polars as pl,psutil
    bank=A/'nonflag_residual_RFF128Low_bank10_20261007'
    old_bank_folder=A/'service_owned_workflows_20261006/nonflag_residual_RFF128Low_native_bank10'
    old_control_folder=A/'service_owned_workflows_20261006/nonflag_RFF128Low_actual_hook6_and_full73_controls'
    bank_row=read(old_bank_folder/'native_launch.json');control_row=read(old_control_folder/'native_launch.json')
    assert owned(bank_row) and owned(control_row) and not (bank/'verification.json').exists()
    assert not (A/'nonflag_residual_RFF128Low_native_hook6_preflight_20261007').exists()
    assert not (A/'nonflag_residual_RFF128Low73_transform_preflight_20261007').exists()
    preserved={n:read(A/'service_owned_workflows_20261006'/n/'native_launch.json') for n in ('neural16384_annual','dependency_queue_v12_local_cache')}
    assert all(owned(r) for r in preserved.values())
    out=A/'RFF128Low_checkpoint_memory_release_actual_handoff_20261007';assert not out.exists();out.mkdir()
    held=[];retired=False
    try:
        bp,bw,bidle=suspended_idle(bank_row,'    main (train_nonflag_residual_RFF128Low_bank10_v1_20261007.py:65)');held.extend((bw,bp))
        cp,cw,cidle=suspended_idle(control_row,'    main (run_nonflag_residual_RFF128Low_hook6_after_bank_20261007.py:12)');held.extend((cw,cp))
        assert not bw.children() and not cw.children()
        plan=read(A/'nonflag_residual_RFF128Low10_plan_20261007.json');infos=sorted(bank.glob('*/info_*.json'))
        assert 0<len(infos)<10 and len(infos)%2==0
        records=[read(p) for p in infos];years=sorted({r['year'] for r in records})
        assert years==list(range(2021,max(years)+1))
        assert {(r['name'],r['year']) for r in records}=={(n,y) for n in plan['configurations'] for y in years}
        assert read(bank/'actual_stage.json')['actual_completed_native_fits']==len(infos)
        immutable={}
        for p,r in zip(infos,records):
            assert r['native_reload_independent_all_prediction_bits_exact']
            for q,d in [(p,sha(p)),(Path(r['native_model_path']),r['native_model_sha256']),
              (Path(r['independent_random_fourier_linear_state_path']),r['independent_random_fourier_linear_state_sha256'])]:
                assert sha(q)==d;immutable[str(q)]=d
        dates=pl.read_parquet(A/'connected_validation_20261002/combined_fold_frame.parquet',columns=['trade_date'])['trade_date'].to_numpy()
        cutoff=(max(years)+1)*10000+101;size=int(np.count_nonzero(dates<cutoff))
        assert np.all(dates[:size]<cutoff) and np.all(dates[size:]>=cutoff)
        prefix={}
        for name in plan['configurations']:
            array=np.load(bank/name/'nonflag_oof_predictions.npy',mmap_mode='r')
            prefix[name]=hashlib.sha256(memoryview(np.ascontiguousarray(array[:size])).cast('B')).hexdigest()
            del array
        sources=read(A/'RFF128Low_memory_release_resume_source_preparation_20261007.json')['input_sha256']
        for p,d in sources.items():assert sha(p)==d,p
        snapshot=A/'RFF128Low_checkpoint_resume_snapshot_20261007.json'
        create(snapshot,{'status':'verified_owned_idle_bank_saved_complete_years_before_memory_release_resume',
          'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'original_owned_bank_identity':bank_row,'original_idle_stack':bidle,
          'saved_native_fit_count':len(infos),'saved_complete_years':years,'immutable_saved_file_sha256':immutable,
          'preserved_prefix_rows':size,'oof_prefix_numeric_sha256':prefix,'input_sha256':sources,
          'existing_original_freeze_preserved':str(bank/'frozen_before_actual_training.json'),
          'no_unsaved_fit_at_handoff':True,'original_GPU_or_queue_stopped':False,'test_labels_read':False})
        create(out/'actual_waiters_before_replacement.json',{'bank':bidle,'controls':cidle,'RAM_before_replacement_GiB':psutil.virtual_memory().available/2**30})
        cw.terminate();cw.wait(timeout=15);cp.terminate();cp.wait(timeout=15)
        bw.terminate();bw.wait(timeout=15);bp.terminate();bp.wait(timeout=15);retired=True
        create(old_bank_folder/'administrative_checkpoint_resume_20261007.json',{'status':'checkpointed_idle_training_worker_replaced_not_claimed_scientifically_complete',
          'identity':bank_row,'saved_native_fits_preserved':len(infos),'unsaved_fits_lost':0,'actual_bank_fits_still_required':10-len(infos)})
        create(old_control_folder/'administrative_unstarted_controls_supersession_20261007.json',{'status':'zero_control_waiter_replaced_not_claimed_scientifically_complete','identity':control_row,'actual_controls_before_replacement':0})
        pins={**sources,str(snapshot):sha(snapshot),str(Path(__file__)):sha(__file__),**immutable}
        bank_new=start_service('nonflag_residual_RFF128Low_native_bank10_v2','train_nonflag_residual_RFF128Low_bank10_v2_20261007.py',[],pins)
        control_new=start_service('nonflag_RFF128Low_actual_hook6_and_full73_controls_v2','run_nonflag_RFF128Low_actual_controls_v2_20261007.py',[],pins)
        assert all(owned(r) for r in preserved.values())
        create(out/'verification.json',{'status':'passed_actual_checkpointed_idle_CPU_bank_resume_with_saved_models_and_prefix_bytes_preserved',
          'input_sha256':pins,'new_bank_identity':bank_new,'new_controls_identity':control_new,
          'saved_native_fits_preserved':len(infos),'active_fits_stopped':0,'unsaved_fit_progress_lost':0,
          'checkpointed_idle_training_worker_replaced':1,'original_GPU_and_queue_identities_preserved':preserved,
          'RAM_after_old_waiters_closed_GiB':psutil.virtual_memory().available/2**30,
          'new_fits_by_handoff':0,'new_quality_scores':0,'test_labels_read':False})
    finally:
        if not retired:
            for p in reversed(held):
                if p.is_running():p.resume()
if __name__=='__main__':main()
