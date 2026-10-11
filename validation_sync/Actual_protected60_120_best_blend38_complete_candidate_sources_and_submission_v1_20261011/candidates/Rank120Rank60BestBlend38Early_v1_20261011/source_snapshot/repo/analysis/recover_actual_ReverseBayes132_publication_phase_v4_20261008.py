"""Preserve the running scorer; recover only the failed scores publication and missing followers."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    services = A / 'service_owned_workflows_20261006'
    scorer = read(services / 'nonflag_ReverseBayes40_official_comparison_v1/native_launch.json')
    assert owned(scorer), 'Inspect terminal scorer evidence before any recovery; never restart it.'
    failed = services / 'nonflag_ReverseBayes40_scores_main_publication_v1'
    assert not owned(read(failed / 'native_launch.json'))
    assert read(failed / 'service_execution.json')['status'] == 'failed'
    assert 'FileExistsError' in (failed / 'stderr.log').read_text(encoding='utf8')
    assert read(services / 'nonflag_ReverseBayes40_full37_controls_main_publication_v1/service_execution.json')['status'] == 'passed'
    source = A / 'publish_nonflag_ReverseBayes40_evidence_v3_20261008.py'
    publisher = A / 'publish_nonflag_ReverseBayes40_evidence_v4_20261008.py'
    text = source.read_text(encoding='utf8')
    old = "with installed(A/'publish_nonflag_ReverseBayes40_evidence_v3_20261008_file_IO'):main(sys.argv[1])"
    assert text.count(old) == 1
    text = text.replace(old, "with installed(A/('publish_nonflag_ReverseBayes40_evidence_v4_20261008_file_IO_'+sys.argv[1])):main(sys.argv[1])")
    compile(text, str(publisher), 'exec')
    assert not publisher.exists()
    publisher.write_text(text, encoding='utf8', newline='\n')
    prep_old = A / 'prepare_nonflag_ReverseBayes40_selected_candidate_v1_20261007.py'
    prep = A / 'prepare_nonflag_ReverseBayes40_selected_candidate_v2_20261008.py'
    text = prep_old.read_text(encoding='utf8').replace("closed('nonflag_ReverseBayes40_scores_main_publication_v1')",
        "closed('nonflag_ReverseBayes40_scores_main_publication_v2_20261008')")
    proof = A / 'actual_ReverseBayes132_publication_phase_recovery_v4_20261008.json'
    needle = "    pins={**protocol_pins,**pilot['input_sha256'],**{str(p):sha(p) for p in sources}}"
    assert text.count(needle) == 1
    text = text.replace(needle, "    sources += [A/'actual_ReverseBayes132_publication_phase_recovery_v4_20261008.json',A/'publish_nonflag_ReverseBayes40_evidence_v4_20261008.py',A/'recover_actual_ReverseBayes132_publication_phase_v4_20261008.py']\n" + needle)
    compile(text, str(prep), 'exec')
    assert not prep.exists()
    prep.write_text(text, encoding='utf8', newline='\n')
    old_full = A / 'run_nonflag_ReverseBayes40_round132_full_registration_v2_20261008.py'
    full = A / 'run_nonflag_ReverseBayes40_round132_full_registration_v3_20261008.py'
    text = old_full.read_text(encoding='utf8').replace('nonflag_ReverseBayes40_scores_main_publication_v1',
        'nonflag_ReverseBayes40_scores_main_publication_v2_20261008')
    text = text.replace('run_nonflag_ReverseBayes40_round132_full_registration_v2_20261008_file_IO',
        'run_nonflag_ReverseBayes40_round132_full_registration_v3_20261008_file_IO')
    needle = "protocol=register();folder=A/'optimization_20261003_r132';pins=protocol['input_sha256']"
    assert text.count(needle) == 1
    text = text.replace(needle, needle + "\n    recovery=A/'actual_ReverseBayes132_publication_phase_recovery_v4_20261008.json'\n    pins={**pins,**read(recovery)['input_sha256'],str(recovery):sha(recovery)}")
    compile(text, str(full), 'exec')
    assert not full.exists()
    full.write_text(text, encoding='utf8', newline='\n')
    sources = [Path(__file__), source, publisher, prep_old, prep, old_full, full,
        A / 'publish_actual_ReverseBayes132_full_scope_v2_20261008.py',
        A / 'actual_ReverseBayes132_manual_routes_v3_20261008.json',
        failed / 'service_execution.json', failed / 'stderr.log', failed / 'job_definition.json',
        services / 'actual_manual_ReverseBayes132_dependency_queue_v3_20261008/service_execution.json',
        services / 'actual_manual_ReverseBayes132_dependency_queue_v3_20261008/stderr.log']
    pins = {str(p): sha(p) for p in sources}
    create(proof, {'status': 'recovered_only_phase_colliding_publication_and_not_yet_dispatched_followers',
        'input_sha256': pins, 'live_original_scorer_preserved': scorer,
        'phase_log_directories_distinct': True, 'original_failed_states_preserved': True,
        'new_native_fits': 0, 'new_quality_scores': 0, 'scorer_restarted_or_rescored': False, 'test_labels_read': False})
    admitted = A / 'nonflag_ReverseBayes40_round132_source_admission_v1_20261007.json'
    pins.update({**read(admitted)['input_sha256'], str(admitted): sha(admitted), str(proof): sha(proof)})
    jobs = [
        ('nonflag_ReverseBayes40_scores_main_publication_v2_20261008', publisher.name, ['scores']),
        ('nonflag_ReverseBayes40_selected_candidate_preparation_v1', prep.name, []),
        ('nonflag_ReverseBayes40_selected_candidate_sealing_v1', 'seal_nonflag_ReverseBayes40_selected_candidate_v1_20261007.py', []),
        ('nonflag_ReverseBayes40_round132_full_registration_v1', full.name, [])]
    assert all(not (services / n).exists() for n, _, _ in jobs)
    launches = {n: start(n, d, args, pins) for n, d, args in jobs}
    create(A / 'actual_ReverseBayes132_recovered4_followers_v4_20261008.json', {
        'status': 'started_only_failed_or_missing_administrative_followers_of_same_live_scorer',
        'launches': launches, 'input_sha256': pins, 'original_live_scorer': scorer})
    print('Recovered only4 followers; original live40 scorer left running.', flush=True)


if __name__ == '__main__':
    main()
