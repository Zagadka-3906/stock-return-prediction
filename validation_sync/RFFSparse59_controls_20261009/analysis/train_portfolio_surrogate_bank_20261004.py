"""Past-checkpoint fine tuning with training proxies; official final-CSV selection only."""
from pathlib import Path
from copy import deepcopy
import importlib.util
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_portfolio_surrogate_trainer_20261004',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
import portfolio_surrogate_loss_20261004 as proxy
OUT=ROOT/'analysis/portfolio_surrogate_bank_20261004'
BASE=ROOT/'analysis/neural_regularization_bank_20261003/rank512_drop000_e32'
PREFLIGHT=ROOT/'analysis/portfolio_surrogate_preflight_v2_20261004/verification.json'
COMMON={'kind':'mlp','target':'y_rank','hidden':[512,256,128],'dropout':0.,'seed':20261007,
    'batch_size':32768,'epochs':32,'learning_rate':.0001,'weight_decay':.0001,
    'training_objective':'warm_checkpoint_portfolio_proxy','fine_tune_epochs':4,
    'tau_fraction':.1,'turnover_weight':.3,'gradient_clip_norm':1.}
CONFIGS={'portfolio512_ic_ret_tau01_e4':{**COMMON,'turnover_weight':0.},
    'portfolio512_ic_ret_turn_tau01_e4':dict(COMMON),
    'portfolio512_ic_ret_turn_tau005_e4':{**COMMON,'tau_fraction':.05},
    'portfolio512_ic_ret_turn_tau01_e8':{**COMMON,'fine_tune_epochs':8}}
engine.OUT,engine.CONFIGS=OUT,CONFIGS
read,dump,log=engine.read,engine.dump,engine.log
YEARS=engine.YEARS

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()

def verify():
    protocol=read(OUT/'protocol.json')
    for p,digest in protocol['input_sha256'].items():assert sha(p)==digest,p
    return protocol

def freeze():
    if (OUT/'protocol.json').exists():verify();return
    assert read(PREFLIGHT)['status']=='passed'
    sources=[Path(__file__),SOURCE,Path(proxy.__file__),PREFLIGHT,
        ROOT/'analysis/verify_portfolio_surrogate_loss_v2_20261004.py',engine.FEATURE_FILE,engine.MANIFEST,
        ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md',ROOT/'evaluate.py',
        ROOT/'analysis/neural_regularization_bank_20261003/protocol.json']
    for year in (*YEARS,2025):sources.extend([BASE/f'info_{year}.json',BASE/f'model_{year}.joblib'])
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'configurations':CONFIGS,'years':YEARS,'features':engine.feature_names(),
        'validation':'Same2020–2024 annual expanding OOF; original mature-label cutoff',
        'warm_start':'Existing512-width seed20261007 no-dropout32-epoch checkpoint for each matching year; never refit',
        'normalization':'Reuse corresponding past-trained checkpoint mean/std andclip[-8,8]',
        'fine_tuning_batches':'Full price-valid pool onconsecutive mature training dates; pool independent of labels',
        'IC_proxy':'Fixed-anchor smooth empirical CDF correlation with provided mature rank labels',
        'return_proxy':'252 times soft-capped eligible labelled top-group excess',
        'turnover_proxy':'Soft holdings overlap over consecutive dates; no extra label filter',
        'proxy_weights':{'rank_correlation':.4,'annual_excess':.3,'holdings_overlap':'.0 or.3'},
        'all_proxies_are_training_losses_not_the_official_evaluator':True,
        'selection':'Original official evaluator on actual calibrated final continuous validation CSV',
        'minimum_available_host_GiB_before_fit_policy':14.,'guard_is_scheduling_not_hardware_limit':True,
        'new_model_fits':20,'reused_pretraining_fits_not_counted_as_new':True,
        'all_validation_years_previously_viewed':True,'selection_bias_uncorrected':True,
        'test_data_read':False,'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)

def subset_hash(array,mask):
    import numpy as np
    h=hashlib.sha256()
    for start in range(0,len(array),65536):
        chunk=np.ascontiguousarray(array[start:start+65536][mask[start:start+65536]])
        h.update(memoryview(chunk).cast('B'))
    return h.hexdigest()

def pool_filter(lazy,cutoff):
    import polars as pl
    return lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)&pl.col('price_valid'))

def pool_frame(year):
    import polars as pl
    cutoff=engine.fold_cutoff(year);features=engine.feature_names()
    columns=list(dict.fromkeys(engine.KEYS+features+['y_rank','y_ret_1d','flag_limit_up']))
    return pool_filter(pl.scan_parquet(engine.FEATURE_FILE),cutoff).select(columns).sort('trade_date','ts_code').collect()

def fine_tune(bundle,clean,dates,codes,flags,rank,ret,cfg):
    import gc
    import numpy as np
    import torch
    assert torch.cuda.is_available()
    torch.set_num_threads(8);torch.manual_seed(cfg['seed']);torch.cuda.manual_seed_all(cfg['seed'])
    torch.use_deterministic_algorithms(True);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
    device='cuda';model=engine.network(clean.shape[1],cfg).to(device);model.load_state_dict(bundle['state'])
    optimizer=torch.optim.AdamW(model.parameters(),lr=cfg['learning_rate'],weight_decay=cfg['weight_decay'])
    xt=torch.from_numpy(clean).to(device)
    ft=torch.from_numpy(np.array(flags,copy=True)).to(device)
    rt=torch.from_numpy(rank.astype(np.float32)).to(device);yt=torch.from_numpy(ret.astype(np.float32)).to(device)
    boundaries=np.r_[0,np.flatnonzero(dates[1:]!=dates[:-1])+1,len(dates)]
    pairs=[]
    for i in range(len(boundaries)-2):
        a,b,c=map(int,boundaries[i:i+3]);n=b-a
        _,left,right=np.intersect1d(codes[a:b],codes[b:c],assume_unique=True,return_indices=True)
        pairs.append((a,b,c,torch.tensor(left,device=device),torch.tensor(n+right,device=device),
            torch.cat([torch.zeros(n,device=device,dtype=torch.long),torch.ones(c-b,device=device,dtype=torch.long)])))
    assert pairs
    losses=[];order=np.random.default_rng(cfg['seed']);steps=0
    for epoch in range(cfg['fine_tune_epochs']):
        total=torch.zeros((),device=device)
        for index in order.permutation(len(pairs)):
            a,b,c,left,right,day=pairs[index];model.train();optimizer.zero_grad(set_to_none=True)
            score=model(xt[a:c]).squeeze(-1)
            terms=proxy.paired_terms(score,day,ft[a:c],rt[a:c],yt[a:c],left,right,tau_fraction=cfg['tau_fraction'])
            value=proxy.objective(terms,cfg['turnover_weight'])
            assert torch.isfinite(value)
            value.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),cfg['gradient_clip_norm'],error_if_nonfinite=True)
            optimizer.step();total+=value.detach();steps+=1
        losses.append(float(total)/len(pairs))
        log(f"Portfolio proxy epoch{epoch+1}/{cfg['fine_tune_epochs']}, mature-pair proxy loss={losses[-1]:.8f}")
    result=deepcopy(bundle);result['state']={k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
    result['config']=deepcopy(cfg);result['fine_tuning_losses']=losses
    result['fine_tuning_pairs_per_epoch']=len(pairs);result['fine_tuning_steps']=steps
    del xt,ft,rt,yt,model,optimizer,pairs;gc.collect();torch.cuda.empty_cache()
    return result

def train_one(name,year):
    import gc
    import numpy as np
    import polars as pl
    import psutil
    verify();cfg=CONFIGS[name];folder=OUT/name;folder.mkdir(exist_ok=True)
    info_path=folder/f'info_{year}.json';model_path=folder/f'model_{year}.joblib';raw_path=folder/f'raw_{year}.parquet'
    if info_path.exists():
        info=read(info_path);assert sha(model_path)==info['model_sha256']
        if year<2025:assert sha(raw_path)==info['prediction_sha256']
        return info
    while psutil.virtual_memory().available<14*2**30:time.sleep(10)
    started=time.monotonic();control=read(BASE/f'info_{year}.json');warm_path=BASE/f'model_{year}.joblib'
    assert sha(warm_path)==control['model_sha256'];bundle=engine.load_bundle(warm_path)
    frame=pool_frame(year);features=engine.feature_names();x=engine.to_matrix(frame,features)
    rank=frame['y_rank'].to_numpy();ret=frame['y_ret_1d'].to_numpy();supervised=np.isfinite(rank)
    dates=frame['trade_date'].to_numpy();meta=control['training_meta']
    assert int(supervised.sum())==meta['rows'] and features==meta['features']
    assert subset_hash(x,supervised)==meta['training_matrix_sha256']
    assert subset_hash(rank,supervised)==meta['training_target_sha256']
    assert subset_hash(frame.select(engine.KEYS).hash_rows(seed=2026).to_numpy(),supervised)==meta['training_keys_sha256']
    code_list=frame['ts_code'].unique().sort().to_list()
    codes=frame['ts_code'].cast(pl.Enum(code_list)).to_physical().to_numpy();flags=frame['flag_limit_up'].to_numpy()
    all_dates=pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    label_end=int(all_dates[np.searchsorted(all_dates,int(dates[-1]))+1])
    assert int(dates[-1])<meta['cutoff_exclusive'] and label_end<=meta['cutoff_exclusive']
    pool_meta={'rows':len(frame),'dates':int(frame['trade_date'].n_unique()),'first':int(dates[0]),'last':int(dates[-1]),
        'last_label_end':label_end,'cutoff_exclusive':meta['cutoff_exclusive'],'features':features,
        'matrix_sha256':engine.array_hash(x),'rank_labels_sha256':engine.array_hash(rank),'return_labels_sha256':engine.array_hash(ret),
        'label_missing_rows':int((~supervised).sum()),'stock_dictionary_is_past_only':True}
    clean=np.clip((np.where(np.isfinite(x),x,bundle['mean'])-bundle['mean'])/bundle['scale'],-8,8).astype(np.float32)
    del frame,x;gc.collect();fit_started=time.monotonic()
    log(f'New {name} fold{year}: fine tuning on{pool_meta["rows"]:,} mature pool rows')
    result=fine_tune(bundle,clean,dates,codes,flags,rank,ret,cfg);fit_seconds=time.monotonic()-fit_started
    assert np.array_equal(result['mean'],bundle['mean']) and np.array_equal(result['scale'],bundle['scale'])
    engine.save_bundle(model_path,result);del clean,dates,codes,flags,rank,ret,bundle;gc.collect()
    info={'status':'passed','model':name,'year':year,'configuration':cfg,'training_meta':deepcopy(meta),
        'fine_tuning_pool_meta':pool_meta,'fit_seconds':fit_seconds,'model_sha256':sha(model_path),
        'warm_start_model_sha256':control['model_sha256'],'warm_start_model_source':str(warm_path.resolve()),
        'past_pretraining_model_andnormalizer_reused':True,'new_model_fits':1,'fine_tuning_steps':result['fine_tuning_steps'],
        'test_data_read':False}
    if year<2025:
        columns=list(dict.fromkeys(engine.KEYS+features+['price_valid']))
        valid=pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).select(columns).sort('trade_date','ts_code').collect()
        vx=engine.to_matrix(valid,features);raw=engine.predict_arrays(result,vx);replay=engine.predict_arrays(engine.load_bundle(model_path),vx)
        assert np.array_equal(raw,replay) and np.isfinite(raw).all();raw[~valid['price_valid'].to_numpy()]=-1e6
        valid.select(engine.KEYS).with_columns(pl.Series('pred_raw',raw)).write_parquet(raw_path)
        info.update(prediction_sha256=sha(raw_path),rows=len(valid),model_reload_bit_identical=True)
        del valid,vx,raw,replay
    else:info['fulltraining_only_test_prediction_not_generated']=True
    info['elapsed_seconds']=time.monotonic()-started;dump(info_path,info,immutable=True)
    del result;gc.collect();log(f'New {name} fold{year} saved andverified in{info["elapsed_seconds"]:.1f}s')
    return info

def all_oof():
    import numpy as np
    import polars as pl
    freeze();prefixes={}
    for name in CONFIGS:
        for year in YEARS:
            info=train_one(name,year);path=OUT/f'prefix_control_{name}_{year}.json'
            if not path.exists():
                features=engine.feature_names();columns=list(dict.fromkeys(engine.KEYS+features+['price_valid']))
                frame=pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).select(columns).sort('trade_date','ts_code').head(32781).collect()
                x=engine.to_matrix(frame,features);model=engine.load_bundle(OUT/name/f'model_{year}.joblib');raw=engine.predict_arrays(model,x)
                for n in (1,80,32767,32768):assert np.array_equal(raw[:n],engine.predict_arrays(model,x[:n]))
                raw[~frame['price_valid'].to_numpy()]=-1e6;saved=pl.read_parquet(OUT/name/f'raw_{year}.parquet').head(len(frame))
                assert frame.select(engine.KEYS).equals(saved.select(engine.KEYS)) and np.array_equal(raw,saved['pred_raw'].to_numpy())
                dump(path,{'status':'passed','model':name,'year':year,'actual_saved_output_andpadded_prefix_bit_identical':True,
                    'prefix_rows':[1,80,32767,32768],'training_info_sha256':sha(OUT/name/f'info_{year}.json')},immutable=True)
            prefixes[f'{name}_{year}']=read(path)
    dump(OUT/'oof_audit.json',{'status':'passed','years':YEARS,'configurations':CONFIGS,'models_trained':20,
        'all_supervised_training_keys_features_andtargets_match_the_past_checkpoint_control':True,
        'holdings_training_pool_uses_all_available_price_valid_rows_independent_of_labels':True,
        'all_training_pool_labels_mature_before_the_corresponding_validation_year':True,
        'prefix_controls':prefixes,'new_quality_scores':0,'test_data_read':False},immutable=True)

if __name__=='__main__':all_oof()
