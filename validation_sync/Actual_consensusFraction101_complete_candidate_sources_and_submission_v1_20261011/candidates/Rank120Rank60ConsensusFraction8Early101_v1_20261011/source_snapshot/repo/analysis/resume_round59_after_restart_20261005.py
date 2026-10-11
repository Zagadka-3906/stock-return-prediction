"""Resume the original immutable R59 protocol after a verified host restart."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]
OUT = ROOT / 'analysis/round59_restart_recovery_20261005'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    from locked_read_hash_cache_20261004 import LockedReadHashCache, fresh_sha
    from run_new_neural_families_locked_pipeline_20261004 import main as original_main
    proof = read(OUT / 'pre_resume_verification.json')
    assert proof['status'] == 'passed'
    expected = dict(proof['recovery_input_sha256'])
    expected[str((OUT / 'pre_resume_verification.json').resolve())] = fresh_sha(OUT / 'pre_resume_verification.json')
    snapshot = read(OUT / 'wave247_before_restart_resume.json')
    original = ROOT / 'analysis/optimization_20261003_r59'
    assert not (original / 'provenance_scope_execution.json').exists()
    with LockedReadHashCache(expected):
        original_main(59)
        scope = read(original / 'provenance_scope_execution.json')
        assert scope['status'] == 'passed' and scope['all_sha_bindings_restored']
        current = read(original / 'wave247_results.json')
        assert current['status'] == 'complete'
        for key, row in snapshot['results'].items():
            assert current['results'][key] == row, key
        assert read(ROOT / 'results/optimization_20261003_r59.json')['status'] == 'complete'
    create(OUT / 'verification.json', {
        'status': 'passed', 'at_local': datetime.now().isoformat(timespec='seconds'),
        'pre_resume_verification_sha256': fresh_sha(OUT / 'pre_resume_verification.json'),
        'original_frozen_protocol_preserved_sha256': fresh_sha(original / 'protocol.json'),
        'preserved_completed_score_records': len(snapshot['results']),
        'all_preserved_records_unchanged': True,
        'recovery_sources_read_locked_and_fully_rehashed_at_end': True,
        'original_scientific_pipeline_and_official_scorer_unchanged': True,
        'original_scope_did_not_close_before_host_restart': True,
        'new_scientific_scope': str(original / 'provenance_scope_execution.json'),
        'new_scientific_scope_sha256': fresh_sha(original / 'provenance_scope_execution.json'),
        'new_model_fits': 0, 'test_labels_read': False,
        'continuous_goal_complete': False,
    })


if __name__ == '__main__':
    main()
