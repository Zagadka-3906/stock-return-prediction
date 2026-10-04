"""Matched RankNet width and temperature variants around the useful R17 signal."""
from pathlib import Path
import argparse
import importlib.util
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_objective_bank_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_pairwise_objective_bank',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/pairwise_bank_20261003'
COMMON=engine.CONFIGS['pair_rank128_e32']
CONFIGS={
    'pair_rank256_e32':{**COMMON,'hidden':[256,128]},
    'pair_rank512_e32':{**COMMON,'hidden':[512,256,128]},
    'pair_rank128_t005_e32':{**COMMON,'temperature':.05},
    'pair_rank128_t020_e32':{**COMMON,'temperature':.2}}
engine.OUT=OUT;engine.CONFIGS=CONFIGS;engine.engine.OUT=OUT;engine.engine.CONFIGS=CONFIGS
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS


def verify():return engine.verify()


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),SOURCE,engine.SOURCE,engine.engine.FEATURE_FILE,engine.engine.MANIFEST,
             ROOT/'data/raw/训练集.csv',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md']
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'configurations':CONFIGS,
         'features':engine.engine.feature_names(),'years':YEARS,'validation':'2020–2024 annual expanding OOF; unchanged mature-label purge',
         'matched_controls':'Same seed, epochs, sampling, MSE penalty and optimizer as pair_rank128_e32. Compare two widths at temperature0.1, and temperatures0.05/0.2 at original width.',
         'objective':'Same-day mature training partner sampling; rank-gap weighted softplus plus 0.1*MSE; centered daily ranks.',
         'preprocessing':'Past-only mean/std and fixed padded inference batches.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,'test_data_read':False,
         'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('Four matched RankNet width/temperature configurations frozen')


def train_one(name,year):return engine.train_one(name,year)


def all_oof():
    freeze();features=engine.engine.feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            path=OUT/f'boundary_control_{name}_{year}.json'
            if not path.exists():dump(path,engine.boundary_control(year,cfg,features),immutable=True)
            proofs[f'{name}_{year}']=read(path);train_one(name,year)
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'boundary_controls':proofs,'test_data_read':False,'models_trained':20},immutable=True)
    log('All20 matched RankNet width/temperature fold models completed')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'));parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
