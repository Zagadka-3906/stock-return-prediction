"""Actual private-fitter parity and fixed-batch prefix controls before fitting."""
from pathlib import Path
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
OUT = ROOT / 'analysis/no_dropout_seed_preflight_20261004'


def main():
    import numpy as np
    import train_no_dropout_seed_bank_20261004 as bank
    import train_neural_regularization_bank_20261003 as control
    OUT.mkdir(exist_ok=True)
    assert not (OUT / 'verification.json').exists()
    cfg = control.CONFIGS['rank512_drop000_e32']
    assert cfg == bank.COMMON
    original_out, original_configs = control.engine.OUT, dict(control.engine.CONFIGS)
    assert bank.engine is not control.engine and bank.engine.OUT != control.engine.OUT
    assert bank.engine.fit_arrays.__code__.co_code == control.engine.fit_arrays.__code__.co_code
    assert bank.engine.predict_arrays.__code__.co_code == control.engine.predict_arrays.__code__.co_code
    assert {(c['seed'], c['epochs']) for c in bank.CONFIGS.values()} == {(20261016, 32), (20261017, 32), (20261018, 32), (20261018, 64)}
    assert all({k: v for k, v in c.items() if k not in ('seed', 'epochs')} == {k: v for k, v in cfg.items() if k not in ('seed', 'epochs')} for c in bank.CONFIGS.values())
    paths = [Path(__file__), Path(bank.__file__), bank.SOURCE, Path(control.__file__),
        ROOT / 'results/optimization_20261003_r31.json',
        ROOT / 'analysis/optimization_20261003_r31/selection.json']
    hashes = {str(p.resolve()): bank.sha(p) for p in paths}
    bank.dump(OUT / 'frozen_before_controls.json', {'status': 'frozen_implementation_controls',
        'input_sha256': hashes, 'new_quality_scores': 0, 'test_data_read': False}, immutable=True)
    rng = np.random.default_rng(20261004)
    x = rng.standard_normal((1024, 63)).astype(np.float32)
    x[::31, 3] = np.nan
    y = np.linspace(-.5, .5, len(x), dtype=np.float32)
    small = {**cfg, 'epochs': 1}
    a = control.engine.fit_arrays(x, y, small)
    b = bank.engine.fit_arrays(x, y, small)
    assert np.array_equal(a['mean'], b['mean']) and np.array_equal(a['scale'], b['scale'])
    assert all(np.array_equal(a['state'][key].numpy(), b['state'][key].numpy()) for key in a['state'])
    full = bank.engine.predict_arrays(b, x)
    assert np.array_equal(full, control.engine.predict_arrays(a, x))
    for n in (1, 80, 1023):
        assert np.array_equal(full[:n], bank.engine.predict_arrays(b, x[:n]))
    assert control.engine.OUT == original_out and control.engine.CONFIGS == original_configs
    for path, digest in hashes.items():
        assert bank.sha(Path(path)) == digest, path
    bank.dump(OUT / 'verification.json', {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_selected_control_private_fitter_preprocessing_weights_andpredictions_bit_identical': True,
        'original_trainer_globals_unchanged': True, 'actual_padded_prediction_prefix_bit_identical': True,
        'prespecified_four_seed_epoch_configs': True,
        'input_sha256': hashes, 'new_quality_scores': 0, 'test_data_read': False,
        'scope': 'Actual one-epoch1024-row fitter parity before20 annual fits; annual maturity, native future andcomplete official scheme controls still required.'}, immutable=True)
    print('Actual no-dropout private-fitter andprefix controls passed', flush=True)


if __name__ == '__main__':
    main()
