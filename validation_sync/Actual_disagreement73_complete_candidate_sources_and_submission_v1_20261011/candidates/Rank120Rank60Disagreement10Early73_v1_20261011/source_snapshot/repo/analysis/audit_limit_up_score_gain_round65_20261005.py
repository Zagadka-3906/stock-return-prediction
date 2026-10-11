"""Attribute R65's tiny gain using every original training-validation row."""
from pathlib import Path
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/round65_limit_up_gain_audit_20261005'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(name, payload):
    with (OUT / name).open('x', encoding='utf-8') as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)


def main():
    import numpy as np
    import pandas as pd
    import polars as pl
    from scipy.stats import spearmanr

    for variable in ('TMP', 'TEMP', 'TMPDIR'):
        assert Path(os.environ[variable]).drive.upper() in ('D:', 'E:')
    OUT.mkdir(exist_ok=True)
    sources = [Path(__file__), ROOT / 'evaluate.py', ROOT / '后续选模标准.md',
               ROOT / 'data/features.parquet',
               ROOT / 'analysis/optimization_20261003_r64/selected_validation.npy',
               ROOT / 'analysis/optimization_20261003_r65/promote_baseline.npy',
               ROOT / 'analysis/optimization_20261003_r65/selected_validation.npy',
               ROOT / 'analysis/optimization_20261003_r65/calibrated_csv_official.json',
               ROOT / 'analysis/optimization_20261003_r65/scoring_validation_only/测试集_X.csv',
               ROOT / 'analysis/optimization_20261003_r65/scoring_validation_only/测试集_Y.csv',
               ROOT / 'results/optimization_20261003_r64.json']
    bindings = {str(path.resolve()): sha(path) for path in sources}
    save('frozen_before_controls.json', {
        'status': 'frozen_before_full_training_validation_pool_and_score_attribution',
        'input_sha256': bindings, 'scope': 'All2020–2024 training-validation rows; scoring adapter filenames denote training-only data.',
        'expected_rows': 5635800, 'expected_days': 1212,
        'original_official_missing_label_and_limit_up_filters_preserved': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    d = ROOT / 'analysis/optimization_20261003_r65'
    a = np.load(ROOT / 'analysis/optimization_20261003_r64/selected_validation.npy', mmap_mode='r')
    promoted = np.load(d / 'promote_baseline.npy', mmap_mode='r')
    b = np.load(d / 'selected_validation.npy', mmap_mode='r')
    assert len(a) == len(b) == 5635800 and np.array_equal(a, promoted)
    original = pl.scan_parquet(ROOT / 'data/features.parquet').filter(
        pl.col('is_train') & pl.col('trade_date').is_between(20200101, 20241231)).select(
        'ts_code', 'trade_date', 'flag_limit_up', 'y_ret_1d').sort('trade_date', 'ts_code').collect()
    x = pl.read_csv(d / 'scoring_validation_only/测试集_X.csv').sort('trade_date', 'ts_code')
    # Match the official pandas parser for labels, then prove their training origin.
    y = pd.read_csv(d / 'scoring_validation_only/测试集_Y.csv').sort_values(['trade_date', 'ts_code']).reset_index(drop=True)
    keys = original.select('ts_code', pl.col('trade_date').cast(pl.Int64))
    assert keys.equals(x.select('ts_code', pl.col('trade_date').cast(pl.Int64)))
    assert keys.equals(pl.from_pandas(y[['ts_code', 'trade_date']]).select('ts_code', pl.col('trade_date').cast(pl.Int64)))
    labels = y['y_ret_1d'].to_numpy(dtype=np.float64)
    original_labels = original['y_ret_1d'].to_numpy()
    assert np.array_equal(np.isnan(labels), np.isnan(original_labels))
    assert np.allclose(labels, original_labels, rtol=1e-12, atol=1e-12, equal_nan=True)
    flags = x['flag_limit_up'].to_numpy()
    assert np.array_equal(flags, original['flag_limit_up'].to_numpy())
    dates = original['trade_date'].to_numpy()
    days, first, counts = np.unique(dates, return_index=True, return_counts=True)
    assert len(days) == 1212 and (counts == 4650).all()
    ic_a, ic_b, turnover_pools, return_pools = [], [], 0, 0
    for date, start, count in zip(days, first, counts):
        stop = start + count
        sa, sb, up, ly = a[start:stop], b[start:stop], flags[start:stop], labels[start:stop]
        return_pool = np.flatnonzero((up == 0) & ~np.isnan(ly))
        turnover_pool = np.flatnonzero(up == 0)
        for pool in (return_pool, turnover_pool):
            old_order = pool[np.argsort(-sa[pool], kind='stable')]
            new_order = pool[np.argsort(-sb[pool], kind='stable')]
            assert np.array_equal(old_order, new_order), int(date)
        return_pools += len(return_pool)
        turnover_pools += len(turnover_pool)
        valid = ~np.isnan(ly)
        assert valid.sum() >= 30
        ic_a.append(float(spearmanr(sa[valid], ly[valid]).statistic))
        ic_b.append(float(spearmanr(sb[valid], ly[valid]).statistic))
    previous = read(ROOT / 'results/optimization_20261003_r64.json')['winner']['metrics']
    selected = read(d / 'calibrated_csv_official.json')['metrics']
    assert abs(float(np.mean(ic_a)) - previous['ic_mean']) < 1e-12
    assert abs(float(np.mean(ic_b)) - selected['ic_mean']) < 1e-12
    assert previous['annual_excess'] == selected['annual_excess']
    assert previous['mean_turnover'] == selected['mean_turnover']
    assert previous['top1_annual_ret'] == selected['top1_annual_ret']
    gain = selected['final_score'] - previous['final_score']
    assert gain > 0. and abs(gain - .4 * (selected['ic_mean'] - previous['ic_mean'])) < 1e-15
    for source, expected in bindings.items():
        assert sha(source) == expected, source
    result = {'status': 'passed_full_original_training_validation_gain_attribution',
              'input_sha256': bindings, 'rows': len(a), 'days': len(days),
              'baseline_replayed_from_previous_selected_vector_bit_identical': True,
              'official_adapter_labels_and_flags_proven_original_training_only': True,
              'all_non_limit_up_prediction_orders_bit_identical': True,
              'return_pool_total_rows': return_pools, 'turnover_pool_total_rows': turnover_pools,
              'top10_percent_return_and_turnover_memberships_identical_every_day': True,
              'four_year_boundaries_preserved': True,
              'independent_full_spearman_ic_previous': float(np.mean(ic_a)),
              'independent_full_spearman_ic_selected': float(np.mean(ic_b)),
              'official_score_gain': gain, 'gain_entirely_from_official_IC_term': True,
              'ICIR_decline_not_used_as_selection_gate': selected['icir'] < previous['icir'],
              'previous_test_labels_not_read': True, 'new_model_fits': 0, 'new_quality_scores': 0,
              'test_labels_read': False}
    save('verification.json', result)
    print(json.dumps({key: value for key, value in result.items() if key != 'input_sha256'}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
