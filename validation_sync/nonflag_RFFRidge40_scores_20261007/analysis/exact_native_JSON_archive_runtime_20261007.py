"""Install the measured, byte-identical archive encoder only in a new admitted scope."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,owned

def install():
    import msgspec
    import immutable_lossless_ranking_snapshot_20261006 as original
    proof_path=A/'exact_native_JSON_full_board_benchmark_20261007/verification.json'
    folder=A/'service_owned_workflows_20261006/exact_native_JSON_full_board_benchmark'
    assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='passed'
    proof=read(proof_path)
    assert proof['status']=='passed_actual6_two_order_bytes_benchmarks_and_full12406_original_raw_and_gzip_exact'
    assert proof['msgspec_version']==msgspec.__version__=='0.22.0'
    for filename,digest in proof['input_sha256'].items():assert sha(filename)==digest,filename
    source=Path(original.__file__);text=source.read_text(encoding='utf8')
    old="""                encoder = json.JSONEncoder(ensure_ascii=False, indent=2, allow_nan=False)
                for part in encoder.iterencode(report):
                    encoded = part.replace('\\n', os.linesep).encode('utf-8')
                    digest.update(encoded)
                    raw_bytes += len(encoded)
                    compressed.write(encoded)
                encoded = os.linesep.encode('utf-8')
                digest.update(encoded)
                raw_bytes += len(encoded)
                compressed.write(encoded)"""
    new="""                from exact_native_pretty_JSON_archive_20261007 import pieces
                for encoded in pieces(report):
                    digest.update(encoded)
                    raw_bytes += len(encoded)
                    compressed.write(encoded)"""
    assert text.count(old)==1;text=text.replace(old,new)
    text=text.replace('from locked_read_hash_cache_20261004 import LockedReadHashCache','from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache')
    needle='    with LockedReadHashCache(inputs):';assert text.count(needle)==1
    text=text.replace(needle,"    inputs.update(NATIVE_ARCHIVE_PINS)\n"+needle)
    needle="'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}"
    assert text.count(needle)==1
    text=text.replace(needle,"'actual_encoder_source': str(Path(__file__).resolve()), 'msgspec_version': '0.22.0', 'actual_pre_adoption_full_board_benchmark': str(NATIVE_ARCHIVE_PROOF), "+needle)
    pins={str(p):sha(p) for p in [source,Path(__file__),proof_path,A/'exact_native_pretty_JSON_archive_20261007.py',
      A/'win32_read_handle_hash_cache_with_filename_v2_20261006.py']}
    pins.update(proof['input_sha256'])
    namespace={'__file__':str(Path(__file__).resolve()),'__name__':'actual_byte_identical_native_archive',
      'NATIVE_ARCHIVE_PINS':pins,'NATIVE_ARCHIVE_PROOF':proof_path}
    exec(compile(text,str(Path(__file__).resolve()),'exec'),namespace)
    prior=original.prepare;original.prepare=namespace['prepare']
    def restore():
        assert original.prepare is namespace['prepare'];original.prepare=prior
    return restore
