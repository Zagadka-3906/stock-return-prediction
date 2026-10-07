"""Measure exact old-vs-native bytes, then reconstruct the whole sealed116 board."""
from pathlib import Path
import sys,time,json,gzip,hashlib,os,io,statistics,gc
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from atomic_optimization_observer_writes_20261005 import write

def main():
    import psutil,msgspec,re
    from build_lossless_ranking_display_v2_20261006 import unpack_report
    from exact_native_pretty_JSON_archive_20261007 import pieces
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    out=A/'exact_native_JSON_full_board_benchmark_20261007';assert not out.exists();out.mkdir()
    display=A/'lossless_ranking_display_v2_20261006/round116'
    proof_path=display/'verification.json';proof=read(proof_path)
    old_snapshot=display/'full_report_reconstructed_for_publication.json.gz';old_proof=read(display/'full_report_publication_snapshot_verification.json')
    page=display/'complete_rankings_lossless.html';assert sha(page)==proof['lossless_HTML_sha256']
    assert sha(old_snapshot)==old_proof['compressed_snapshot_sha256']
    cache=Path('E:/赛题五_本机临时/exact_native_JSON_archive_benchmark_20261007');assert not cache.exists();cache.mkdir(parents=True)
    result_path=cache/'round116_full_exact_native.json.gz'
    paths=[Path(__file__),A/'exact_native_pretty_JSON_archive_20261007.py',proof_path,
      page,old_snapshot,display/'full_report_publication_snapshot_verification.json',A/'build_lossless_ranking_display_v2_20261006.py',
      *list((ROOT/'.venv/Lib/site-packages/msgspec').glob('*.pyd'))]
    pins={str(p):sha(p) for p in paths}
    create(out/'frozen_before_benchmark.json',{'input_sha256':pins,'msgspec_version':msgspec.__version__,
      'full_source_round':116,'only_benchmark_no_pipeline_adoption':True,'test_labels_read':False})
    while psutil.virtual_memory().available<10*2**30:time.sleep(10)
    with LockedReadHashCache(pins) as scope:
        text=page.read_text(encoding='utf8');data=re.search(r'<script\s+id="data"\s+type="application/json">(.*?)</script>',text,re.S)
        assert data;report=unpack_report(json.loads(data.group(1)));del text,data;gc.collect()
        assert len(report['connected'])==12406
        records=[]
        def compressed(value,native):
            destination=io.BytesIO();digest=hashlib.sha256();raw=0
            with gzip.GzipFile(filename='',mode='wb',fileobj=destination,compresslevel=6,mtime=0) as stream:
                if native:chunks=pieces(value)
                else:
                    def chunks_old():
                        encoder=json.JSONEncoder(ensure_ascii=False,indent=2,allow_nan=False)
                        for part in encoder.iterencode(value):yield part.replace('\n',os.linesep).encode('utf8')
                        yield os.linesep.encode('utf8')
                    chunks=chunks_old()
                for chunk in chunks:digest.update(chunk);raw+=len(chunk);stream.write(chunk)
            return destination.getvalue(),digest.hexdigest(),raw
        examples=[{'connected':report['connected'][:32]}, {'connected':report['connected'][-32:]},
          {'representative':report['representative'][:16],'summary':report['summary'],'historical':report['historical'][:8]}]
        for order in (('old','native'),('native','old')):
            for index,example in enumerate(examples):
                outputs={};timings={}
                for name in order:
                    start=time.perf_counter();outputs[name]=compressed(example,name=='native');timings[name]=time.perf_counter()-start
                assert outputs['old']==outputs['native'],index
                records.append({'case':index,'order':order,'timings':timings,'speedup':timings['old']/timings['native'],
                  'raw_bytes':outputs['native'][2],'raw_sha256':outputs['native'][1],
                  'compressed_sha256':hashlib.sha256(outputs['native'][0]).hexdigest(),
                  'all_original_raw_and_compressed_bytes_exact':True})
                print({'case':index,'order':order,'speedup':records[-1]['speedup']},flush=True)
        write(out/'actual_stage.json',{'status':'actual_whole12406_record_native_reconstruction','control_cases':len(records)})
        digest=hashlib.sha256();raw_bytes=0;start=time.perf_counter()
        with result_path.open('xb') as destination:
            with gzip.GzipFile(filename='',mode='wb',fileobj=destination,compresslevel=6,mtime=0) as stream:
                for chunk in pieces(report):digest.update(chunk);raw_bytes+=len(chunk);stream.write(chunk)
        elapsed=time.perf_counter()-start
        assert digest.hexdigest()==proof['original_report_sha256']==old_proof['original_report_sha256']
        assert raw_bytes==old_proof['full_original_bytes']
        assert sha(result_path)==old_proof['compressed_snapshot_sha256']
        with gzip.open(result_path,'rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==proof['original_report_sha256']
        scope.reverify()
        create(out/'verification.json',{'status':'passed_actual6_two_order_bytes_benchmarks_and_full12406_original_raw_and_gzip_exact',
          'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'msgspec_version':msgspec.__version__,
          'median_measured_subset_encoding_and_compression_speedup':statistics.median(r['speedup'] for r in records),
          'actual_whole_board_encoding_and_compression_seconds':elapsed,'full_original_bytes':raw_bytes,
          'full_original_sha256':digest.hexdigest(),'compressed_snapshot_sha256':sha(result_path),'benchmark_output':str(result_path),
          'all12406_records_parameters_source_pointers_and_scientific_values_exact':True,
          'full_old_encoding_time_not_measured_again':True,'actual_pipeline_adoption':False,
          'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
