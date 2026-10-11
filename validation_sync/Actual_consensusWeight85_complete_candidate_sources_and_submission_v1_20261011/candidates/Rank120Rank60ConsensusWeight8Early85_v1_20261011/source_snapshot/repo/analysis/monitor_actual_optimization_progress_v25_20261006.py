"""Publish only the fully verified observer generation; keep all scientific gates."""
from pathlib import Path
from datetime import datetime
import json
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import monitor_actual_optimization_progress_v23_20261006 as previous
from complete_observer_snapshot_transaction_v2_20261006 import transaction

original_update = previous.update


def update():
    with transaction() as (pending, commit):
        state = original_update()
        value = pending[A / 'ongoing_optimization_state.json']
        value['actual_progress_monitor'] = str(Path(__file__).relative_to(ROOT))
        value['actual_observer_version'] = 25
        pending[A / 'resume_optimization_20261004.json'] = dict(value)
        state.update(actual_observer_version=25, at_local=datetime.now().isoformat(timespec='seconds'))
        pending[A / 'actual_optimization_monitor_state_20261005.json'] = state
        generation = uuid.uuid4().hex
        commit(generation)
    print(json.dumps({'actual_observer_version': 25, 'complete_observer_generation': generation,
        'actual_active_quality_rounds': value['actual_active_quality_rounds'],
        'intermediate_layers_kept_private': True}), flush=True)
    return state


def main():
    previous.update = update
    previous.main()


if __name__ == '__main__':
    main()
