"""Frozen equal-weight no-dropout ensembles, with actual portable child replay."""
from pathlib import Path
import argparse
import importlib.util
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
SOURCE = ROOT / 'analysis/train_neural_ensemble_bank_20261003.py'
spec = importlib.util.spec_from_file_location('isolated_no_dropout_ensemble_trainer_20261004', SOURCE)
engine = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = engine
spec.loader.exec_module(engine)
import no_dropout_seed_member_sources_20261004 as members
OUT = ROOT / 'analysis/no_dropout_ensemble_bank_20261004'
GROUPS = {
    'nn512_drop000_three32': ['rank512_drop000_e32', 'rank512_drop000_seed16_e32', 'rank512_drop000_seed17_e32'],
    'nn512_drop000_all5': ['rank512_drop000_e32', 'rank512_drop000_seed16_e32', 'rank512_drop000_seed17_e32', 'rank512_drop000_seed18_e32', 'rank512_drop000_seed18_e64']}
CONFIGS = {f'{group}_{mode}': {'kind': 'neural_ensemble', 'target': 'y_rank', 'members': names,
    'aggregation': mode, 'weights': [1 / len(names)] * len(names)}
    for group, names in GROUPS.items() for mode in ('rawmean', 'rankmean')}
engine.OUT, engine.CONFIGS, engine.GROUPS, engine.members = OUT, CONFIGS, GROUPS, members
read, dump, sha, log = members.read, members.dump, members.sha, members.log
YEARS = members.YEARS
aggregate, predict_arrays, load_bundle = engine.aggregate, engine.predict_arrays, engine.load_bundle


def verify():
    return engine.verify()


def freeze():
    if (OUT / 'protocol.json').exists():
        verify()
        return
    native = members.bank
    assert (native.OUT / 'protocol.json').exists()
    paths = [Path(__file__), SOURCE, Path(members.__file__), Path(native.__file__),
        native.OUT / 'protocol.json', native.PREFLIGHT,
        ROOT / 'run.py', ROOT / '后续选模标准.md',
        ROOT / 'results/optimization_20261003_r31.json']
    for year in YEARS:
        paths += [native.BASELINE / f'{kind}_{year}.{extension}' for kind, extension in (('info', 'json'), ('raw', 'parquet'), ('model', 'joblib'))]
    dump(OUT / 'protocol.json', {'frozen_at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'configurations': CONFIGS, 'years': YEARS, 'features': native.engine.feature_names(),
        'expected_annual_forecast_artifacts': 20, 'new_model_fits': 0,
        'members': 'Selected original no-dropout model plus prespecified new mature seed/epoch fits; original member reused.',
        'aggregation': 'Fixed equal raw-score or price-valid daily-rank mean; target availability never defines rank pool.',
        'new_member_infos_andbytes_frozen_before_assembly': 'assembly_inputs.json is written only after actual20-fit OOF audit passes.',
        'new_quality_scores': 0, 'test_data_read': False,
        'input_sha256': {str(path.resolve()): sha(path) for path in paths}}, immutable=True)
    log('Four equal-weight no-dropout ensemble recipes frozen before any ensemble quality scores')


def assembly_freeze():
    freeze()
    members.verify()
    path = OUT / 'assembly_inputs.json'
    if path.exists():
        for source, digest in read(path)['input_sha256'].items():
            assert sha(Path(source)) == digest, source
        return
    sources = [members.bank.OUT / 'oof_audit.json', OUT / 'protocol.json']
    for name in dict.fromkeys(name for names in GROUPS.values() for name in names):
        for year in YEARS:
            directory = members.source_dir(name)
            sources += [directory / f'info_{year}.json', directory / f'model_{year}.joblib', directory / f'raw_{year}.parquet']
    dump(path, {'status': 'frozen_actual_members_before_assembly',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'new_model_fits': 0, 'test_data_read': False,
        'input_sha256': {str(source.resolve()): sha(source) for source in sources}}, immutable=True)


def train_one(name, year):
    assembly_freeze()
    return engine.train_one(name, year)


def all_oof():
    freeze()
    while not (members.bank.OUT / 'oof_audit.json').exists():
        time.sleep(10)
    assembly_freeze()
    for name in CONFIGS:
        for year in YEARS:
            train_one(name, year)
    dump(OUT / 'oof_audit.json', {'status': 'passed', 'configurations': CONFIGS, 'years': YEARS,
        'actual_annual_forecast_artifacts': 20, 'models_trained': 0,
        'actual_member_model_reload_andfull_annual_output_bit_identical': True,
        'complete80_day_prefix_checks': 20, 'label_independent_aggregation': True,
        'assembly_inputs_sha256': sha(OUT / 'assembly_inputs.json'),
        'new_quality_scores': 0, 'test_data_read': False}, immutable=True)
    log('All20 no-dropout virtual ensemble outputs andactual child replay passed; zero new fits')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('freeze', 'all', 'train'))
    parser.add_argument('--name', choices=tuple(CONFIGS))
    parser.add_argument('--year', type=int)
    args = parser.parse_args()
    if args.stage == 'freeze':
        freeze()
    elif args.stage == 'all':
        all_oof()
    else:
        assert args.name and args.year in (*YEARS, 2025)
        train_one(args.name, args.year)
