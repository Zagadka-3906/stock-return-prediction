"""Generate an uncovered GOSS sampling contrast from the immutable leaf trainer."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    original = A / 'train_linear_leaf_bank_20261005.py'
    source = original.read_text(encoding='utf-8-sig').replace('linear_leaf', 'gradient_sampling')
    begin, end = source.index('CONFIGS = {'), source.index('engine.OUT, engine.CONFIGS =')
    source = source[:begin] + '''CONFIGS = {
    f'{label}_goss_{level}_r300': {
        'kind': 'lightgbm_gradient_sampling', 'target': target,
        'linear_tree': False, 'linear_lambda': 0.,
        'data_sample_strategy': 'goss', 'top_rate': top, 'other_rate': other,
        'num_boost_round': 300, 'learning_rate': .05,
        'num_leaves': 31, 'max_depth': 8, 'min_data_in_leaf': 128,
        'max_bin': 127, 'lambda_l2': 1., 'seed': 20261005,
        'num_threads': 8, 'clip_z': 8., 'chunk_rows': 32768,
        'return_quantiles': [.005, .995], 'reserve_available_ram_GiB': 14.}
    for label, target in (('rank', 'y_rank'), ('return', 'y_ret_1d'))
    for level, top, other in (('low', .1, .1), ('medium', .2, .1), ('high', .4, .2))}
''' + source[end:]
    source = source.replace("'bagging_fraction': 1., 'bagging_freq': 0,", "'bagging_fraction': 1., 'bagging_freq': 0,\n        'data_sample_strategy': cfg['data_sample_strategy'],\n        'top_rate': cfg['top_rate'], 'other_rate': cfg['other_rate'],")
    source = source.replace('Matched constant/linear LightGBM leaves, using only mature past raw63 rows.',
        'Matched GOSS gradient sampling, using only mature past raw63 rows.')
    source = source.replace('Matched300-round constant leaves versus linear leaves with lambda1 or10, rank and return targets; all other parameters identical.',
        'Six300-round GOSS configurations: top/other=.1/.1,.2/.1,.4/.2, rank and return; remaining parameters and training rows match the existing constant-leaf models.')
    source = source.replace('https://lightgbm.readthedocs.io/en/latest/Parameters.html#linear_tree',
        'https://lightgbm.readthedocs.io/en/stable/Parameters.html#data_sample_strategy')
    source = source.replace("paths = [Path(__file__), SOURCE, STORAGE, proof,", "paths = [Path(__file__), SOURCE, STORAGE, proof,\n        ROOT / 'analysis/prepare_gradient_sampling_sources_20261005.py',\n        ROOT / 'analysis/train_linear_leaf_bank_20261005.py',\n        ROOT / 'analysis/gradient_sampling_complete_search_plan_20261005.json',")
    source = source.replace("model = booster.model_to_string()", "model = booster.model_to_string()\n    assert '[data_sample_strategy: goss]' in model\n    assert booster.current_iteration() == cfg['num_boost_round']\n    log(f\"GOSS {cfg['target']} top{cfg['top_rate']} other{cfg['other_rate']}: actual{booster.current_iteration()} trees\")")
    source = source.replace("reference = ROOT / 'analysis/linear_bank_20261003'", "reference = ROOT / 'analysis/linear_bank_20261003'")
    needle = "            prefix_path = OUT / f'prefix_control_{name}_{year}.json'"
    inserted = '''            matched = read(ROOT / 'analysis/linear_leaf_bank_20261005' /
                ('rank_lgb_constant_r300' if cfg['target'] == 'y_rank' else 'return_lgb_constant_r300') / f'info_{year}.json')
            assert info['training_meta'] == matched['training_meta']
            assert info['configuration']['num_boost_round'] == matched['configuration']['num_boost_round']
'''
    assert needle in source
    source = source.replace(needle, inserted + needle)
    preflight_path = A / 'verify_linear_leaf_bank_20261005.py'
    preflight = preflight_path.read_text(encoding='utf-8-sig').replace('linear_leaf', 'gradient_sampling')
    preflight = preflight.replace('Exercise actual past data, linear coefficients, saved native models and causality.',
        'Exercise actual mature data, GOSS sampling, native trees and prefix causality.')
    preflight = preflight.replace("for suffix in ('constant', 'linear_l1', 'linear_l10')", "for suffix in ('low', 'medium', 'high')")
    preflight = preflight.replace("f'{label}_lgb_{suffix}_r300'", "f'{label}_goss_{suffix}_r300'")
    preflight = preflight.replace("        assert np.isfinite(values).all()", "        assert np.isfinite(values).all()\n        assert bundle['native_training_parameters']['data_sample_strategy'] == 'goss'\n        assert bundle['native_training_parameters']['top_rate'] == cfg['top_rate']\n        assert bundle['native_training_parameters']['other_rate'] == cfg['other_rate']\n        assert '[data_sample_strategy: goss]' in bundle['model_string']")
    preflight = preflight.replace('Actual linear-leaf controls passed:', 'Actual GOSS controls passed:')
    preflight = preflight.replace('Actual gradient_sampling controls passed:', 'Actual GOSS controls passed:')
    sources = {
        A / 'train_gradient_sampling_bank_20261005.py': source,
        A / 'verify_gradient_sampling_bank_20261005.py': preflight}
    for path, text in sources.items():
        compile(text, str(path), 'exec')
        with path.open('x', encoding='utf-8', newline='') as stream:
            stream.write(text)
    create(A / 'gradient_sampling_source_generation_20261005.json', {
        'status': 'generated_new_native_GOSS_sources_without_editing_frozen_templates',
        'template_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (original, preflight_path)},
        'generated_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        'six_new_configurations': True, 'historical_DART_attempts_not_misclassified_as_new': True,
        'existing_GOSS_native_models_or_scores_found': False, 'new_quality_scores': 0})


if __name__ == '__main__':
    main()
