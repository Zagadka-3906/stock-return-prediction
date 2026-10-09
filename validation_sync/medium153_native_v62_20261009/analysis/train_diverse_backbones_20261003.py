"""New backbones with frozen preprocessing, mature labels and full annual OOF."""
from __future__ import annotations
import argparse
import gc
import importlib.metadata
import os
from pathlib import Path
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[name]='8'
os.environ['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from optimize_training_round12 import YEARS,KEYS,read,dump,sha,log
from run import FEATURE_FILE,MANIFEST,feature_names,fold_cutoff,to_matrix
OUT=ROOT/'analysis/diverse_backbones_20261003'
CONFIGS={
    'rank_mlp128':{'kind':'mlp','target':'y_rank','hidden':[128,64],'epochs':16,'batch_size':32768,
                   'learning_rate':.001,'weight_decay':.0001,'dropout':.05,'seed':20261003},
    'return_mlp128':{'kind':'mlp','target':'y_ret_1d','hidden':[128,64],'epochs':16,'batch_size':32768,
                     'learning_rate':.001,'weight_decay':.0001,'dropout':.05,'seed':20261004},
    'rank_extra192':{'kind':'extra','target':'y_rank','n_estimators':192,'max_depth':12,
                     'min_samples_leaf':128,'max_features':.7,'bootstrap':True,'max_samples':.25,'seed':20261003}}


def network(features,cfg):
    import torch
    layers=[];width=features
    for hidden in cfg['hidden']:
        layers.extend([torch.nn.Linear(width,hidden),torch.nn.LayerNorm(hidden),torch.nn.SiLU(),torch.nn.Dropout(cfg['dropout'])]);width=hidden
    layers.append(torch.nn.Linear(width,1))
    return torch.nn.Sequential(*layers)


def fit_arrays(x,y,cfg):
    import numpy as np
    import torch
    mean=np.nanmean(x,axis=0,dtype=np.float64).astype(np.float32);mean=np.where(np.isfinite(mean),mean,0.)
    if cfg['kind']=='extra':
        from sklearn.ensemble import ExtraTreesRegressor
        clean=np.where(np.isfinite(x),x,mean).astype(np.float32)
        model=ExtraTreesRegressor(n_estimators=cfg['n_estimators'],max_depth=cfg['max_depth'],
              min_samples_leaf=cfg['min_samples_leaf'],max_features=cfg['max_features'],bootstrap=cfg['bootstrap'],
              max_samples=cfg['max_samples'],n_jobs=8,random_state=cfg['seed'])
        model.fit(clean,y)
        model.set_params(n_jobs=1)
        return {'kind':'extra','model':model,'mean':mean,'config':cfg}
    torch.set_num_threads(8);torch.manual_seed(cfg['seed']);torch.cuda.manual_seed_all(cfg['seed'])
    torch.use_deterministic_algorithms(True);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    scale=np.nanstd(x,axis=0,dtype=np.float64).astype(np.float32);scale=np.where(np.isfinite(scale)&(scale>1e-5),scale,1.)
    clean=np.clip((np.where(np.isfinite(x),x,mean)-mean)/scale,-8.,8.).astype(np.float32)
    device='cuda' if torch.cuda.is_available() else 'cpu';xt=torch.from_numpy(clean).to(device)
    if cfg['target']=='y_rank':low,high=0.,1.;target=y.astype(np.float32)-.5;target_scale=1.
    else:
        low,high=np.quantile(y,[.005,.995]);target_scale=20.;target=(np.clip(y,low,high)*target_scale).astype(np.float32)
    yt=torch.from_numpy(target).to(device);model=network(x.shape[1],cfg).to(device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=cfg['learning_rate'],weight_decay=cfg['weight_decay'])
    objective=torch.nn.MSELoss() if cfg['target']=='y_rank' else torch.nn.HuberLoss(delta=.5)
    losses=[]
    for epoch in range(cfg['epochs']):
        model.train();order=torch.randperm(len(y),device=device);sum_loss=0.
        for offset in range(0,len(y),cfg['batch_size']):
            index=order[offset:offset+cfg['batch_size']];optimizer.zero_grad(set_to_none=True)
            loss=objective(model(xt[index]).squeeze(-1),yt[index]);loss.backward();optimizer.step();sum_loss+=float(loss.detach())*len(index)
        losses.append(sum_loss/len(y))
        if epoch==0 or (epoch+1)%4==0:log(f"MLP {cfg['target']} epoch{epoch+1}/{cfg['epochs']} mature-training loss={losses[-1]:.8f}")
    state={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    del xt,yt,model,optimizer;gc.collect()
    if device=='cuda':torch.cuda.empty_cache()
    return {'kind':'mlp','state':state,'mean':mean,'scale':scale,'target_bounds':[float(low),float(high)],
            'target_scale':target_scale,'config':cfg,'training_losses':losses,'device':device}


def predict_arrays(bundle,x):
    import numpy as np
    if bundle['kind']=='extra':return bundle['model'].predict(np.where(np.isfinite(x),x,bundle['mean']).astype(np.float32))
    import torch
    torch.set_num_threads(8);torch.use_deterministic_algorithms(True);torch.backends.cuda.matmul.allow_tf32=False
    device='cuda' if torch.cuda.is_available() else 'cpu'
    model=network(x.shape[1],bundle['config']).to(device);model.load_state_dict(bundle['state']);model.eval()
    clean=np.clip((np.where(np.isfinite(x),x,bundle['mean'])-bundle['mean'])/bundle['scale'],-8.,8.).astype(np.float32)
    parts=[]
    with torch.no_grad():
        for offset in range(0,len(x),32768):
            chunk=clean[offset:offset+32768];size=len(chunk)
            if size<32768:
                padded=np.zeros((32768,x.shape[1]),dtype=np.float32);padded[:size]=chunk;chunk=padded
            values=model(torch.from_numpy(chunk).to(device)).squeeze(-1).cpu().numpy()[:size]
            parts.append(values.astype(np.float64))
    raw=np.concatenate(parts)
    if bundle['config']['target']=='y_ret_1d':raw/=bundle['target_scale']
    del model;gc.collect()
    if device=='cuda':torch.cuda.empty_cache()
    return raw


def save_bundle(path,bundle):
    import joblib
    joblib.dump(bundle,path,compress=3)


def load_bundle(path):
    import joblib
    return joblib.load(path)


def verify():
    protocol=read(OUT/'protocol.json')
    for path,digest in protocol['input_sha256'].items():assert sha(path)==digest,path
    return protocol


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),FEATURE_FILE,MANIFEST,ROOT/'data/raw/训练集.csv',ROOT/'run.py',
             ROOT/'src/features.py',ROOT/'后续选模标准.md']
    versions={name:importlib.metadata.version(name) for name in ('numpy','polars','scikit-learn','torch','joblib')}
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'configurations':CONFIGS,
         'features':feature_names(),'years':YEARS,'validation':'2020–2024 annual expanding OOF',
         'maturity_rule':'For year Y, train is_train rows with date < the last prevalidation trading date; remove the immature one-day label boundary.',
         'preprocessing':'Per-fold past training mean/std; MLP clip z to [-8,8]; return target winsor bounds learned from past training only.',
         'SGD_order':'Randomize only past training minibatches; CV dates never shuffled.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,'test_data_read':False,
         'extra_inference':'Serial deterministic estimator reduction; parallel fit with fixed tree seeds.',
         'documentation':'https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html',
         'versions':versions,'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('New MLP and ExtraTrees mature-label training protocol frozen')


def training_frame(lazy,cutoff,cfg):
    import polars as pl
    target=cfg['target']
    return lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)&pl.col('price_valid')&pl.col(target).is_finite())


def array_hash(value):
    import hashlib
    import numpy as np
    return hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest()


def boundary_control(year,cfg,features):
    import numpy as np
    import polars as pl
    cutoff=fold_cutoff(year);lazy=pl.scan_parquet(FEATURE_FILE)
    cols=KEYS+features+[c for c in ('y_rank','y_ret_1d','is_train','price_valid') if c not in features]
    past=training_frame(lazy,cutoff,cfg).select(cols).head(4096).collect()
    future=lazy.filter(pl.col('is_train')&(pl.col('trade_date')>=cutoff)).select(cols).head(1024).collect()
    sample=pl.concat([past,future]);poisoned=sample.with_columns([
        pl.when(pl.col('trade_date')>=cutoff).then(pl.lit(12345.,dtype=sample.schema[c])).otherwise(pl.col(c)).alias(c) for c in ('y_rank','y_ret_1d')])
    clean=training_frame(sample.lazy(),cutoff,cfg).collect();changed=training_frame(poisoned.lazy(),cutoff,cfg).collect()
    assert clean.equals(changed)
    small=dict(cfg,epochs=1,n_estimators=8,max_depth=4)
    x=to_matrix(clean,features);y=clean[cfg['target']].to_numpy()
    a=fit_arrays(x,y,small);b=fit_arrays(to_matrix(changed,features),changed[cfg['target']].to_numpy(),small)
    assert np.array_equal(a['mean'],b['mean']) and np.array_equal(predict_arrays(a,x[:512]),predict_arrays(b,x[:512]))
    if a['kind']=='mlp':assert all(np.array_equal(a['state'][k].numpy(),b['state'][k].numpy()) for k in a['state'])
    return {'status':'passed','year':year,'boundary_future_label_poisoning_bit_identical':True,
            'learned_preprocessing_bit_identical':True,'small_model_retraining_bit_identical':True,
            'cutoff_exclusive':cutoff,'control_training_rows':len(clean)}


def train_one(name,year):
    import numpy as np
    import polars as pl
    verify();cfg=CONFIGS[name];features=feature_names();folder=OUT/name;folder.mkdir(exist_ok=True)
    info_path=folder/f'info_{year}.json';model_path=folder/f'model_{year}.joblib';raw_path=folder/f'raw_{year}.parquet'
    if info_path.exists():
        info=read(info_path)
        assert sha(model_path)==info['model_sha256']
        if year<2025:assert sha(raw_path)==info['prediction_sha256']
        return info
    started=time.monotonic();cutoff=fold_cutoff(year);lazy=pl.scan_parquet(FEATURE_FILE)
    train=training_frame(lazy,cutoff,cfg).select(KEYS+features+[cfg['target']]).sort('trade_date','ts_code').collect()
    x=to_matrix(train,features);y=train[cfg['target']].to_numpy()
    dates=train['trade_date'].to_numpy();all_dates=lazy.filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    last=int(dates[-1]);label_end=int(all_dates[np.searchsorted(all_dates,last)+1]);assert last<cutoff and label_end<=cutoff
    metadata={'rows':len(train),'days':len(np.unique(dates)),'first':int(dates[0]),'last':last,
              'cutoff_exclusive':cutoff,'last_label_end':label_end,'validation_year':year,
              'training_matrix_sha256':array_hash(x),'training_target_sha256':array_hash(y),
              'training_keys_sha256':array_hash(train.select(KEYS).hash_rows(seed=2026).to_numpy()),'features':features}
    del train,dates;gc.collect()
    log(f'New {name} fold{year}: fitting {len(y):,} mature rows, {len(features)} features')
    fit_start=time.monotonic();bundle=fit_arrays(x,y,cfg);fit_seconds=time.monotonic()-fit_start
    save_bundle(model_path,bundle);del x,y;gc.collect()
    info={'status':'passed','model':name,'year':year,'configuration':cfg,'training_meta':metadata,
          'fit_seconds':fit_seconds,'model_sha256':sha(model_path),'test_data_read':False}
    if year<2025:
        cols=KEYS+features+[c for c in ('price_valid',) if c not in features]
        valid=lazy.filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).select(cols).sort('trade_date','ts_code').collect()
        vx=to_matrix(valid,features);raw=predict_arrays(bundle,vx);replay=predict_arrays(load_bundle(model_path),vx)
        assert np.array_equal(raw,replay) and np.isfinite(raw).all()
        raw[~valid['price_valid'].to_numpy()]=-1e6
        valid.select(KEYS).with_columns(pl.Series('pred_raw',raw)).write_parquet(raw_path)
        info.update(prediction_sha256=sha(raw_path),rows=len(valid),model_reload_bit_identical=True)
        del valid,vx,raw,replay
    else:
        info['fulltraining_only_test_prediction_not_generated']=True
    info['elapsed_seconds']=time.monotonic()-started;dump(info_path,info,immutable=True)
    del bundle;gc.collect();log(f'New {name} fold{year} saved and verified in {info["elapsed_seconds"]:.1f}s')
    return info


def all_oof():
    freeze();features=feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            control_path=OUT/f'boundary_control_{name}_{year}.json'
            if not control_path.exists():dump(control_path,boundary_control(year,cfg,features),immutable=True)
            proofs[f'{name}_{year}']=read(control_path)
            train_one(name,year)
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'boundary_controls':proofs,'test_data_read':False,'models_trained':len(CONFIGS)*len(YEARS)},immutable=True)
    log('All15 new fold backbones and mature-label controls completed')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'));parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)


if __name__=='__main__':main()
