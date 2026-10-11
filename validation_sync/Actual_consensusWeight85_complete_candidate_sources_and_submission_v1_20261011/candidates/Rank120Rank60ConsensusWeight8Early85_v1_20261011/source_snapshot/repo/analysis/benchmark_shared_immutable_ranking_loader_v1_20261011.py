"""Measure a shared-node full-board loader and prove every native report byte.

Use the immutable, fully qualified round180 report, not any Test labels.
This benchmark changes no live reader or scientific pipeline.
"""
from pathlib import Path
from datetime import datetime
import gc, hashlib, json, os, re, sys, time

A = Path(__file__).resolve().parent
ROOT = A.parent
sys.path[:0] = [str(ROOT), str(A)]
OUT = Path('E:/赛题五_本机临时/shared_immutable_ranking_loader_benchmark_v1_20261011')


def main():
    from run_dependency_queue_v3_20261006 import read, sha, create
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    import psutil
    assert allowed()
    OUT.mkdir(exist_ok=False)
    scratch = OUT / 'tmp'
    scratch.mkdir()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[key] = str(scratch)
    import tempfile
    tempfile.tempdir = str(scratch)
    while psutil.virtual_memory().available < 6 * 2**30:
        assert allowed()
        time.sleep(10)
    display = A / 'lossless_ranking_display_v2_20261006/round180'
    page = display / 'complete_rankings_lossless.html'
    encoded_proof = display / 'verification.json'
    archive_proof = display / 'full_report_publication_snapshot_verification.json'
    receipt = A / 'github_validation_sync_main_20261005/round180_receipt.json'
    registration = A / 'optimization_20261003_r180/full_registration_execution.json'
    from build_lossless_ranking_display_v2_20261006 import unpack_report
    from exact_native_pretty_JSON_archive_20261007 import pieces
    import build_lossless_ranking_display_v2_20261006 as codec
    import exact_native_pretty_JSON_archive_20261007 as native
    inputs = [Path(__file__), page, encoded_proof, archive_proof, receipt, registration,
              Path(codec.__file__), Path(native.__file__)]
    pins = {str(p): sha(p) for p in inputs}
    source = read(encoded_proof)
    archive = read(archive_proof)
    assert read(receipt)['status'] == 'pushed_and_remote_head_verified'
    assert read(registration)['status'] == 'passed'
    assert source['status'] == 'passed_all_original_report_values_and_six_views_lossless_roundtrip'
    assert archive['status'] == 'passed_exact_original_full_report_bytes_from_immutable_lossless_HTML'
    assert source['original_report_sha256'] == archive['original_report_sha256']
    assert source['connected_records'] == archive['connected_records'] == 17062
    assert source['lossless_HTML_sha256'] == sha(page)
    create(OUT / 'frozen_before_measurement.json', {
        'input_sha256': pins, 'source_round': 180,
        'actual_entire_board_reencoding_required': True,
        'scientific_runtime_adoption_not_performed': True,
        'same_dataset_original_decoder_speedup_not_claimed': True,
        'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False,
    })
    process = psutil.Process()
    before = process.memory_info()
    started = time.perf_counter()
    text = page.read_text(encoding='utf8')
    match = re.search(r'<script\s+id="data"\s+type="application/json">(.*?)</script>', text, re.S)
    assert match is not None
    packed = json.loads(match.group(1))
    report = unpack_report(packed)
    decoded = process.memory_info()
    elapsed = time.perf_counter() - started
    del text, match, packed
    gc.collect()
    retained = process.memory_info()
    assert len(report['connected']) == 17062
    digest, count = hashlib.sha256(), 0
    encoding_started = time.perf_counter()
    for block in pieces(report):
        digest.update(block)
        count += len(block)
    assert count == archive['full_original_bytes']
    assert digest.hexdigest() == source['original_report_sha256']
    for path, expected in pins.items():
        assert sha(path) == expected, path
    assert allowed()
    result = {
        'status': 'passed_actual_complete180_shared_loader_all_native_bytes_exact',
        'at_local': datetime.now().isoformat(), 'source_round': 180,
        'input_sha256': pins, 'connected_records': 17062,
        'original_native_bytes': count, 'original_native_sha256': digest.hexdigest(),
        'actual_load_and_decode_seconds': elapsed,
        'actual_full_native_reencoding_seconds': time.perf_counter() - encoding_started,
        'before_RSS_bytes': before.rss,
        'decoded_RSS_bytes': decoded.rss,
        'retained_RSS_bytes': retained.rss,
        'decoded_private_bytes': getattr(decoded, 'private', None),
        'retained_private_bytes': getattr(retained, 'private', None),
        'all_values_types_key_order_and_float_spellings_byte_exact': True,
        'all_six_original_report_views_preserved': True,
        'scientific_runtime_adoption_not_performed': True,
        'same_dataset_original_decoder_speedup_not_claimed': True,
        'eligible_for_separately_verified_runtime_adoption': decoded.rss < 4 * 2**30,
        'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False,
    }
    create(OUT / 'verification.json', result)
    create(A / 'shared_immutable_ranking_loader_actual_complete180_benchmark_v1_20261011.json', result)
    print({k: result[k] for k in ('status', 'actual_load_and_decode_seconds',
                                 'decoded_RSS_bytes', 'retained_RSS_bytes',
                                 'eligible_for_separately_verified_runtime_adoption')}, flush=True)


if __name__ == '__main__':
    main()
