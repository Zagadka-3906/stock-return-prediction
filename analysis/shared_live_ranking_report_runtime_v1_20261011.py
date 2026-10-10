"""Reuse a byte-proven live report only in codec and original QA namespaces."""
from pathlib import Path
from contextlib import contextmanager
import builtins, hashlib, json, math

A = Path(__file__).resolve().parent
REPORT = A.parent / 'results/all_model_rankings_20261003.json'
PROOF = A / 'shared_live_ranking_report_actual180_controls_v1_20261011.json'

def validate_json_tree(value):
    seen, active = set(), set()
    def visit(x):
        t = type(x)
        if t in (str, int, bool, type(None)): return
        if t is float:
            assert math.isfinite(x); return
        assert t in (dict, list), t
        identity = id(x)
        assert identity not in active, 'JSON graph must be acyclic'
        if identity in seen: return
        active.add(identity)
        if t is dict:
            for k, v in x.items():
                assert type(k) is str; visit(v)
        else:
            for v in x: visit(v)
        active.remove(identity); seen.add(identity)
    visit(value)
    return len(seen)

def native_digest(report):
    from exact_native_pretty_JSON_archive_20261007 import pieces
    h, count = hashlib.sha256(), 0
    for block in pieces(report): h.update(block); count += len(block)
    return h.hexdigest(), count

class ReportText:
    def __init__(self, state): self.state = state

class JsonProxy:
    def __init__(self, original): self.original = original
    def __getattr__(self, name): return getattr(self.original, name)
    def loads(self, value, *args, **kwargs):
        if isinstance(value, ReportText):
            assert not args and not kwargs
            state = value.state
            assert state['report'] is not None
            state['shared_reads'] += 1
            return state['report']
        return self.original.loads(value, *args, **kwargs)

@contextmanager
def installed(number):
    from run_dependency_queue_v3_20261006 import read, sha, create
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    proof = read(PROOF)
    assert proof['status'] == 'passed_actual180_native_bytes_typed_graph_and_private_reader_controls'
    for p, d in proof['input_sha256'].items(): assert sha(p) == d, p
    import importlib
    import build_all_model_rankings_20261003 as ranking
    codec = importlib.import_module(f'build_lossless_ranking_display_round{number}_v2_20261011')
    verifier = importlib.import_module(f'verify_lossless_ranking_display_round{number}_v2_20261011')
    namespace = ranking.main.__globals__
    assert 'write_exact_report' in namespace, 'Install inside verified byte exact writer scope'
    original_writer = namespace['write_exact_report']
    original_read = Path.read_text
    original_json = codec.json
    original_exec = verifier.__dict__.get('exec', None)
    execute = original_exec or builtins.exec
    state = {'report': None, 'shared_reads': 0, 'captures': 0}
    qa_restores = []
    def writer(path, report):
        assert Path(path).resolve() == REPORT.resolve()
        validate_json_tree(report)
        result = original_writer(path, report)
        digest, count = native_digest(report)
        assert sha(REPORT) == digest, 'Live graph must equal actual native output bytes'
        state.update(report=report, native_sha256=digest, native_bytes=count)
        state['captures'] += 1
        return result
    def read_text(path, *args, **kwargs):
        if Path(path).resolve() == REPORT.resolve() and state['report'] is not None:
            assert not args and kwargs == {'encoding': 'utf-8'}
            assert sha(REPORT) == state['native_sha256']
            return ReportText(state)
        return original_read(path, *args, **kwargs)
    def execute_qa(code, scope, *args, **kwargs):
        result = execute(code, scope, *args, **kwargs)
        assert scope['__name__'] == 'actual_lossless_ranking_QA'
        original = scope['json']; proxy = JsonProxy(original)
        scope['json'] = proxy; qa_restores.append((scope, original, proxy))
        return result
    proxy = JsonProxy(original_json)
    namespace['write_exact_report'] = writer
    Path.read_text = read_text; codec.json = proxy; verifier.exec = execute_qa
    try:
        yield state
    finally:
        assert namespace['write_exact_report'] is writer and Path.read_text is read_text
        assert codec.json is proxy and verifier.exec is execute_qa
        namespace['write_exact_report'] = original_writer; Path.read_text = original_read
        codec.json = original_json
        if original_exec is None: del verifier.exec
        else: verifier.exec = original_exec
        for scope, original, replacement in reversed(qa_restores):
            assert scope['json'] is replacement; scope['json'] = original
        if state['report'] is not None:
            assert native_digest(state['report']) == (state['native_sha256'], state['native_bytes'])
            assert sha(REPORT) == state['native_sha256']
            create(A / f'shared_live_ranking_report_round{number}_execution_v1_20261011.json',
                {'status': 'passed_actual_native_graph_capture_and_private_codec_QA_reader_restored',
                 'native_sha256': state['native_sha256'], 'native_bytes': state['native_bytes'],
                 'captures': state['captures'], 'shared_reads': state['shared_reads'],
                 'all_original_codec_and_QA_assertions_retained': True,
                 'new_fits': 0, 'new_scores': 0, 'test_labels_read': False})
