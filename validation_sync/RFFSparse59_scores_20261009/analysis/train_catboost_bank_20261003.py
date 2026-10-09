"""Full mature-label CatBoost OOF; distinguish GPU fitting from deterministic frozen inference."""
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
spec=importlib.util.spec_from_file_location('isolated_catboost_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/catboost_bank_20261003'
COMMON={'kind':'catboost','target':'y_rank','loss_function':'RMSE','iterations':600,'learning_rate':.05,
        'l2_leaf_reg':10.,'border_count':128,'task_type':'GPU','gpu_ram_part':.65,'bootstrap_type':'Bayesian',
        'bagging_temperature':1.,'boosting_type':'Plain'}
CONFIGS={
    'cat_rank6_e600':{**COMMON,'depth':6,'seed':20261013},
    'cat_rank8_e600':{**COMMON,'depth':8,'seed':20261014},
    'cat_return6_e600':{**COMMON,'target':'y_ret_1d','loss_function':'Huber:delta=0.5','depth':6,'seed':20261015}}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS
load_bundle=engine.load_bundle


def fit_arrays(x,y,cfg):
    import numpy as np
    from catboost import CatBoostRegressor
    mean=np.nanmean(x,axis=0,dtype=np.float64).astype(np.float32);mean=np.where(np.isfinite(mean),mean,0.)
    clean=np.where(np.isfinite(x),x,mean).astype(np.float32)
    if cfg['target']=='y_rank':
        assert y.min()>=-.501 and y.max()<=.501
        target=y.astype(np.float32);bounds=None;target_scale=1.
    else:
        low,high=np.quantile(y,[.005,.995]);bounds=[float(low),float(high)];target_scale=20.
        target=(np.clip(y,low,high)*target_scale).astype(np.float32)
    parameters={key:cfg[key] for key in ('loss_function','iterations','learning_rate','l2_leaf_reg','border_count',
                'task_type','bootstrap_type','bagging_temperature','boosting_type','depth')}
    parameters.update(random_seed=cfg['seed'],thread_count=8,allow_writing_files=False,use_best_model=False)
    if cfg['task_type']=='GPU':parameters.update(devices='0',gpu_ram_part=cfg['gpu_ram_part'])
    model=CatBoostRegressor(**parameters)
    model.fit(clean,target,verbose=100 if cfg['iterations']>8 else False)
    return {'kind':'catboost','model':model,'mean':mean,'config':cfg,'target_scale':target_scale,'target_bounds':bounds,
            'gpu_training_bit_deterministic':False if cfg['task_type']=='GPU' else None,
            'frozen_model_serial_inference':True}


def predict_arrays(bundle,x):
    import numpy as np
    return bundle['model'].predict(np.where(np.isfinite(x),x,bundle['mean']).astype(np.float32),thread_count=1)/bundle['target_scale']


engine.fit_arrays=fit_arrays;engine.predict_arrays=predict_arrays


def verify():return engine.verify()


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    import catboost
    sources=[Path(__file__),SOURCE,engine.FEATURE_FILE,engine.MANIFEST,ROOT/'data/raw/训练集.csv',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md']
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'configurations':CONFIGS,
         'features':engine.feature_names(),'years':YEARS,'catboost_version':catboost.__version__,
         'validation':'2020–2024 annual expanding OOF; identical mature-label exclusion',
         'preprocessing':'Only past training means for missing values; return winsor .005/.995 learned on mature past labels, multiplied by 20.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,'test_data_read':False,
         'gpu_training_bit_deterministic':False,'gpu_disclosure':'Floating-point summation order makes separate GPU fits nondeterministic; freeze and SHA-check the actual fitted model, then verify serial inference.',
         'boundary_controls':'Bit-identical selected training inputs; CPU small-model refits with poisoned future labels; do not claim bit-identical GPU refits.',
         'documentation':'https://catboost.ai/docs/en/features/training-on-gpu',
         'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('Three GPU CatBoost target/depth configurations frozen, GPU fitting nondeterminism disclosed')


def train_one(name,year):return engine.train_one(name,year)


def all_oof():
    freeze();features=engine.feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            path=OUT/f'boundary_control_{name}_{year}.json'
            if not path.exists():
                proof=engine.boundary_control(year,dict(cfg,task_type='CPU',iterations=8,depth=4),features)
                proof.update(control_fit_device='CPU',gpu_retraining_bit_identity_not_claimed=True)
                dump(path,proof,immutable=True)
            proofs[f'{name}_{year}']=read(path);train_one(name,year)
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'boundary_controls':proofs,'test_data_read':False,'models_trained':15,
         'frozen_inference_reload_bit_identical':True,'gpu_refit_bit_deterministic':False},immutable=True)
    log('All15 CatBoost fold models, serial reloads and CPU boundary controls completed')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'));parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)


if __name__=='__main__':main()
