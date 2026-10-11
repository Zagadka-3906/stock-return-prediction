"""Execute the actual archive compatibility interface on the entire sealed116 board."""
from pathlib import Path
import sys,os,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    from exact_native_JSON_archive_runtime_20261007 import install
    import immutable_lossless_ranking_snapshot_20261006 as runtime
    out=A/'exact_native_JSON_archive_runtime_full_preflight_20261007';assert not out.exists();out.mkdir()
    source=A/'lossless_ranking_display_v2_20261006/round116'
    for name in ('complete_rankings_lossless.html','verification.json'):os.link(source/name,out/name)
    pins={str(p):sha(p) for p in [Path(__file__),A/'exact_native_JSON_archive_runtime_20261007.py',
      A/'exact_native_JSON_full_board_benchmark_20261007/verification.json',*list(out.glob('*.json')),*list(out.glob('*.html'))]}
    create(out/'frozen_before_actual_runtime.json',{'input_sha256':pins,'complete_source_round':116,'new_quality_scores':0})
    start=time.perf_counter();restore=install()
    try:snapshot=runtime.prepare(out)
    finally:restore()
    expected=read(source/'full_report_publication_snapshot_verification.json')
    actual=read(out/'full_report_publication_snapshot_verification.json')
    assert actual['full_original_bytes']==expected['full_original_bytes']==2076897250
    assert actual['original_report_sha256']==expected['original_report_sha256']
    assert sha(snapshot)==actual['compressed_snapshot_sha256']==expected['compressed_snapshot_sha256']
    assert Path(actual['actual_encoder_source'])==A/'exact_native_JSON_archive_runtime_20261007.py'
    assert actual['connected_records']==12406 and actual['msgspec_version']=='0.22.0'
    create(out/'runtime_verification.json',{'status':'passed_actual_installed_runtime_full12406_original2076897250_raw_and_gzip_bytes_exact',
      'input_sha256':pins,'actual_full_runtime_seconds':time.perf_counter()-start,
      'actual_original_byte_count':actual['full_original_bytes'],'actual_compressed_snapshot_sha256':sha(snapshot),
      'all_original_record_values_parameters_provenance_preserved':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
