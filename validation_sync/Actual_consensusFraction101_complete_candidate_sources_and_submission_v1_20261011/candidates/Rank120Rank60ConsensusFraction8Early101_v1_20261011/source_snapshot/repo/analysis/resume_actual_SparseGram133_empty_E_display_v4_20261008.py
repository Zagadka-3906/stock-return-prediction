"""Continue already registered40 scores, admitting only the precreated empty E display junction."""
from pathlib import Path
import ast
import os
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    services = A / 'service_owned_workflows_20261006'
    failed = services / 'nonflag_SparseGram40_round133_full_registration_recovery_v3_20261008'
    assert not owned(read(failed / 'native_launch.json'))
    assert read(failed / 'service_execution.json')['status'] == 'failed'
    assert 'assert not display.exists() and not qa_folder.exists()' in (failed / 'stderr.log').read_text(encoding='utf8')
    folder = A / 'optimization_20261003_r133'
    assert read(folder / 'actual_registration_preparation.json')['status'] == 'passed_actual40_scores_controls_and_sealed_selected_model_candidate_registered'
    assert not (folder / 'full_registration_execution.json').exists()
    assert not (A / 'lossless_ranking_display_qa_v44_20261007/round133').exists()
    from admit_empty_E_display_junction_v1_20261008 import ensure
    ensure(A / 'lossless_ranking_display_v2_20261006/round133', 133, create=False)
    old_builder = A / 'build_lossless_ranking_display_round133_20261007.py'
    builder = A / 'build_lossless_ranking_display_round133_empty_E_v2_20261008.py'
    text = old_builder.read_text(encoding='utf8')
    before = '    assert not out.exists()\n    out.mkdir(parents=True)'
    after = '    from admit_empty_E_display_junction_v1_20261008 import ensure\n    ensure(out, number)'
    assert text.count(before) == 1
    corrected = text.replace(before, after)
    assert ast.dump(ast.parse(corrected.replace(after, before))) == ast.dump(ast.parse(text))
    assert not builder.exists()
    builder.write_text(corrected, encoding='utf8', newline='\n')
    old_adapter = A / 'lossless_ranking_runtime_adapter_round133_20261007.py'
    adapter = A / 'lossless_ranking_runtime_adapter_round133_empty_E_v2_20261008.py'
    text = old_adapter.read_text(encoding='utf8')
    before = '    assert not display.exists() and not qa_folder.exists()'
    after = '    assert not qa_folder.exists()\n    from admit_empty_E_display_junction_v1_20261008 import ensure\n    ensure(display, number, create=False)'
    assert text.count(before) == 1
    text = text.replace(before, after).replace(old_builder.stem, builder.stem)
    assert not adapter.exists()
    adapter.write_text(text, encoding='utf8', newline='\n')
    old_full = A / 'run_nonflag_SparseGram40_round133_full_registration_v3_20261008.py'
    full = A / 'run_nonflag_SparseGram40_round133_full_registration_v4_20261008.py'
    proof = A / 'actual_SparseGram133_empty_E_display_resume_v4_20261008.json'
    text = old_full.read_text(encoding='utf8')
    text = text.replace('nonflag_SparseGram40_round133_actual_registration_v3_20261008',
                        'nonflag_SparseGram40_round133_actual_registration_v4_20261008')
    start_at = text.index('    # Original eight sources already materialized')
    end_at = text.index('    parent_number=protocol', start_at)
    replacement = "    # Registration and scientific local publication already completed before display setup failed.\n" \
        "    folder=A/'optimization_20261003_r133'\n" \
        "    ready=read(A/'nonflag_SparseGram40_selected_release_v1_20261007/selected_candidate_ready_for_registration.json')\n" \
        "    assert ready['sealed_candidate_complete'] and not ready['new_inference_claimed']\n" \
        "    protocol=read(folder/'protocol.json')\n" \
        "    assert protocol['expected_scored_records']==40\n" \
        "    assert read(folder/'selection.json')['winner']['metrics']==ready['best']['metrics']\n" \
        "    pins=read(folder/'frozen_before_actual_full_registration.json')['input_sha256']\n" \
        "    recovery=A/'actual_SparseGram133_empty_E_display_resume_v4_20261008.json'\n" \
        "    pins={**pins,**read(recovery)['input_sha256'],str(recovery):sha(recovery)}\n" \
        "    for p,d in pins.items():assert sha(p)==d,p\n" \
        "    candidate=ROOT/'candidates/optimization_20261003_r133'\n" \
        "    for p in [Path(__file__),A/'lossless_ranking_runtime_adapter_round133_empty_E_v2_20261008.py',A/'build_lossless_ranking_display_round133_empty_E_v2_20261008.py',A/'admit_empty_E_display_junction_v1_20261008.py',recovery]:\n" \
        "        target=candidate/'registration_sources/round133_resumed_display_v4'/p.relative_to(ROOT)\n" \
        "        target.parent.mkdir(parents=True,exist_ok=True);os.link(p,target)\n"
    text = text[:start_at] + replacement + text[end_at:]
    text = text.replace('lossless_ranking_runtime_adapter_round133_20261007', adapter.stem)
    text = text.replace('frozen_before_actual_full_registration.json', 'frozen_before_actual_full_registration_resume_v4_20261008.json')
    # Preserve the original frozen input authority used by the already completed registration.
    text = text.replace("pins=read(folder/'frozen_before_actual_full_registration_resume_v4_20261008.json')['input_sha256']",
                        "pins=read(folder/'frozen_before_actual_full_registration.json')['input_sha256']")
    text = text.replace('actual_main7_idle_before_and_after_hold.json', 'actual_main7_idle_before_and_after_hold_resume_v4_20261008.json')
    text = text.replace('actual_hidden_registration_children.json', 'actual_hidden_registration_children_resume_v4_20261008.json')
    text = text.replace('full_registration_failure.json', 'full_registration_resume_v4_failure_20261008.json')
    text = text.replace('run_nonflag_SparseGram40_round133_full_registration_v3_file_IO_20261008',
                        'run_nonflag_SparseGram40_round133_full_registration_v4_file_IO_20261008')
    compile(text, str(full), 'exec')
    assert not full.exists()
    full.write_text(text, encoding='utf8', newline='\n')
    sources = [Path(__file__), old_builder, builder, old_adapter, adapter, old_full, full,
               A / 'admit_empty_E_display_junction_v1_20261008.py',
               folder / 'actual_registration_preparation.json', folder / 'full_registration_failure.json',
               failed / 'job_definition.json', failed / 'service_execution.json', failed / 'stderr.log']
    pins = {str(p): sha(p) for p in sources}
    create(proof, {'status': 'passed_actual40_already_registered_resume_with_empty_owned_E_display_junction_only',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'display_destination_verified_exact_empty_owned_E_junction': True,
        'all_original_six_views_and_45_second_browser_QA_requirements_preserved': True,
        'original_failure_and_registered40_scores_and_selected_parameter_bytes_preserved': True,
        'new_quality_scores': 0, 'new_native_fits': 0, 'new_inference': 0, 'test_labels_read': False})
    pins[str(proof)] = sha(proof)
    name = 'nonflag_SparseGram40_round133_full_registration_resume_v4_20261008'
    row = start(name, full.name, [], pins)
    create(A / 'actual_SparseGram133_empty_E_display_resume_hidden_launch_v4_20261008.json', {
        'status': 'started_only_missing_actual133_full_display_QA44_and_main', 'identity': row,
        'input_sha256': pins, 'new_quality_scores': 0, 'test_labels_read': False})
    print('Resuming existing40 records with exact empty E display junction and unchanged full QA.', flush=True)


if __name__ == '__main__':
    main()
