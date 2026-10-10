"""Scope actual whole-board-proven LF parameter serialization to main publication."""
from pathlib import Path
from contextlib import contextmanager
import sys
A=Path(__file__).resolve().parent;sys.path.insert(0,str(A))
from run_dependency_queue_v3_20261006 import read,sha

@contextmanager
def installed():
    import publish_classifier_consensus_workflows_20261006 as helpers
    from exact_native_pretty_JSON_archive_20261007 import native_block
    proof=read(A/'full_ranking_JSON_decoder_benchmark_v2_20261010.json')
    assert proof['status']=='passed_actual_complete_native_report_two_fresh_decoder_processes_and_byte_exact_full_reencoding'
    assert proof['adopt_parameter_encoder']
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    original,optimized=proof['records']
    assert original['all_parameter_row_boundary_and_bytes_sha256']==optimized['all_parameter_row_boundary_and_bytes_sha256']
    assert original['all_parameter_encoded_bytes']==optimized['all_parameter_encoded_bytes']
    assert original['actual_parameter_rows']==optimized['actual_parameter_rows']==15595
    sync=helpers.sync;previous=sync.encoded
    def encoded(value):
        # The installed safe transport adds chunk descriptors to this manifest.
        if isinstance(value,dict) and value.get('status')=='validated_local_snapshot':return previous(value)
        try:return native_block(value,0).replace(b'\r\n',b'\n')+b'\n'
        except (ValueError,TypeError):return previous(value)
    sync.encoded=encoded
    try:yield
    finally:
        assert sync.encoded is encoded;sync.encoded=previous
