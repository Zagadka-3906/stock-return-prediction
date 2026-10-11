"""Serialize completed49-score evidence after the actual full101 recovery writer."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import publish_conditional_residual_evidence_20261006 as publication


def main():
    original = publication.wait_closed

    def after_current_registration(service):
        service = Path(service)
        if service.name == 'conditional_flag_round101_full_registration_v2':
            service = service.with_name('conditional_flag_round101_full_registration_v3')
            while not (service / 'native_launch.json').exists():
                time.sleep(30)
        return original(service)

    publication.wait_closed = after_current_registration
    try:
        publication.main('scores')
    finally:
        publication.wait_closed = original


if __name__ == '__main__':
    main()
