"""Retain the lightweight queue and the original recovered-R66 qualification."""
from copy import deepcopy
import run_dependency_queue_20261006 as original

original_ready = original.ready


def ready(job, jobs):
    if job['gate'].get('parent') != 66:
        return original_ready(job, jobs)
    probe = deepcopy(job)
    probe['gate'].pop('parent')
    if not original_ready(probe, jobs):
        return False
    # R66's first scope failed; its independent v3 recovery is the authoritative
    # completed scope. Use the same strict verifier as every original driver.
    import qualified_round_recovery_evidence_v2_20261005 as qualification
    try:
        return qualification.complete_round_evidence(66) is not None
    finally:
        qualification.close()


if __name__ == '__main__':
    original.ready = ready
    original.main()
