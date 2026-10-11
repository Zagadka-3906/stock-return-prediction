"""Retain the terminal V2 full attempt and repair read-only key verification."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'streaming_rank_classifier_recovery_v3_20261005'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    assert not OUT.exists()
    failed = A / 'streaming_rank_classification_bank_v2_20261005/training_execution_scope.json'
    proof = json.loads(failed.read_text(encoding='utf-8'))
    assert proof['status'] == 'failed' and proof['failure'] == 'ValueError: sort array is read-only'
    stdout = A / 'run_logs/streaming_rank_classifier_native_20261005.stdout.log'
    assert 'fold2020 epoch32/32 actual1694259 mature rows' in stdout.read_text(encoding='utf-8')
    names = {
        'streaming_rank_classification_v2_20261005.py': 'streaming_rank_classification_v3_20261005.py',
        'verify_streaming_rank_classification_v2_20261005.py': 'verify_streaming_rank_classification_v3_20261005.py',
        'train_streaming_rank_classifier_bank_20261005.py': 'train_streaming_rank_classifier_bank_v3_20261005.py',
        'run_streaming_rank_classifier_bank_20261005.py': 'run_streaming_rank_classifier_bank_v3_20261005.py',
        'verify_streaming_rank_classifier_full_future_20261005.py': 'verify_streaming_rank_classifier_full_future_v3_20261005.py'}
    replacements = {old.removesuffix('.py'): new.removesuffix('.py') for old, new in names.items()}
    replacements.update({
        'streaming_rank_classification_bank_v2_20261005': 'streaming_rank_classification_bank_v3_20261005',
        'streaming_rank_classification_preflight_v2_20261005': 'streaming_rank_classification_preflight_v3_20261005',
        'streaming_rank_classifier_future_qa_20261005': 'streaming_rank_classifier_future_qa_v3_20261005',
        'streaming_rank_classifier_storage_20261005': 'streaming_rank_classifier_storage_v3_20261005',
        'streaming_rank_classifier_bank_run_20261005': 'streaming_rank_classifier_bank_run_v3_20261005',
        'streaming_rank_classifier_future_run_20261005': 'streaming_rank_classifier_future_run_v3_20261005'})
    retained = {str(A / name): sha(A / name) for name in names}
    retained.update({str(p): sha(p) for p in (failed, stdout,
        A / 'run_logs/streaming_rank_classifier_native_20261005.stderr.log',
        A / 'run_logs/streaming_rank_classifier_future_20261005.stderr.log',
        A / 'streaming_rank_classification_bank_v2_20261005/protocol.json',
        A / 'streaming_rank_classification_bank_v2_20261005/actual_cpu_resource_samples.jsonl')})
    for old, new in names.items():
        body = (A / old).read_text(encoding='utf-8')
        for before, after in sorted(replacements.items(), key=lambda item: -len(item[0])):
            body = body.replace(before, after)
        if old.startswith('streaming_rank_classification_'):
            helper = '''def sorted_key_hash_digest(values):
    """Sort a copy; Polars zero-copy NumPy arrays may be read-only."""
    import numpy as np
    ordered = np.sort(np.asarray(values, dtype=np.uint64))
    return hashlib.sha256(memoryview(ordered).cast('B')).hexdigest()


'''
            body = body.replace('def fit_stream(', helper + 'def fit_stream(', 1)
            before = "        expected.sort()\n        assert hashlib.sha256(memoryview(expected).cast('B')).hexdigest() == key_digest"
            assert body.count(before) == 1
            body = body.replace(before, "        assert sorted_key_hash_digest(expected) == key_digest")
        if old.startswith('verify_streaming_rank_classification_'):
            body = body.replace("    import numpy as np\n", "    import numpy as np\n    import polars as pl\n", 1)
            before = '    features = method.feature_names()'
            regression = '''    # Reproduce the original failure using every actual mature 2020 key.
    full_keys = (pl.scan_parquet(method.FEATURE_FILE).filter(pl.col('is_train') & pl.col('price_valid')
        & (pl.col('trade_date') < method.cutoff(2020)) & pl.col('y_rank').is_finite())
        .select(method.KEYS).collect(engine='streaming').hash_rows(seed=2026).to_numpy())
    assert len(full_keys) == 1694259 and not full_keys.flags.writeable
    original_key_bytes = full_keys.tobytes()
    try:
        full_keys.sort()
    except ValueError as error:
        assert 'read-only' in str(error)
    else:
        raise AssertionError('The actual original read-only failure was not reproduced.')
    copied = np.array(full_keys, copy=True)
    copied.sort()
    expected_digest = hashlib.sha256(memoryview(copied).cast('B')).hexdigest()
    assert method.sorted_key_hash_digest(full_keys) == expected_digest
    assert full_keys.tobytes() == original_key_bytes
    regression = {'actual_full_mature_training_keys': len(full_keys),
        'original_read_only_sort_error_reproduced': True,
        'repaired_full_key_digest_matches_independent_writable_copy': True,
        'original_read_only_input_not_modified': True,
        'sorted_mature_key_multiset_sha256': expected_digest}
    del full_keys, copied, original_key_bytes
    method.dump(OUT / 'actual_full_readonly_key_regression.json', regression, immutable=True)
    features = method.feature_names()'''
            assert body.count(before) == 1
            body = body.replace(before, regression)
            body = body.replace("'controls': controls, 'actual_small32epoch_fits': 16,", "'controls': controls, 'readonly_full1694259_key_regression': regression, 'actual_small32epoch_fits': 16,")
        destination = A / new
        assert not destination.exists()
        compile(body, str(destination), 'exec')
        destination.write_text(body, encoding='utf-8', newline='\n')
    OUT.mkdir()
    (OUT / 'original_failure_retained.json').write_text(json.dumps({
        'status': 'retained_actual_terminal_v2_full32pass_attempt_and_failed_key_verification',
        'input_sha256': retained, 'actual_logged_full2020_rows': 1694259,
        'actual_logged_completed_passes': 32, 'qualified_complete_annual_fits': 0,
        'repair': 'Use sorted copy for the exact same complete mature key multiset SHA256 check.',
        'model_configuration_label_maturity_row_order_and32passes_not_changed': True,
        'new_version_outputs_keep_original_failed_directory_untouched': True,
        'test_labels_read': False, 'new_quality_scores': 0}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    storage = json.loads((A / 'streaming_rank_classifier_storage_20261005.json').read_text(encoding='utf-8'))
    storage['output_directory'] = str(A / 'streaming_rank_classification_bank_v3_20261005')
    storage['temporary_directory'] = str(ROOT / 'tmp/streaming_rank_classifier_v3_20261005')
    path = A / 'streaming_rank_classifier_storage_v3_20261005.json'
    assert not path.exists()
    path.write_text(json.dumps(storage, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    assert all(sha(p) == digest for p, digest in retained.items())
    print('V3 sources prepared; complete terminal V2 evidence retained.', flush=True)


if __name__ == '__main__':
    main()
