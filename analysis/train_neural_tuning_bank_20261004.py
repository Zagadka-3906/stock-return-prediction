"""Matched rank512 target-offset and learning-rate grid; past-only annual OOF."""
from pathlib import Path
import argparse
import importlib.util
import inspect
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_neural_tuning_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
original_fit_arrays=engine.fit_arrays
fit_source=inspect.getsource(original_fit_arrays)
old_target='target=y.astype(np.float32)-.5'
assert fit_source.count(old_target)==1
fit_source=fit_source.replace(old_target,"target=y.astype(np.float32)+cfg['rank_training_offset']")
old_return="'target_scale':target_scale,'config':cfg"
assert fit_source.count(old_return)==1
fit_source=fit_source.replace(old_return,"'actual_fit_target_sha256':array_hash(target), 'actual_fit_target_mean':float(target.mean(dtype=np.float64)), 'actual_fit_target_min':float(target.min()), 'actual_fit_target_max':float(target.max()), "+old_return)
exec(compile(fit_source,str(Path(__file__))+'::matched_fit_arrays','exec'),engine.__dict__)
OUT=ROOT/'analysis/neural_tuning_bank_20261004'
PREFLIGHT=ROOT/'analysis/neural_tuning_preflight_20261004/verification.json'
BASELINE=ROOT/'analysis/neural_bank_20261003/rank512_e32'
COMMON={'kind':'mlp','target':'y_rank','batch_size':32768,'learning_rate':.001,
        'weight_decay':.0001,'dropout':.05,'hidden':[512,256,128],'epochs':32,
        'seed':20261007,'rank_training_offset':-.5}
CONTROL={**COMMON}
CONFIGS={
    'rank512_o05_lr0005_e32':{**COMMON,'learning_rate':.0005},
    'rank512_o05_lr002_e32':{**COMMON,'learning_rate':.002},
    'rank512_o0_lr0005_e32':{**COMMON,'rank_training_offset':0.,'learning_rate':.0005},
    'rank512_o0_lr001_e32':{**COMMON,'rank_training_offset':0.},
    'rank512_o0_lr002_e32':{**COMMON,'rank_training_offset':0.,'learning_rate':.002}}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS


def verify():return engine.verify()


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    assert read(PREFLIGHT)['status']=='passed'
    sources=[Path(__file__),SOURCE,engine.FEATURE_FILE,engine.MANIFEST,ROOT/'data/raw/训练集.csv',
             ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md',PREFLIGHT,
             ROOT/'analysis/verify_neural_tuning_20261004.py',
             ROOT/'analysis/neural_tuning_model_sources_20261004.py',
             ROOT/'analysis/train_neural_bank_20261003.py',*[BASELINE/f'info_{year}.json' for year in YEARS]]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'configurations':CONFIGS,'features':engine.feature_names(),'years':YEARS,
         'validation':'2020–2024 annual expanding OOF; identical mature-label cutoff',
         'design':'Prespecified 2x3 grid: rank target offsets {-0.5,0} after float32 cast; learning rates {0.0005,0.001,0.002}. Reuse rank512_e32 for offset -0.5/lr0.001 control; five new configurations.',
         'matched_baseline':'rank512_e32; identical architecture, seed,32 epochs, batch, dropout, weight decay, raw training keys/features/provided targets.',
         'target_interpretation':'Both offsets are legitimate affine objectives. Raw provided y_rank is centered; the historical -0.5 shift is retained as the matched control, not treated as leakage or invalidity.',
         'implementation':'Private copy of frozen fitter; only float32 rank-target offset expression and target diagnostic metadata change. Original source remains unchanged.',
         'preprocessing':'Past-only feature mean/std, imputation and clipping; fixed padded inference batches.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,
         'test_data_read':False,'expected_annual_fits':25,
         'input_sha256':{str(path.resolve()):sha(path) for path in sources}},immutable=True)
    log('Five target-offset/learning-rate configurations frozen; baseline control reused')


def train_one(name,year):
    info=engine.train_one(name,year);baseline=read(BASELINE/f'info_{year}.json')
    keys=('rows','days','first','last','cutoff_exclusive','last_label_end','features',
          'training_matrix_sha256','training_target_sha256','training_keys_sha256')
    assert all(info['training_meta'][key]==baseline['training_meta'][key] for key in keys),(name,year)
    return info


def all_oof():
    import numpy as np
    import polars as pl
    freeze();features=engine.feature_names();proofs={};prefix={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            path=OUT/f'boundary_control_{name}_{year}.json'
            if not path.exists():dump(path,engine.boundary_control(year,cfg,features),immutable=True)
            proofs[f'{name}_{year}']=read(path);train_one(name,year)
            replay_path=OUT/f'prefix_control_{name}_{year}.json'
            if not replay_path.exists():
                frame=pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).sort('trade_date','ts_code').select(features).head(32781).collect()
                x=engine.to_matrix(frame,features);bundle=engine.load_bundle(OUT/name/f'model_{year}.joblib')
                full=engine.predict_arrays(bundle,x)
                for n in (1,80,32767,32768):assert np.array_equal(full[:n],engine.predict_arrays(bundle,x[:n])),(name,year,n)
                dump(replay_path,{'status':'passed','model':name,'year':year,'prefix_rows':[1,80,32767,32768],
                     'full_rows':len(x),'padded_prefix_bit_identical':True,
                     'actual_fit_target_sha256':bundle['actual_fit_target_sha256'],
                     'actual_fit_target_mean':bundle['actual_fit_target_mean'],
                     'actual_fit_target_min':bundle['actual_fit_target_min'],
                     'actual_fit_target_max':bundle['actual_fit_target_max']},immutable=True)
            prefix[f'{name}_{year}']=read(replay_path)
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'boundary_controls':proofs,'prefix_controls':prefix,
         'raw_training_inputs_bit_identical_to_baseline':True,
         'actual_rank_fit_target_expression':'provided_y_rank.astype(float32)+configured_offset',
         'test_data_read':False,'models_trained':25},immutable=True)
    log('All25 matched target-offset/learning-rate fold models and maturity controls completed')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'))
    parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
