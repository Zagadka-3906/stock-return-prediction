"""Retain the failed unit-rank assumption and version past-learned label cutoffs."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def main():
    source = A / 'streaming_rank_classification_20261005.py'
    verifier = A / 'verify_streaming_rank_classification_20261005.py'
    proof = A / 'streaming_rank_classification_preflight_20261005/frozen_before_actual_controls.json'
    original = json.loads(proof.read_text(encoding='utf-8'))
    for filename, digest in original['input_sha256'].items():
        with Path(filename).open('rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == digest, filename
    out = A / 'streaming_rank_classifier_label_recovery_v2_20261005'
    assert not out.exists()
    out.mkdir()
    retained = {'status': 'original_preflight_failed_at_rank_domain_assertion_before_any_classifier_fit',
        'source': str(source), 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'verifier': str(verifier), 'verifier_sha256': hashlib.sha256(verifier.read_bytes()).hexdigest(),
        'original_frozen_proof_sha256': hashlib.sha256(proof.read_bytes()).hexdigest(),
        'actual_original_small_fits_completed': 0,
        'observed_actual_provided_rank_min_in_control': -.49971073865890503,
        'observed_actual_provided_rank_max_in_control': .5,
        'repair': 'Fit exact class quantiles using only eligible mature past supplied rank labels.',
        'test_labels_read': False, 'new_quality_scores': 0}
    (out / 'original_failure_retained.json').write_text(json.dumps(retained, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    body = source.read_text(encoding='utf-8')
    body = body.replace('streaming_rank_classification_bank_20261005', 'streaming_rank_classification_bank_v2_20261005')
    old = """def rank_classes(y, cfg):
    import numpy as np
    y = np.asarray(y, dtype=np.float32)
    assert np.isfinite(y).all() and np.all((y >= 0) & (y <= 1))
    if cfg['rank_objective'] == 'top10':
        return (y >= np.float32(.9)).astype(np.int64)
    assert cfg['rank_objective'] == 'decile'
    thresholds = np.arange(1, 10, dtype=np.float32) / np.float32(10)
    return np.searchsorted(thresholds, y, side='right').astype(np.int64)
"""
    new = """def learned_rank_thresholds(y, cfg):
    import numpy as np
    y = np.asarray(y, dtype=np.float64)
    assert np.isfinite(y).all() and len(y)
    quantiles = [.9] if cfg['rank_objective'] == 'top10' else np.arange(1, 10) / 10
    return np.quantile(y, quantiles)


def rank_classes(y, cfg, thresholds):
    import numpy as np
    y = np.asarray(y, dtype=np.float64)
    assert np.isfinite(y).all()
    assert len(thresholds) == (1 if cfg['rank_objective'] == 'top10' else 9)
    return np.searchsorted(thresholds, y, side='right').astype(np.int64)
"""
    assert body.count(old) == 1
    body = body.replace(old, new)
    body = body.replace('def build_bundle(model, scaler, cfg, rows, steps):', 'def build_bundle(model, scaler, cfg, rows, steps, thresholds):')
    body = body.replace("'config': dict(cfg), 'completed_epochs':", "'config': dict(cfg), 'class_thresholds': thresholds, 'completed_epochs':")
    body = body.replace("scaler = RunningStats()\n    chunk = cfg['chunk_rows']", "scaler = RunningStats()\n    thresholds = learned_rank_thresholds(y, cfg)\n    chunk = cfg['chunk_rows']")
    body = body.replace("rank_classes(y[offset:offset + len(block)], cfg)", "rank_classes(y[offset:offset + len(block)], cfg, thresholds)")
    body = body.replace('build_bundle(model, scaler, cfg, len(y), steps)', 'build_bundle(model, scaler, cfg, len(y), steps, thresholds)')
    body = body.replace('rows, dates, key_hashes = 0, set(), []', 'rows, dates, key_hashes = 0, set(), []\n    target_values = []')
    body = body.replace('        rank_classes(y, cfg)\n        scaler.partial_fit', '        assert np.isfinite(y).all()\n        target_values.append(y.copy())\n        scaler.partial_fit')
    body = body.replace('    key_values = np.concatenate(key_hashes)', '    thresholds = learned_rank_thresholds(np.concatenate(target_values), cfg)\n    del target_values\n    key_values = np.concatenate(key_hashes)')
    body = body.replace('rank_classes(y, cfg), classes=classes(cfg)', 'rank_classes(y, cfg, thresholds), classes=classes(cfg)')
    body = body.replace('build_bundle(model, scaler, cfg, rows, steps)', 'build_bundle(model, scaler, cfg, rows, steps, thresholds)')
    actual = A / 'streaming_rank_classification_v2_20261005.py'
    assert not actual.exists()
    compile(body, str(actual), 'exec')
    actual.write_text(body, encoding='utf-8', newline='\n')
    body = verifier.read_text(encoding='utf-8')
    body = body.replace('import streaming_rank_classification_20261005 as method', 'import streaming_rank_classification_v2_20261005 as method')
    body = body.replace('streaming_rank_classification_preflight_20261005', 'streaming_rank_classification_preflight_v2_20261005')
    old = """        probe = np.asarray([0., .1, .5, .9, 1.], dtype=np.float32)
        assert np.array_equal(method.rank_classes(probe, {'rank_objective': 'decile'}), [0, 1, 5, 9, 9])
        assert np.array_equal(method.rank_classes(probe, {'rank_objective': 'top10'}), [0, 0, 0, 1, 1])
"""
    new = """        probe = np.asarray([-.5, -.4, 0., .4, .5], dtype=np.float32)
        thresholds = (np.arange(1, 10, dtype=np.float32) / np.float32(10) - np.float32(.5)).astype(np.float64)
        probe[1] = thresholds[0]
        probe[3] = thresholds[-1]
        assert np.array_equal(method.rank_classes(probe, {'rank_objective': 'decile'}, thresholds), [0, 1, 5, 9, 9])
        assert np.array_equal(method.rank_classes(probe, {'rank_objective': 'top10'}, thresholds[-1:]), [0, 0, 0, 1, 1])
"""
    assert body.count(old) == 1
    body = body.replace(old, new)
    body = body.replace("for key in ('mean', 'scale'):", "for key in ('mean', 'scale', 'class_thresholds'):")
    old = """            labels = (y >= np.float32(.9)).astype(np.int64) if cfg['rank_objective'] == 'top10' else np.digitize(
                y, np.arange(1, 10, dtype=np.float32) / np.float32(10), right=False)
"""
    new = """            labels = np.digitize(y.astype(np.float64), streamed['class_thresholds'], right=False)
            expected_quantiles = [.9] if cfg['rank_objective'] == 'top10' else np.arange(1, 10) / 10
            assert np.array_equal(streamed['class_thresholds'], np.quantile(y.astype(np.float64), expected_quantiles))
"""
    assert body.count(old) == 1
    body = body.replace(old, new)
    body = body.replace("'provided_float32_rank_class_boundaries_explicitly_checked': True,", "'class_thresholds_learned_from_mature_past_only_and_independently_checked': True,")
    actual_verifier = A / 'verify_streaming_rank_classification_v2_20261005.py'
    assert not actual_verifier.exists()
    compile(body, str(actual_verifier), 'exec')
    actual_verifier.write_text(body, encoding='utf-8', newline='\n')
    print('Original failed assumption retained; two versioned sources prepared.', flush=True)


if __name__ == '__main__':
    main()
