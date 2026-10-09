"""Past-only sampled RBF landmarks plus raw63 streamed ridge models."""
from pathlib import Path
import argparse
import importlib.util
import os
import sys
import time
for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[variable]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_nystrom_trainer_20261004',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/nystrom_ridge_bank_20261004'
CONFIGS={f'{label}_nystrom{components}_s1_l01':{
    'kind':'ridge_nystrom','target':target,'ridge_lambda':.1,'chunk_rows':32768,
    'clip_z':8.,'lengthscale':1.,'landmark_components':components,'seed':20261004,
    'kernel_mass':128.,'singular_value_floor':1e-12,'reserve_available_ram_GiB':14.,
    'return_quantiles':[.005,.995]}
    for label,target in (('rank','y_rank'),('return','y_ret_1d')) for components in (64,128)}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS

def standardize(x,mean,scale,cfg):
    import numpy as np
    values=np.asarray(x,dtype=np.float64)
    return np.clip((np.where(np.isfinite(values),values,mean)-mean)/scale,-cfg['clip_z'],cfg['clip_z'])

def landmark_basis(x,mean,scale,cfg):
    import numpy as np
    from sklearn.metrics.pairwise import rbf_kernel
    count=cfg['landmark_components'];assert len(x)>=count
    indices=np.random.RandomState(cfg['seed']).permutation(len(x))[:count]
    landmarks=standardize(x[indices],mean,scale,cfg)
    gamma=.5/(x.shape[1]*cfg['lengthscale']**2)
    gram=rbf_kernel(landmarks,gamma=gamma)
    left,values,right=np.linalg.svd(gram)
    floored=np.maximum(values,cfg['singular_value_floor'])
    normalization=(left/np.sqrt(floored))@right
    assert np.isfinite(normalization).all()
    return indices,landmarks,normalization,gamma,values

def transform(x,mean,scale,cfg,landmarks,normalization,gamma):
    import numpy as np
    from sklearn.metrics.pairwise import rbf_kernel
    parts=[];batch=cfg['chunk_rows']
    for offset in range(0,len(x),batch):
        z=standardize(x[offset:offset+batch],mean,scale,cfg)
        padded=np.zeros((batch,len(mean)),dtype=np.float64);padded[:len(z)]=z
        kernel=rbf_kernel(padded,landmarks,gamma=gamma)
        projected=kernel@normalization.T
        parts.append(np.concatenate([z,np.sqrt(cfg['kernel_mass'])*projected[:len(z)]],axis=1))
    width=len(mean)+len(landmarks)
    return np.concatenate(parts) if parts else np.empty((0,width),dtype=np.float64)

def fit_arrays(x,y,cfg):
    import numpy as np
    mean=np.nanmean(x,axis=0,dtype=np.float64);mean=np.where(np.isfinite(mean),mean,0.)
    scale=np.nanstd(x,axis=0,dtype=np.float64);scale=np.where(np.isfinite(scale)&(scale>1e-5),scale,1.)
    target=np.asarray(y,dtype=np.float64);assert np.isfinite(target).all() and len(target)==len(x)
    bounds=None
    if cfg['target']=='y_ret_1d':
        bounds=[float(v) for v in np.quantile(target,cfg['return_quantiles'])]
        target=np.clip(target,*bounds)
    indices,landmarks,normalization,gamma,singular_values=landmark_basis(x,mean,scale,cfg)
    n=len(x);width=x.shape[1]+len(landmarks)
    sum_x=np.zeros(width);sum_xx=np.zeros((width,width));sum_xy=np.zeros(width)
    for offset in range(0,n,cfg['chunk_rows']):
        z=transform(x[offset:offset+cfg['chunk_rows']],mean,scale,cfg,landmarks,normalization,gamma)
        labels=target[offset:offset+len(z)]
        sum_x+=z.sum(axis=0);sum_xx+=z.T@z;sum_xy+=z.T@labels
    center=sum_x/n;target_mean=float(target.mean())
    normal=sum_xx/n-np.outer(center,center)+cfg['ridge_lambda']*np.eye(width)
    cross=sum_xy/n-center*target_mean
    coefficients=np.linalg.solve(normal,cross);intercept=target_mean-float(center@coefficients)
    residual=float(np.max(np.abs(normal@coefficients-cross)))
    assert residual<1e-10 and np.isfinite(coefficients).all() and np.isfinite(intercept)
    return {'kind':'ridge_nystrom','config':dict(cfg),'mean':mean,'scale':scale,
        'landmark_indices':indices,'landmarks':landmarks,'normalization':normalization,
        'gamma':gamma,'landmark_singular_values':singular_values,'coefficients':coefficients,
        'intercept':intercept,'target_bounds':bounds,'target_units':cfg['target'],
        'normal_equation_max_abs_residual':residual,
        'ridge_penalty_equivalent_sklearn_alpha':float(cfg['ridge_lambda']*n),
        'landmarks_sampled_from_training_rows_without_targets':True}

def predict_arrays(bundle,x):
    import numpy as np
    cfg=bundle['config'];parts=[]
    for offset in range(0,len(x),cfg['chunk_rows']):
        z=transform(x[offset:offset+cfg['chunk_rows']],bundle['mean'],bundle['scale'],cfg,
            bundle['landmarks'],bundle['normalization'],bundle['gamma'])
        parts.append(np.einsum('ij,j->i',z,bundle['coefficients'],optimize=False)+bundle['intercept'])
    return np.concatenate(parts) if parts else np.empty(0,dtype=np.float64)

def enhanced_engine_dump(path,payload,immutable=False):
    if path.name.startswith('info_') and payload.get('training_meta'):
        bundle=engine.load_bundle(path.parent/f"model_{payload['year']}.joblib")
        indices=bundle['landmark_indices'];assert len(set(indices))==len(indices)
        assert min(indices)>=0 and max(indices)<payload['training_meta']['rows']
        payload.update(new_model_fits=1,landmark_count=len(indices),
            landmark_indices_sha256=engine.array_hash(indices),
            standardized_landmarks_sha256=engine.array_hash(bundle['landmarks']),
            landmark_sampling_uses_only_corresponding_mature_training_matrix=True,
            normal_equation_max_abs_residual=bundle['normal_equation_max_abs_residual'])
    return dump(path,payload,immutable=immutable)

engine.fit_arrays=fit_arrays;engine.predict_arrays=predict_arrays;engine.dump=enhanced_engine_dump
def verify():return engine.verify()

def freeze():
    OUT.mkdir(exist_ok=True)
    if (OUT/'protocol.json').exists():verify();return
    proof=ROOT/'analysis/nystrom_ridge_preflight_20261004/verification.json';assert read(proof)['status']=='passed'
    sources=[Path(__file__),SOURCE,engine.FEATURE_FILE,engine.MANIFEST,
        ROOT/'data/raw/训练集.csv',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md',
        ROOT/'analysis/nystrom_ridge_model_sources_20261004.py',
        ROOT/'analysis/verify_nystrom_ridge_bank_20261004.py',proof,
        ROOT/'analysis/nystrom_ridge_complete_output_search_plan_20261004.json']
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'configurations':CONFIGS,'features':engine.feature_names(),'years':YEARS,
        'validation':'2020–2024 annual expanding OOF, identical original mature one-day label purge',
        'preprocessing':'Past eligible rows fit raw63 mean/std/imputation, clip z to [-8,8]. Seeded uniform landmark indices sample only the matching mature training matrix. RBF gamma=.5/(63*lengthscale**2); singular values floor1e-12. Append sqrt128 times normalized landmark kernel features to raw63. Return clipping quantiles use the past target only.',
        'objective':'Mean squared error plus .1 times sum(coefficients squared), unpenalized intercept; rank or one-day return target.',
        'comparison':'Existing random-Fourier family uses fixed data-independent random features. This family learns its kernel landmarks from each past training fold; all four choices are fixed before scoring.',
        'inference':'Fixed padded32768-row kernels and normalization projection; per-row einsum; actual reload and prefixes must be bit identical.',
        'method_reference':'https://scikit-learn.org/stable/modules/generated/sklearn.kernel_approximation.Nystroem.html',
        'versions':{name:engine.importlib.metadata.version(name) for name in ('numpy','scikit-learn','polars','joblib')},
        'expected_annual_fits':20,'expected_five_year_configurations':4,
        'no_validation_early_stopping':True,'no_feature_selection':True,'test_data_read':False,
        '14GiB_available_host_reserve_is_scheduling_policy_not_capacity_measurement':True,
        'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)

def train_one(name,year):
    import psutil
    last=time.monotonic()
    while not (OUT/name/f'info_{year}.json').exists() and psutil.virtual_memory().available<CONFIGS[name]['reserve_available_ram_GiB']*2**30:
        time.sleep(10)
        if time.monotonic()-last>=50:log(f'Waiting for Nyström fit reserve: {name} year{year}');last=time.monotonic()
    engine.train_one(name,year)
    return read(OUT/name/f'info_{year}.json')

def all_oof():
    import numpy as np
    import polars as pl
    freeze();features=engine.feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            boundary=OUT/f'boundary_control_{name}_{year}.json'
            if not boundary.exists():dump(boundary,engine.boundary_control(year,cfg,features),immutable=True)
            info=train_one(name,year)
            ref=ROOT/'analysis/linear_bank_20261003'/('rank_ridge_l01' if cfg['target']=='y_rank' else 'return_ridge_l01')/f'info_{year}.json'
            reference=read(ref)
            for field in ('training_matrix_sha256','training_target_sha256','training_keys_sha256'):
                assert info['training_meta'][field]==reference['training_meta'][field],field
            prefix_path=OUT/f'prefix_control_{name}_{year}.json'
            if not prefix_path.exists():
                frame=pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).select(engine.KEYS+features+['price_valid']).sort('trade_date','ts_code').collect()
                cutoff=int(frame['trade_date'].unique().sort()[79]);prefix=frame.filter(pl.col('trade_date')<=cutoff)
                predicted=predict_arrays(engine.load_bundle(OUT/name/f'model_{year}.joblib'),engine.to_matrix(prefix,features))
                predicted[~prefix['price_valid'].to_numpy()]=-1e6
                raw=pl.read_parquet(OUT/name/f'raw_{year}.parquet').filter(pl.col('trade_date')<=cutoff)
                assert prefix.select(engine.KEYS).equals(raw.select(engine.KEYS)) and np.array_equal(predicted,raw['pred_raw'].to_numpy())
                dump(prefix_path,{'status':'passed','actual_saved_model80_day_prefix_bit_identical':True,
                    'rows':len(prefix),'raw63_training_features_targets_andkeys_bit_identical':True,
                    'reference_info_sha256':sha(ref),'test_data_read':False},immutable=True)
                del frame,prefix,predicted,raw;engine.gc.collect()
            proofs[f'{name}_{year}']={'boundary':read(boundary),'actual_prefix':read(prefix_path)}
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
        'boundary_controls':proofs,'actual_annual_fits':20,'new_quality_scores':0,'test_data_read':False},immutable=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'))
    parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
