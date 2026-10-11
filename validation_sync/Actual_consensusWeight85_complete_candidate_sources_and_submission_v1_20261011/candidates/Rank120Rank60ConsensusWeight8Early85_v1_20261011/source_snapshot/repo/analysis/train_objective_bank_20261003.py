"""Past-only neural objectives: head classification, head-weighted MSE, same-day RankNet."""
from pathlib import Path
import argparse
import gc
import importlib.util
import os
import sys
import time
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='8'
os.environ['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_objective_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/objective_bank_20261003'
COMMON={'kind':'mlp','target':'y_rank','hidden':[128,64],'epochs':32,'batch_size':32768,
        'learning_rate':.001,'weight_decay':.0001,'dropout':.05}
CONFIGS={
    'tail_bce128_e32':{**COMMON,'objective':'top_decile_bce','positive_weight':9.,'seed':20261010},
    'tail_mse128_e32':{**COMMON,'objective':'head_weighted_mse','positive_weight':10.,'seed':20261011},
    'pair_rank128_e32':{**COMMON,'objective':'same_day_ranknet','temperature':.1,'mse_weight':.1,'seed':20261012}}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS
load_bundle=engine.load_bundle
predict_arrays=engine.predict_arrays
_TRAIN_DATES=None


def fit_arrays(x,y,cfg):
    import numpy as np
    import torch
    from torch.nn import functional as functional
    assert np.isfinite(y).all() and y.min()>=-.501 and y.max()<=.501,'Cached rank labels must be centered percentiles'
    torch.set_num_threads(8);torch.manual_seed(cfg['seed']);torch.cuda.manual_seed_all(cfg['seed'])
    torch.use_deterministic_algorithms(True);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    mean=np.nanmean(x,axis=0,dtype=np.float64).astype(np.float32);mean=np.where(np.isfinite(mean),mean,0.)
    scale=np.nanstd(x,axis=0,dtype=np.float64).astype(np.float32);scale=np.where(np.isfinite(scale)&(scale>1e-5),scale,1.)
    clean=np.clip((np.where(np.isfinite(x),x,mean)-mean)/scale,-8.,8.).astype(np.float32)
    device='cuda' if torch.cuda.is_available() else 'cpu';xt=torch.from_numpy(clean).to(device)
    yt=torch.from_numpy(y.astype(np.float32)).to(device);model=engine.network(x.shape[1],cfg).to(device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=cfg['learning_rate'],weight_decay=cfg['weight_decay'])
    pair=cfg['objective']=='same_day_ranknet'
    if pair:
        assert _TRAIN_DATES is not None and len(_TRAIN_DATES)==len(y)
        assert np.all(_TRAIN_DATES[:-1]<=_TRAIN_DATES[1:])
        _,starts,counts=np.unique(_TRAIN_DATES,return_index=True,return_counts=True)
        group=np.repeat(np.arange(len(starts)),counts)
        lower=torch.from_numpy(starts[group].astype(np.int64)).to(device)
        sizes=torch.from_numpy(counts[group].astype(np.int64)).to(device)
    losses=[]
    for epoch in range(cfg['epochs']):
        model.train();order=torch.randperm(len(y),device=device);total=0.
        for offset in range(0,len(y),cfg['batch_size']):
            index=order[offset:offset+cfg['batch_size']];optimizer.zero_grad(set_to_none=True)
            if pair:
                partner=lower[index]+(torch.rand(len(index),device=device)*sizes[index]).long()
                both=model(torch.cat([xt[index],xt[partner]],dim=0)).squeeze(-1)
                first,second=both[:len(index)],both[len(index):]
                gap=yt[index]-yt[partner];weight=gap.abs()+.05
                pair_loss=functional.softplus(-gap.sign()*(first-second)/cfg['temperature'])
                loss=(pair_loss*weight).sum()/weight.sum()+cfg['mse_weight']*functional.mse_loss(first,yt[index])
            else:
                output=model(xt[index]).squeeze(-1);head=(yt[index]>=.4)
                if cfg['objective']=='top_decile_bce':
                    loss=functional.binary_cross_entropy_with_logits(output,head.float(),pos_weight=torch.tensor(cfg['positive_weight'],device=device))
                else:
                    weight=torch.where(head,cfg['positive_weight'],1.)
                    loss=((output-yt[index]).square()*weight).sum()/weight.sum()
            loss.backward();optimizer.step();total+=float(loss.detach())*len(index)
        losses.append(total/len(y))
        if epoch==0 or (epoch+1)%4==0:log(f"Objective {cfg['objective']} epoch{epoch+1}/{cfg['epochs']} mature loss={losses[-1]:.8f}")
    state={key:value.detach().cpu().clone() for key,value in model.state_dict().items()}
    del xt,yt,model,optimizer;gc.collect()
    if device=='cuda':torch.cuda.empty_cache()
    return {'kind':'mlp','state':state,'mean':mean,'scale':scale,'config':cfg,'target_scale':1.,
            'target_bounds':[-.5,.5],'training_losses':losses,'device':device,
            'output_definition':'Head logit' if cfg['objective']=='top_decile_bce' else 'Relative ranking score; future-return mapping required'}


engine.fit_arrays=fit_arrays


def verify():return engine.verify()


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),SOURCE,engine.FEATURE_FILE,engine.MANIFEST,ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md']
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'configurations':CONFIGS,
         'features':engine.feature_names(),'years':YEARS,'validation':'2020–2024 annual expanding OOF; same mature-label cutoff',
         'targets':'Cached centered daily y_rank in [-0.5,0.5]; upper decile defined as >=0.4. No extra -0.5 offset.',
         'pair_sampling':'Randomize only mature past rows; independently choose each partner from that row\'s same trading-date training group.',
         'pair_loss':'Gap-weighted softplus(-sign(rank difference)*prediction difference/0.1), plus 0.1*MSE.',
         'preprocessing':'Past-only mean/std; fixed batch padding during inference.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,'test_data_read':False,
         'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('Three head-aware and same-day pairwise neural objectives frozen')


def set_dates(frame):
    global _TRAIN_DATES
    _TRAIN_DATES=frame['trade_date'].to_numpy()


def boundary_control(year,cfg,features):
    import numpy as np
    import polars as pl
    cutoff=engine.fold_cutoff(year);lazy=pl.scan_parquet(engine.FEATURE_FILE)
    columns=engine.KEYS+features+[c for c in ('y_rank','y_ret_1d','is_train','price_valid') if c not in features]
    past=engine.training_frame(lazy,cutoff,cfg).select(columns).head(4096).collect()
    future=lazy.filter(pl.col('is_train')&(pl.col('trade_date')>=cutoff)).select(columns).head(1024).collect()
    sample=pl.concat([past,future]);changed=sample.with_columns([
        pl.when(pl.col('trade_date')>=cutoff).then(pl.lit(12345.,dtype=sample.schema[c])).otherwise(pl.col(c)).alias(c) for c in ('y_rank','y_ret_1d')])
    clean=engine.training_frame(sample.lazy(),cutoff,cfg).sort('trade_date','ts_code').collect()
    poisoned=engine.training_frame(changed.lazy(),cutoff,cfg).sort('trade_date','ts_code').collect()
    assert clean.equals(poisoned);small=dict(cfg,epochs=1)
    set_dates(clean);x=engine.to_matrix(clean,features);a=fit_arrays(x,clean['y_rank'].to_numpy(),small)
    set_dates(poisoned);b=fit_arrays(engine.to_matrix(poisoned,features),poisoned['y_rank'].to_numpy(),small)
    assert np.array_equal(a['mean'],b['mean']) and np.array_equal(a['scale'],b['scale'])
    assert all(np.array_equal(a['state'][k].numpy(),b['state'][k].numpy()) for k in a['state'])
    assert np.array_equal(predict_arrays(a,x[:512]),predict_arrays(b,x[:512]))
    return {'status':'passed','year':year,'boundary_future_label_poisoning_bit_identical':True,
            'learned_preprocessing_bit_identical':True,'small_model_retraining_bit_identical':True,
            'pair_dates_past_only':True,'cutoff_exclusive':cutoff,'control_training_rows':len(clean)}


def train_one(name,year):
    verify();cfg=CONFIGS[name]
    if not (OUT/name/f'info_{year}.json').exists() and cfg['objective']=='same_day_ranknet':
        import polars as pl
        cutoff=engine.fold_cutoff(year)
        dates=engine.training_frame(pl.scan_parquet(engine.FEATURE_FILE),cutoff,cfg).select(engine.KEYS).sort('trade_date','ts_code').collect()
        set_dates(dates)
    return engine.train_one(name,year)


def all_oof():
    freeze();features=engine.feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            path=OUT/f'boundary_control_{name}_{year}.json'
            if not path.exists():dump(path,boundary_control(year,cfg,features),immutable=True)
            proofs[f'{name}_{year}']=read(path);train_one(name,year)
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'boundary_controls':proofs,'test_data_read':False,'models_trained':15},immutable=True)
    log('All15 objective fold models and boundary controls completed')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'));parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)


if __name__=='__main__':main()
