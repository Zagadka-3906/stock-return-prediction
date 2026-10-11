"""Verify actual publisher import order and restoration without running its main."""
from pathlib import Path
from types import SimpleNamespace
import ast, sys

A = Path(__file__).resolve().parent
ROOT = A.parent
sys.path[:0] = [str(ROOT), str(A)]


def main():
    from run_dependency_queue_v3_20261006 import read, sha, create
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    from byte_exact_publication_encoder_runtime_v1_20261010 import installed as encode
    from late_bound_dynamic_snapshot_encoder_runtime_v1_20261010 import installed as late_encoder
    from late_bound_shared_immutable_snapshot_runtime_v1_20261011 import installed as late_shared
    from shared_immutable_board_snapshot_runtime_v2_20261011 import load, archive_digest
    import publish_classifier_consensus_workflows_20261006 as helpers
    assert allowed()
    out = Path('E:/赛题五_本机临时/shared_snapshot_actual_late_import_CPU_v1_20261011')
    out.mkdir(exist_ok=False)
    module_name = 'publish_StockRankWide32Embedding181_round181_full_validation_v4_20261010'
    source = A / (module_name + '.py')
    function = next(n for n in ast.parse(source.read_text(encoding='utf8')).body
                    if isinstance(n, ast.FunctionDef) and n.name == 'main')
    start = next(i for i, n in enumerate(function.body) if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'source' for t in n.targets))
    stop = next(i for i, n in enumerate(function.body) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name)
                        and t.value.id == 'namespace' and isinstance(t.slice, ast.Constant)
                        and t.slice.value == 'PUBLICATION_FULL_REPORT' for t in n.targets)) + 1
    prefix = compile(ast.fix_missing_locations(ast.Module(body=function.body[start:stop], type_ignores=[])), str(source), 'exec')
    captured = {}
    def run_prefix():
        import publish_StockRankWide32Embedding181_round181_full_validation_v4_20261010 as publisher
        outer = {'A': A, 'ROOT': ROOT, 'sync': helpers.sync, 'Path': Path, 'exec': publisher.exec}
        exec(prefix, outer)
        namespace = outer['namespace']
        assert namespace['SHARED_IMMUTABLE_BOARD_LOAD'] is load
        assert namespace['SHARED_IMMUTABLE_ARCHIVE_DIGEST'] is archive_digest
        assert namespace['encoded'] is helpers.sync.encoded
        captured.update(namespace=namespace, publisher=publisher)
    receiver = SimpleNamespace(main=run_prefix)
    previous_encoder = helpers.sync.encoded
    with encode(), late_encoder(receiver, module_name, out / 'late_encoder.json') as encoded_events, late_shared(receiver, module_name, out / 'late_shared.json') as shared_events:
        receiver.main()
        assert len(encoded_events) == len(shared_events) == 1
    assert receiver.main is run_prefix
    assert helpers.sync.encoded is previous_encoder
    assert 'exec' not in vars(captured['publisher'])
    assert 'SHARED_IMMUTABLE_BOARD_LOAD' not in captured['namespace']
    assert 'SHARED_IMMUTABLE_ARCHIVE_DIGEST' not in captured['namespace']
    scope = read(out / 'shared_snapshot_scope_execution.json')
    assert scope['status'] == 'shared_immutable_snapshot_scope_restored'
    assert len(scope['events']) == 1 and scope['events'][0]['original_generated_snapshot_code_verified']
    paths = [Path(__file__), source,
             A / 'late_bound_shared_immutable_snapshot_runtime_v1_20261011.py',
             A / 'shared_immutable_board_snapshot_runtime_v2_20261011.py',
             A / 'shared_immutable_snapshot_actual181_payload_controls_v2_20261011.json']
    proof = {'status': 'passed_actual181_two_late_import_bindings_and_all_scope_restorations_CPU',
             'input_sha256': {str(p): sha(p) for p in paths},
             'actual_encoder_import_bindings': 1, 'actual_shared_import_bindings': 1,
             'publisher_main_invoked': False, 'new_native_fits': 0, 'new_quality_scores': 0,
             'all_original_snapshot_code_signature_verified': True,
             'entire_payload_equivalence_proven_separately_by_actual181_controls_v2': True,
             'test_labels_read': False}
    assert allowed()
    create(A / 'shared_immutable_snapshot_actual181_late_import_CPU_controls_v1_20261011.json', proof)
    print({'actual_two_late_import_bindings_and_restoration': 'passed'}, flush=True)


if __name__ == '__main__':
    main()
