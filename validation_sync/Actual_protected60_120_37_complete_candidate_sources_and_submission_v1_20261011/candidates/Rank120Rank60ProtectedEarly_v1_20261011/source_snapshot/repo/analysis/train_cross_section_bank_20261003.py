"""Train the same neural objectives on label-free current-day feature percentiles."""
from pathlib import Path
import argparse
import importlib.util
import os
import sys
import time
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_cross_section_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/cross_section_bank_20261003'
FEATURE_DIR=OUT/'features'
ORIGINAL_FEATURE_FILE=engine.FEATURE_FILE
COMMON={'kind':'mlp','batch_size':32768,'learning_rate':.001,'weight_decay':.0001,'dropout':.05}
CONFIGS={
    'csrank128_e16':{**COMMON,'target':'y_rank','hidden':[128,64],'epochs':16,'seed':20261003},
    'csrank256_e32':{**COMMON,'target':'y_rank','hidden':[256,128],'epochs':32,'seed':20261006},
    'csreturn128_e16':{**COMMON,'target':'y_ret_1d','hidden':[128,64],'epochs':16,'seed':20261004}}
engine.OUT=OUT;engine.CONFIGS=CONFIGS;engine.FEATURE_FILE=FEATURE_DIR/'year*.parquet'
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS
load_bundle=engine.load_bundle
predict_preprocessed=engine.predict_arrays


def normalize_frame(frame,features):
    import polars as pl
    clean=frame.with_columns([pl.when(pl.col('price_valid')&pl.col(c).is_finite()).then(pl.col(c)).otherwise(None).alias(c) for c in features])
    return clean.with_columns([(pl.col(c).rank(method='average').over('trade_date')/pl.col(c).count().over('trade_date')).cast(pl.Float32).alias(c) for c in features])


def normalize_matrix(x,dates,valid):
    import polars as pl
    features=engine.feature_names()
    assert x.shape[1]==len(features) and len(x)==len(dates)==len(valid)
    frame=pl.DataFrame({c:x[:,i] for i,c in enumerate(features)})
    frame=frame.with_columns(pl.Series('trade_date',dates),pl.Series('price_valid',valid))
    return normalize_frame(frame,features).select(features).to_numpy()


def predict_arrays(bundle,x,dates=None,valid=None,preprocessed=False):
    if not preprocessed:
        assert dates is not None and valid is not None,'Current-day preprocessing requires aligned dates/price validity'
        x=normalize_matrix(x,dates,valid)
    return predict_preprocessed(bundle,x)


def verify():return engine.verify()


def freeze_features():
    path=OUT/'feature_protocol.json'
    if path.exists():
        for filename,digest in read(path)['input_sha256'].items():assert sha(filename)==digest,filename
        return
    sources=[Path(__file__),SOURCE,ORIGINAL_FEATURE_FILE,engine.MANIFEST,ROOT/'src/features.py',ROOT/'后续选模标准.md']
    dump(path,{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'transform':'Per date/feature: average rank divided by finite price-valid current-day count; preserve nulls.',
         'label_independent':True,'feature_pool_does_not_filter_on_label_availability':True,'training_data_only':True,
         'new_future_price_use':False,'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)


def build_features():
    import polars as pl
    freeze_features();features=engine.feature_names();lazy=pl.scan_parquet(ORIGINAL_FEATURE_FILE).filter(pl.col('is_train'))
    years=lazy.select((pl.col('trade_date')//10000).alias('year')).unique().sort('year').collect()['year'].to_list()
    FEATURE_DIR.mkdir(exist_ok=True);controls=[]
    columns=engine.KEYS+features+[c for c in ('price_valid','is_train','y_rank','y_ret_1d') if c not in features]
    for year in years:
        path=FEATURE_DIR/f'year{year}.parquet';info_path=FEATURE_DIR/f'year{year}.json'
        if info_path.exists():
            info=read(info_path);assert sha(path)==info['feature_sha256'];controls.append(info);continue
        frame=lazy.filter(pl.col('trade_date')//10000==year).select(columns).sort('trade_date','ts_code').collect()
        normalized=normalize_frame(frame,features)
        last=int(frame['trade_date'].unique().sort()[min(19,frame['trade_date'].n_unique()-1)])
        prefix=normalize_frame(frame.filter(pl.col('trade_date')<=last),features)
        assert normalized.filter(pl.col('trade_date')<=last).select(features).equals(prefix.select(features))
        poison=normalize_frame(frame.with_columns(pl.lit(float('nan')).alias('y_rank'),pl.lit(float('nan')).alias('y_ret_1d')),features)
        assert normalized.select(features).equals(poison.select(features))
        normalized.write_parquet(path,compression='zstd')
        info={'year':year,'rows':len(frame),'feature_sha256':sha(path),'label_poisoning_bit_identical':True,
              'future_append_prefix_bit_identical':True,'prefix_through':last,'test_data_read':False}
        dump(info_path,info,immutable=True);controls.append(info);log(f'Cross-sectional features {year}: {len(frame):,} rows, both causal controls passed')
        del frame,normalized,prefix,poison
    dump(OUT/'feature_audit.json',{'status':'passed','years':controls,'features':features,'test_data_read':False},immutable=True)


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    build_features()
    sources=[Path(__file__),SOURCE,OUT/'feature_protocol.json',OUT/'feature_audit.json',engine.MANIFEST,
             ROOT/'run.py',ROOT/'后续选模标准.md',*sorted(FEATURE_DIR.glob('*.parquet')),*sorted(FEATURE_DIR.glob('*.json'))]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'configurations':CONFIGS,
         'features':engine.feature_names(),'years':YEARS,'validation':'2020–2024 annual expanding OOF with identical mature-label purge',
         'feature_preprocessing':'Current-day cross-sectional percentiles before past-only mean/std; no label-dependent feature pool.',
         'target_definition':'Keep the original cached y_rank target and the frozen engine offset; future one-day return mapping occurs only after output selection.',
         'raw_matched_control':'csrank128_e16 and csreturn128_e16 use the same architecture, epochs and seeds as the raw-input models.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,'test_data_read':False,
         'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('Three cross-sectional-input neural configurations frozen')


def train_one(name,year):return engine.train_one(name,year)


def all_oof():
    freeze();features=engine.feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            path=OUT/f'boundary_control_{name}_{year}.json'
            if not path.exists():dump(path,engine.boundary_control(year,cfg,features),immutable=True)
            proofs[f'{name}_{year}']=read(path);train_one(name,year)
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'boundary_controls':proofs,'test_data_read':False,'models_trained':len(CONFIGS)*len(YEARS)},immutable=True)
    log('All15 cross-sectional neural fold models and maturity controls completed')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('features','freeze','all','train'));parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='features':build_features()
    elif args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)


if __name__=='__main__':main()
