"""Prepare complete stronger-L2127 routes without changing any admitted ancestor source."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from nonflag_RFF128Hi127_route_mapping_20261007 import convert


def main():
    names = ['run_nonflag_RFF128Low76_official_comparison_v1_20261007.py',
             'prepare_nonflag_RFF128Low76_selected_candidate_v1_20261007.py',
             'seal_nonflag_RFF128Low76_selected_candidate_v1_20261007.py',
             'run_nonflag_RFF128Low76_admitted_comparison_v1_20261007.py',
             'run_nonflag_RFF128Low76_round126_full_registration_v1_20261007.py',
             'publish_nonflag_RFF128Low76_evidence_v1_20261007.py',
             'verify_nonflag_RFF128Low76_round126_sources_v1_20261007.py',
             'verify_nonflag_RFF128Low76_prospective_routes_v1_20261007.py',
             'predict_nonflag_residual_RFF128Low_complete_scheme_20261007.py']
    paths = [Path(__file__), A / 'nonflag_RFF128Hi127_route_mapping_20261007.py',
             A / 'prepare_nonflag_RFF128Hi76_round127_sources_v1_20261007.py',
             A / 'nonflag_RFF128Hi76_plan_20261007.json',
             A / 'nonflag_RFF128Hi_actual_native_and_transform_controls_20261007.json',
             A / 'actual4_official_scoring_8_5GiB_gate_preflight_20261007/verification.json']
    for name in names:
        old, new = A / name, A / convert(name)
        assert not new.exists(), new
        text = convert(old.read_text(encoding='utf-8'))
        if name.startswith('publish_'):
            text = text.replace('完整126候选', '完整127候选')
        compile(text, str(new), 'exec')
        new.write_text(text, encoding='utf-8', newline='\n')
        paths.extend((old, new))
    create(A / 'nonflag_RFF128Hi76_science_route_preparation_v1_20261007.json', {
        'status': 'compiled_fresh_complete_RFF128Hi127_both_signs_scoring_freeze_replay_and_publication_routes',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256': {str(p): sha(p) for p in paths}, 'actual_official_scores': 0,
        'actual_full127_admission_not_yet_claimed': True, 'test_labels_read': False})
    from verify_nonflag_RFF128Hi76_prospective_routes_v1_20261007 import main as prospective
    prospective()


if __name__ == '__main__':
    main()
