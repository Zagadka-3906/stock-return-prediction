"""Registry for the 66 actually scored mature cohort calibration schemes."""
from pathlib import Path
import json
from run_dependency_queue_v3_20261006 import read, sha

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/optimization_20261003_r100'
PREVIOUS_NUMBER = 95
PREVIOUS = ROOT / 'analysis/optimization_20261003_r95'
NUMBER = 100
WAVES = (383,)
MEMBERS = ('mature_cohort_rank_calibration',)
GRAPH_FIELD = 'extended_cohort_rank_calibration_scheme_graph'


def dump(path, value, immutable=False):
    path = Path(path)
    if path == ROOT / 'candidates/optimization_20261003_r100/manifest.json':
        # Cover nested evidence manifests too; exclude only this outer manifest.
        value = {'status': 'passed', 'files': {
            p.relative_to(path.parent).as_posix(): {'sha256': sha(p), 'bytes': p.stat().st_size}
            for p in sorted(path.parent.rglob('*')) if p.is_file() and p != path}}
    if immutable and path.exists():
        assert read(path) == value
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def configuration(row):
    return {'kind': 'mature_cohort_rank_calibration_after_complete_parent95_graph',
            'whole_scheme_graph': row[GRAPH_FIELD], 'training_parent_round': PREVIOUS_NUMBER}


def signature(row):
    return json.dumps(configuration(row), ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def freeze():
    record = read(OUT / 'protocol.json')
    assert record['registration_only_of_existing_executed_validation']
    assert record['expected_scored_records'] == 66
    return record
