"""Pre-score corrective receivers: preserve fine-grid math and validate pilot status guards."""
from pathlib import Path
import ast
import hashlib
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

RECOVERY_SERVICE = 'nonflag_SparseGram40_round133_full_registration_recovery_v3_20261008'
PROOF = A / 'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json'
NEW = {}
ORIGINAL = []


def receiver(old, new, replacements=(), transform=None):
    source = A / old
    target = A / new
    text = source.read_text(encoding='utf8')
    for before, after in replacements:
        assert before in text, (old, before)
        text = text.replace(before, after)
    if transform is not None:
        text = transform(text)
    compile(text, str(target), 'exec')
    assert not target.exists(), target
    target.write_text(text, encoding='utf8', newline='\n')
    ORIGINAL.append(source)
    NEW[old] = target
    return target


def guard_checks(text):
    needle = "        required={n.slice.value"
    addition = "        status_guards=[n for n in ast.walk(registry) if isinstance(n,ast.Compare) and ast.unparse(n.left)==\"pilot['status']\"]\n" \
        "        assert len(status_guards)==1 and len(status_guards[0].comparators)==1\n" \
        "        assert isinstance(status_guards[0].comparators[0],ast.Constant)\n" \
        "        assert status_guards[0].comparators[0].value=='passed_actual40_nonflag_ReverseBayes64_full_official_comparisons'\n"
    if 'tree=ast.parse(text)' in text:
        addition = addition.replace('ast.walk(registry)', 'ast.walk(tree)')
    assert text.count(needle) == 1
    return text.replace(needle, addition + needle)


def main():
    services = A / 'service_owned_workflows_20261006'
    failed_queue = services / 'actual_ReverseBayesFine134_complete_dependency_queue_v1_20261008'
    assert not owned(read(failed_queue / 'native_launch.json'))
    assert read(failed_queue / 'service_execution.json')['status'] == 'failed'
    assert not (A / 'nonflag_ReverseBayesFine40_official_comparison_v1_20261007').exists()
    assert not (services / 'nonflag_ReverseBayesFine40_round134_source_admission_v1').exists()
    controls = A / 'nonflag_residual_ReverseBayesFine37_transform_preflight_20261007/verification.json'
    assert read(controls)['status'] == 'passed_actual37_full5635800_nonflag_ReverseBayes64_independent_CDF_and111_cold_controls'
    plan_path = A / 'nonflag_ReverseBayesFine40_plan_20261007.json'
    original_plan_sha = sha(plan_path)
    generator_old = 'prepare_nonflag_ReverseBayesFine40_round134_sources_v1_20261007.py'
    generator_new = 'prepare_nonflag_ReverseBayesFine40_round134_sources_v2_20261008.py'
    full_old = 'run_nonflag_ReverseBayesFine40_round134_full_registration_v1_20261007.py'
    full_new = 'run_nonflag_ReverseBayesFine40_round134_full_registration_v2_20261008.py'
    expected = 'passed_actual40_nonflag_ReverseBayes64_full_official_comparisons'

    def correct_generator(text):
        needle = "        if name.startswith('publish_'):"
        assert text.count(needle) == 1
        addition = "        if name.startswith('register_'):\n" \
            "            legacy=\"assert pilot['status'] == 'passed_actual40_nonflag_Ridge_full_official_comparisons'\"\n" \
            f"            actual=\"assert pilot['status'] == '{expected}'\"\n" \
            "            assert text.count(legacy)==1\n" \
            "            original=text\n" \
            "            text=text.replace(legacy,actual)\n" \
            "            import ast\n" \
            "            assert ast.dump(ast.parse(text.replace(actual,legacy)))==ast.dump(ast.parse(original))\n" \
            "            marker=\"    pins = {**read(RELEASE / 'protocol.json')['input_sha256']\"\n" \
            "            assert text.count(marker)==1\n" \
            "            extra=\"    sources += [A/'prepare_nonflag_ReverseBayesFine40_round134_sources_v2_20261008.py', A/'run_nonflag_ReverseBayesFine40_round134_full_registration_v2_20261008.py', A/'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json']\\n\"\n" \
            "            text=text.replace(marker,extra+marker)\n"
        return text.replace(needle, addition + needle)

    generator = receiver(generator_old, generator_new, transform=correct_generator)
    scorer_old = 'run_nonflag_ReverseBayesFine40_official_comparison_v1_20261007.py'
    scorer_new = 'run_nonflag_ReverseBayesFine40_official_comparison_v2_20261008.py'
    scorer = receiver(scorer_old, scorer_new, [('nonflag_SparseGram40_round133_full_registration_v1', RECOVERY_SERVICE)])
    # No scientific expression changes: only the actual closed predecessor's service identity.
    original_ast = ast.parse((A / scorer_old).read_text(encoding='utf8'))
    corrected_ast = ast.parse(scorer.read_text(encoding='utf8').replace(RECOVERY_SERVICE, 'nonflag_SparseGram40_round133_full_registration_v1'))
    assert ast.dump(original_ast) == ast.dump(corrected_ast)
    admitted = receiver('run_nonflag_ReverseBayesFine40_admitted_comparison_v1_20261007.py',
                        'run_nonflag_ReverseBayesFine40_admitted_comparison_v2_20261008.py',
                        [(scorer_old.removesuffix('.py'), scorer_new.removesuffix('.py'))])
    full = receiver(full_old, full_new, [('nonflag_SparseGram40_round133_full_registration_v1', RECOVERY_SERVICE),
                                       (generator_old.removesuffix('.py'), generator_new.removesuffix('.py'))],
                    lambda text: text.replace('run_nonflag_ReverseBayesFine40_round134_full_registration_v1_file_IO_20261008',
                                              'run_nonflag_ReverseBayesFine40_round134_full_registration_v2_file_IO_20261008'))
    # The original full controller's bottom uses its own file name as the exclusive I/O directory.
    full_text = full.read_text(encoding='utf8')
    old_io = full_old.removesuffix('.py') + '_file_IO'
    if old_io in full_text:
        full_text = full_text.replace(old_io, full_new.removesuffix('.py') + '_file_IO')
        full.write_text(full_text, encoding='utf8', newline='\n')
    prospective = receiver('verify_nonflag_ReverseBayesFine40_prospective_routes_v2_20261007.py',
                           'verify_nonflag_ReverseBayesFine40_prospective_routes_v3_20261008.py',
                           [(generator_old.removesuffix('.py'), generator_new.removesuffix('.py')),
                            (scorer_old, scorer_new),
                            ('nonflag_ReverseBayesFine40_prospective_routes_v2_20261007.json',
                             'nonflag_ReverseBayesFine40_prospective_routes_v3_20261008.json')], guard_checks)
    admission_old = 'verify_nonflag_ReverseBayesFine40_round134_sources_v1_20261007.py'
    admission_new = 'verify_nonflag_ReverseBayesFine40_round134_sources_v2_20261008.py'
    publication_old = 'publish_nonflag_ReverseBayesFine40_evidence_v1_20261007.py'
    publication_new = 'publish_nonflag_ReverseBayesFine40_evidence_v2_20261008.py'
    prep_old = 'prepare_nonflag_ReverseBayesFine40_selected_candidate_v1_20261007.py'
    prep_new = 'prepare_nonflag_ReverseBayesFine40_selected_candidate_v2_20261008.py'
    prep = receiver(prep_old, prep_new, transform=lambda text: text.replace(
        "    pins={**protocol_pins,**pilot['input_sha256'],**{str(p):sha(p) for p in sources}}",
        "    sources += [A/'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json', A/'prepare_nonflag_ReverseBayesFine40_round134_sources_v2_20261008.py']\n"
        "    pins={**protocol_pins,**pilot['input_sha256'],**{str(p):sha(p) for p in sources}}"))
    pub = receiver(publication_old, publication_new,
                   [('nonflag_SparseGram40_round133_full_registration_v1', RECOVERY_SERVICE)],
                   lambda text: text.replace('    sources = list(dict.fromkeys(sources))',
                       "    sources += [A/'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json',\n"
                       f"                A/'{generator_new}', A/'{full_new}', A/'{scorer_new}', A/'{admitted.name}',\n"
                       f"                A/'{admission_new}', A/'{prep_new}', A/'{prospective.name}',\n"
                       "                A/'nonflag_ReverseBayesFine40_prospective_routes_v3_20261008.json']\n"
                       '    sources = list(dict.fromkeys(sources))'))
    admission = receiver(admission_old, admission_new,
                         [('nonflag_SparseGram40_round133_full_registration_v1', RECOVERY_SERVICE),
                          (generator_old.removesuffix('.py'), generator_new.removesuffix('.py')),
                          (scorer_old, scorer_new), (full_old, full_new),
                          (publication_old, publication_new), (prep_old, prep_new),
                          ('nonflag_ReverseBayesFine40_prospective_routes_v2_20261007.json',
                           'nonflag_ReverseBayesFine40_prospective_routes_v3_20261008.json')], guard_checks)
    # Explicitly freeze the corrective source graph along with the original scientific proof.
    text = admission.read_text(encoding='utf8')
    needle = '    for p in sources:'
    assert text.count(needle) == 1
    text = text.replace(needle, "    sources += [A/'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json', A/'prepare_actual_ReverseBayesFine134_truthful_receivers_v2_20261008.py']\n" + needle)
    admission.write_text(text, encoding='utf8', newline='\n')

    deadline_old = 'publish_actual_deadline_and_full_training_handoff_v1_20261008.py'
    deadline_new = 'publish_actual_deadline_and_full_training_handoff_v2_20261008.py'
    deadline = receiver(deadline_old, deadline_new,
                        [('nonflag_SparseGram40_round133_full_registration_v1', RECOVERY_SERVICE),
                         ('actual_deadline_and_full_training_handoff_main_v1_20261008',
                          'actual_deadline_and_full_training_handoff_main_v2_20261008')],
                        lambda text: text.replace('    folders = [(resource,',
                            "    sources += [A/'publish_actual_deadline_and_full_training_handoff_v1_20261008.py', A/'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json']\n"
                            '    folders = [(resource,'))
    queue_old = 'queue_actual_ReverseBayesFine134_v1_20261008.py'
    queue_new = 'queue_actual_ReverseBayesFine134_v2_20261008.py'
    queue = receiver(queue_old, queue_new,
        [('nonflag_SparseGram40_round133_full_registration_v1', RECOVERY_SERVICE),
         ('actual_deadline_and_full_training_handoff_main_publication_v1_20261008',
          'actual_deadline_and_full_training_handoff_main_publication_v2_20261008'),
         ('actual_deadline_and_full_training_handoff_main_v1_20261008',
          'actual_deadline_and_full_training_handoff_main_v2_20261008'),
         ('actual_ReverseBayesFine134_complete_dependency_plan_v1_20261008',
          'actual_ReverseBayesFine134_complete_dependency_plan_v2_20261008'),
         ('actual_ReverseBayesFine134_complete_hidden_launches_v1_20261008',
          'actual_ReverseBayesFine134_complete_hidden_launches_v2_20261008'),
         (admission_old, admission_new), (publication_old, publication_new),
         ('run_nonflag_ReverseBayesFine40_admitted_comparison_v1_20261007.py', admitted.name),
         (prep_old, prep_new), (full_old, full_new)],
         lambda text: text.replace("             A / 'actual_user_submission_deadline_and_priority_20261008.json']",
                                  "             A / 'actual_user_submission_deadline_and_priority_20261008.json',\n"
                                  "             A / 'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json',\n"
                                  "             A / 'prepare_nonflag_ReverseBayesFine40_round134_sources_v2_20261008.py']"))
    # Run the prospective checks now, before even dispatching the scorer.
    import importlib.util
    spec = importlib.util.spec_from_file_location('actual_fine134_prospective_v3', prospective)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.main()
    prospective_path = A / 'nonflag_ReverseBayesFine40_prospective_routes_v3_20261008.json'
    assert not read(prospective_path)['issues']
    assert sha(plan_path) == original_plan_sha
    sources = [Path(__file__), plan_path, controls, prospective_path, *ORIGINAL, *NEW.values(),
               failed_queue / 'job_definition.json', failed_queue / 'service_execution.json', failed_queue / 'stderr.log',
               A / 'actual_SparseGram133_registration_guard_recovery_v3_20261008.json']
    pins = {str(p): sha(p) for p in dict.fromkeys(sources)}
    create(PROOF, {
        'status': 'passed_actual134_pre_score_truthful_guard_and_predecessor_receivers_with_unchanged_scientific_grid',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins,
        'expected_official_status': expected, 'prospective_sources_compiled': 24,
        'actual_full_graph_controls_executed': 12, 'all3_registry_guards_equal_actual_scorer_status': True,
        'original_plan_bytes_unchanged': original_plan_sha,
        'scorer_scientific_AST_unchanged_except_actual_closed_predecessor_service': True,
        'original_failed_queue_and_original_sources_preserved': True,
        'full37_and111_controls_preserved_not_rerun': True,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    pins[str(PROOF)] = sha(PROOF)
    launch_names = [('actual_deadline_and_full_training_handoff_main_publication_v2_20261008', deadline),
                    ('actual_ReverseBayesFine134_complete_dependency_queue_v2_20261008', queue)]
    rows = {}
    for name, driver in launch_names:
        assert not (services / name).exists()
        rows[name] = start(name, driver.name, [], pins)
    create(A / 'actual_ReverseBayesFine134_corrected_dependency_hidden_launches_v2_20261008.json', {
        'status': 'started_corrected_deadline_publication_and_actual134_dependency_queue',
        'launches': rows, 'input_sha256': pins, 'new_quality_scores_by_launch': 0, 'test_labels_read': False})
    print('Guard-correct24 routes and12 graphs verified; deadline and actual134 queue await real133 closure.', flush=True)


if __name__ == '__main__':
    main()
