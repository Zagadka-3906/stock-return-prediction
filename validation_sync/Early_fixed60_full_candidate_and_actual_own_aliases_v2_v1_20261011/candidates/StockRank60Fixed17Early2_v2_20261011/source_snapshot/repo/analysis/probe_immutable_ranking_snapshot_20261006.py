"""Prove full-byte report recovery on the actual immutable R81 lossless page."""
from pathlib import Path
import json


def main():
    root = Path(__file__).resolve().parents[1]
    from immutable_lossless_ranking_snapshot_20261006 import prepare
    display = root / 'analysis/lossless_ranking_display_20261006/round81'
    snapshot = prepare(display)
    proof = json.loads((display / 'full_report_publication_snapshot_verification.json').read_text(encoding='utf-8'))
    assert proof['connected_records'] == 9946 and proof['full_original_bytes'] == 634015041
    print(json.dumps({'status': proof['status'], 'snapshot': str(snapshot),
        'full_original_bytes': proof['full_original_bytes'], 'connected_records': 9946}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
