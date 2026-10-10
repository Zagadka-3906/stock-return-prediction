"""Correct only a legacy pilot status guard; preserve every executed scientific byte."""
from pathlib import Path
import ast
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    services = A / 'service_owned_workflows_20261006'
    failed = services / 'nonflag_SparseGram40_round133_full_registration_v1'
    assert not owned(read(failed / 'native_launch.json'))
    assert read(failed / 'service_execution.json')['status'] == 'failed'
    error = (failed / 'stderr.log').read_text(encoding='utf8')
    assert "pilot['status'] == 'passed_actual40_nonflag_Ridge_full_official_comparisons'" in error
    assert not (A / 'optimization_20261003_r133').exists()
    assert not (ROOT / 'candidates/optimization_20261003_r133').exists()
    for name in ('nonflag_SparseGram40_official_comparison_v1',
                 'nonflag_SparseGram40_scores_main_publication_v1',
                 'nonflag_SparseGram40_selected_candidate_preparation_v1',
                 'nonflag_SparseGram40_selected_candidate_sealing_v1'):
        assert read(services / name / 'service_execution.json')['status'] == 'passed', name
    prep_path = A / 'nonflag_SparseGram40_round133_source_preparation_v1_20261007.json'
    prep = read(prep_path)
    assert prep['status'] == 'passed_actual40_sealed_candidate_and_admitted_full133_QA44_sources'
    for p, digest in prep['input_sha256'].items():
        assert sha(p) == digest, p
    pilot_path = A / 'nonflag_SparseGram40_official_comparison_v1_20261007/verification.json'
    pilot = read(pilot_path)
    expected = 'passed_actual40_nonflag_SparseGram64_full_official_comparisons'
    assert pilot['status'] == expected and len(pilot['records']) == 40
    assert pilot['best']['metrics']['final_score'] == 0.45111411010253927
    for record in pilot['records']:
        capsule = Path(record['official_score_cache']['official_metrics_source'])
        assert sha(capsule) == record['official_metric_capsule_sha256']
        assert read(capsule)['metrics'] == record['metrics']
    ready_path = A / 'nonflag_SparseGram40_selected_release_v1_20261007/selected_candidate_ready_for_registration.json'
    ready = read(ready_path)
    assert ready['best'] == pilot['best'] and ready['sealed_candidate_complete']
    assert not ready['new_inference_claimed']
    proof_path = A / 'actual_SparseGram133_registration_guard_recovery_v3_20261008.json'
    old_registry = A / 'register_nonflag_SparseGram40_round133_artifacts_20261007.py'
    registry = A / 'register_nonflag_SparseGram40_round133_artifacts_v2_20261008.py'
    old_full = A / 'run_nonflag_SparseGram40_round133_full_registration_v2_20261008.py'
    full = A / 'run_nonflag_SparseGram40_round133_full_registration_v3_20261008.py'
    original = old_registry.read_text(encoding='utf8')
    before = "assert pilot['status'] == 'passed_actual40_nonflag_Ridge_full_official_comparisons'"
    after = f"assert pilot['status'] == '{expected}'"
    assert original.count(before) == 1
    corrected = original.replace(before, after)
    assert ast.dump(ast.parse(corrected.replace(after, before))) == ast.dump(ast.parse(original))
    needle = "    pins = {**read(RELEASE / 'protocol.json')['input_sha256']"
    extra = "    sources += [A / 'register_nonflag_SparseGram40_round133_artifacts_20261007.py',\n" \
        "        A / 'run_nonflag_SparseGram40_round133_full_registration_v2_20261008.py',\n" \
        "        A / 'run_nonflag_SparseGram40_round133_full_registration_v3_20261008.py',\n" \
        "        A / 'recover_actual_SparseGram133_registration_guard_v3_20261008.py',\n" \
        "        A / 'actual_SparseGram133_registration_guard_recovery_v3_20261008.json']\n"
    assert corrected.count(needle) == 1
    corrected = corrected.replace(needle, extra + needle)
    compile(corrected, str(registry), 'exec')
    assert not registry.exists()
    registry.write_text(corrected, encoding='utf8', newline='\n')
    text = old_full.read_text(encoding='utf8')
    text = text.replace("out=A/'nonflag_SparseGram40_round133_actual_registration_v1_20261007'",
                        "out=A/'nonflag_SparseGram40_round133_actual_registration_v3_20261008'")
    prepare = "    from prepare_nonflag_SparseGram40_round133_sources_v1_20261007 import main as prepare_sources\n    prepare_sources()\n"
    assert text.count(prepare) == 1
    text = text.replace(prepare, "    # Original eight sources already materialized before the preserved failed guard.\n")
    text = text.replace('from register_nonflag_SparseGram40_round133_artifacts_20261007 import main as register',
                        'from register_nonflag_SparseGram40_round133_artifacts_v2_20261008 import main as register')
    text = text.replace("registry=A/'register_nonflag_SparseGram40_round133_artifacts_20261007.py'",
                        "registry=A/'register_nonflag_SparseGram40_round133_artifacts_v2_20261008.py'")
    text = text.replace('nonflag_SparseGram40_actual_source_paths_before_registration_20261007.json',
                        'nonflag_SparseGram40_actual_source_paths_before_registration_v3_20261008.json')
    text = text.replace('run_nonflag_SparseGram40_round133_full_registration_v2_file_IO_20261008',
                        'run_nonflag_SparseGram40_round133_full_registration_v3_file_IO_20261008')
    needle = "    pins={**pins,**read(recovery)['input_sha256'],str(recovery):sha(recovery)}"
    assert text.count(needle) == 1
    text = text.replace(needle, needle + "\n    guard_recovery=A/'actual_SparseGram133_registration_guard_recovery_v3_20261008.json'\n    pins={**pins,**read(guard_recovery)['input_sha256'],str(guard_recovery):sha(guard_recovery)}")
    compile(text, str(full), 'exec')
    assert not full.exists()
    full.write_text(text, encoding='utf8', newline='\n')
    sources = [Path(__file__), old_registry, registry, old_full, full, prep_path, pilot_path, ready_path,
               failed / 'job_definition.json', failed / 'native_launch.json',
               failed / 'service_execution.json', failed / 'stderr.log']
    pins = {**prep['input_sha256'], **{str(p): sha(p) for p in sources}}
    create(proof_path, {
        'status': 'passed_actual133_preserved40_scores_and_original8_sources_with_truthful_pilot_guard_receiver',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'legacy_guard_status': 'passed_actual40_nonflag_Ridge_full_official_comparisons',
        'actual_pilot_status_and_corrected_guard': expected,
        'guard_only_scientific_AST_unchanged_before_adding_audit_sources': True,
        'all40_existing_official_metric_capsules_rehashed': True,
        'original_predeclared8_sources_and_original_failure_preserved': True,
        'selected_candidate_original_freeze_and_all_native_proofs_preserved': True,
        'new_quality_scores': 0, 'new_native_fits': 0, 'new_inference': 0,
        'test_labels_read': False, 'scientific_workers_restarted': 0})
    pins[str(proof_path)] = sha(proof_path)
    name = 'nonflag_SparseGram40_round133_full_registration_recovery_v3_20261008'
    assert not (services / name).exists()
    row = start(name, full.name, [], pins)
    create(A / 'actual_SparseGram133_registration_guard_recovery_hidden_launch_v3_20261008.json', {
        'status': 'started_only_actual133_registration_QA44_and_main_recovery',
        'identity': row, 'input_sha256': pins, 'new_quality_scores': 0,
        'new_native_fits': 0, 'new_inference': 0, 'test_labels_read': False})
    print('Preserved40 scores; corrected only actual pilot guard; full133 QA44 recovery started.', flush=True)


if __name__ == '__main__':
    main()
