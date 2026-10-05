"""Independently inspect four actual final native states and full keyed forecasts."""
from pathlib import Path
import sys
import json
import numpy as np
import polars as pl

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
OUT = A / 'streaming_classifier_actual_final_completion_audit_20261005'


def main():
    import train_streaming_rank_classifier_bank_v3_20261005 as bank
    assert not OUT.exists()
    future = A / 'streaming_rank_classifier_future_qa_v3_20261005'
    proof = bank.read(future / 'verification.json')
    resources = bank.read(future / 'resource_summary.json')
    assert proof['status'] == resources['status'] == 'passed'
    assert proof['actual_fulltraining_fits'] == 4 and proof['all4_model_fullfuture_reload_and_cold80_controls_passed']
    baseline = bank.read(bank.BASELINE / 'info_2025.json')['training_meta']
    assert baseline['rows'] == 6754006
    sources = [Path(__file__), Path(bank.__file__), bank.SOURCE, bank.BASELINE / 'info_2025.json',
        future / 'verification.json', future / 'resource_summary.json', future / 'protocol.json',
        A / 'streaming_classifier_actual_annual_completion_audit_20261005/verification.json']
    sources += [bank.OUT / name / 'info_2025.json' for name in bank.CONFIGS]
    bindings = {str(path): bank.sha(path) for path in sources}
    OUT.mkdir()
    bank.dump(OUT / 'frozen_before_inspection.json', {'source_sha256': bindings,
        'all4_actual_models_and_raw_forecasts_inspected_without_new_inference_or_fit': True,
        'test_labels_read': False}, immutable=True)
    expected = pl.read_parquet(ROOT / 'deliveries/connected_topk0175_20261003/generation_inputs.parquet', columns=bank.KEYS)
    assert len(expected) == 1599600
    measurements = [json.loads(line) for line in (bank.OUT / 'actual_native_fit_measurements.jsonl').read_text(encoding='utf-8').splitlines()]
    checks = []
    for name, cfg in bank.CONFIGS.items():
        info = bank.read(bank.OUT / name / 'info_2025.json')
        actual = next(row for row in proof['checks'] if row['model'] == name)
        meta = info['training_meta']
        assert info['status'] == 'passed' and info['configuration'] == cfg and info['completed_epochs'] == 32
        for key in ('rows', 'days', 'first', 'last', 'cutoff_exclusive', 'last_label_end', 'features'):
            assert meta[key] == baseline[key], (name, key)
        assert meta['full_selected_row_keys_match_independent_original_filter']
        assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive']
        original, copied = bank.OUT / name / 'model_2025.joblib', future / f'{name}.joblib'
        assert bank.sha(original) == bank.sha(copied) == info['model_sha256'] == actual['model_sha256']
        bundle = bank.core.load_bundle(copied)
        assert bundle['training_rows'] == 6754006 and bundle['completed_epochs'] == 32
        assert bundle['classifier'].t_ == bundle['actual_native_sample_counter'] == info['actual_native_sample_counter'] == 1 + 32 * 6754006
        assert np.isfinite(bundle['classifier'].coef_).all() and np.isfinite(bundle['classifier'].intercept_).all()
        assert np.array_equal(bundle['class_thresholds'], info['class_thresholds_learned_from_mature_past'])
        fits = [row for row in measurements if row['model'] == name and row['year'] == 2025]
        assert len(fits) == 1 and fits[0]['actual_rows_in_each_epoch'] == [6754006] * 32
        assert fits[0]['actual_native_sample_counter'] == bundle['classifier'].t_
        raw = future / f'{name}_raw.parquet'
        assert bank.sha(raw) == actual['raw_sha256']
        frame = pl.read_parquet(raw)
        assert frame.select(bank.KEYS).equals(expected)
        assert frame['pred_raw'].is_finite().all() and frame['trade_date'].n_unique() == 344
        assert frame['ts_code'].n_unique() == 4650 and len(frame) == 1599600
        assert meta['cutoff_exclusive'] <= int(frame['trade_date'].min())
        for key in ('actual_full1599600_row_reload_bit_identical', 'actual_cold80_day_prefix_bit_identical',
                    'actual_native131_row_and1_80_130_prefix_bit_identical'):
            assert actual[key]
        checks.append({'model': name, 'model_sha256': actual['model_sha256'], 'raw_sha256': actual['raw_sha256'],
            'actual_saved_full32pass_sample_counter': bundle['classifier'].t_,
            'actual_full_forecast_rows': len(frame), 'days': 344, 'codes': 4650,
            'full_future_key_order_matches_formal_input': True,
            'native_producer_reload_and_real_cold80_controls_passed': True})
    assert all(bank.sha(path) == digest for path, digest in bindings.items())
    bank.dump(OUT / 'verification.json', {'status': 'passed_actual4_final_native_models_and_full_keyed_forecasts_independently_inspected',
        'checks': checks, 'source_sha256': bindings, 'actual_full_annual_fits_already_verified': 20,
        'actual_full_final_fits_independently_inspected': 4,
        'final_fits_not_official_quality_or_adoption': True,
        'new_model_fits_by_audit': 0, 'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    print(json.dumps({'status': 'passed_actual4_final_classifier_model_and_full_forecast_inspection',
        'full_future_rows_each': 1599600, 'official_quality_pending': True}), flush=True)


if __name__ == '__main__':
    main()
