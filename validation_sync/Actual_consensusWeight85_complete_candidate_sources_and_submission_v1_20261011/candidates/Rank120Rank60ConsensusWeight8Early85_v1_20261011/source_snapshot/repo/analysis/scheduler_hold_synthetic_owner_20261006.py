"""Exercise recovery of a synthetic scheduler with normal closure or intentional os._exit."""
from pathlib import Path
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def main():
    from handoff_distribution_views_progress_monitor_20261006 import read, create
    from owned_scheduler_native_fit_hold_v2_20261006 import FitHold
    folder, mode, controller = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
    assert folder.name == 'scheduler_fit_guard_controls_v2_20261006' and mode in ('normal', 'abrupt_exit')
    with FitHold(folder, read(controller), mode):
        heartbeat = folder / 'dummy_heartbeat.jsonl'
        first = heartbeat.stat().st_size
        time.sleep(2.)
        assert heartbeat.stat().st_size == first, 'Synthetic scheduler heartbeat did not pause.'
        create(folder / f'{mode}_actual_owner_control.json', {'status': 'actual_synthetic_dispatch_held',
            'heartbeat_bytes_during_hold': first, 'only_synthetic_scheduler_touched': True})
        if mode == 'abrupt_exit':
            os._exit(37)


if __name__ == '__main__':
    main()
