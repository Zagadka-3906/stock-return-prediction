"""Mature raw63 factorization machines with matched first-order controls."""
from pathlib import Path
import importlib.util,sys,time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_factorization_machine_trainer_20261005',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
STORAGE=ROOT/'analysis/factorization_machine_storage_20261005.json'
OUT=Path(read(STORAGE)['output_directory']) if STORAGE.exists() else ROOT/'analysis/factorization_machine_bank_20261005'
YEARS=engine.YEARS
CONFIGS={f'{label}_fm_k{factors}_e32':{'kind':'factorization_machine','target':target,'latent_factors':factors,'epochs':32,'batch_size':32768,'learning_rate':.001,'weight_decay':.0001,'seed':20261005,'initial_factor_std':.01,'clip_z':8.,'chunk_rows':32768,'return_quantiles':[.005,.995],'return_target_scale':20.,'gradient_norm_max':10.,'reserve_available_ram_GiB':14.,'training_device':'cpu'} for label,target in (('rank','y_rank'),('return','y_ret_1d')) for factors in (0,8,32)}
engine.OUT,engine.CONFIGS=OUT,CONFIGS
def network(features,cfg):
    import torch
    class FM(torch.nn.Module):
        def __init__(self):
            super().__init__();self.bias=torch.nn.Parameter(torch.zeros(()));self.linear=torch.nn.Parameter(torch.zeros(features))
            self.factors=torch.nn.Parameter(torch.randn(features,cfg['latent_factors'])*cfg['initial_factor_std'])
        def forward(self,x):
            first=self.bias+x@self.linear
            if cfg['latent_factors']==0:return first
            return first+.5*((x@self.factors).square().sum(1)-(x.square()@self.factors.square()).sum(1))
    return FM()
def preprocessing(x):
    import numpy as np
    mean=np.zeros(x.shape[1],dtype=np.float64);scale=np.ones(x.shape[1],dtype=np.float64)
    for column in range(x.shape[1]):
        values=np.asarray(x[:,column],dtype=np.float64);values=values[np.isfinite(values)]
        if len(values):
            mean[column]=values.mean();deviation=values.std()
            if np.isfinite(deviation) and deviation>1e-5:scale[column]=deviation
    return mean,scale
def standardize(x,mean,scale,cfg):
    import numpy as np
    clean=np.empty(x.shape,dtype=np.float32)
    for offset in range(0,len(x),cfg['chunk_rows']):
        block=np.asarray(x[offset:offset+cfg['chunk_rows']],dtype=np.float64)
        block=np.where(np.isfinite(block),block,mean)
        clean[offset:offset+len(block)]=np.clip((block-mean)/scale,-cfg['clip_z'],cfg['clip_z'])
    return clean
def fit_arrays(x,y,cfg):
    import numpy as np,torch
    torch.set_num_threads(8);torch.manual_seed(cfg['seed']);torch.cuda.manual_seed_all(cfg['seed'])
    torch.use_deterministic_algorithms(True);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    mean,scale=preprocessing(x);clean=standardize(x,mean,scale,cfg)
    target=np.asarray(y,dtype=np.float64);assert len(target)==len(x) and np.isfinite(target).all()
    bounds=None;target_scale=1.
    if cfg['target']=='y_rank':target=(target-.5).astype(np.float32)
    else:
        bounds=[float(v) for v in np.quantile(target,cfg['return_quantiles'])];target_scale=cfg['return_target_scale']
        target=(np.clip(target,*bounds)*target_scale).astype(np.float32)
    device=cfg['training_device'];assert device=='cpu'
    xt=torch.from_numpy(clean).to(device);yt=torch.from_numpy(target).to(device)
    model=network(x.shape[1],cfg).to(device);optimizer=torch.optim.AdamW(model.parameters(),lr=cfg['learning_rate'],weight_decay=cfg['weight_decay'])
    objective=torch.nn.MSELoss() if cfg['target']=='y_rank' else torch.nn.HuberLoss(delta=.5)
    losses=[]
    for epoch in range(cfg['epochs']):
        order=torch.randperm(len(y),device=device);sum_loss=0.
        for offset in range(0,len(y),cfg['batch_size']):
            index=order[offset:offset+cfg['batch_size']];optimizer.zero_grad(set_to_none=True)
            loss=objective(model(xt[index]),yt[index]);assert bool(torch.isfinite(loss))
            loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),cfg['gradient_norm_max']);optimizer.step()
            sum_loss+=float(loss.detach())*len(index)
        losses.append(sum_loss/len(y))
        if epoch==0 or (epoch+1)%4==0:log(f"FM {cfg['target']} k{cfg['latent_factors']} epoch{epoch+1}/{cfg['epochs']} mature-training loss={losses[-1]:.8f}")
    weights={key:value.detach().cpu().numpy().copy() for key,value in model.state_dict().items()}
    assert all(np.isfinite(value).all() for value in weights.values())
    result={'kind':'factorization_machine','config':dict(cfg),'mean':mean,'scale':scale,'weights':weights,'target_bounds':bounds,'target_scale':target_scale,'target_units':cfg['target'],'training_losses':losses,'device':device,'actual_parameter_count':sum(value.size for value in weights.values()),'no_validation_early_stopping':True,'finite_missing_values_imputed_to_past_mean':True}
    del xt,yt,model,optimizer,clean,target;engine.gc.collect()
    if device=='cuda':torch.cuda.empty_cache()
    return result
def predict_arrays(bundle,x):
    import numpy as np
    assert bundle['kind']=='factorization_machine'
    cfg=bundle['config'];weights=bundle['weights'];linear=np.asarray(weights['linear'],dtype=np.float64);factors=np.asarray(weights['factors'],dtype=np.float64);bias=float(weights['bias'])
    result=np.empty(len(x),dtype=np.float64)
    for offset in range(0,len(x),cfg['chunk_rows']):
        z=standardize(x[offset:offset+cfg['chunk_rows']],bundle['mean'],bundle['scale'],cfg).astype(np.float64,order='F')
        values=np.full(len(z),bias,dtype=np.float64)
        for feature in range(z.shape[1]):values+=z[:,feature]*linear[feature]
        for latent in range(cfg['latent_factors']):
            accumulated=np.zeros(len(z),dtype=np.float64);squared=np.zeros(len(z),dtype=np.float64)
            for feature in range(z.shape[1]):
                contribution=z[:,feature]*factors[feature,latent];accumulated+=contribution;squared+=contribution*contribution
            values+=.5*(accumulated*accumulated-squared)
        result[offset:offset+len(z)]=values/bundle['target_scale']
    assert np.isfinite(result).all();return result
def enhanced_dump(path,payload,immutable=False):
    if path.name.startswith('info_') and payload.get('training_meta'):
        bundle=engine.load_bundle(path.parent/f"model_{payload['year']}.joblib")
        payload.update(new_model_fits=1,actual_parameter_count=bundle['actual_parameter_count'],completed_training_epochs=len(bundle['training_losses']),native_training_device=bundle['device'],actual_latent_factors=bundle['config']['latent_factors'])
    return dump(path,payload,immutable=immutable)
engine.fit_arrays,engine.predict_arrays,engine.dump=fit_arrays,predict_arrays,enhanced_dump
verify=engine.verify
def train_one(name,year):
    import psutil
    while not (OUT/name/f'info_{year}.json').exists() and psutil.virtual_memory().available<14*2**30:time.sleep(10)
    engine.train_one(name,year);return read(OUT/name/f'info_{year}.json')


def freeze():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / 'protocol.json').exists():
        verify()
        return
    proof = ROOT / 'analysis/factorization_machine_preflight_20261005/verification.json'
    assert read(proof)['status'] == 'passed_actual_factorization_formula_gradients_maturity_saved_models_andprefix_controls'
    paths = [Path(__file__), SOURCE, STORAGE, proof,
        ROOT / 'analysis/verify_factorization_machine_bank_20261005.py',
        ROOT / 'analysis/run_factorization_machine_bank_20261005.py',
        ROOT / 'analysis/prepare_factorization_machine_bank_20261005.py',
        ROOT / 'analysis/factorization_machine_bank_run_20261005.json',
        engine.FEATURE_FILE, engine.MANIFEST, ROOT / 'data/raw/训练集.csv',
        ROOT / 'run.py', ROOT / 'src/features.py', ROOT / '后续选模标准.md']
    paths += [ROOT / 'analysis/linear_bank_20261003' / name / f'info_{year}.json'
              for name in ('rank_ridge_l01', 'return_ridge_l01') for year in YEARS]
    dump(OUT / 'protocol.json', {'status': 'frozen_before30_actual_mature_annual_fits',
        'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'configurations': CONFIGS,
        'features': engine.feature_names(), 'years': YEARS, 'expected_annual_fits': 30,
        'expected_five_year_configurations': 6,
        'validation': 'Original2020–2024 expanding OOF and mature one-day label purge.',
        'contrast': 'Matched first-order and second-order factor ranks0/8/32;32 fixed epochs; rank and return targets; same optimizer and past raw63 rows.',
        'preprocessing': 'Past eligible rows per-column finite mean/std; float32 z clipped8; missing imputed to past mean; zero is valid; return quantiles.005/.995 past only.',
        'no_validation_early_stopping': True, 'selection_bias_uncorrected': True,
        'minimum_available_host_RAM_before_each_fit_GiB': 14.,
        'reserve_is_scheduling_policy_not_physical_boundary': True,
        'fulltraining_future_and_complete_output_quality_are_separate_pending_steps': True,
        'method_reference': 'https://www.libfm.org/libfm-1.42.manual.pdf',
        'versions': {name: engine.importlib.metadata.version(name) for name in ('torch', 'numpy', 'polars', 'joblib')},
        'new_quality_scores': 0, 'test_data_read': False,
        'input_sha256': {str(path.resolve()): sha(path) for path in paths}}, immutable=True)


def boundary_control(year, cfg, features):
    import numpy as np
    import polars as pl
    cutoff = engine.fold_cutoff(year)
    lazy = pl.scan_parquet(engine.FEATURE_FILE)
    cols = engine.KEYS + features + [c for c in ('y_rank', 'y_ret_1d', 'is_train', 'price_valid') if c not in features]
    past = engine.training_frame(lazy, cutoff, cfg).select(cols).head(4096).collect()
    future = lazy.filter(pl.col('is_train') & (pl.col('trade_date') >= cutoff)).select(cols).head(1024).collect()
    sample = pl.concat([past, future])
    poisoned = sample.with_columns([
        pl.when(pl.col('trade_date') >= cutoff).then(pl.lit(12345., dtype=sample.schema[c])).otherwise(pl.col(c)).alias(c)
        for c in ('y_rank', 'y_ret_1d')])
    clean = engine.training_frame(sample.lazy(), cutoff, cfg).collect()
    changed = engine.training_frame(poisoned.lazy(), cutoff, cfg).collect()
    assert clean.equals(changed)
    small = dict(cfg, epochs=2)
    x = engine.to_matrix(clean, features)
    a = fit_arrays(x, clean[cfg['target']].to_numpy(), small)
    b = fit_arrays(engine.to_matrix(changed, features), changed[cfg['target']].to_numpy(), small)
    assert all(np.array_equal(a['weights'][key],b['weights'][key]) for key in a['weights']) and a['target_bounds'] == b['target_bounds']
    assert np.array_equal(a['mean'], b['mean']) and np.array_equal(a['scale'], b['scale'])
    assert np.array_equal(predict_arrays(a, x), predict_arrays(b, x))
    return {'status': 'passed', 'year': year, 'cutoff_exclusive': cutoff,
        'control_training_rows': len(clean), 'boundary_future_label_poisoning_bit_identical': True,
        'actual2_epoch_control_models_and_past_preprocessing_bit_identical': True,
        'small_control_fits_excluded_from_actual_annual_counts': True, 'test_data_read': False}


def all_oof():
    import numpy as np
    import polars as pl
    import psutil
    freeze()
    features, checks = engine.feature_names(), []
    for name, cfg in CONFIGS.items():
        for year in YEARS:
            while not (OUT / name / f'info_{year}.json').exists() and psutil.virtual_memory().available < 14 * 2**30:
                time.sleep(10)
            boundary = OUT / f'boundary_control_{name}_{year}.json'
            if not boundary.exists():
                dump(boundary, boundary_control(year, cfg, features), immutable=True)
            info = train_one(name, year)
            reference = ROOT / 'analysis/linear_bank_20261003' / ('rank_ridge_l01' if cfg['target'] == 'y_rank' else 'return_ridge_l01') / f'info_{year}.json'
            baseline = read(reference)
            for key in ('rows', 'days', 'first', 'last', 'cutoff_exclusive', 'last_label_end',
                        'features', 'training_matrix_sha256', 'training_target_sha256', 'training_keys_sha256'):
                assert info['training_meta'][key] == baseline['training_meta'][key], key
            prefix_path = OUT / f'prefix_control_{name}_{year}.json'
            if not prefix_path.exists():
                frame = pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(engine.KEYS + features + ['price_valid']).sort('trade_date', 'ts_code').collect()
                cutoff = int(frame['trade_date'].unique().sort()[79])
                prefix = frame.filter(pl.col('trade_date') <= cutoff)
                values = predict_arrays(engine.load_bundle(OUT / name / f'model_{year}.joblib'), engine.to_matrix(prefix, features))
                values[~prefix['price_valid'].to_numpy()] = -1e6
                saved = pl.read_parquet(OUT / name / f'raw_{year}.parquet').filter(pl.col('trade_date') <= cutoff)
                assert prefix.select(engine.KEYS).equals(saved.select(engine.KEYS))
                assert np.array_equal(values, saved['pred_raw'].to_numpy())
                dump(prefix_path, {'status': 'passed', 'rows': len(prefix),
                    'actual_saved_model_cold80_day_prefix_bit_identical': True,
                    'original_mature_training_matrices_targets_andkeys_match': True,
                    'reference_info_sha256': sha(reference), 'test_data_read': False}, immutable=True)
                del frame, prefix, values, saved
                engine.gc.collect()
            checks.append({'model': name, 'year': year, 'boundary': read(boundary), 'prefix': read(prefix_path)})
    verify()
    dump(OUT / 'oof_audit.json', {'status': 'passed', 'actual_annual_fits': 30,
        'configurations': CONFIGS, 'checks': checks, 'new_quality_scores': 0,
        'complete_output_quality_and_final_future_controls_pending': True, 'test_data_read': False}, immutable=True)


if __name__ == '__main__':
    all_oof()
