"""Replace only the large immutable-board decode in a private publication scope."""
from contextlib import contextmanager
from pathlib import Path
import ast, builtins, gc, gzip, hashlib, json, re, types

A = Path(__file__).resolve().parent
ROOT = A.parent
CONTROL = A / 'shared_immutable_snapshot_actual181_payload_controls_v2_20261011.json'


def signature(code):
    return (code.co_code, code.co_names, code.co_varnames, code.co_argcount,
            code.co_kwonlyargcount, code.co_flags, code.co_freevars, code.co_cellvars,
            tuple(signature(c) if isinstance(c, types.CodeType) else c for c in code.co_consts))


def archive_digest(path, expected):
    with gzip.open(path, 'rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    assert actual == expected, path
    return True


def load(number, archive_path):
    from run_dependency_queue_v3_20261006 import read, sha
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    from build_lossless_ranking_display_v2_20261006 import unpack_report
    display = A / 'lossless_ranking_display_v2_20261006' / f'round{number}'
    page = display / 'complete_rankings_lossless.html'
    proof_path = display / 'verification.json'
    archive_proof = display / 'full_report_publication_snapshot_verification.json'
    proof, archive = read(proof_path), read(archive_proof)
    assert proof['status'] == 'passed_all_original_report_values_and_six_views_lossless_roundtrip'
    assert archive['status'] == 'passed_exact_original_full_report_bytes_from_immutable_lossless_HTML'
    assert proof['original_report_sha256'] == archive['original_report_sha256']
    assert Path(archive_path).resolve() == (display / 'full_report_reconstructed_for_publication.json.gz').resolve()
    assert sha(archive_path) == archive['compressed_snapshot_sha256']
    assert sha(page) == proof['lossless_HTML_sha256']
    codec = A / 'build_lossless_ranking_display_v2_20261006.py'
    assert archive['input_sha256'][str(codec.resolve())] == sha(codec)
    pins = {str(p): sha(p) for p in (page, proof_path, archive_proof, codec, Path(archive_path))}
    with LockedReadHashCache(pins) as scope:
        text = page.read_text(encoding='utf8')
        match = re.search(r'<script\s+id="data"\s+type="application/json">(.*?)</script>', text, re.S)
        assert match is not None
        packed = json.loads(match.group(1))
        report = unpack_report(packed)
        assert len(report['connected']) == proof['connected_records'] == archive['connected_records']
        assert report['summary']['connected_exact_records'] == proof['connected_records']
        del text, match, packed
        gc.collect()
        scope.reverify()
    return report, archive['original_report_sha256']


def transformed_snapshot(original):
    """Verify the exact original generated function before applying four decode changes."""
    source = A / 'sync_validated_rounds_main_20261005.py'
    text = source.read_text(encoding='utf8')
    qa = [c for c in original.__code__.co_consts if isinstance(c, str)
          and c.startswith('analysis/lossless_ranking_display_qa_')
          and c.endswith('/qa/interaction_result.json')]
    assert len(qa) == 1, qa
    patches = {
        'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
        "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'": 'ROOT / ' + repr(qa[0]),
        'assert sha(board_path.read_bytes()) == board_sha': 'assert sha(gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())) == board_sha',
        "        assert len(data) < 5 * 1024**2, f'Unexpected large review artifact: {source}'":
            "        raw_digest = sha(data)\n        if len(data) >= 5 * 1024**2:\n            data = gzip.compress(data, mtime=0)\n            destination = Path(str(destination) + '.gz')\n            assert sha(gzip.decompress(data)) == raw_digest",
        "bindings[str(source.relative_to(ROOT)).replace('\\\\', '/')] = sha(data)":
            "bindings[str(source.relative_to(ROOT)).replace('\\\\', '/')] = raw_digest",
    }
    for before, after in patches.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    tree = ast.parse(text)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'snapshot')
    before = ast.get_source_segment(text, node)
    reference = next(c for c in compile(text, str(source), 'exec').co_consts
                     if isinstance(c, types.CodeType) and c.co_name == 'snapshot')
    assert signature(reference) == signature(original.__code__), 'generated snapshot differs from admitted publisher'
    changes = {
        '    board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())\n    board = json.loads(board_bytes.decode(\'utf-8-sig\'))':
            '    board, board_sha = SHARED_IMMUTABLE_BOARD_LOAD(number, PUBLICATION_FULL_REPORT)',
        '    board_sha = sha(board_bytes)\n    del board_bytes':
            '    # Shared loader returns the byte-verified original immutable report SHA.',
        '    assert sha(gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())) == board_sha':
            '    assert SHARED_IMMUTABLE_ARCHIVE_DIGEST(PUBLICATION_FULL_REPORT, board_sha)',
    }
    after = before
    for old, new in changes.items():
        assert after.count(old) == 1, old
        after = after.replace(old, new)
    assert text.count(before) == 1
    replaced_module = text.replace(before, after)
    replacement_code = next(c for c in compile(replaced_module, str(source), 'exec').co_consts
                            if isinstance(c, types.CodeType) and c.co_name == 'snapshot')
    return source, before, after, changes, replacement_code


@contextmanager
def installed(publisher, log, *, controls_only=False):
    from run_dependency_queue_v3_20261006 import read, sha, create
    benchmark = read(A / 'shared_immutable_ranking_loader_actual_complete180_benchmark_v1_20261011.json')
    assert benchmark['status'] == 'passed_actual_complete180_shared_loader_all_native_bytes_exact'
    assert benchmark['eligible_for_separately_verified_runtime_adoption']
    for path, expected in benchmark['input_sha256'].items():
        assert sha(path) == expected, path
    if not controls_only:
        proof = read(CONTROL)
        assert proof['status'] == 'passed_actual181_snapshot_six_critical_payloads_equal_main_and_scope_restored'
        for path, expected in proof['runtime_input_sha256'].items():
            assert sha(path) == expected, path
    absent = object()
    previous = publisher.__dict__.get('exec', absent)
    delegate = builtins.exec if previous is absent else previous
    events, bindings = [], []
    def execute(code, namespace, *args, **kwargs):
        result = delegate(code, namespace, *args, **kwargs)
        original = namespace['snapshot']
        source, before, after, changes, replacement_code = transformed_snapshot(original)
        namespace.update(SHARED_IMMUTABLE_BOARD_LOAD=load, SHARED_IMMUTABLE_ARCHIVE_DIGEST=archive_digest)
        replacement = types.FunctionType(replacement_code, namespace, 'snapshot', original.__defaults__)
        replacement.__kwdefaults__ = original.__kwdefaults__
        replacement.__annotations__ = original.__annotations__
        namespace['snapshot'] = replacement
        bindings.append((namespace, original, replacement))
        events.append({'original_generated_snapshot_code_verified': True,
                       'before_source_sha256': hashlib.sha256(before.encode()).hexdigest(),
                       'after_source_sha256': hashlib.sha256(after.encode()).hexdigest(),
                       'only_changes': changes, 'all_original_snapshot_assertions_preserved': True})
        return result
    publisher.exec = execute
    try:
        yield events
    finally:
        assert publisher.exec is execute
        if previous is absent:
            del publisher.exec
        else:
            publisher.exec = previous
        for namespace, original, replacement in reversed(bindings):
            assert namespace['snapshot'] is replacement
            namespace['snapshot'] = original
            del namespace['SHARED_IMMUTABLE_BOARD_LOAD'], namespace['SHARED_IMMUTABLE_ARCHIVE_DIGEST']
        create(Path(log), {'status': 'shared_immutable_snapshot_scope_restored', 'events': events,
                           'controls_only': controls_only, 'new_quality_scores': 0,
                           'new_native_fits': 0, 'test_labels_read': False})
