"""Verify a new gate on actual mature annual OOF ranks without quality selection."""
from pathlib import Path
import hashlib
import itertools
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis'), str(ROOT / 'analysis/connected_validation_20261002')]
OUT = ROOT / 'analysis/agreement_gate_preflight_20261005'
MODELS = {
    'rank512_drop000_seed18_e64': ROOT / 'analysis/no_dropout_seed_bank_20261004/rank512_drop000_seed18_e64',
    'rank512_drop000_lr0005_e64': ROOT / 'analysis/neural_interaction_bank_20261004/rank512_drop000_lr0005_e64'}


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'POLARS_MAX_THREADS'):
        os.environ[key] = '8'
    import numpy as np
    import polars as pl
    from run import FEATURE_FILE
    import optimize_wave15 as rank_module
    from optimize_wave15 import daily_ranks
    from agreement_gated_weights_20261005 import gated_weight
    OUT.mkdir(exist_ok=True)
    source_paths = [Path(__file__), ROOT / 'analysis/agreement_gated_weights_20261005.py',
                    Path(rank_module.__file__), ROOT / 'run.py', FEATURE_FILE,
                    ROOT / '后续选模标准.md']
    source_paths += [folder / f'{kind}_{year}.{suffix}' for folder in MODELS.values()
                     for year in range(2020, 2025) for kind, suffix in (('info', 'json'), ('raw', 'parquet'))]
    bindings = {str(p.resolve()): sha(p) for p in source_paths}
    grid = [{'mode': mode, 'width': width, 'strength': strength}
            for mode, width, strength in itertools.product(('agreement', 'diversity'), (.1, .25, .5), (.25, .5, 1.))]
    create(OUT / 'frozen_before_actual_controls.json', {
        'status': 'frozen_before_actual_past_oof_controls', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': bindings, 'models': list(MODELS), 'gate_grid': grid,
        'zero_strength_restores_original_weight_without_new_math': True,
        'future_reference_must_remain_an_effective_frozen_model': True,
        'intended_followup': 'Compare gated effective layer weights against the unchanged latest qualified complete graph using the full continuous official score.',
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    observations = []
    keys = ['ts_code', 'trade_date']
    for year in range(2020, 2025):
        frame = pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train') & (pl.col('trade_date') // 10000 == year)).select(keys + ['price_valid']).sort('trade_date', 'ts_code').collect()
        dates, valid = frame['trade_date'].to_numpy(), frame['price_valid'].to_numpy()
        limit = int(np.searchsorted(dates, np.unique(dates)[79], side='right'))
        ranks, maturity = {}, {}
        for name, folder in MODELS.items():
            info = read(folder / f'info_{year}.json')
            meta = info['training_meta']
            assert info['status'] == 'passed' and meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive']
            raw = pl.read_parquet(folder / f'raw_{year}.parquet', columns=keys + ['pred_raw']).sort('trade_date', 'ts_code')
            assert raw.select(keys).equals(frame.select(keys))
            values = raw['pred_raw'].to_numpy()
            full = daily_ranks(values, valid, dates)
            prefix = daily_ranks(values[:limit], valid[:limit], dates[:limit])
            assert np.array_equal(full[:limit], prefix)
            poison = values.copy()
            poison[limit:] = np.arange(len(poison) - limit) * 1e6
            assert np.array_equal(full[:limit], daily_ranks(poison, valid, dates)[:limit])
            ranks[name] = full
            maturity[name] = {k: meta[k] for k in ('first', 'last', 'last_label_end', 'cutoff_exclusive', 'rows')}
        names = list(MODELS)
        checked = []
        for name, reference in ((names[0], names[1]), (names[1], names[0])):
            signal, ref = ranks[name], ranks[reference]
            for mode in ('agreement', 'diversity'):
                gate = {'mode': mode, 'width': .25, 'strength': 0.}
                assert gated_weight(.0375, signal, ref, gate) == .0375
                assert np.array_equal(gated_weight(np.full(len(signal), .0375), signal, ref, gate), np.full(len(signal), .0375))
            for gate in grid:
                result = gated_weight(.0375, signal, ref, gate)
                assert np.array_equal(result[:limit], gated_weight(.0375, signal[:limit], ref[:limit], gate))
                row_valid = valid & (signal > -9) & (ref > -9)
                checked.append({'model': name, 'reference': reference, **gate,
                                'minimum_weight': float(result[row_valid].min()),
                                'maximum_weight': float(result[row_valid].max()),
                                'mean_weight': float(result[row_valid].mean()),
                                'attenuated_rows': int(np.count_nonzero(result[row_valid] < .0375))})
        observations.append({'year': year, 'rows': len(frame), 'days': len(np.unique(dates)),
                             'actual80_day_prefix_rows': limit, 'mature_training': maturity, 'controls': checked,
                             'actual_prefix_and_future_source_poisoning_bit_identical': True})
        print(f'Actual{year} OOF gate controls passed: {len(checked)} nonzero andfour zero-strength controls.', flush=True)
    for path, digest in bindings.items():
        assert sha(path) == digest, path
    create(OUT / 'verification.json', {
        'status': 'passed_actual_mature_oof_gate_controls', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': bindings, 'observations': observations,
        'actual_nonzero_gate_cases': sum(len(row['controls']) for row in observations),
        'actual_zero_strength_weight_cases': 20,
        'same_day_percentile_ranks_only': True, 'zero_new_model_training': True,
        'model_raw_sources_matched_actual_keys_andmature_training': True,
        'official_whole_output_quality_not_yet_tested': True,
        'complete_graph_replay_future_inference_and_official_quality_still_required': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__':
    main()
