"""Admit the byte-verified shared snapshot reader into a fresh, unstarted189 scope."""
from pathlib import Path
import ast, importlib, re, subprocess, sys

A = Path(__file__).resolve().parent
ROOT = A.parent
sys.path[:0] = [str(ROOT), str(A)]
import prepare_MixedObjectiveWindow189_complete149_pipeline_v2_20261011 as previous
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

FACTORY = Path(__file__).stem
PROOF = 'mixed_objective_window189_full_execution_sources_admission_v3_20261011.json'


def next_name(name):
    return name.replace('_v2_20261011', '_v3_20261011') if ('189' in name) else name


NAMES = [next_name(n) for n in previous.NAMES]
EXTRAS = [next_name(n) for n in previous.EXTRAS] + [
    'shared_immutable_board_snapshot_runtime_v2_20261011.py',
    'late_bound_shared_immutable_snapshot_runtime_v1_20261011.py',
    'shared_immutable_snapshot_actual181_payload_controls_v2_20261011.json',
    'shared_immutable_snapshot_actual181_late_import_CPU_controls_v1_20261011.json',
    'shared_immutable_snapshot_compiler_module_context_recovery_v2_20261011.json',
]


def source_paths():
    return list(dict.fromkeys([Path(__file__), A / PROOF, *previous.source_paths(),
                              *[A / n for n in NAMES + EXTRAS]]))


def main():
    import psutil
    from handoff_ready_goss_full_execution_20261006 import retire
    assert allowed()
    controls = read(A / 'shared_immutable_snapshot_actual181_payload_controls_v2_20261011.json')
    assert controls['status'] == 'passed_actual181_snapshot_six_critical_payloads_equal_main_and_scope_restored'
    for p, d in controls['runtime_input_sha256'].items():
        assert sha(p) == d, p
    binding = read(A / 'shared_immutable_snapshot_actual181_late_import_CPU_controls_v1_20261011.json')
    assert binding['status'] == 'passed_actual181_two_late_import_bindings_and_all_scope_restorations_CPU'
    for p, d in binding['input_sha256'].items():
        assert sha(p) == d, p
    old_name = 'MixedObjectiveWindow189_complete149_family_v2_20261011'
    identity = read(A / 'service_owned_workflows_20261006' / old_name / 'native_launch.json')
    assert owned(identity) and not psutil.Process(identity['owned_worker_pid']).children()
    stack = subprocess.run([str(ROOT / 'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),
                            'dump', '--pid', str(identity['owned_worker_pid'])],
                           capture_output=True, text=True, encoding='utf8', check=True).stdout
    assert '(idle)' in stack and 'closed' in stack
    storage = importlib.import_module('mixed_objective_window189_storage_v2_20261011')
    assert len(storage.OUTPUTS) == 6
    assert all(not p.exists() and not q.exists() for p, q in storage.OUTPUTS.items())
    mapping = {old: next_name(old) for old in previous.NAMES + previous.EXTRAS[2:11]}
    mapping[previous.FACTORY + '.py'] = FACTORY + '.py'
    mapping.update({Path(old).stem: Path(new).stem for old, new in list(mapping.items()) if old.endswith('.py')})
    pattern = re.compile('|'.join(re.escape(k) for k in sorted(mapping, key=len, reverse=True)))
    inputs = [A / n for n in previous.NAMES + previous.EXTRAS[2:9]]
    outputs = []
    for source in inputs:
        text = pattern.sub(lambda m: mapping[m.group()], source.read_text(encoding='utf8'))
        if source.name == previous.EXTRAS[6]:
            lines = text.splitlines()
            matches = [i for i, line in enumerate(lines) if line.startswith('    with external_capsules(')]
            assert len(matches) == 1
            index = matches[0]
            assert lines[index].endswith(':')
            lines[index] = lines[index][:-1] + ",shared(receiver,'" + Path(NAMES[1]).stem + "',Path('E:/赛题五_本机临时/第189轮_20261010/late_shared_snapshot_import_v3.json')):"
            lines.insert(index, '    from late_bound_shared_immutable_snapshot_runtime_v1_20261011 import installed as shared')
            text = '\n'.join(lines) + '\n'
        target = A / next_name(source.name)
        assert not target.exists(), target
        compile(text, str(target), 'exec')
        target.write_text(text, encoding='utf8', newline='\n')
        outputs.append(target)
    for old, new in zip(previous.NAMES[2:4], NAMES[2:4]):
        canonical = A / re.sub(r'_v3_20261011(?=\.py$)', '', new)
        functions = lambda p: [ast.dump(n, include_attributes=False) for n in ast.parse(p.read_text(encoding='utf8')).body if isinstance(n, ast.FunctionDef)]
        assert functions(canonical) == functions(A / new), ('canonical functional alias', canonical)
    opt = importlib.import_module(Path(NAMES[2]).stem)
    assert (opt.NUMBER, opt.PREVIOUS_NUMBER, opt.WAVES) == (189, 188, (472,))
    assert '(189, 100, 149)' in (A / NAMES[-1]).read_text(encoding='utf8')
    for source in outputs:
        for node in ast.walk(ast.parse(source.read_text(encoding='utf8'))):
            if isinstance(node, ast.ImportFrom) and node.module and ('189' in node.module):
                assert (A / (node.module + '.py')).is_file(), (source, node.module)
    pins = {str(p): sha(p) for p in [Path(__file__), *inputs, *outputs,
                                    *[A / n for n in EXTRAS if n not in EXTRAS[9:11]]]} 
    for name in EXTRAS[9:11]:
        create(A / name, {'status': 'compiled_exact149_QA100_sources_and_byte_verified_shared_snapshot_before_future',
                         'input_sha256': pins, 'expected_records': 149, 'expected_full_board': 17687,
                         'parent_rounds': [175, 188], 'new_quality_scores': 0,
                         'actual_future_X_read': False, 'test_labels_read': False})
    create(A / PROOF, {'status': 'compiled_complete149_QA100_with_actual181_byte_verified_shared_snapshot',
                      'input_sha256': pins, 'expected_records': 149, 'expected_full_board': 17687,
                      'shared_snapshot_six_payloads_equal_verified_main': True,
                      'actual_two_late_import_bindings_CPU_passed': True,
                      'actual189_future_and_full_QA_still_pending': True,
                      'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False})
    assert all(p.is_file() for p in source_paths())
    assert all(not p.exists() and not q.exists() for p, q in storage.OUTPUTS.items())
    assert owned(identity) and not psutil.Process(identity['owned_worker_pid']).children()
    create(A / 'mixed189_shared_snapshot_before_science_recovery_v3_20261011.json', {
        'status': 'verified_idle_v2_before_any189_scientific_outputs_and_admitted_shared_snapshot_v3',
        'original_identity': identity, 'idle_stack': stack,
        'original_v2_sources_preserved': True, 'active_prior_scientific_jobs_modified': False,
        'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False})
    assert allowed()
    retire(identity, 'Replace exact idle189 family with separately byte-verified shared snapshot scope; no189 scientific outputs exist')
    assert allowed()
    name = 'MixedObjectiveWindow189_complete149_family_v3_20261011'
    row = start_service(name, EXTRAS[5], [], {str(A / EXTRAS[5]): sha(A / EXTRAS[5]), str(A / PROOF): sha(A / PROOF)})
    create(A / (name + '_activation.json'), row)
    print({'actual189_shared_snapshot_v3_queued': owned(row), 'worker_pid': row['owned_worker_pid'],
           'new_scores': 0, 'selected149_future_qualification_pending': True}, flush=True)


if __name__ == '__main__':
    main()
