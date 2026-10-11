"""One-day additive hinge-basis ridge with frozen causal preprocessing."""
from pathlib import Path
import argparse
import importlib.util
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_additive_ridge_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/additive_ridge_bank_20261004'
CONFIGS={f'{label}_additive_ridge_{suffix}':{'kind':'ridge_additive','target':target,'ridge_lambda':value,
          'chunk_rows':32768,'clip_z':8.,'hinge_knots':[-1.,0.,1.],'reserve_available_ram_GiB':8.,'return_quantiles':[.005,.995]}
         for label,target in (('rank','y_rank'),('return','y_ret_1d'))
         for suffix,value in (('l0001',.001),('l01',.1),('l1',1.))}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS


def transform(x,mean,scale,clip,knots):
    import numpy as np
    values=np.asarray(x,dtype=np.float64)
    z=np.clip((np.where(np.isfinite(values),values,mean)-mean)/scale,-clip,clip)
    return np.concatenate([z,*[np.maximum(z-knot,0.) for knot in knots]],axis=1)


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
    n=len(x);width=x.shape[1]*(1+len(cfg['hinge_knots']));sum_x=np.zeros(width);sum_y=float(target.sum())
    sum_xx=np.zeros((width,width));sum_xy=np.zeros(width)
    for offset in range(0,n,cfg['chunk_rows']):
        z=transform(x[offset:offset+cfg['chunk_rows']],mean,scale,cfg['clip_z'],cfg['hinge_knots'])
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
    return {'kind':'ridge_additive','mean':mean,'scale':scale,'coefficients':coefficients,
            'intercept':intercept,'config':dict(cfg),'target_bounds':bounds,
            'normal_equation_max_abs_residual':residual,'target_units':cfg['target'],
            'ridge_penalty_equivalent_sklearn_alpha':float(cfg['ridge_lambda']*n)}


def predict_arrays(bundle,x):
    import numpy as np
    parts=[];cfg=bundle['config']
    for offset in range(0,len(x),cfg['chunk_rows']):
        z=transform(x[offset:offset+cfg['chunk_rows']],bundle['mean'],bundle['scale'],cfg['clip_z'],cfg['hinge_knots'])
        # Fixed per-row reduction avoids batch-size-dependent BLAS kernels.
        parts.append(np.einsum('ij,j->i',z,bundle['coefficients'],optimize=False)+bundle['intercept'])
    return np.concatenate(parts) if parts else np.empty(0,dtype=np.float64)


engine.fit_arrays=fit_arrays;engine.predict_arrays=predict_arrays


def verify():return engine.verify()


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),SOURCE,engine.FEATURE_FILE,engine.MANIFEST,
             ROOT/'data/raw/训练集.csv',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md',
             ROOT/'analysis/additive_ridge_model_sources_20261004.py',
             ROOT/'analysis/verify_additive_ridge_bank_20261004.py',ROOT/'analysis/additive_ridge_preflight_20261004/verification.json']
    assert read(sources[-1])['status']=='passed'
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'configurations':CONFIGS,'features':engine.feature_names(),'years':YEARS,
         'validation':'2020–2024 annual expanding OOF; identical mature-label purge',
         'objective':'Mean squared loss plus lambda*sum(coefficients**2), with unpenalized intercept; use the supplied centered one-day rank label or one-day return label.',
         'preprocessing':'Past mature target-eligible rows fit raw63 mean/std and missing imputation; clip z to [-8,8]. Fixed basis order: z followed by max(z-k,0) for k=-1,0,1, yielding252 columns. All knots fixed before validation, no feature interactions or future quantiles. Return winsor bounds use past fold only.',
         'inference':'Fixed float64 per-row einsum reduction, invariant to row prefix and inference batch boundaries.',
         'raw_linear_comparison':'Use matching one-day raw63 rank/return linear-ridge targets and penalties; fixed hinges add an independent nonlinear additive family. Compare as complete calibrated output schemes.',
         'scheduling_reserve':'Chosen8GiB available-memory reserve before each full annual fit; not a measured model memory requirement or hardware exhaustion boundary.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,
         'test_data_read':False,'expected_annual_fits':30,
         'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('Six additive hinge-basis ridge configurations frozen')


def train_one(name,year):
    import psutil
    if not (OUT/name/f'info_{year}.json').exists():
        last_notice=time.monotonic()
        while psutil.virtual_memory().available<CONFIGS[name]['reserve_available_ram_GiB']*2**30:
            time.sleep(10)
            if time.monotonic()-last_notice>=50:
                log(f'Waiting for additive fit scheduling reserve: {name} year{year}')
                last_notice=time.monotonic()
    return engine.train_one(name,year)


def all_oof():
    import numpy as np
    import polars as pl
    gate=ROOT/'analysis/expanded_stacking_future_pipelines_qa_20261004/verification.json'
    while not gate.exists():time.sleep(10)
    assert read(gate)['status']=='passed'
    freeze();features=engine.feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            path=OUT/f'boundary_control_{name}_{year}.json'
            if not path.exists():dump(path,engine.boundary_control(year,cfg,features),immutable=True)
            proofs[f'{name}_{year}']=read(path);info=train_one(name,year)
            linear_name=name.replace('_additive_ridge_','_ridge_')
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
         'boundary_controls':proofs,'test_data_read':False,'models_trained':30},immutable=True)
    log('All30 additive ridge fold models and mature-label controls completed')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'))
    parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
