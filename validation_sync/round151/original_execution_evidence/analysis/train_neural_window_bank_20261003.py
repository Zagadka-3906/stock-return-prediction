"""Prespecified two/three-year neural windows with unchanged mature-label purge."""
from pathlib import Path
import argparse
import importlib.util
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_window_neural_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/neural_window_bank_20261003'
COMMON={'kind':'mlp','batch_size':32768,'learning_rate':.001,'weight_decay':.0001,'dropout':.05,'epochs':32}
CONFIGS={
    'rank512_window2_e32':{**COMMON,'target':'y_rank','hidden':[512,256,128],'seed':20261007,'rolling_years':2},
    'rank512_window3_e32':{**COMMON,'target':'y_rank','hidden':[512,256,128],'seed':20261007,'rolling_years':3},
    'return256_window2_e32':{**COMMON,'target':'y_ret_1d','hidden':[256,128],'seed':20261009,'rolling_years':2},
    'return256_window3_e32':{**COMMON,'target':'y_ret_1d','hidden':[256,128],'seed':20261009,'rolling_years':3}}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS
original_training_frame=engine.training_frame


def lower_bound(cutoff,cfg):return (cutoff//10000+1-cfg['rolling_years'])*10000+101


def training_frame(lazy,cutoff,cfg):
    import polars as pl
    return original_training_frame(lazy,cutoff,cfg).filter(pl.col('trade_date')>=lower_bound(cutoff,cfg))


engine.training_frame=training_frame


def verify():return engine.verify()


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),SOURCE,engine.FEATURE_FILE,engine.MANIFEST,ROOT/'data/raw/训练集.csv',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md']
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'configurations':CONFIGS,
         'features':engine.feature_names(),'years':YEARS,'validation':'2020–2024 annual OOF; fixed rolling past window; identical mature-label purge',
         'window_rule':'January 1 of prediction_year minus rolling_years, inclusive, through the original exclusive mature-label cutoff. First folds use all available history within that range.',
         'matched_controls':'Architecture, seed, epochs and optimizer match rank512_e32 and return256_e32. Only the eligible past training history changes.',
         'preprocessing':'Mean/std and return winsor limits fitted only on the selected mature past window. Original fixed inference batch padding.',
         'rank_target_engine_behavior':'Match the frozen expanding model exactly, including its constant centered-rank offset.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,'test_data_read':False,
         'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('Four matched neural two/three-year training windows frozen')


def boundary_control(year,cfg,features):
    import polars as pl
    proof=engine.boundary_control(year,cfg,features);cutoff=engine.fold_cutoff(year);lower=lower_bound(cutoff,cfg)
    lazy=pl.scan_parquet(engine.FEATURE_FILE)
    cols=engine.KEYS+features+[c for c in ('y_rank','y_ret_1d','is_train','price_valid') if c not in features]
    past=training_frame(lazy,cutoff,cfg).select(cols).head(4096).collect()
    old=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<lower)).select(cols).head(1024).collect()
    sample=pl.concat([old,past]);poisoned=sample.with_columns([
        pl.when(pl.col('trade_date')<lower).then(pl.lit(12345.,dtype=sample.schema[c])).otherwise(pl.col(c)).alias(c) for c in ('y_rank','y_ret_1d')])
    assert training_frame(sample.lazy(),cutoff,cfg).collect().equals(training_frame(poisoned.lazy(),cutoff,cfg).collect())
    return {**proof,'rolling_years':cfg['rolling_years'],'window_start_inclusive':lower,
            'excluded_old_rows':len(old),'old_history_label_poisoning_bit_identical':True}


def train_one(name,year):
    info=engine.train_one(name,year);meta=info['training_meta'];assert meta['first']>=lower_bound(meta['cutoff_exclusive'],CONFIGS[name])
    return info


def all_oof():
    freeze();features=engine.feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            path=OUT/f'boundary_control_{name}_{year}.json'
            if not path.exists():dump(path,boundary_control(year,cfg,features),immutable=True)
            proofs[f'{name}_{year}']=read(path);train_one(name,year)
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'boundary_controls':proofs,'test_data_read':False,'models_trained':20},immutable=True)
    log('All20 matched rolling-window neural fold models and exclusion controls completed')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'));parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
