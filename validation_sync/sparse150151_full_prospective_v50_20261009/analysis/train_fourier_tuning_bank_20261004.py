"""One-day raw-plus-random-Fourier ridge with past-only normalization and fixed projections."""
from pathlib import Path
import argparse
import importlib.util
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_fourier_tuning_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/fourier_tuning_bank_20261004'
VARIANTS=(('c256_mass128',256,.1,20261004),('c512_mass128',512,.1,20261004),
          ('c128_l0001',128,.001,20261004),('c128_l1',128,1.,20261004),
          ('c128_seed20261005',128,.1,20261005))
CONFIGS={f'{label}_fourier_tuning_{suffix}':{'kind':'ridge_fourier','target':target,'ridge_lambda':penalty,
          'chunk_rows':32768,'clip_z':8.,'lengthscale':1.,'random_components':components,'seed':seed,
          'fixed_fourier_mass':128.,'reserve_available_ram_GiB':8.,'return_quantiles':[.005,.995]}
         for label,target in (('rank','y_rank'),('return','y_ret_1d'))
         for suffix,components,penalty,seed in VARIANTS}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS


def random_basis(cfg,raw_width):
    import numpy as np
    gamma=.5/(raw_width*cfg['lengthscale']**2)
    rng=np.random.RandomState(cfg['seed'])
    weights=rng.normal(size=(raw_width,cfg['random_components']))*np.sqrt(2*gamma)
    phase=rng.uniform(0,2*np.pi,size=cfg['random_components'])
    return weights,phase,gamma


def transform(x,mean,scale,cfg,weights,phase):
    import numpy as np
    result=[];batch=cfg['chunk_rows']
    for offset in range(0,len(x),batch):
        values=np.asarray(x[offset:offset+batch],dtype=np.float64)
        z=np.clip((np.where(np.isfinite(values),values,mean)-mean)/scale,-cfg['clip_z'],cfg['clip_z'])
        # All projected blocks have fixed dimensions, including short prefixes.
        padded=np.zeros((batch,len(mean)),dtype=np.float64);padded[:len(z)]=z
        projected=padded@weights
        random=np.sqrt(2.*cfg['fixed_fourier_mass']/cfg['random_components'])*np.cos(projected[:len(z)]+phase)
        result.append(np.concatenate([z,random],axis=1))
    return np.concatenate(result) if result else np.empty((0,len(mean)+len(phase)),dtype=np.float64)


def fit_arrays(x,y,cfg):
    import numpy as np
    mean=np.nanmean(x,axis=0,dtype=np.float64)
    mean=np.where(np.isfinite(mean),mean,0.)
    scale=np.nanstd(x,axis=0,dtype=np.float64)
    scale=np.where(np.isfinite(scale)&(scale>1e-5),scale,1.)
    target=np.asarray(y,dtype=np.float64)
    assert np.isfinite(target).all() and len(target)==len(x)
    bounds=None
    if cfg['target']=='y_ret_1d':
        low,high=np.quantile(target,cfg['return_quantiles'])
        target=np.clip(target,low,high);bounds=[float(low),float(high)]
    weights,phase,gamma=random_basis(cfg,x.shape[1])
    n=len(x);width=x.shape[1]+cfg['random_components'];sum_x=np.zeros(width);sum_y=float(target.sum())
    sum_xx=np.zeros((width,width));sum_xy=np.zeros(width)
    for offset in range(0,n,cfg['chunk_rows']):
        z=transform(x[offset:offset+cfg['chunk_rows']],mean,scale,cfg,weights,phase)
        labels=target[offset:offset+len(z)]
        sum_x+=z.sum(axis=0);sum_xx+=z.T@z;sum_xy+=z.T@labels
    center=sum_x/n;target_mean=sum_y/n
    covariance=sum_xx/n-np.outer(center,center)
    cross=sum_xy/n-center*target_mean
    normal=covariance+cfg['ridge_lambda']*np.eye(width)
    coefficients=np.linalg.solve(normal,cross)
    intercept=target_mean-float(center@coefficients)
    assert np.isfinite(coefficients).all() and np.isfinite(intercept)
    residual=float(np.max(np.abs(normal@coefficients-cross)))
    assert residual<1e-10
    return {'kind':'ridge_fourier','mean':mean,'scale':scale,'coefficients':coefficients,
            'intercept':intercept,'config':dict(cfg),'random_weights':weights,'random_phase':phase,'gamma':gamma,'target_bounds':bounds,
            'normal_equation_max_abs_residual':residual,'target_units':cfg['target'],
            'ridge_penalty_equivalent_sklearn_alpha':float(cfg['ridge_lambda']*n)}


def predict_arrays(bundle,x):
    import numpy as np
    parts=[];cfg=bundle['config']
    for offset in range(0,len(x),cfg['chunk_rows']):
        z=transform(x[offset:offset+cfg['chunk_rows']],bundle['mean'],bundle['scale'],cfg,bundle['random_weights'],bundle['random_phase'])
        # Fixed per-row reduction avoids batch-size-dependent BLAS kernels.
        parts.append(np.einsum('ij,j->i',z,bundle['coefficients'],optimize=False)+bundle['intercept'])
    return np.concatenate(parts) if parts else np.empty(0,dtype=np.float64)


engine.fit_arrays=fit_arrays;engine.predict_arrays=predict_arrays


def verify():return engine.verify()


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),ROOT/'analysis/prepare_fourier_tuning_bank_20261004.py',ROOT/'analysis/fourier_tuning_sources_prepared_20261004.json',ROOT/'analysis/train_fourier_ridge_bank_20261004.py',SOURCE,engine.FEATURE_FILE,engine.MANIFEST,
             ROOT/'data/raw/训练集.csv',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md',
             ROOT/'analysis/fourier_tuning_model_sources_20261004.py',
             ROOT/'analysis/verify_fourier_tuning_bank_20261004.py',ROOT/'analysis/fourier_tuning_preflight_20261004/verification.json']
    assert read(sources[-1])['status']=='passed'
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'configurations':CONFIGS,'features':engine.feature_names(),'years':YEARS,
         'validation':'2020–2024 annual expanding OOF; identical mature-label purge',
         'objective':'Mean squared loss plus lambda*sum(coefficients**2), with unpenalized intercept; use the supplied centered one-day rank label or one-day return label.',
         'preprocessing':'Past mature training rows fit raw63 mean/std and missing imputation; clip z to [-8,8]. Append128/256/512 fixed seeded cosine features sqrt(2*128/components)*cos(z@W+phase), total191/319/575 columns. Fixed mass128 preserves the Fourier component kernel scale across capacity variants. Gaussian W gamma=.5/(63*lengthscale**2), random phase uniform[0,2pi]. Seed/projection dimensions/lengthscales fixed before any validation scoring; no feature-data sampling or future quantiles. Return winsor bounds use past fold only.',
         'inference':'Fixed padded32768-row float64 matrix projection and per-row final einsum; validate bit-identical prefix/reload. All Fourier amplitudes equal sqrt128 times standard RBFSampler output, independent of feature count.',
         'method_reference':'https://scikit-learn.org/stable/modules/kernel_approximation.html',
         'versions':{name:engine.importlib.metadata.version(name) for name in ('numpy','scikit-learn','polars','joblib')},
         'raw_linear_comparison':'Use matching one-day raw63 rank/return linear-ridge targets and penalties; fixed Fourier features add a nonlinear joint-feature family. Compare as complete calibrated output schemes.',
         'scheduling_reserve':'Chosen8GiB available-memory reserve before each full annual fit; not a measured model memory requirement or hardware exhaustion boundary.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,
         'test_data_read':False,'expected_annual_fits':50,
         'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('Ten matched Fourier capacity/penalty/seed controls frozen')


def train_one(name,year):
    import psutil
    if not (OUT/name/f'info_{year}.json').exists():
        last_notice=time.monotonic()
        while psutil.virtual_memory().available<CONFIGS[name]['reserve_available_ram_GiB']*2**30:
            time.sleep(10)
            if time.monotonic()-last_notice>=50:
                log(f'Waiting for Fourier fit scheduling reserve: {name} year{year}')
                last_notice=time.monotonic()
    return engine.train_one(name,year)


def all_oof():
    import numpy as np
    import polars as pl
    gate=ROOT/'analysis/nonlinear_stacking_future_pipelines_qa_20261004/verification.json'
    while not gate.exists():time.sleep(10)
    assert read(gate)['status']=='passed'
    freeze();features=engine.feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            path=OUT/f'boundary_control_{name}_{year}.json'
            if not path.exists():dump(path,engine.boundary_control(year,cfg,features),immutable=True)
            proofs[f'{name}_{year}']=read(path);info=train_one(name,year)
            linear_name=('rank' if cfg['target']=='y_rank' else 'return')+'_ridge_l01'
            reference=read(ROOT/'analysis/linear_bank_20261003'/linear_name/f'info_{year}.json')
            for field in ('training_matrix_sha256','training_target_sha256','training_keys_sha256'):
                assert info['training_meta'][field]==reference['training_meta'][field],field
            replay_path=OUT/f'prefix_control_{name}_{year}.json'
            if not replay_path.exists():
                frame=pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).select(engine.KEYS+features+['price_valid']).sort('trade_date','ts_code').collect()
                last=int(frame['trade_date'].unique().sort()[79]);prefix=frame.filter(pl.col('trade_date')<=last)
                predicted=predict_arrays(engine.load_bundle(OUT/name/f'model_{year}.joblib'),engine.to_matrix(prefix,features))
                predicted[~prefix['price_valid'].to_numpy()]=-1e6
                raw=pl.read_parquet(OUT/name/f'raw_{year}.parquet').filter(pl.col('trade_date')<=last)
                assert prefix.select(engine.KEYS).equals(raw.select(engine.KEYS))
                assert np.array_equal(predicted,raw['pred_raw'].to_numpy())
                dump(replay_path,{'status':'passed','complete_first_days':80,'rows':len(prefix),
                     'actual_saved_model_prefix_bit_identical':True,'raw_linear_training_keys_features_targets_bit_identical':True,
                     'reference_info_sha256':sha(ROOT/'analysis/linear_bank_20261003'/linear_name/f'info_{year}.json'),
                     'test_data_read':False},immutable=True)
                del frame,prefix,predicted,raw
                engine.gc.collect()
            proofs[f'{name}_{year}']['actual_prefix_control']=read(replay_path)
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'boundary_controls':proofs,'test_data_read':False,'models_trained':50},immutable=True)
    log('All50 matched Fourier tuning fold models and mature-label controls completed')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'))
    parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
