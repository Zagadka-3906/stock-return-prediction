"""Actual future18 private readers, bounded HTML and identity packer binding/restoration."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def main():
    assert allowed();closed('actual_bounded_HTML_exact_future18_shared_scopes_controls_v1_20261011');closed('actual_identity_memoized_lossless_codec_full180_controls_v1_20261011')
    old=A/'verify_shared_live_report_exact15_tuple_scope_controls_v4_20261011.py';text=old.read_text(encoding='utf-8')
    text=text.replace('共享榜对象精确15作用域控制_v4_20261011','共享榜身份复用与有界HTML联合18作用域_v1_20261011')
    text=text.replace("    namespace = {'write_exact_report': original_writer}","    namespace = {'write_exact_report': original_writer,'__file__':ranking.__file__}")
    text=text.replace('    import shared_live_ranking_report_runtime_v3_20261011 as runtime','    import shared_live_ranking_report_runtime_v3_20261011 as runtime\n    import bounded_original_ranking_HTML_runtime_v1_20261011 as html\n    import identity_memoized_original_lossless_codec_runtime_v1_20261011 as identity')
    text=text.replace("    original_read, original_json = Path.read_text, codec.json","    original_pack=codec.pack_report\n    original_read, original_json = Path.read_text, codec.json")
    needle="with runtime.installed(row['number'],row['codec_name'],row['verifier_name']) as state:";assert text.count(needle)==1
    text=text.replace(needle,needle[:-1]+',html.installed(),identity.installed(codec):')
    needle="            namespace['write_exact_report'](fixture, report)";assert text.count(needle)==1
    text=text.replace(needle,needle+"\n            assert codec.pack_report is identity.optimized.pack_report\n            assert json.dumps(codec.pack_report(report),ensure_ascii=False,separators=(',',':'),allow_nan=False)==json.dumps(original_pack(report),ensure_ascii=False,separators=(',',':'),allow_nan=False)\n            assert ranking.main.__globals__['write_bounded_original_html'] is html.writer.write\n            assert ranking.main.__globals__['write_exact_report'] is namespace['write_exact_report']")
    text=text.replace('        assert Path.read_text is original_read and codec.json is original_json','        assert codec.pack_report is original_pack\n        assert Path.read_text is original_read and codec.json is original_json')
    namespace={'__name__':'actual_future18_combined_performance_scope_fixture','__file__':str(old)};exec(compile(text,str(old),'exec'),namespace)
    variants=read(A/'bounded_original_HTML_exact_future18_shared_scopes_admission_v1_20261011.json')['variants'];assert len(variants)==18
    results=[namespace['run_variant'](r) for r in variants]
    paths=[Path(__file__),old,A/'identity_memoized_original_lossless_codec_runtime_v1_20261011.py',A/'identity_memoized_original_lossless_report_codec_v1_20261011.py',A/'bounded_original_ranking_HTML_runtime_v1_20261011.py',A/'bounded_original_HTML_exact_future18_shared_scopes_admission_v1_20261011.json',A/'actual_identity_memoized_lossless_codec_full180_location_v1_20261011.json',*[Path(r['execution']) for r in results]]
    create(A/'identity_codec_and_bounded_HTML_actual18_scope_admission_v1_20261011.json',{'status':'passed_actual18_private_codec_QA_readers_original_pack_AST_and_bytes_bounded_HTML_identity_memoized_packer_scope_restoration','variants':variants,'actual_scope_results':results,'input_sha256':{str(p):sha(p) for p in paths},'actual_original_codec_fixture_node_bytes_exact':True,'actual_scientific_rounds_not_executed_by_fixture':True,'all_original_per_round_browser_QA_still_required':True,'new_fits':0,'new_scores':0,'test_labels_read':False})
    print('Actual18 combined reader, codec node bytes, bounded HTML and restoration scopes passed; future adoption pending',flush=True)

if __name__=='__main__':main()
