"""Test actual sealed report subsets and the complete existing lossless codebook."""
from pathlib import Path
import sys,json,time,re,statistics,gc
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from exact_early_long_string_lossless_codec_20261007 import pack_report as fast
from build_lossless_ranking_display_v2_20261006 import pack_report as old,unpack_report
def main():
    import psutil
    out=A/'exact_early_string_lossless_codec_benchmark_20261007'
    assert not out.exists();out.mkdir()
    display=A/'lossless_ranking_display_v2_20261006/round116'
    page=display/'complete_rankings_lossless.html';proof=read(display/'verification.json')
    assert sha(page)==proof['lossless_HTML_sha256']
    paths=[Path(__file__),A/'exact_early_long_string_lossless_codec_20261007.py',
        A/'build_lossless_ranking_display_v2_20261006.py',page,display/'verification.json']
    pins={str(p):sha(p) for p in paths}
    create(out/'frozen_before_benchmark.json',{'input_sha256':pins,'source_round':116,
        'actual_pipeline_adoption':False,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    while psutil.virtual_memory().available<9*2**30:time.sleep(10)
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    with LockedReadHashCache(pins) as scope:
        text=page.read_text(encoding='utf8')
        match=re.search(r'<script\s+id="data"\s+type="application/json">(.*?)</script>',text,re.S)
        assert match;original_packed=json.loads(match.group(1));del text,match
        report=unpack_report(original_packed);assert len(report['connected'])==12406
        examples=[{'connected':report['connected'][:32]}, {'connected':report['connected'][-32:]},
            {'representative':report['representative'][:16],'summary':report['summary'],'historical':report['historical'][:8]}]
        records=[]
        for order in (('old','fast'),('fast','old')):
            for index,example in enumerate(examples):
                # Match the live builder's json.loads input: independently allocate repeated objects.
                independent=json.loads(json.dumps(example,ensure_ascii=False,allow_nan=False))
                results={};timings={}
                for name in order:
                    start=time.perf_counter();results[name]=(old if name=='old' else fast)(independent)
                    timings[name]=time.perf_counter()-start
                encoded={k:json.dumps(v,ensure_ascii=False,separators=(',',':'),allow_nan=False) for k,v in results.items()}
                assert encoded['old']==encoded['fast']
                assert unpack_report(json.loads(encoded['fast']))==independent
                records.append({'case':index,'order':order,'seconds':timings,'speedup':timings['old']/timings['fast'],
                    'all_original_node_ids_values_and_serialized_bytes_exact':True})
                print(records[-1],flush=True)
                del independent,results,encoded;gc.collect()
        start=time.perf_counter();full=fast(report);elapsed=time.perf_counter()-start
        assert json.dumps(full,ensure_ascii=False,separators=(',',':'),allow_nan=False)==json.dumps(original_packed,ensure_ascii=False,separators=(',',':'),allow_nan=False)
        rebuilt=unpack_report(full)
        for view in ('representative','connected','mlp_bounds','historical','csv_test','legacy_annual'):
            assert rebuilt[view]==report[view]
        scope.reverify()
        create(out/'verification.json',{'status':'passed_actual6_two_order_independent_report_subset_benchmarks_and_full12406_original_codebook_exact',
            'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,
            'median_measured_subset_packing_speedup':statistics.median(r['speedup'] for r in records),
            'full12406_optimized_packing_seconds':elapsed,'full_old_packing_not_retimed':True,
            'all_original_node_ids_values_serialized_bytes_and_six_views_exact':True,
            'actual_pipeline_adoption':False,'active_round120_or121_sources_changed':False,
            'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
        print({'status':'passed_full12406_codebook_exact','seconds':elapsed},flush=True)
if __name__=='__main__':main()
