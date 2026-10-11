"""Actual complete180 HTML bytes: independent whole-tree encoder versus bounded row encoder."""
from pathlib import Path
from datetime import datetime
import sys,hashlib,json,time,os,psutil,threading,tracemalloc
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
OUT=Path('E:/赛题五_本机临时/原始完整榜HTML有界写出实测_v1_20261011')
for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(OUT/'tmp')
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
import bounded_original_ranking_HTML_writer_v1_20261011 as writer

def digest(pieces):
    h=hashlib.sha256();size=0;largest=0
    for piece in pieces:h.update(piece);size+=len(piece);largest=max(largest,len(piece))
    return {'sha256':h.hexdigest(),'bytes':size,'largest_chunk_bytes':largest}

def main():
    assert allowed();OUT.mkdir(exist_ok=False);(OUT/'tmp').mkdir()
    import build_all_model_rankings_20261003 as ranking
    fixture={'rows':[{},[],{'中文':'</script>\n引号"🚀','floats':[0.,-0.,1e-7,1e20,1e21,1.2345678901234567],'tuple':(1,2),'banner':'__PROVENANCE_BANNER__','date':'__REPORT_DATE__','score':'__VALIDATION_BEST__','count':'__CONNECTED_COUNT__','data':'__DATA__'}], 'key</script>':'value\r\n'}
    records=[]
    for page in [ranking.PAGE,'__PROVENANCE_BANNER__|__DATA__|__REPORT_DATE__|__VALIDATION_BEST__|__CONNECTED_COUNT__']:
        for report in [{},fixture,{'empty':[],'value':None}]:
            banner='test __REPORT_DATE__ __CONNECTED_COUNT__';stamp='2026-10-11 08:00'
            native=page.replace('__DATA__',json.dumps(report,ensure_ascii=False,separators=(',',':'),allow_nan=False).replace('</','<\\/')).replace('__PROVENANCE_BANNER__',banner).replace('__REPORT_DATE__',stamp).replace('__VALIDATION_BEST__',f'{.45144551353324136:.9f}').replace('__CONNECTED_COUNT__',f'{17062:,}').replace('\n',os.linesep).encode('utf-8')
            a=b''.join(writer.html_pieces(page,report,banner,stamp,.45144551353324136,17062));b=b''.join(writer.html_pieces(page,report,banner,stamp,.45144551353324136,17062,True))
            assert a==b==native;records.append({'bytes':len(native),'native_bytes_exact':True})
    for value in (float('nan'),float('inf'),float('-inf')):
        try:list(writer.compact_pieces({'invalid':[value]}))
        except ValueError:pass
        else:raise AssertionError('Nonfinite JSON accepted')
    proof=A/'bounded_original_ranking_HTML_actual_fixture_controls_v1_20261011.json'
    create(proof,{'status':'passed_actual6_original_PAGE_escape_unicode_floats_substitution_order_and_Windows_newline_byte_fixtures','records':records,'nonfinite_cases_refused':3,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(writer.__file__),Path(ranking.__file__)]},'full180_controls_not_yet_claimed':True,'new_scores':0,'test_labels_read':False})
    print('Actual6 original PAGE byte fixtures passed; full180 benchmark next',flush=True)
    from verified_shared_publication_board_loader_v1_20261011 import SharedBoard
    folder=A/'lossless_ranking_display_v2_20261006/round180';archive=folder/'full_report_reconstructed_for_publication.json.gz'
    paths=[Path(__file__),Path(writer.__file__),Path(ranking.__file__),proof,archive,folder/'complete_rankings_lossless.html',folder/'verification.json',folder/'full_report_publication_snapshot_verification.json']
    pins={str(p):sha(p) for p in paths};create(OUT/'frozen_before_actual_full180_HTML_controls.json',{'input_sha256':pins,'expected_connected_records':17062,'full_compact_HTML_not_materialized':True,'new_scores':0,'test_labels_read':False})
    while psutil.virtual_memory().available<2*2**30:assert allowed();time.sleep(10)
    board=SharedBoard(archive);report=board.load();assert len(report['connected'])==17062
    baseline_info=read(A/'shared_live_ranking_report_actual180_controls_v1_20261011.json');assert baseline_info['connected_records']==17062
    peak=[psutil.Process().memory_info().rss];stop=threading.Event()
    def sampling():
        while not stop.wait(.1):peak.append(psutil.Process().memory_info().rss)
    monitor=threading.Thread(target=sampling,daemon=True);monitor.start()
    try:
        assert allowed();started=time.perf_counter();bounded=digest(writer.html_pieces(ranking.PAGE,report,'审计说明','2026-10-11 08:00',.45144551353324136,17062));bounded_seconds=time.perf_counter()-started
        print({'bounded_complete180_HTML':bounded,'seconds':bounded_seconds},flush=True)
        assert allowed();started=time.perf_counter();reference=digest(writer.html_pieces(ranking.PAGE,report,'审计说明','2026-10-11 08:00',.45144551353324136,17062,True));reference_seconds=time.perf_counter()-started
        assert bounded['sha256']==reference['sha256'] and bounded['bytes']==reference['bytes']
        for p,d in pins.items():assert sha(p)==d,p
        board.reverify()
        create(OUT/'verification.json',{'status':'passed_actual_complete180_original_HTML_full_tree_encoder_vs_bounded_row_encoder_bytes_exact','at_local':datetime.now().isoformat(),'input_sha256':pins,'connected_records':17062,'original_full_native_JSON_bytes':baseline_info['original_native_bytes'],'bounded':bounded,'reference':reference,'bounded_seconds':bounded_seconds,'reference_seconds':reference_seconds,'sampled_process_peak_RSS_bytes':max(peak),'no_full_HTML_or_JSON_string_materialized':True,'actual_original6_fixture_controls':str(proof),'new_scores':0,'new_native_fits':0,'test_labels_read':False,'live_scientific_workers_unchanged':True,'runtime_not_yet_adopted':True})
        create(A/'actual_bounded_original_ranking_HTML_full180_location_v1_20261011.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
        print('Actual full180 original HTML byte equivalence passed; live runtime not modified',flush=True)
    finally:stop.set();monitor.join(timeout=2)

if __name__=='__main__':main()
