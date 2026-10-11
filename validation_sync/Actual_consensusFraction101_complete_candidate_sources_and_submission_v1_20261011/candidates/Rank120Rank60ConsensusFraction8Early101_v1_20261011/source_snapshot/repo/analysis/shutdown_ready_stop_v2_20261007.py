"""Preserve the original stop contract; tolerate actual asynchronous Windows suspend."""
from pathlib import Path
import sys
import time
import psutil

A = Path(__file__).resolve().parent
sys.path.insert(0, str(A))
import shutdown_ready_stop_20261007 as original
from scheduled_user_pause_20261007 import Journal, identity, exact, protected, now


class StableJournal(Journal):
    def suspend(self, process, owner, role):
        record = identity(process)
        assert not protected(process) and process.pid != psutil.Process().pid
        entry = next((e for e in self.data['entries'] if e['identity'] == record
                      and e['phase'] in ('pending', 'suspended')), None)
        if entry is None and process.status() == psutil.STATUS_STOPPED:
            return super().suspend(process, owner, role)
        if entry is None:
            entry = {'identity': record, 'owner': owner, 'role': role,
                     'previous_status': process.status(), 'phase': 'pending', 'at_local': now()}
            self.data['entries'].append(entry)
        entry['phase'] = 'pending'
        self.flush()
        for _ in range(3):
            current = exact(record)
            if current is None:
                entry['phase'] = 'exited_before_suspend'
                self.flush()
                return
            if current.status() != psutil.STATUS_STOPPED:
                current.suspend()
            for _ in range(20):
                current = exact(record)
                if current is None or current.status() == psutil.STATUS_STOPPED:
                    entry['phase'] = 'exited_before_suspend' if current is None else 'suspended'
                    self.flush()
                    return
                time.sleep(.05)
        raise RuntimeError('Verified process did not reach suspended state; readiness not claimed.')


if __name__ == '__main__':
    original.Journal = StableJournal
    original.main()
