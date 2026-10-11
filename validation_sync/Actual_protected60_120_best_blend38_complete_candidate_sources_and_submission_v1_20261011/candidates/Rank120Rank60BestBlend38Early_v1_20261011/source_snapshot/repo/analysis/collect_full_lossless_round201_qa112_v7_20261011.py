"""Route the unchanged full collector to actual QA18's October7 directory."""
from pathlib import Path

SOURCE = Path(__file__).with_name('collect_full_lossless_round_publication_20261006.py')
original = SOURCE.read_text(encoding='utf-8')
before = "qa = A / f'lossless_ranking_display_qa_v{qa_version}_20261006' / f'round{number}'"
after = "qa = A / f'lossless_ranking_display_qa_v{qa_version}_20261010' / f'round{number}'"
assert original.count(before) == 1
text = original.replace(before, after)
assert text.replace(after, before) == original
namespace = {'__file__': str(SOURCE), '__name__': 'actual_round116_full_QA18_collection'}
exec(compile(text, str(SOURCE), 'exec'), namespace)


def collect(number, qa_version, expected_records):
    assert (number, qa_version, expected_records) == (201, 112, 35)
    from exact_native_JSON_archive_runtime_20261007 import install
    restore=install()
    try:return namespace['collect'](number, qa_version, expected_records)
    finally:restore()
