"""Registry for the74 actually scored conditional residual schemes."""
from pathlib import Path
import json
from run_dependency_queue_v3_20261006 import read, sha

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/optimization_20261003_r109'
PREVIOUS_NUMBER = 108
PREVIOUS = ROOT / 'analysis/optimization_20261003_r108'
NUMBER = 109
WAVES = (392,)
MEMBERS = ('native_conditional_residual_ensemble',)
GRAPH_FIELD = 'conditional_flag_residual_scheme_graph'


def dump(path, value, immutable=False):
    path = Path(path)
    if path == ROOT / 'candidates/optimization_20261003_r109/manifest.json':
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
    return {'kind': 'actual_direct_rank_CDF_comparison_after_complete_parent106_or_explicit_anchor_graph',
            'whole_scheme_graph': row[GRAPH_FIELD], 'training_parent_round': 100, 'comparison_baseline_round': PREVIOUS_NUMBER}


def signature(row):
    return json.dumps(configuration(row), ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def freeze():
    record = read(OUT / 'protocol.json')
    assert record['registration_only_of_existing_executed_validation']
    assert record['expected_scored_records'] == 74
    return record
