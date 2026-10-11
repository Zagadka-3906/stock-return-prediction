"""Fresh administrative receivers bind exact sparse labels while retaining all original routes."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create


def main():
    old = A / 'run_nonflag_SparseGram40_round133_full_registration_v1_20261007.py'
    new = A / 'run_nonflag_SparseGram40_round133_full_registration_v2_20261008.py'
    text = old.read_text(encoding='utf8')
    before = "publish(133,'完整父方案的非涨停残差Ridge补充','conditional_flag_residual_causal_checks.json',['预定52项完整官方比较：三个合格锚点、48项非涨停残差Ridge和一个消融'])"
    after = "publish(133,'完整父方案的稀疏L1和Elastic残差融合','conditional_flag_residual_causal_checks.json',['预定40项完整官方比较：112、131、132三个合格锚点、36项稀疏L1和Elastic残差融合和一个消融'])"
    assert text.count(before) == 1
    text = text.replace(before, after)
    before = "protocol=register();folder=A/'optimization_20261003_r133';pins=protocol['input_sha256']"
    after = before + "\n    recovery=A/'actual_SparseGram133_metadata_receivers_v2_20261008.json'\n    pins={**pins,**read(recovery)['input_sha256'],str(recovery):sha(recovery)}"
    assert text.count(before) == 1
    text = text.replace(before, after).replace('run_nonflag_SparseGram40_round133_full_registration_v1_file_IO_20261008', 'run_nonflag_SparseGram40_round133_full_registration_v2_file_IO_20261008')
    compile(text, str(new), 'exec')
    assert not new.exists()
    new.write_text(text, encoding='utf8', newline='\n')
    old_admission = A / 'verify_nonflag_SparseGram40_round133_sources_v1_20261007.py'
    new_admission = A / 'verify_nonflag_SparseGram40_round133_sources_v2_20261008.py'
    text = old_admission.read_text(encoding='utf8')
    marker = '    for p in sources:'
    assert text.count(marker) == 1
    text = text.replace(marker, "    sources += [A/'run_nonflag_SparseGram40_round133_full_registration_v2_20261008.py',A/'actual_SparseGram133_metadata_receivers_v2_20261008.json']\n" + marker)
    compile(text, str(new_admission), 'exec')
    assert not new_admission.exists()
    new_admission.write_text(text, encoding='utf8', newline='\n')
    paths = [Path(__file__), old, new, old_admission, new_admission,
             A / 'nonflag_SparseGram40_plan_20261007.json',
             A / 'nonflag_SparseGram40_science_route_preparation_v1_20261007.json',
             A / 'nonflag_SparseGram40_prospective_routes_v2_20261007.json',
             A / 'prepare_nonflag_SparseGram40_round133_sources_v1_20261007.py']
    create(A / 'actual_SparseGram133_metadata_receivers_v2_20261008.json', {
        'status': 'fresh_full133_metadata_receiver_exact40_records_and_sparse_labels_before_scores',
        'input_sha256': {str(p): sha(p) for p in paths},
        'all_original24_sources12_graph37_full111_cold_controls_preserved': True,
        'official_source_math_and_candidate_inference_checks_unchanged': True,
        'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__': main()
