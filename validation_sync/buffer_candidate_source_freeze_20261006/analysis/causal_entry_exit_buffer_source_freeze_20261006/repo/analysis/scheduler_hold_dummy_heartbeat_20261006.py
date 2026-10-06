"""Only synthetic dispatch-control heartbeat; never train or score a model."""
from pathlib import Path
import json
import os
import sys
import time


def main():
    folder = Path(sys.argv[1]).resolve()
    assert folder.drive.upper() == 'D:' and folder.name == 'scheduler_fit_guard_controls_v2_20261006'
    with (folder / 'dummy_heartbeat.jsonl').open('x', encoding='utf-8', buffering=1) as stream:
        while not (folder / 'dummy_finish.json').exists():
            stream.write(json.dumps({'pid': os.getpid(), 'monotonic': time.monotonic()}) + '\n')
            time.sleep(.1)


if __name__ == '__main__':
    main()
