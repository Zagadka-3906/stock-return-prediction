"""Freeze real twenty-session targets, an independent decoder, and own replay/training sources."""
from pathlib import Path
import sys,os
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[k]='2'
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    import numpy as np,polars as pl
    import forward20_mature_training_labels_v1_20261010 as labels
    import neural_BF16_medium2048_forward20huber050_seed09_e64_native_v1_20261009 as native
    from run import FEATURE_FILE,feature_names,to_matrix
    folder=Path('E:/赛题五_本机临时/Forward20Huber050_past_fixture_v2_20261010');folder.mkdir(exist_ok=False)
    features=feature_names();cutoff=20191231
    frame=labels.training_frame(pl.scan_parquet(FEATURE_FILE),cutoff,native.CONFIG).select(['ts_code','trade_date',*features,'y_ret_20mean','label_end_20d']).limit(49153).collect()
    assert len(frame)==49153 and len(features)==63
    x=to_matrix(frame,features);y=frame['y_ret_20mean'].to_numpy()
    last=int(frame['trade_date'].max());end=int(frame['label_end_20d'].max())
    assert last<end<cutoff and np.isfinite(y).all()
    np.save(folder/'past_features.npy',x,allow_pickle=False);np.save(folder/'past_return_targets.npy',y,allow_pickle=False)
    create(folder/'verification.json',{'status':'passed_actual49153_real_mature20day_mean_training_return_fixture','rows':len(frame),'features':features,'last':last,'last_label_end':end,'cutoff_exclusive':cutoff,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(native.__file__),Path(labels.__file__),FEATURE_FILE,folder/'past_features.npy',folder/'past_return_targets.npy']},'actual_native_fits':0,'test_labels_read':False})
    create(A/'actual_Forward20Huber050_past_fixture_location_v2_20261010.json',{'output':str(folder),'verification_sha256':sha(folder/'verification.json')})
    route=lambda s:s.replace('returnhuber050','forward20huber050').replace('ReturnHuber050166','Forward20Huber050167').replace('ReturnHuber050','Forward20Huber050').replace('Forward20Huber050_past_fixture_location_v1_20261010','Forward20Huber050_past_fixture_location_v2_20261010')
    outputs={}
    # Preserve the initial wrong decoder and plan as an unadopted prototype.
    old=A/'neural_BF16_medium2048_forward20huber050_seed09_independent_forward_v1_20261009.py'
    corrected=old.read_text(encoding='utf8').replace("config['target']=='y_ret_1d'","config['target']=='y_ret_20mean'").replace('==20.','==100.').replace('/20.','/100.')
    decoder='neural_BF16_medium2048_forward20huber050_seed09_independent_forward_v2_20261010.py'
    outputs[decoder]=corrected
    originals=['verify_neural_BF16_medium2048_returnhuber050_seed09_restart_v1_20261009.py','verify_BF16ReturnHuber050166_independent_small_CPU_v1_20261009.py','verify_BF16ReturnHuber050166_full5_independent_GPU_v1_20261009.py','BF16ReturnHuber050166_complete_parent_native_stage_v1_20261009.py','verify_BF16ReturnHuber050166_native42_calendar_v1_20261009.py']
    for name in originals:
        text=route((A/name).read_text(encoding='utf8')).replace('neural_BF16_medium2048_forward20huber050_seed09_independent_forward_v1_20261009',decoder[:-3])
        outputs[route(name)]=text
    trainer=route((A/'train_neural_BF16_medium2048_returnhuber050_seed09_e64_bank6_v1_20261009.py').read_text(encoding='utf8'))
    trainer=trainer.replace('\n\ndef main():','\nimport forward20_mature_training_labels_v1_20261010 as labels\n\ndef main():',1)
    trainer=trainer.replace('native.architecture.training_frame','labels.training_frame').replace("['y_ret_1d']).sort","['y_ret_20mean','label_end_20d']).sort").replace("train['y_ret_1d'].to_numpy()","train['y_ret_20mean'].to_numpy()")
    trainer=trainer.replace('label_end = int(all_dates[np.searchsorted(all_dates, last) + 1])',"label_end = int(train['label_end_20d'].max())").replace('label_end <= cutoff','label_end < cutoff')
    begin=trainer.index('        past = labels.training_frame(')
    endpos=trainer.index("        meta =",begin)
    trainer=trainer[:begin]+'''        past_dates=all_dates[all_dates<cutoff][-60:]
        past=lazy.filter(pl.col('is_train') & pl.col('trade_date').is_in(past_dates.tolist())).select(cols).collect()
        # Synthetic later labels prove invariance without reading actual future X/Y.
        later=past.head(1024).with_columns(pl.lit(cutoff).cast(past.schema['trade_date']).alias('trade_date'))
        sample=pl.concat([past,later])
        poisoned=sample.with_columns([pl.when(pl.col('trade_date')>=cutoff).then(pl.lit(12345.,dtype=sample.schema[c])).otherwise(pl.col(c)).alias(c) for c in ('y_rank','y_ret_1d')])
        baseline=labels.training_frame(sample.lazy(),cutoff,native.CONFIG).collect()
        assert len(baseline)>0 and baseline.equals(labels.training_frame(poisoned.lazy(),cutoff,native.CONFIG).collect())
        assert int(baseline['label_end_20d'].max())<cutoff
        del baseline
''' + trainer[endpos:]
    trainer=trainer.replace("'one_day_label_boundary_purged': True","'twenty_day_label_boundary_purged': True, 'label_horizon_trading_days':20")
    trainer=trainer.replace("FEATURE_FILE, MANIFEST, control / 'verification.json'","FEATURE_FILE, MANIFEST, control / 'verification.json', Path(labels.__file__), A/'forward20_mature_training_labels_actual_CPU_controls_v1_20261010.json', A/'Forward20Huber050_independent_targets_loss_gradient_controls_v1_20261010.json'")
    trainer=trainer.replace("'actual_future_training_label_poisoning_population_exact': True","'actual_synthetic_future_label_poisoning_nonempty_population_exact': True, 'label_horizon_trading_days':20")
    outputs['train_neural_BF16_medium2048_forward20huber050_seed09_e64_bank6_v1_20261009.py']=trainer
    for name,text in outputs.items():assert not (A/name).exists();compile(text,str(A/name),'exec')
    for name,text in outputs.items():(A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'Forward20Huber050_own_bank_controls_source_admission_v2_20261010.json',{'status':'passed_real49153_mature20day_fixture_and_compiled_own_restart_CPU_full5_native42_trainer','input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(native.__file__),Path(labels.__file__),*[A/n for n in outputs],folder/'verification.json',A/'Forward20Huber050_independent_targets_loss_gradient_controls_v1_20261010.json']},'unadopted_initial_decoder':str(old),'corrected_target_scale':100.,'actual_annual_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print('PASS real mature20day49153 fixture, independent100x decoder and own sources; GPU controls pending',flush=True)
if __name__=='__main__':main()
