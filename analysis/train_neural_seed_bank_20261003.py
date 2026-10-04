"""Prespecified MLP capacity/epoch bank; isolate the frozen base trainer globals."""
from pathlib import Path
import argparse
import importlib.util
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_seed_neural_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/neural_seed_bank_20261003'
COMMON={'kind':'mlp','target':'y_rank','batch_size':32768,'learning_rate':.001,'weight_decay':.0001,'dropout':.05}
CONFIGS={
    'rank512_seed16_e32':{**COMMON,'hidden':[512,256,128],'epochs':32,'seed':20261016},
    'rank512_seed17_e32':{**COMMON,'hidden':[512,256,128],'epochs':32,'seed':20261017},
    'rank512_seed18_e64':{**COMMON,'hidden':[512,256,128],'epochs':64,'seed':20261018},
    'rank1024_seed19_e32':{**COMMON,'hidden':[1024,512,256],'epochs':32,'seed':20261019}}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS


def verify():return engine.verify()


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),SOURCE,engine.FEATURE_FILE,engine.MANIFEST,ROOT/'data/raw/训练集.csv',ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md']
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'configurations':CONFIGS,
         'features':engine.feature_names(),'years':YEARS,'validation':'2020–2024 annual expanding OOF with identical mature-label purge',
         'preprocessing':'Each fold learns only past mean/std and return winsor bounds; fixed inference batch padding guarantees row-prefix replay.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,'test_data_read':False,
         'baseline_training_engine_sha256':sha(SOURCE),'isolated_module_globals':True,
         'purpose':'Compare seeds and capacity near the R15 signal, then frozen ensemble recipes; all model parameters preset before any score for these new models, no validation-driven epoch selection.',
         'input_sha256':{str(p.resolve()):sha(p) for p in sources}},immutable=True)
    log('Four neural seed/capacity configurations frozen')


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
    log('All20 additional neural seed/capacity fold models and maturity controls completed')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'));parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)


if __name__=='__main__':main()
