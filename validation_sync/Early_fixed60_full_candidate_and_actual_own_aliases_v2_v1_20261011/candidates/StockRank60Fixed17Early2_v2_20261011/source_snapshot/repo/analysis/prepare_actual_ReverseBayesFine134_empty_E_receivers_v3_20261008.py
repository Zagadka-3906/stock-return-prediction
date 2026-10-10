"""Bind fine-grid receivers to real133 completion and predeclare empty E display admission."""
from pathlib import Path
import importlib.util
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    proof = A / 'actual_ReverseBayesFine134_empty_E_receiver_preparation_v3_20261008.json'
    assert not proof.exists()
    assert not (A / 'nonflag_ReverseBayesFine40_official_comparison_v1_20261007').exists()
    services = A / 'service_owned_workflows_20261006'
    assert not (services / 'nonflag_ReverseBayesFine40_round134_source_admission_v1').exists()
    old_proof = A / 'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json'
    for p, d in read(old_proof)['input_sha256'].items(): assert sha(p) == d, p
    stems = ['prepare_nonflag_ReverseBayesFine40_round134_sources',
             'run_nonflag_ReverseBayesFine40_official_comparison',
             'run_nonflag_ReverseBayesFine40_admitted_comparison',
             'run_nonflag_ReverseBayesFine40_round134_full_registration',
             'prepare_nonflag_ReverseBayesFine40_selected_candidate',
             'publish_nonflag_ReverseBayesFine40_evidence',
             'verify_nonflag_ReverseBayesFine40_round134_sources',
             'publish_actual_deadline_and_full_training_handoff',
             'queue_actual_ReverseBayesFine134']
    mapping = {stem + '_v2_20261008': stem + '_v3_20261008' for stem in stems}
    mapping.update({'verify_nonflag_ReverseBayesFine40_prospective_routes_v3_20261008':
                    'verify_nonflag_ReverseBayesFine40_prospective_routes_v4_20261008',
                    'nonflag_ReverseBayesFine40_prospective_routes_v3_20261008':
                    'nonflag_ReverseBayesFine40_prospective_routes_v4_20261008',
                    'nonflag_SparseGram40_round133_full_registration_recovery_v3_20261008':
                    'nonflag_SparseGram40_round133_full_registration_resume_v4_20261008',
                    'actual_deadline_and_full_training_handoff_main_publication_v2_20261008':
                    'actual_deadline_and_full_training_handoff_main_publication_v3_20261008',
                    'actual_deadline_and_full_training_handoff_main_v2_20261008':
                    'actual_deadline_and_full_training_handoff_main_v3_20261008',
                    'actual_ReverseBayesFine134_complete_dependency_plan_v2_20261008':
                    'actual_ReverseBayesFine134_complete_dependency_plan_v3_20261008',
                    'actual_ReverseBayesFine134_complete_hidden_launches_v2_20261008':
                    'actual_ReverseBayesFine134_complete_hidden_launches_v3_20261008'})
    pairs = [(A / (stem + '_v2_20261008.py'), A / (stem + '_v3_20261008.py')) for stem in stems]
    pairs.append((A / 'verify_nonflag_ReverseBayesFine40_prospective_routes_v3_20261008.py',
                  A / 'verify_nonflag_ReverseBayesFine40_prospective_routes_v4_20261008.py'))
    for source, target in pairs:
        text = source.read_text(encoding='utf8')
        for before, after in mapping.items(): text = text.replace(before, after)
        if target.name.startswith('prepare_nonflag_ReverseBayesFine40_round134_sources'):
            needle = "        if name.startswith('register_'):"
            assert text.count(needle) == 1
            addition = "        if name.startswith('build_lossless_'):\n" \
                "            before='    assert not out.exists()\\n    out.mkdir(parents=True)'\n" \
                "            after='    from admit_empty_E_display_junction_v1_20261008 import ensure\\n    ensure(out, number)'\n" \
                "            assert text.count(before)==1\n" \
                "            text=text.replace(before,after)\n" \
                "        if name.startswith('lossless_ranking_runtime_'):\n" \
                "            before='    assert not display.exists() and not qa_folder.exists()'\n" \
                "            after='    assert not qa_folder.exists()\\n    from admit_empty_E_display_junction_v1_20261008 import ensure\\n    ensure(display, number, create=False)'\n" \
                "            assert text.count(before)==1\n" \
                "            text=text.replace(before,after)\n"
            text = text.replace(needle, addition + needle)
            needle = '            text=text.replace(marker,extra+marker)'
            assert text.count(needle) == 1
            text = text.replace(needle,
                "            extra += \"    sources += [A/'admit_empty_E_display_junction_v1_20261008.py', A/'actual_ReverseBayesFine134_empty_E_receiver_preparation_v3_20261008.json']\\n\"\n" + needle)
        if target.name.startswith('queue_actual_'):
            text = text.replace("             A / 'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json',",
                                "             A / 'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json',\n"
                                "             A / 'actual_ReverseBayesFine134_empty_E_receiver_preparation_v3_20261008.json',")
        if target.name.startswith('verify_nonflag_ReverseBayesFine40_round134_sources'):
            text = text.replace('    for p in sources:',
                "    sources += [A/'actual_ReverseBayesFine134_empty_E_receiver_preparation_v3_20261008.json', A/'admit_empty_E_display_junction_v1_20261008.py']\n    for p in sources:")
        if target.name.startswith('publish_actual_deadline_'):
            text = text.replace('    folders = [(resource,',
                "    sources += [A/'actual_SparseGram133_empty_E_display_resume_v4_20261008.json', A/'actual_ReverseBayesFine134_empty_E_receiver_preparation_v3_20261008.json']\n"
                '    folders = [(resource,')
        compile(text, str(target), 'exec')
        assert not target.exists(), target
        target.write_text(text, encoding='utf8', newline='\n')
    prospective = A / 'verify_nonflag_ReverseBayesFine40_prospective_routes_v4_20261008.py'
    spec = importlib.util.spec_from_file_location('actual_fine134_E_prospective_v4', prospective)
    module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.main()
    prospective_proof = A / 'nonflag_ReverseBayesFine40_prospective_routes_v4_20261008.json'
    assert not read(prospective_proof)['issues']
    from admit_empty_E_display_junction_v1_20261008 import ensure
    ensure(A / 'lossless_ranking_display_v2_20261006/round134', 134, create=False)
    paths = [Path(__file__), old_proof, prospective_proof,
             A / 'actual_SparseGram133_empty_E_display_resume_v4_20261008.json',
             A / 'admit_empty_E_display_junction_v1_20261008.py', *[p for pair in pairs for p in pair]]
    pins = {str(p): sha(p) for p in paths}
    create(proof, {'status': 'passed_actual134_pre_score_empty_E_display_and_real133_predecessor_routes',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'original_fine_grid_weights_and_native_transform_controls_preserved': True,
        'all24_prospective_sources_and12_full_graph_controls_and3_pilot_status_guards_checked': True,
        'display_existing_only_if_exact_empty_owned_E_junction': True,
        'original_six_view_and45_second_full_browser_QA_preserved': True,
        'original_failed_sources_and_failed_states_preserved': True,
        'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False})
    pins[str(proof)] = sha(proof)
    jobs = [('actual_deadline_and_full_training_handoff_main_publication_v3_20261008',
             'publish_actual_deadline_and_full_training_handoff_v3_20261008.py'),
            ('actual_ReverseBayesFine134_complete_dependency_queue_v3_20261008',
             'queue_actual_ReverseBayesFine134_v3_20261008.py')]
    rows = {}
    for name, driver in jobs:
        assert not (services / name).exists()
        rows[name] = start(name, driver, [], pins)
    create(A / 'actual_ReverseBayesFine134_empty_E_dependency_hidden_launches_v3_20261008.json', {
        'status': 'started_real133_completion_gated_deadline_and_fine134_pipeline',
        'launches': rows, 'input_sha256': pins, 'new_quality_scores_by_launch': 0, 'test_labels_read': False})
    print('24 sources,12 graphs,3 truthful status guards,empty E output verified; actual133-gated pipeline launched.', flush=True)


if __name__ == '__main__':main()
