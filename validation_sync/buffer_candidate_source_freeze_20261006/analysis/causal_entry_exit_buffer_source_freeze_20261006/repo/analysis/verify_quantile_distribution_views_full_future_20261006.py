"""Audit the actual closed six-view whole-future execution and exact output bytes."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def evidence():
    import polars as pl
    import build_quantile_distribution_views_bank_20261006 as bank
    from run_dependency_queue_v3_20261006 import owned
    service = ROOT / 'analysis/service_owned_workflows_20261006/quantile_distribution_views_full_workflow'
    assert bank.read(service / 'service_execution.json')['status'] == 'passed'
    assert not owned(bank.read(service / 'native_launch.json'))
    assert bank.read(bank.OUT / 'execution_scope.json')['status'] == 'passed'
    proof = bank.read(bank.FUTURE / 'verification.json')
    assert proof['status'] == 'passed' and proof['actual_full_future_views'] == 6
    assert proof['actual_native_fits'] == proof['new_quality_scores'] == 0
    assert proof['test_labels_read'] is False and proof['all6_entire_future_and_cold80_passed']
    protocol = bank.verify()
    expected = pl.scan_parquet(bank.engine.FEATURE_FILE).filter(~pl.col('is_train')).select(bank.KEYS).sort('trade_date', 'ts_code').collect()
    assert len(proof['checks']) == len(bank.CONFIGS) == 6
    for check in proof['checks']:
        name = check['model']
        assert name in bank.CONFIGS
        assert (check['rows'], check['days'], check['codes']) == (1599600, 344, 4650)
        assert check['actual_whole_future_selfcontained_independent_codec_bit_identical']
        assert check['actual_cold80_reload372000_rows_bit_identical']
        assert bank.sha(bank.OUT / name / 'model_2025.joblib') == check['model_sha256']
        path = bank.FUTURE / f'{name}_raw.parquet'
        assert bank.sha(path) == check['raw_sha256']
        assert pl.read_parquet(path, columns=bank.KEYS).equals(expected)
    return {'status': 'passed_actual_closed_six_view_future_evidence_audit',
        'actual_full_future_views': 6, 'new_native_fits': 0, 'new_quality_scores': 0,
        'all_original198_and_new262_complete_quality_records_still_required': True,
        'test_labels_read': False}


if __name__ == '__main__':
    print(__import__('json').dumps(evidence()))
