"""Exercise the real binding scope on an isolated E fixture; never call model QA."""
from pathlib import Path
import sys, json, time, builtins
A = Path(__file__).resolve().parent; sys.path[:0] = [str(A.parent), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed, closed

def run_variant(row):
    assert allowed()
    closed('actual_shared_live_ranking_report180_reader_controls_v1_20261011')
    import shared_live_ranking_report_runtime_v2_20261011 as runtime
    import build_all_model_rankings_20261003 as ranking
    import importlib
    codec=importlib.import_module(row['codec_name'])
    verifier=importlib.import_module(row['verifier_name'])
    from exact_native_pretty_JSON_archive_20261007 import pieces
    sandbox = Path('E:/赛题五_本机临时/共享榜对象精确15作用域控制_v2_20261011')/str(row['number'])
    assert not sandbox.exists(); sandbox.mkdir(parents=True)
    fixture = sandbox/'report.json'
    other = sandbox/'ordinary.json'; other.write_text('{"unchanged":true}', encoding='utf8')
    shared = {'nested': [1, 2, 0., -0., 1e-7, '中文', None, False]}
    report = {'connected': [shared, shared], 'empty': [], 'other': {'x': shared}}
    def original_writer(path, value):
        with Path(path).open('wb') as stream:
            for b in pieces(value): stream.write(b)
    namespace = {'write_exact_report': original_writer}
    exec('def run_variant(row): pass', namespace)
    original_main = ranking.main
    original_read, original_json = Path.read_text, codec.json
    original_exec = verifier.__dict__.get('exec')
    old_a, old_report = runtime.A, runtime.REPORT
    ranking.main = namespace['main']; runtime.A, runtime.REPORT = sandbox, fixture
    try:
        with runtime.installed(row['number'],row['codec_name'],row['verifier_name']) as state:
            namespace['write_exact_report'](fixture, report)
            assert codec.json.loads(fixture.read_text(encoding='utf-8')) is report
            assert codec.json.loads(other.read_text(encoding='utf8')) == {'unchanged': True}
            assert codec.json.loads('{"ordinary":[1,2]}') == {'ordinary': [1,2]}
            qa_scope = {'__name__': 'actual_lossless_ranking_QA'}
            verifier.exec(compile('import json\ndef run_variant(row): return json.loads(TEXT)', '<isolated-reader-control>', 'exec'), qa_scope)
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
    fixture_receipt = sandbox/f"shared_live_ranking_report_round{row['number']}_execution_v1_20261011.json"
    assert read(fixture_receipt)['shared_reads'] == 2
    return {'variant':row,'execution':str(fixture_receipt),'execution_sha256':sha(fixture_receipt)}

def main():
    assert allowed()
    path=A/'shared_live_report_exact15_variants_admission_v2_20261011.json'
    proof=read(path)
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    results=[run_variant(row) for row in proof['variants']]
    assert len(results)==15
    pins={**proof['input_sha256'],str(path):sha(path),str(Path(__file__)):sha(__file__)}
    pins.update({r['execution']:r['execution_sha256'] for r in results})
    create(A/'shared_live_report_exact15_scope_controls_v2_20261011.json',
      {'status':'passed_actual_all15_exact_codec_QA_namespace_scope_and_restoration_controls',
       'input_sha256':pins,'variants':proof['variants'],'actual_scope_results':results,
       'full180_original_native_bytes_proof':str(A/'shared_live_ranking_report_actual180_controls_v1_20261011.json'),
       'actual_scientific_rounds_not_executed_by_fixture':True,'new_fits':0,'new_scores':0,'test_labels_read':False})
    print({'actual_exact15_scopes_and_restorations_passed':True},flush=True)

if __name__=='__main__':main()
