"""Registry namespace for the 16 already executed causal buffer comparisons."""
from pathlib import Path
import json
from run_dependency_queue_v3_20261006 import read, sha

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/optimization_20261003_r98'
PREVIOUS_NUMBER = 85
PREVIOUS = ROOT / 'analysis/optimization_20261003_r85'
NUMBER = 98
WAVES = (381,)
MEMBERS = ('causal_entry_exit_buffer',)
GRAPH_FIELD = 'entry_exit_buffer_complete_scheme_graph'


def dump(path, value, immutable=False):
    path = Path(path)
    if immutable and path.exists():
        assert read(path) == value
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def configuration(row):
    return {'kind': 'causal_entry_exit_buffer_after_complete_parent85_output',
        'whole_scheme_graph': row[GRAPH_FIELD], 'training_parent_round': PREVIOUS_NUMBER}


def signature(row):
    return json.dumps(configuration(row), ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def freeze():
    # This registers an existing scientific freeze; it must never replace it
    # with a new backdated selection or rerun the already scored grid.
    record = read(OUT / 'protocol.json')
    assert record['registration_only_of_existing_executed_validation'] is True
    assert record['expected_scored_records'] == 16
    return record
