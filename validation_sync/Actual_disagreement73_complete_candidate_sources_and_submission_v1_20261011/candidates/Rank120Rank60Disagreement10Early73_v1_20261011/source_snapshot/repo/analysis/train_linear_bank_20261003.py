"""One-day rank/return ridge backbones, distinct from the archived five-day mapping."""
from pathlib import Path
import argparse
import importlib.util
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_linear_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/linear_bank_20261003'
CONFIGS={f'{label}_ridge_{suffix}':{'kind':'ridge_linear','target':target,'ridge_lambda':value,
          'chunk_rows':32768,'clip_z':8.,'return_quantiles':[.005,.995]}
         for label,target in (('rank','y_rank'),('return','y_ret_1d'))
         for suffix,value in (('l0001',.001),('l01',.1),('l1',1.))}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS


def transform(x,mean,scale,clip):
    import numpy as np
    values=np.asarray(x,dtype=np.float64)
    return np.clip((np.where(np.isfinite(values),values,mean)-mean)/scale,-clip,clip)


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
    n,width=x.shape;sum_x=np.zeros(width);sum_y=float(target.sum())
    sum_xx=np.zeros((width,width));sum_xy=np.zeros(width)
    for offset in range(0,n,cfg['chunk_rows']):
        z=transform(x[offset:offset+cfg['chunk_rows']],mean,scale,cfg['clip_z'])
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
    return {'kind':'ridge_linear','mean':mean,'scale':scale,'coefficients':coefficients,
            'intercept':intercept,'config':dict(cfg),'target_bounds':bounds,
            'normal_equation_max_abs_residual':residual,'target_units':cfg['target'],
            'ridge_penalty_equivalent_sklearn_alpha':float(cfg['ridge_lambda']*n)}


def predict_arrays(bundle,x):
    import numpy as np
    parts=[];cfg=bundle['config']
    for offset in range(0,len(x),cfg['chunk_rows']):
        z=transform(x[offset:offset+cfg['chunk_rows']],bundle['mean'],bundle['scale'],cfg['clip_z'])
        # Fixed per-row reduction avoids batch-size-dependent BLAS kernels.
        parts.append(np.einsum('ij,j->i',z,bundle['coefficients'],optimize=False)+bundle['intercept'])
    return np.concatenate(parts) if parts else np.empty(0,dtype=np.float64)


engine.fit_arrays=fit_arrays;engine.predict_arrays=predict_arrays


def verify():return engine.verify()


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),SOURCE,engine.FEATURE_FILE,engine.MANIFEST,
             ROOT/'data/raw/训练集.csv',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md',
             ROOT/'analysis/verify_linear_bank_20261003.py',ROOT/'analysis/linear_bank_preflight_20261003/verification.json']
    assert read(sources[-1])['status']=='passed'
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'configurations':CONFIGS,'features':engine.feature_names(),'years':YEARS,
         'validation':'2020–2024 annual expanding OOF; identical mature-label purge',
         'objective':'Mean squared loss plus lambda*sum(coefficients**2), with unpenalized intercept; use the supplied centered one-day rank label or one-day return label.',
         'preprocessing':'Past mature target-eligible training rows only: feature mean/std, missing-value mean imputation, standardized feature clipping to [-8,8]. Return winsorization bounds learned only from that past training fold.',
         'inference':'Fixed float64 per-row einsum reduction, invariant to row prefix and inference batch boundaries.',
         'archived_ridge_distinction':'Historical Ridge records mapped five-day signals; these fit all provided causal features to one-day targets and must compete as complete output schemes.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,
         'test_data_read':False,'expected_annual_fits':30,
         'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('Six one-day linear rank/return configurations frozen')


def train_one(name,year):return engine.train_one(name,year)


def all_oof():
    freeze();features=engine.feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            path=OUT/f'boundary_control_{name}_{year}.json'
            if not path.exists():dump(path,engine.boundary_control(year,cfg,features),immutable=True)
            proofs[f'{name}_{year}']=read(path);train_one(name,year)
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'boundary_controls':proofs,'test_data_read':False,'models_trained':30},immutable=True)
    log('All30 one-day linear fold models and mature-label controls completed')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'))
    parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
