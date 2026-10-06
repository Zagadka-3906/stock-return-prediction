"""Reconstruct the exact original report bytes from an immutable lossless page."""
from pathlib import Path
import gzip
import hashlib
import json
import os
import re
import time


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def prepare(display):
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from build_lossless_ranking_display_v2_20261006 import unpack_report
    display = Path(display).resolve()
    proof_path, page = display / 'verification.json', display / 'complete_rankings_lossless.html'
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    assert proof['status'] == 'passed_all_original_report_values_and_six_views_lossless_roundtrip'
    assert sha(page) == proof['lossless_HTML_sha256']
    snapshot = display / 'full_report_reconstructed_for_publication.json.gz'
    verification = display / 'full_report_publication_snapshot_verification.json'
    if verification.exists():
        prior = json.loads(verification.read_text(encoding='utf-8'))
        assert prior['status'] == 'passed_exact_original_full_report_bytes_from_immutable_lossless_HTML'
        assert sha(snapshot) == prior['compressed_snapshot_sha256']
        return snapshot
    assert not snapshot.exists()
    inputs = {str(path): sha(path) for path in (Path(__file__).resolve(), proof_path, page,
        Path(__file__).parent / 'build_lossless_ranking_display_v2_20261006.py')}
    with LockedReadHashCache(inputs):
        text = page.read_text(encoding='utf-8')
        data = re.search(r'<script\s+id="data"\s+type="application/json">(.*?)</script>', text, re.S)
        assert data, 'The entire lossless report payload must be present.'
        report = unpack_report(json.loads(data.group(1)))
        digest, raw_bytes = hashlib.sha256(), 0
        with snapshot.open('xb') as destination:
            with gzip.GzipFile(filename='', mode='wb', fileobj=destination, compresslevel=6, mtime=0) as compressed:
                encoder = json.JSONEncoder(ensure_ascii=False, indent=2, allow_nan=False)
                for part in encoder.iterencode(report):
                    encoded = part.replace('\n', os.linesep).encode('utf-8')
                    digest.update(encoded)
                    raw_bytes += len(encoded)
                    compressed.write(encoded)
                encoded = os.linesep.encode('utf-8')
                digest.update(encoded)
                raw_bytes += len(encoded)
                compressed.write(encoded)
        assert digest.hexdigest() == proof['original_report_sha256'], 'Exact original report byte hash must match.'
        with gzip.open(snapshot, 'rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == proof['original_report_sha256']
    with verification.open('x', encoding='utf-8') as stream:
        json.dump({'status': 'passed_exact_original_full_report_bytes_from_immutable_lossless_HTML',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'original_report_sha256': proof['original_report_sha256'],
            'compressed_snapshot_sha256': sha(snapshot), 'full_original_bytes': raw_bytes,
            'connected_records': proof['connected_records'], 'input_sha256': inputs,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False},
            stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    return snapshot
