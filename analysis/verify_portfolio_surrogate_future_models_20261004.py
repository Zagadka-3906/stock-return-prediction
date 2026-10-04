"""Actual copied full-training models andfuture-only-X prefix checks, no scores."""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'analysis'),str(ROOT)]
OUT=ROOT/'analysis/portfolio_surrogate_future_models_qa_20261004'


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    gate=ROOT/'analysis/portfolio_surrogate_bank_20261004/oof_audit.json'
    execution=ROOT/'analysis/portfolio_surrogate_bank_20261004/training_execution_scope.json'
    while not (gate.exists() and execution.exists()):time.sleep(10)
    assert read(execution)['status']=='passed'
    assert read(gate)['status']=='passed'
    import gc
    import shutil
    import threading
    import numpy as np
    import polars as pl
    import psutil
    import train_portfolio_surrogate_bank_20261004 as bank
    import portfolio_surrogate_model_sources_20261004 as router
    while psutil.virtual_memory().available<14*2**30:time.sleep(10)
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    sources=[Path(__file__),Path(bank.__file__),Path(router.__file__),bank.SOURCE,
        bank.OUT/'protocol.json',gate,execution,ROOT/'analysis/portfolio_bank_implementation_preflight_20261004/verification.json',
        ROOT/'deliveries/connected_topk0175_20261003/generation_inputs.parquet',
        ROOT/'deliveries/connected_topk0175_20261003/train_test.json']
    sources += list(bank.OUT.glob('*/info_202[0-4].json'))+list(bank.OUT.glob('*/model_202[0-4].joblib'))
    inputs={str(p.resolve()):bank.sha(p) for p in sources}
    bank.dump(OUT/'protocol.json',{'status':'frozen_before_fulltraining_andfuture_inference',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':inputs,
        'configurations':bank.CONFIGS,'rows':1599600,'days':344,'codes':4650,
        'new_quality_scores':0,'test_labels_read':False,
        'minimum_available_ram_before_fullfit_GiB':14.,'start_reserve_is_scheduling_rule':True,
        'scope':'Four native full-training model fits onmature past rows andactual fullfuture raw-signal replay. Complete output scheme selection andofficial future scoring are not performed.'},immutable=True)
    stopped=threading.Event();phase=['loading_future_X'];samples=[]
    def observe():
        with (OUT/'resource_samples.jsonl').open('x',encoding='utf-8') as stream:
            while not stopped.is_set():
                workers=[]
                try:
                    registry=ROOT/read(ROOT/'analysis/ongoing_optimization_state.json')['active_run_registry']
                    for entry in read(registry):
                        try:
                            for p in psutil.Process(entry['pid']).children(recursive=True):
                                try:
                                    command=' '.join(p.cmdline())
                                    if 'multiprocessing.spawn' in command and '--multiprocessing-fork' in command:workers.append(p.pid)
                                except psutil.Error:continue
                        except psutil.Error:continue
                except (FileNotFoundError,json.JSONDecodeError):pass
                row={'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'phase':phase[0],
                    'available_ram_bytes':psutil.virtual_memory().available,'qa_python_rss_bytes':psutil.Process().memory_info().rss,
                    'actual_official_worker_pids':sorted(set(workers))}
                stream.write(json.dumps(row,separators=(',',':'))+'\n');stream.flush();samples.append(row)
                stopped.wait(1.)
    thread=threading.Thread(target=observe,daemon=True);thread.start();checks=[];failure=None
    try:
        features=bank.engine.feature_names();assert len(features)==63
        test=pl.scan_parquet(bank.engine.FEATURE_FILE).filter(~pl.col('is_train')).select(bank.engine.KEYS+features+['price_valid']).sort('trade_date','ts_code').collect()
        expected=pl.read_parquet(ROOT/'deliveries/connected_topk0175_20261003/generation_inputs.parquet',columns=bank.engine.KEYS+['price_valid'])
        assert test.select(bank.engine.KEYS+['price_valid']).equals(expected)
        assert len(test)==1599600 and test['trade_date'].n_unique()==344 and test['ts_code'].n_unique()==4650
        x=bank.engine.to_matrix(test,features);valid=test['price_valid'].to_numpy()
        last=int(test['trade_date'].unique().sort()[79]);prefix=test.filter(pl.col('trade_date')<=last);px=bank.engine.to_matrix(prefix,features)
        for name,cfg in bank.CONFIGS.items():
            while psutil.virtual_memory().available<14*2**30:phase[0]=f'waiting_for_fullfit_reserve_{name}';time.sleep(10)
            phase[0]=f'fit_{name}';info=bank.train_one(name,2025)
            assert info['test_data_read'] is False and info['fulltraining_only_test_prediction_not_generated']
            assert info['training_meta']['last_label_end']<=info['training_meta']['cutoff_exclusive']<20250101
            model=bank.OUT/name/'model_2025.joblib';copied=OUT/f'{name}.joblib';shutil.copyfile(model,copied)
            assert bank.sha(model)==bank.sha(copied)==info['model_sha256']
            bank.dump(OUT/f'{name}_frozen_before_inference.json',{'model_sha256':info['model_sha256'],
                'training_info_sha256':bank.sha(bank.OUT/name/'info_2025.json'),
                'configuration':cfg,'test_labels_read':False,'new_quality_scores':0},immutable=True)
            phase[0]=f'predict_{name}';bundle=router.load_bundle(copied)
            pred=router.predict_arrays(bundle,x);replay=router.predict_arrays(router.load_bundle(copied),x)
            assert np.array_equal(pred,replay) and np.isfinite(pred).all()
            phase[0]=f'prefix_{name}';assert np.array_equal(pred[:len(prefix)],router.predict_arrays(router.load_bundle(copied),px))
            assert bundle['config']==cfg
            assert np.array_equal(pred[:131],bank.engine.predict_arrays(router.load_bundle(copied),x[:131]))
            pred[~valid]=-1e6
            raw=OUT/f'{name}_raw.parquet';test.select(bank.engine.KEYS).with_columns(pl.Series('pred_raw',pred)).write_parquet(raw)
            checks.append({'model':name,'model_sha256':info['model_sha256'],'raw_sha256':bank.sha(raw),
                'actual_full1599600_row_copied_model_reload_bit_identical':True,
                'actual80_day_prefix_bit_identical':True,'frozen_native_fitter131_row_prediction_bit_identical':True,
                'mature_training':info['training_meta'],'new_quality_scores':0,'test_labels_read':False})
            del pred,replay,bundle;gc.collect()
            print(f'Future mature portfolio-loss model checked: {name}',flush=True)
        for path,digest in inputs.items():assert bank.sha(path)==digest,path
    except BaseException as error:failure=f'{type(error).__name__}: {error}';raise
    finally:
        stopped.set();thread.join(timeout=10)
        bank.dump(OUT/'resource_summary.json',{'status':'passed' if failure is None else 'implementation_check_failed',
            'failure':failure,'samples':len(samples),'minimum_available_ram_bytes_sampled':min((s['available_ram_bytes'] for s in samples),default=None),
            'maximum_qa_python_rss_bytes_sampled':max((s['qa_python_rss_bytes'] for s in samples),default=None),
            'samples_with_actual_official_workers':sum(bool(s['actual_official_worker_pids']) for s in samples),
            'resource_samples_sha256':bank.sha(OUT/'resource_samples.jsonl'),
            'scope':'This actual fulltraining andnative future-replay QA only; sampled memory is not aphysical exhaustion proof.',
            'physical_resource_boundary_established':False,'test_labels_read':False},immutable=True)
    bank.dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'native_models':checks,'rows':1599600,'days':344,'codes':4650,
        'all4_fulltraining_models_mature_andcopied_model_replay_passed':True,
        'actual80_day_cold_model_prefix_controls_passed':True,'input_sha256':inputs,
        'resource_summary_sha256':bank.sha(OUT/'resource_summary.json'),
        'new_quality_scores':0,'test_labels_read':False,
        'scope':'Native raw predictions only; complete standalone androle output schemes still require official training validation, freezing, calibration andcandidate inference.'},immutable=True)


if __name__=='__main__':main()
