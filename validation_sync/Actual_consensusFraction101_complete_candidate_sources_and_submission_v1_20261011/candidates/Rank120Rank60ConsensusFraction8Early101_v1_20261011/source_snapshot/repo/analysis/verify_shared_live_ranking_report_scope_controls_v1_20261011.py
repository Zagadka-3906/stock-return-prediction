"""Exercise the real binding scope on an isolated E fixture; never call model QA."""
from pathlib import Path
import sys, json, time, builtins
A = Path(__file__).resolve().parent; sys.path[:0] = [str(A.parent), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed, closed

def main():
    assert allowed()
    closed('actual_shared_live_ranking_report180_reader_controls_v1_20261011')
    import shared_live_ranking_report_runtime_v1_20261011 as runtime
    import build_all_model_rankings_20261003 as ranking
    import build_lossless_ranking_display_round187_v2_20261011 as codec
    import verify_lossless_ranking_display_round187_v2_20261011 as verifier
    from exact_native_pretty_JSON_archive_20261007 import pieces
    sandbox = Path('E:/赛题五_本机临时/共享榜对象作用域控制_v1_20261011')
    assert not sandbox.exists(); sandbox.mkdir()
    fixture = sandbox/'report.json'
    other = sandbox/'ordinary.json'; other.write_text('{"unchanged":true}', encoding='utf8')
    shared = {'nested': [1, 2, 0., -0., 1e-7, '中文', None, False]}
    report = {'connected': [shared, shared], 'empty': [], 'other': {'x': shared}}
    def original_writer(path, value):
        with Path(path).open('wb') as stream:
            for b in pieces(value): stream.write(b)
    namespace = {'write_exact_report': original_writer}
    exec('def main(): pass', namespace)
    original_main = ranking.main
    original_read, original_json = Path.read_text, codec.json
    original_exec = verifier.__dict__.get('exec')
    old_a, old_report = runtime.A, runtime.REPORT
    ranking.main = namespace['main']; runtime.A, runtime.REPORT = sandbox, fixture
    try:
        with runtime.installed(187) as state:
            namespace['write_exact_report'](fixture, report)
            assert codec.json.loads(fixture.read_text(encoding='utf-8')) is report
            assert codec.json.loads(other.read_text(encoding='utf8')) == {'unchanged': True}
            assert codec.json.loads('{"ordinary":[1,2]}') == {'ordinary': [1,2]}
            qa_scope = {'__name__': 'actual_lossless_ranking_QA'}
            verifier.exec(compile('import json\ndef main(): return json.loads(TEXT)', '<isolated-reader-control>', 'exec'), qa_scope)
            qa_scope['TEXT'] = fixture.read_text(encoding='utf-8')
            assert qa_scope['main']() is report
            assert state['shared_reads'] == 2 and state['captures'] == 1
        assert Path.read_text is original_read and codec.json is original_json
        assert verifier.__dict__.get('exec') is original_exec
        assert namespace['write_exact_report'] is original_writer and qa_scope['json'] is json
        assert json.loads(fixture.read_text(encoding='utf-8')) == report
    finally:
        ranking.main = original_main; runtime.A, runtime.REPORT = old_a, old_report
    assert ranking.main is original_main
    fixture_receipt = sandbox/'shared_live_ranking_report_round187_execution_v1_20261011.json'
    assert read(fixture_receipt)['shared_reads'] == 2
    pins = {str(p): sha(p) for p in [Path(__file__), Path(runtime.__file__), runtime.PROOF, fixture, other, fixture_receipt]}
    create(A/'shared_live_ranking_report_scope_controls_v1_20261011.json',
        {'status': 'passed_actual_installed_scope_small_E_fixture_bindings_and_restoration',
         'input_sha256': pins, 'actual_capture_and_private_codec_and_executed_QA_namespace_reads': True,
         'all_runtime_bindings_restored': True, 'full180_native_control': str(runtime.PROOF),
         'actual_scientific_round187_not_executed': True, 'runtime_not_yet_adopted': True,
         'new_fits': 0, 'new_scores': 0, 'test_labels_read': False})
    print({'status': 'passed_actual_installed_shared_report_scope_controls'}, flush=True)

if __name__ == '__main__': main()
