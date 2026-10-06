"""Keep the original main publisher and export recovered scientific scope explicitly."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))


def main():
    from locked_read_hash_cache_20261004 import fresh_sha
    run = json.loads((ROOT / 'analysis/github_validation_sync_main_20261005/run_v3.json').read_text(encoding='utf-8'))
    for source, digest in run['input_sha256'].items():
        assert fresh_sha(source) == digest, source
    import watch_validations_main_v2_20261005 as old
    from recovered_round66_publication_adapter_20261005 import install
    original = install(old.sync)
    try:
        old.main()
    finally:
        old.sync.snapshot = original


if __name__ == '__main__':
    main()
