"""Matched CatBoost learning-rate/budget, regularization and depth controls."""
from pathlib import Path
import argparse
import importlib.util
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import train_catboost_bank_20261003 as reference
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_catboost_tuning_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/catboost_tuning_bank_20261004'
PREFLIGHT=ROOT/'analysis/catboost_tuning_preflight_20261004/verification.json'
BASELINE=reference.OUT/'cat_rank6_e600'
COMMON={**reference.CONFIGS['cat_rank6_e600']}
CONFIGS={
    'cat_rank6_lr0025_e600':{**COMMON,'learning_rate':.025},
    'cat_rank6_lr0025_e1200':{**COMMON,'learning_rate':.025,'iterations':1200},
    'cat_rank6_l2_1_e600':{**COMMON,'l2_leaf_reg':1.},
    'cat_rank6_l2_100_e600':{**COMMON,'l2_leaf_reg':100.},
    'cat_rank10_e600':{**COMMON,'depth':10}}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
engine.fit_arrays=reference.fit_arrays;engine.predict_arrays=reference.predict_arrays
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS


def verify():return engine.verify()


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    import catboost
    assert read(PREFLIGHT)['status']=='passed'
    sources=[Path(__file__),Path(reference.__file__),SOURCE,engine.FEATURE_FILE,engine.MANIFEST,
             ROOT/'data/raw/训练集.csv',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md',
             PREFLIGHT,ROOT/'analysis/verify_catboost_tuning_20261004.py',
             ROOT/'analysis/catboost_tuning_model_sources_20261004.py',
             *[BASELINE/f'info_{year}.json' for year in YEARS]]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'configurations':CONFIGS,'matched_control':COMMON,'features':engine.feature_names(),'years':YEARS,
         'catboost_version':catboost.__version__,'validation':'2020–2024 annual expanding OOF with unchanged mature-label cutoff',
         'design':'Five prespecified controls: lr0.025 at600/1200 iterations; l2_leaf_reg1/100 at baseline lr0.05 and600 iterations; depth10 at the baseline budget. All use rank6 baseline seed20261013, original63 features and provided centered one-day ranks.',
         'reused_baseline':'cat_rank6_e600; depth6,lr0.05,600 iterations,l2_leaf_reg10',
         'raw_training_inputs':'Training feature, provided target and key hashes must match the depth6 baseline at every annual/full-training cutoff.',
         'preprocessing':'Past training means impute missing inputs; unchanged frozen CatBoost fitter and serial CPU inference.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,'expected_annual_fits':25,
         'gpu_training_bit_deterministic':False,'frozen_actual_model_inference_verified':True,
         'boundary_controls':'Identical mature rows and CPU small-model repeated fitting under poisoned future labels; no claim of bit-identical GPU refits.',
         'test_data_read':False,'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('Five matched CatBoost tuning configurations frozen; original fitter and control reused')


def train_one(name,year):
    info=engine.train_one(name,year);baseline=read(BASELINE/f'info_{year}.json')
    fields=('rows','days','first','last','cutoff_exclusive','last_label_end','features',
            'training_matrix_sha256','training_target_sha256','training_keys_sha256')
    assert all(info['training_meta'][key]==baseline['training_meta'][key] for key in fields),(name,year)
    return info


def all_oof():
    import numpy as np
    import polars as pl
    freeze();features=engine.feature_names();boundaries={};prefixes={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            control=OUT/f'boundary_control_{name}_{year}.json'
            if not control.exists():
                proof=engine.boundary_control(year,dict(cfg,task_type='CPU',iterations=8,depth=4),features)
                proof.update(control_fit_device='CPU',gpu_retraining_bit_identity_not_claimed=True)
                dump(control,proof,immutable=True)
            boundaries[f'{name}_{year}']=read(control);train_one(name,year)
            target=OUT/f'prefix_control_{name}_{year}.json'
            if not target.exists():
                frame=pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).sort('trade_date','ts_code').select(features).head(32781).collect()
                x=engine.to_matrix(frame,features);bundle=engine.load_bundle(OUT/name/f'model_{year}.joblib');full=engine.predict_arrays(bundle,x)
                for n in (1,80,32767,32768):assert np.array_equal(full[:n],engine.predict_arrays(bundle,x[:n])),(name,year,n)
                dump(target,{'status':'passed','model':name,'year':year,'rows':len(x),
                     'prefix_rows':[1,80,32767,32768],'serial_cpu_prefix_bit_identical':True,
                     'frozen_model_sha256':sha(OUT/name/f'model_{year}.joblib')},immutable=True)
            prefixes[f'{name}_{year}']=read(target)
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'boundary_controls':boundaries,'prefix_controls':prefixes,'models_trained':25,
         'raw_training_inputs_bit_identical_to_baseline':True,'frozen_model_reload_bit_identical':True,
         'gpu_refit_bit_deterministic':False,'test_data_read':False},immutable=True)
    log('All25 CatBoost tuning annual models, CPU maturity controls and frozen inference checks completed')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'))
    parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
