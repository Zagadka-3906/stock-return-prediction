"""Scope byte-proven original HTML streaming inside the unchanged native JSON writer."""
from pathlib import Path
from contextlib import contextmanager
import bounded_original_ranking_HTML_writer_v1_20261011 as writer

def patched_source(text):
    pretty=[
        '    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+"\\n", encoding="utf-8")',
        '        output_json.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+"\\n",encoding="utf-8")']
    for old in pretty:
        assert text.count(old)==1
        text=text.replace(old,old[:len(old)-len(old.lstrip())]+'write_exact_report(output_json,report)')
    embedding=[
        '    embedded = json.dumps(report, ensure_ascii=False, separators=(",", ":"), allow_nan=False).replace("</", "<\\\\/")',
        '        embedded=json.dumps(report,ensure_ascii=False,separators=(",",":"),allow_nan=False).replace("</","<\\\\/")']
    for old in embedding:
        assert text.count(old)==1,repr(old)
        text=text.replace(old,old[:len(old)-len(old.lstrip())]+'embedded=None')
    page='''    page=(PAGE.replace("__DATA__",embedded).replace("__PROVENANCE_BANNER__",banner).replace("__REPORT_DATE__",datetime.now().strftime('%Y-%m-%d %H:%M'))
          .replace("__VALIDATION_BEST__",f"{valid_best:.9f}").replace("__CONNECTED_COUNT__",f"{len(connected):,}"))
    output_html.write_text(page, encoding="utf-8")'''
    assert text.count(page)==1
    return text.replace(page,"    write_bounded_original_html(output_html,PAGE,report,banner,datetime.now().strftime('%Y-%m-%d %H:%M'),valid_best,len(connected))")

@contextmanager
def installed():
    from run_dependency_queue_v3_20261006 import read,sha
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    A=Path(__file__).resolve().parent
    location=read(A/'actual_bounded_original_ranking_HTML_full180_location_v1_20261011.json')
    proof=read(Path(location['output'])/'verification.json')
    assert proof['status']=='passed_actual_complete180_original_HTML_full_tree_encoder_vs_bounded_row_encoder_bytes_exact'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    import build_all_model_rankings_20261003 as ranking
    old=ranking.main
    assert 'write_exact_report' in old.__globals__
    source=Path(ranking.__file__);namespace=dict(old.__globals__)
    namespace.update(__name__='byte_exact_bounded_original_ranking_HTML',write_bounded_original_html=writer.write)
    exec(compile(patched_source(source.read_text(encoding='utf-8')),str(source),'exec'),namespace)
    ranking.main=namespace['main']
    try:yield
    finally:
        assert ranking.main is namespace['main'];ranking.main=old
