"""Preserve the failed export and retry with the authoritative snapshot source path."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def main():
    source = A / 'publish_recovered_round81_main_20261006.py'
    data = source.read_bytes()
    assert hashlib.sha256(data).hexdigest() == '029a7445c6fc1b893e28e39b09e0b6ec705ad2c29cd4546e9e2ff05c01e4ce6c'
    text = data.decode('utf-8')
    replacements = {
        'from recovered_round81_publication_adapter_20261006 import install':
            'from recovered_round81_publication_adapter_v2_20261006 import install',
        "'round81_recovered_publication_github_20261006'":
            "'round81_recovered_publication_github_v2_20261006'",
    }
    for before, after in replacements.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    namespace = {'__name__': 'actual_round81_publication_retry', '__file__': str(Path(__file__).resolve())}
    exec(compile(text, str(Path(__file__).resolve()), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
