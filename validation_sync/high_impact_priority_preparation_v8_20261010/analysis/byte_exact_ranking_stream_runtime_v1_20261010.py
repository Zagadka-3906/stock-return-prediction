"""Scope an evidenced bounded byte-identical writer to only the full ranking builder."""
from pathlib import Path
from contextlib import contextmanager
import sys
A=Path(__file__).resolve().parent;sys.path.insert(0,str(A))
from run_dependency_queue_v3_20261006 import read,sha

@contextmanager
def installed():
    import build_all_model_rankings_20261003 as ranking
    from exact_native_pretty_JSON_archive_20261007 import pieces
    proof=read(A/'byte_exact_ranking_stream_benchmark_v1_20261010.json')
    assert proof['status']=='passed_actual_full155_original_report_bytes_and_two_order_timing' and proof['adopt']
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    source=Path(ranking.__file__);text=source.read_text(encoding='utf8')
    before=[
        '    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+"\\n", encoding="utf-8")',
        '        output_json.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+"\\n",encoding="utf-8")']
    for old in before:
        assert text.count(old)==1
        indent=old[:len(old)-len(old.lstrip())]
        text=text.replace(old,indent+'write_exact_report(output_json,report)')
    def write_exact_report(path,report):
        with Path(path).open('wb') as stream:
            for raw in pieces(report):stream.write(raw)
    namespace=dict(ranking.__dict__);namespace.update(__name__='byte_exact_bounded_ranking_writer',write_exact_report=write_exact_report)
    exec(compile(text,str(source),'exec'),namespace)
    original=ranking.main;ranking.main=namespace['main']
    try:yield
    finally:
        assert ranking.main is namespace['main'];ranking.main=original
