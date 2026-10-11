"""Re-admit original numerical routes with actual new-day administrative receivers."""
from pathlib import Path
import ast
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    old_parent = 'nonflag_RidgeMicro40_round131_full_registration_v1'
    new_parent = 'round131_preserved_QA42_main_publication_recovery_v3_20261008'
    originals = {
        'verify_nonflag_ReverseBayes40_round132_sources_v2_20261007.py': 'verify_nonflag_ReverseBayes40_round132_sources_v3_20261008.py',
        'run_nonflag_ReverseBayes40_official_comparison_v1_20261007.py': 'run_nonflag_ReverseBayes40_official_comparison_v2_20261008.py',
        'run_nonflag_ReverseBayes40_admitted_comparison_v2_20261007.py': 'run_nonflag_ReverseBayes40_admitted_comparison_v3_20261008.py',
        'publish_nonflag_ReverseBayes40_evidence_v2_20261007.py': 'publish_nonflag_ReverseBayes40_evidence_v3_20261008.py',
        'run_nonflag_ReverseBayes40_round132_full_registration_v1_20261007.py': 'run_nonflag_ReverseBayes40_round132_full_registration_v2_20261008.py'}
    paths = [Path(__file__), A / 'queue_actual_manual_ReverseBayes132_after131_v3_20261008.py',
        A / 'actual_manual_resume_after_shutdown_20261008.json',
        A / 'nonflag_ReverseBayes40_round132_dispatch_deferred_until_manual_continue_20261007.json',
        A / 'signed132_actual_import_and_publication_recovery_v2_20261007.json']
    controls = []
    for old_name, new_name in originals.items():
        old, new = A / old_name, A / new_name
        text = old.read_text(encoding='utf8').replace(old_parent, new_parent)
        if old_name.startswith(('verify_', 'run_nonflag_ReverseBayes40_admitted')):
            text = text.replace('run_nonflag_ReverseBayes40_official_comparison_v1_20261007',
                'run_nonflag_ReverseBayes40_official_comparison_v2_20261008')
        if old_name.startswith(('publish_', 'run_nonflag_ReverseBayes40_round132')):
            text = text.replace('main_publisher_v7', 'main_publisher_v8_20261008')
            needle = "if __name__=='__main__':"
            first = text.index(needle)
            call = "main(sys.argv[1])" if old_name.startswith('publish_') else 'main()'
            text = text[:first] + needle + "\n    from file_backed_hidden_git_runtime_20261007 import installed\n    with installed(A/" + repr(new.stem + '_file_IO') + '):' + call + '\n'
        if old_name.startswith('verify_'):
            needle = '    for p in sources:\n'
            assert text.count(needle) == 1
            additions = [A / n for n in originals.values()] + paths
            text = text.replace(needle, '    sources += [' + ','.join('A/' + repr(p.relative_to(A).as_posix()) for p in additions) + ']\n' + needle)
        if old_name.startswith('run_nonflag_ReverseBayes40_round132'):
            # Keep the admitted generator's original bytes; correct only the publication explanation at invocation.
            text = text.replace('from publish_nonflag_ReverseBayes40_round132_full_validation_20261007 import main as github',
                'from publish_actual_ReverseBayes132_full_scope_v2_20261008 import main as github')
        compile(text, str(new), 'exec')
        assert not new.exists()
        new.write_text(text, encoding='utf8', newline='\n')
        if old_name.startswith('run_nonflag_ReverseBayes40_official'):
            before = old.read_text(encoding='utf8').replace(old_parent, new_parent)
            assert before == text
            controls.append({'source': new_name, 'numerical_code_identical_after_only_actual_parent_service_gate_replacement': True})
        paths.extend((old, new))
    wrapper = A / 'publish_actual_ReverseBayes132_full_scope_v2_20261008.py'
    assert wrapper.exists()
    paths.append(wrapper)
    preparation = A / 'nonflag_ReverseBayes40_science_route_preparation_v1_20261007.json'
    prospective = A / 'nonflag_ReverseBayes40_prospective_routes_v1_20261007.json'
    pins = {**read(preparation)['input_sha256'], **read(prospective)['input_sha256'], **{str(p): sha(p) for p in [*paths, preparation, prospective]}}
    for p, d in pins.items(): assert sha(p) == d, p
    create(A / 'actual_ReverseBayes132_manual_routes_v3_20261008.json', {
        'status': 'redeclared_actual_administrative_routes_original_negative40_math_unchanged',
        'input_sha256': pins, 'numerical_source_controls': controls,
        'original24_prospective_and12_graph_controls_preserved': True,
        'actual_full131_and_source_admission_still_required_before_scores': True,
        'old_expired_dispatch_and_old_failed131_services_not_restarted': True,
        'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False})
    row = start('actual_manual_ReverseBayes132_dependency_queue_v3_20261008',
        'queue_actual_manual_ReverseBayes132_after131_v3_20261008.py', [], pins)
    create(A / 'actual_manual_ReverseBayes132_hidden_queue_v3_20261008.json', {'identity': row, 'input_sha256': pins})
    print('Started actual manually resumed negative40 source admission queue.', flush=True)


if __name__ == '__main__':
    main()
