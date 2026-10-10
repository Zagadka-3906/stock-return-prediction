"""Keep the entire original QA and use separate output and browser-profile paths."""
from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def main(number):
    source = A / 'verify_lossless_ranking_display_20261006.py'
    data = source.read_bytes()
    assert hashlib.sha256(data).hexdigest() == '6c12d8ddfa623ee47e2a343b1d56dc8fcdce730d195746c7f27905195316979d'
    text = data.decode('utf-8')
    patches = {
        "'lossless_ranking_display_qa_20261006'": "'lossless_ranking_display_qa_v3_20261006'",
        "'tmp/ranking_display_qa_20261006'": "'tmp/ranking_display_qa_v3_20261006'",
    }
    for before, after in patches.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    namespace = {'__name__': 'actual_recovery_lossless_QA', '__file__': str(Path(__file__).resolve())}
    exec(compile(text, str(Path(__file__).resolve()), 'exec'), namespace)
    namespace['main'](number)


if __name__ == '__main__':
    main(int(sys.argv[1]))
