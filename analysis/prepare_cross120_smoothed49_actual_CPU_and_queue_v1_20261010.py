"""Admit actual own120 smoothing hypotheses on real TRAIN peers before queued full scoring."""
from pathlib import Path
import sys,importlib,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    import numpy as np,polars as pl
    import causal_neural_rank_smoothing_v1_20261010 as smoothing
    import immutable_prepared_rank_panel_cache_v1_20261010 as cache
    from cross120_after_complete169_native_stage_v2_20261010 import CODECS
    import run_Cross120Smoothed_after170_high_impact49_screen_v1_20261010 as runner
    framepath=A/'connected_validation_20261002/combined_fold_frame.parquet';parentpath=A/'optimization_20261003_r169/selected_validation.npy'
    frame=pl.read_parquet(framepath,columns=['ts_code','trade_date','flag_limit_up','price_valid']).head(13950);parent=np.load(parentpath,mmap_mode='r')[:13950]
    dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')];grid=frame['ts_code'].to_numpy().reshape(3,4650)
    assert np.all(grid==grid[0]) and np.array_equal(grid[0],np.asarray(sorted(grid[0]))) and len(set(grid[0]))==4650
    paths=[Path(__file__),Path(runner.__file__),Path(smoothing.__file__),Path(cache.__file__),framepath,parentpath];signals={}
    for recipe,pointer in runner.POINTERS.items():
        p=A/pointer;folder=Path(read(p)['output']);rawpath=folder/'combined_raw.parquet';proof=folder/'verification.json'
        assert read(proof)['rows_days_stocks']==[5635800,1212,4650]
        f=pl.read_parquet(rawpath).head(13950);assert f.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))
        signals[recipe]=f['pred_raw'].to_numpy();paths += [p,rawpath,proof]
    records=[];exact=lambda x,y:np.array_equal(np.asarray(x,dtype=np.float64).view('u8'),np.asarray(y,dtype=np.float64).view('u8'))
    for c in runner.cases()[1:]:
        raw=signals[c['recipe']];native=smoothing.smooth(raw,dates,valid,c['decay']);oracle=smoothing.smooth(raw,dates,valid,c['decay'],oracle=True);assert exact(native,oracle)
        value=cache.Panel(parent,native,dates,flags,valid).transform(c);codec=importlib.import_module(CODECS[c['kind']]);args=(c['role'],c['weight'],c['sign']) if c['kind']=='CDF' else (c['weight'],c['protect_fraction'],c['sign'])
        expected=codec.pandas_oracle(parent,oracle,dates,flags,valid,*args);assert exact(value,expected)
        if c['kind']=='CDF':assert exact(value[~codec.selected(flags,valid,c['role'])],parent[~codec.selected(flags,valid,c['role'])])
        else:codec.assert_invariants(parent,value,dates,flags,valid,c['protect_fraction'])
        for n in (4650,9300):
            signal=smoothing.smooth(raw[:n],dates[:n],valid[:n],c['decay']);prefix=cache.Panel(parent[:n],signal,dates[:n],flags[:n],valid[:n]).transform(c);assert exact(value[:n],prefix)
            poisoned=raw.copy();poisoned[n:]=np.arange(len(raw)-n)+98765.;changed=smoothing.smooth(poisoned,dates,valid,c['decay']);assert exact(native[:n],changed[:n])
        records.append({'configuration':c,'actual_rows':13950,'full_native_independent_Pandas_bits_exact':True,'cold4650_9300_bits_exact':True,'future_signal_poisoning_preserves_prefix_bits':True,'numeric_sha256':hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()})
    assert len(records)==48
    proof=A/'cross120_smoothed49_actual13950_TRAIN_CPU_controls_v1_20261010.json'
    create(proof,{'status':'passed48_actual_own120_TRAIN_smoothing_permutation_independent_prefix_and_future_signal_poisoning_controls','input_sha256':{str(p):sha(p) for p in paths},'records':records,'probe_parent_round':169,'predeclared_full_quality_parent_round':170,'no_quality_or_full_candidate_claimed_from_probe_parent':True,'new_quality_scores':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False})
    plan=A/'cross120_smoothed49_predeclared_training_only_selection_plan_v1_20261010.json'
    create(plan,{'status':'predeclared49_own120_causal_smoothed_forecasts_after_qualified170_TRAIN_only','parent_round':170,'cases':runner.cases(),'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(runner.__file__),Path(smoothing.__file__),Path(cache.__file__),proof,A/'immutable_prepared_rank_panel_cache_actual_full_TRAIN_benchmark_v1_20261010.json']},'actual_scoring_GATE':'actual_Dual120Consensus_after169_high_impact193_screen_v3_20261010','nonidentity_full_controls':48,'nonidentity_cold_prefix_controls':144,'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,'selected_full_native_stage_freeze_inference_and_registry_required_before_adoption':True})
    from handoff_ready_goss_full_execution_20261006 import start_service
    assert allowed();row=start_service('actual_Cross120Smoothed_after170_high_impact49_screen_v1_20261010',Path(runner.__file__).name,[],{str(p):sha(p) for p in [Path(runner.__file__),plan,proof]})
    create(A/'actual_Cross120Smoothed_after170_high_impact49_activation_v1_20261010.json',row)
    print({'actual_CPU_cases':48,'new_quality_scores':0,'queued_full_official_cases':49,'worker_pid':row['owned_worker_pid']},flush=True)

if __name__=='__main__':main()
