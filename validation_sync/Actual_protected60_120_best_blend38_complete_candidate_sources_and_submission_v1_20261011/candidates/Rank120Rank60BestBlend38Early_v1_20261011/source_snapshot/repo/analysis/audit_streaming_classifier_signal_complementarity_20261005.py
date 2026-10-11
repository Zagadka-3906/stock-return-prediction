"""Training-only daily forecast correlations; diagnostic, never a quality gate."""
from pathlib import Path
import itertools
import json
import sys
import numpy as np
import polars as pl
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
OUT = A / 'streaming_classifier_signal_complementarity_20261005'


def main():
    import train_streaming_rank_classifier_bank_v3_20261005 as bank
    assert not OUT.exists()
    assert bank.read(bank.OUT / 'oof_audit.json')['status'] == 'passed'
    assert bank.read(A / 'streaming_classifier_actual_annual_completion_audit_20261005/verification.json')['actual_annual_fits'] == 20
    reference = A / 'connected_validation_20261002/combined_fold_frame.parquet'
    sources = [Path(__file__), bank.OUT / 'oof_audit.json', reference,
        A / 'streaming_classifier_actual_annual_completion_audit_20261005/verification.json']
    sources += list(bank.OUT.glob('*/info_202[0-4].json')) + list(bank.OUT.glob('*/raw_202[0-4].parquet'))
    frozen = {str(path): bank.sha(path) for path in sources}
    OUT.mkdir()
    bank.dump(OUT / 'frozen_before_inspection.json', {
        'status': 'frozen_before_training_only_signal_complementarity_inspection',
        'source_sha256': frozen, 'no_target_columns_or_test_data_read': True,
        'not_a_selection_or_rejection_gate': True, 'new_quality_scores': 0}, immutable=True)
    keys = pl.read_parquet(reference, columns=bank.KEYS + ['price_valid'])
    dates = keys['trade_date'].to_numpy()
    assert len(keys) == 5635800 and len(np.unique(dates)) == 1212
    names, values = list(bank.CONFIGS), []
    for name in names:
        parts = []
        for year in bank.YEARS:
            frame = pl.read_parquet(bank.OUT / name / f'raw_{year}.parquet')
            assert frame.select(bank.KEYS).equals(keys.filter(pl.col('trade_date') // 10000 == year).select(bank.KEYS))
            parts.append(frame['pred_raw'].to_numpy())
        value = np.concatenate(parts)
        assert np.isfinite(value).all()
        values.append(value)
    boundaries = np.r_[0, np.flatnonzero(dates[1:] != dates[:-1]) + 1, len(dates)]
    valid = keys['price_valid'].to_numpy()
    correlations = {pair: [] for pair in itertools.combinations(range(4), 2)}
    days, rows_used, constant_cases = 0, 0, 0
    for left, right in zip(boundaries[:-1], boundaries[1:]):
        mask = valid[left:right]
        centered = []
        for value in values:
            ranks = rankdata(value[left:right][mask], method='average')
            ranks -= ranks.mean()
            norm = float(np.sqrt(np.dot(ranks, ranks)))
            centered.append(ranks / norm if norm > 0 else None)
        for pair, results in correlations.items():
            first, second = (centered[i] for i in pair)
            if first is None or second is None:
                constant_cases += 1
                continue
            results.append(float(np.dot(first, second)))
        days += 1
        rows_used += int(mask.sum())
    checks = [{'first': names[first], 'second': names[second], 'days': len(result),
        'mean_daily_spearman': float(np.mean(result)), 'min_daily_spearman': float(np.min(result)),
        'max_daily_spearman': float(np.max(result))}
        for (first, second), result in correlations.items()]
    assert all(bank.sha(path) == digest for path, digest in frozen.items())
    bank.dump(OUT / 'verification.json', {'status': 'passed_actual_complete_training_period_signal_complementarity_inspection',
        'source_sha256': frozen, 'all_original_forecast_rows': len(keys), 'continuous_days': days,
        'diagnostic_price_valid_rows': rows_used, 'pairwise_comparisons': checks,
        'constant_signal_pair_day_cases': constant_cases,
        'diagnostic_only_no_candidates_removed_no_official_quality_or_test_labels_read': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    print(json.dumps({'status': 'passed', 'pairwise_comparisons': checks,
        'not_a_quality_or_selection_gate': True}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
