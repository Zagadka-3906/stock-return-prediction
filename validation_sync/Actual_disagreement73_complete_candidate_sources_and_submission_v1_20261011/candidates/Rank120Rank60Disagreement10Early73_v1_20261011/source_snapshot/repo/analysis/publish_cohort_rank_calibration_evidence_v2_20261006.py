"""Retry publication in a new evidence directory, preserving the original TLS failure."""
from pathlib import Path
import sys

SOURCE = Path(__file__).with_name('publish_cohort_rank_calibration_evidence_20261006.py')
text = SOURCE.read_text(encoding='utf-8')
text = text.replace("f'cohort_rank_calibration_{phase}_github_20261006'",
                    "f'cohort_rank_calibration_{phase}_github_v2_20261006'")
text = text.replace("sources = [Path(__file__),", "sources = [Path(__file__), SOURCE,\n        *(A / 'cohort_rank_calibration_pilot_github_20261006').glob('*.json'),")
assert text != SOURCE.read_text(encoding='utf-8')
namespace = {'__file__': __file__, '__name__': 'cohort_publication_recovery', 'SOURCE': SOURCE}
exec(compile(text, str(SOURCE), 'exec'), namespace)

if __name__ == '__main__':
    namespace['main'](sys.argv[1])
