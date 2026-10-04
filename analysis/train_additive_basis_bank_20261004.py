"""Matched fixed additive-basis layouts; isolated engine andmature past folds."""
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
import train_additive_ridge_bank_20261004 as original
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_additive_basis_trainer_20261004',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/additive_basis_bank_20261004'
LAYOUTS={'narrow':[-.5,0.,.5],'wide5':[-2.,-1.,0.,1.,2.]}
CONFIGS={f'{label}_additive_{layout}_ridge_{suffix}':
    {'kind':'ridge_additive','target':target,'ridge_lambda':value,'chunk_rows':32768,'clip_z':8.,
     'hinge_knots':knots,'basis_layout':layout,'reserve_available_ram_GiB':8.,
     'return_quantiles':[.005,.995],'linear_reference_name':f'{label}_ridge_{suffix}'}
    for layout,knots in LAYOUTS.items()
    for label,target in (('rank','y_rank'),('return','y_ret_1d'))
    for suffix,value in (('l0001',.001),('l01',.1),('l1',1.))}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
transform,fit_arrays,predict_arrays=original.transform,original.fit_arrays,original.predict_arrays
engine.fit_arrays=fit_arrays;engine.predict_arrays=predict_arrays
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS


def verify():return engine.verify()


def freeze():
    OUT.mkdir(exist_ok=True)
    if (OUT/'protocol.json').exists():verify();return
    proof=ROOT/'analysis/additive_basis_preflight_20261004/verification.json'
    assert read(proof)['status']=='passed'
    sources=[Path(__file__),SOURCE,Path(original.__file__),engine.FEATURE_FILE,engine.MANIFEST,
        ROOT/'data/raw/训练集.csv',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md',
        ROOT/'analysis/additive_basis_model_sources_20261004.py',
        ROOT/'analysis/verify_additive_basis_bank_20261004.py',proof]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'configurations':CONFIGS,'features':engine.feature_names(),'years':YEARS,
        'validation':'2020–2024 annual expanding; same mature one-day label purge andtraining samples asraw63 linear andoriginal252-column additive bank',
        'preprocessing':'Past eligible rows fit mean/std andimputation; clip z to [-8,8]; basis z thenmax(z-k,0). Fixed knots never fitted on validation orfuture. Return winsorization uses training only.',
        'fixed_layouts':LAYOUTS,'expanded_columns':{'narrow':252,'wide5':378},
        'matched_controls':'Same two one-day targets andthree penalties asoriginal additive bank; altered knot locations andone wider layout only.',
        'inference':'Float64 fixed per-row einsum; model reload andprefix equality required.',
        'expected_annual_fits':60,'expected_five_year_configurations':12,
        'no_validation_early_stopping':True,'no_feature_selection':True,'test_data_read':False,
        'basis_choice_frozen_before_first_fit_andscoring':True,
        'scheduling_reserve':'Chosen8GiB available-memory reserve; no physical capacity claim.',
        'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)


def train_one(name,year):
    import psutil
    if not (OUT/name/f'info_{year}.json').exists():
        last=time.monotonic()
        while psutil.virtual_memory().available<CONFIGS[name]['reserve_available_ram_GiB']*2**30:
            time.sleep(10)
            if time.monotonic()-last>=50:log(f'Waiting for additive basis reserve: {name} year{year}');last=time.monotonic()
    return engine.train_one(name,year)


def all_oof():
    import numpy as np
    import polars as pl
    freeze();features=engine.feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            path=OUT/f'boundary_control_{name}_{year}.json'
            if not path.exists():dump(path,engine.boundary_control(year,cfg,features),immutable=True)
            info=train_one(name,year)
            reference_path=ROOT/'analysis/linear_bank_20261003'/cfg['linear_reference_name']/f'info_{year}.json'
            reference=read(reference_path)
            for field in ('training_matrix_sha256','training_target_sha256','training_keys_sha256'):
                assert info['training_meta'][field]==reference['training_meta'][field],field
            replay_path=OUT/f'prefix_control_{name}_{year}.json'
            if not replay_path.exists():
                frame=pl.scan_parquet(engine.FEATURE_FILE).filter(pl.col('is_train')&(pl.col('trade_date')//10000==year)).select(engine.KEYS+features+['price_valid']).sort('trade_date','ts_code').collect()
                last=int(frame['trade_date'].unique().sort()[79]);prefix=frame.filter(pl.col('trade_date')<=last)
                pred=predict_arrays(engine.load_bundle(OUT/name/f'model_{year}.joblib'),engine.to_matrix(prefix,features));pred[~prefix['price_valid'].to_numpy()]=-1e6
                raw=pl.read_parquet(OUT/name/f'raw_{year}.parquet').filter(pl.col('trade_date')<=last)
                assert prefix.select(engine.KEYS).equals(raw.select(engine.KEYS)) and np.array_equal(pred,raw['pred_raw'].to_numpy())
                dump(replay_path,{'status':'passed','actual_saved_model80_day_prefix_bit_identical':True,
                    'rows':len(prefix),'matched_raw63_training_keys_features_targets_bit_identical':True,
                    'reference_info_sha256':sha(reference_path),'test_data_read':False},immutable=True)
                del frame,prefix,pred,raw;engine.gc.collect()
            proofs[f'{name}_{year}']={'boundary':read(path),'actual_prefix':read(replay_path)}
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
        'boundary_controls':proofs,'test_data_read':False,'actual_annual_fits':60,
        'new_quality_scores':0},immutable=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'))
    parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
