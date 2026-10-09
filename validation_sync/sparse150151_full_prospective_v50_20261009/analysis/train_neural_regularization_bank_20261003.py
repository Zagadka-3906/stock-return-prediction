"""Matched512-wide dropout/weight-decay variations with the original seed and budget."""
from pathlib import Path
import argparse
import importlib.util
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
SOURCE=ROOT/'analysis/train_diverse_backbones_20261003.py'
spec=importlib.util.spec_from_file_location('isolated_regularization_neural_trainer',SOURCE)
engine=importlib.util.module_from_spec(spec);sys.modules[spec.name]=engine;spec.loader.exec_module(engine)
OUT=ROOT/'analysis/neural_regularization_bank_20261003'
BASELINE=ROOT/'analysis/neural_bank_20261003/rank512_e32'
COMMON={'kind':'mlp','target':'y_rank','batch_size':32768,'learning_rate':.001,
        'weight_decay':.0001,'dropout':.05,'hidden':[512,256,128],'epochs':32,'seed':20261007}
CONFIGS={
    'rank512_drop000_e32':{**COMMON,'dropout':0.},
    'rank512_drop015_e32':{**COMMON,'dropout':.15},
    'rank512_wd001_e32':{**COMMON,'weight_decay':.001},
    'rank512_wd00001_e32':{**COMMON,'weight_decay':.00001}}
engine.OUT=OUT;engine.CONFIGS=CONFIGS
read,dump,sha,log=engine.read,engine.dump,engine.sha,engine.log
YEARS=engine.YEARS


def verify():return engine.verify()


def freeze():
    if (OUT/'protocol.json').exists():verify();return
    sources=[Path(__file__),SOURCE,engine.FEATURE_FILE,engine.MANIFEST,ROOT/'data/raw/训练集.csv',
             ROOT/'run.py',ROOT/'src/features.py',ROOT/'后续选模标准.md',
             ROOT/'analysis/train_neural_bank_20261003.py',*[BASELINE/f'info_{year}.json' for year in YEARS]]
    dump(OUT/'protocol.json',{'frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'configurations':CONFIGS,'features':engine.feature_names(),'years':YEARS,
         'validation':'2020–2024 annual expanding OOF; identical mature-label purge',
         'matched_baseline':'rank512_e32; identical architecture, seed, learning rate,32 epochs, training keys, features and target. Exactly one configured dropout or weight-decay value changes.',
         'randomness':'Same initial seed; removing dropout naturally changes subsequent stochastic RNG consumption. Do not claim identical minibatch orders for the no-dropout variant.',
         'rank_target_behavior':'Match the frozen baseline engine, including its existing centered-rank constant shift.',
         'preprocessing':'Past-only feature mean/std, imputation and clipping; fixed padded inference batches.',
         'no_early_stopping_on_validation':True,'no_feature_selection':True,
         'test_data_read':False,'expected_annual_fits':20,
         'input_sha256':{str(path.resolve()):sha(path) for path in sources}},immutable=True)
    log('Four matched neural dropout/weight-decay configurations frozen')


def train_one(name,year):
    info=engine.train_one(name,year);baseline=read(BASELINE/f'info_{year}.json')
    keys=('rows','days','first','last','cutoff_exclusive','last_label_end','features',
          'training_matrix_sha256','training_target_sha256','training_keys_sha256')
    assert all(info['training_meta'][key]==baseline['training_meta'][key] for key in keys),(name,year)
    return info


def all_oof():
    freeze();features=engine.feature_names();proofs={}
    for name,cfg in CONFIGS.items():
        for year in YEARS:
            path=OUT/f'boundary_control_{name}_{year}.json'
            if not path.exists():dump(path,engine.boundary_control(year,cfg,features),immutable=True)
            proofs[f'{name}_{year}']=read(path);train_one(name,year)
    dump(OUT/'oof_audit.json',{'status':'passed','configurations':CONFIGS,'years':YEARS,
         'boundary_controls':proofs,'training_inputs_bit_identical_to_baseline':True,
         'test_data_read':False,'models_trained':20},immutable=True)
    log('All20 matched regularization fold models and maturity controls completed')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('freeze','all','train'))
    parser.add_argument('--name',choices=tuple(CONFIGS));parser.add_argument('--year',type=int)
    args=parser.parse_args()
    if args.stage=='freeze':freeze()
    elif args.stage=='all':all_oof()
    else:
        if not args.name or args.year not in (*YEARS,2025):parser.error('train requires --name and --year')
        train_one(args.name,args.year)
