"""Run the actual181 generated snapshot with a scoped low-memory board loader.

Compare six scientific/ranking payloads against their immutable main commit.
Do not run a publisher main, write its worktree, or rescore any candidate.
"""
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime
import ast, hashlib, os, sys, time

A = Path(__file__).resolve().parent
ROOT = A.parent
sys.path[:0] = [str(ROOT), str(A)]
OUT = Path('E:/赛题五_本机临时/shared_immutable_snapshot_actual181_payload_controls_v1_20261011')


def main():
    from run_dependency_queue_v3_20261006 import read, sha, create
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    import psutil
    assert allowed()
    OUT.mkdir(exist_ok=False)
    scratch = OUT / 'tmp'
    scratch.mkdir()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        os.environ[key] = str(scratch)
    import tempfile
    tempfile.tempdir = str(scratch)
    while psutil.virtual_memory().available < 6 * 2**30:
        assert allowed()
        time.sleep(10)
    import publish_classifier_consensus_workflows_20261006 as helpers
    from byte_exact_publication_encoder_runtime_v1_20261010 import installed as encode
    from byte_exact_dynamic_snapshot_encoder_runtime_v1_20261010 import installed as bind
    from shared_immutable_board_snapshot_runtime_v1_20261011 import installed as shared
    source = A / 'publish_StockRankWide32Embedding181_round181_full_validation_v4_20261010.py'
    tree = ast.parse(source.read_text(encoding='utf8'))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    start = next(i for i, n in enumerate(function.body) if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'source' for t in n.targets))
    stop = next(i for i, n in enumerate(function.body) if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name)
                        and t.value.id == 'namespace' and isinstance(t.slice, ast.Constant)
                        and t.slice.value == 'PUBLICATION_FULL_REPORT' for t in n.targets)) + 1
    prefix = ast.Module(body=function.body[start:stop], type_ignores=[])
    compiled = compile(ast.fix_missing_locations(prefix), str(source), 'exec')
    receipt_path = A / 'github_validation_sync_main_20261005/round181_receipt.json'
    receipt = read(receipt_path)
    assert receipt['status'] == 'pushed_and_remote_head_verified'
    runtime_inputs = [Path(__file__), source,
        A / 'shared_immutable_board_snapshot_runtime_v1_20261011.py',
        A / 'shared_immutable_ranking_loader_actual_complete180_benchmark_v1_20261011.json',
        A / 'byte_exact_dynamic_snapshot_encoder_runtime_v1_20261010.py',
        A / 'byte_exact_publication_encoder_runtime_v1_20261010.py',
        A / 'sync_validated_rounds_main_20261005.py', receipt_path]
    pins = {str(p): sha(p) for p in runtime_inputs}
    create(OUT / 'frozen_before_actual_payload_controls.json', {
        'runtime_input_sha256': pins, 'main_commit': receipt['commit'],
        'actual_round': 181, 'new_quality_scores': 0,
        'publication_main_not_invoked': True, 'test_labels_read': False,
    })
    proxy = SimpleNamespace()
    previous_encoder = helpers.sync.encoded
    started = time.perf_counter()
    with encode(), bind(proxy, OUT / 'encoder_scope.json'), shared(proxy, OUT / 'shared_scope.json', controls_only=True):
        outer = {'A': A, 'ROOT': ROOT, 'sync': helpers.sync, 'Path': Path, 'exec': proxy.exec}
        exec(compiled, outer)
        namespace = outer['namespace']
        manifest, payload = namespace['snapshot'](181)
        names = [f'validation_sync/round181/{name}' for name in (
            'ranking_all.csv', 'ranking_metadata.json', 'selected_scheme.json',
            'ranking_round.csv', 'all_round_configurations.json.gz')]
        names.append('validation_sync/latest.json')
        expected = {n: hashlib.sha256(payload[n]).hexdigest() for n in names}
        actual = helpers.blob_hashes(receipt['commit'], expected)
        assert actual == expected, {n: (actual.get(n), expected[n]) for n in names if actual.get(n) != expected[n]}
        assert manifest['connected_records'] == 17110 and manifest['scored_records'] == 48
        assert manifest['original_full_ranking_sha256'] == read(A / 'lossless_ranking_display_v2_20261006/round181/verification.json')['original_report_sha256']
        memory = psutil.Process().memory_info()
    assert helpers.sync.encoded is previous_encoder
    assert 'exec' not in vars(proxy)
    for path, expected_hash in pins.items():
        assert sha(path) == expected_hash, path
    assert allowed()
    result = {
        'status': 'passed_actual181_snapshot_six_critical_payloads_equal_main_and_scope_restored',
        'at_local': datetime.now().isoformat(), 'runtime_input_sha256': pins,
        'actual_round': 181, 'main_commit': receipt['commit'],
        'actual_checked_payload_sha256': actual,
        'connected_records': 17110, 'scored_records': 48,
        'actual_snapshot_seconds': time.perf_counter() - started,
        'actual_snapshot_retained_RSS_bytes': memory.rss,
        'actual_snapshot_retained_private_bytes': getattr(memory, 'private', None),
        'original_generated_function_code_signature_verified': True,
        'all_original_scientific_and_snapshot_assertions_retained': True,
        'scoped_exec_snapshot_and_encoder_restored': True,
        'worktree_or_main_modified': False,
        'production_runtime_adoption_not_performed': True,
        'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False,
    }
    create(OUT / 'verification.json', result)
    create(A / 'shared_immutable_snapshot_actual181_payload_controls_v1_20261011.json', result)
    print({k: result[k] for k in ('status', 'actual_snapshot_seconds', 'actual_snapshot_retained_RSS_bytes')}, flush=True)


if __name__ == '__main__':
    main()
