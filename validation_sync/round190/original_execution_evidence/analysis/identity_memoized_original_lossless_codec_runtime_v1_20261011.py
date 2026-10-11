"""Bind a fully byte-proven memoized packer to an otherwise unchanged round codec."""
from pathlib import Path
from contextlib import contextmanager
import ast
import identity_memoized_original_lossless_report_codec_v1_20261011 as optimized

@contextmanager
def installed(codec):
    from run_dependency_queue_v3_20261006 import read,sha
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed();A=Path(__file__).resolve().parent
    p=read(A/'actual_identity_memoized_lossless_codec_full180_location_v1_20261011.json')
    proof=read(Path(p['output'])/'verification.json')
    assert proof['status']=='passed_actual_complete180_original_every_codec_node_and_embedded_JSON_byte_identity_memoized_input_containers'
    for source,digest in proof['input_sha256'].items():assert sha(source)==digest,source
    import build_lossless_ranking_display_v2_20261006 as baseline
    def definition(module):
        tree=ast.parse(Path(module.__file__).read_text(encoding='utf-8'))
        return ast.dump(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='pack_report'),include_attributes=False)
    assert definition(codec)==definition(baseline)
    old=codec.pack_report;codec.pack_report=optimized.pack_report
    try:yield
    finally:assert codec.pack_report is optimized.pack_report;codec.pack_report=old
