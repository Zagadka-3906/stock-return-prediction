"""Predeclare eight complete round133 sources for every actual qualified comparison parent."""
from pathlib import Path
import hashlib
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from nonflag_SparseGram40_round133_mapping_v1_20261008 import convert
import prepare_nonflag_EmpiricalBayes40_round130_sources_v1_20261007 as base
NAMES = {name: convert(name) for name in base.NAMES.values()}


def generate(parent):
    assert parent in (112, 131, 132)
    overrides = {'_r112': f'_r{parent}', 'round112_receipt.json': f'round{parent}_receipt.json',
        'PREVIOUS_NUMBER = 112': f'PREVIOUS_NUMBER = {parent}',
        'explicit_comparison_parent_round=112': f'explicit_comparison_parent_round={parent}',
        "'explicit_parent_round': 112": f"'explicit_parent_round': {parent}"}
    result = {NAMES[name]: substitute(convert(text), overrides) for name, text in base.generate(112).items()}
    for name, text in result.items():
        if name.startswith('publish_'):
            text = text.replace('本轮52项完整官方比较：112、119、120合格锚点，两组非涨停残差Ridge及等权集成乘16幅度，以及消融。',
                                '本轮40项完整官方比较：112、131、132合格锚点，两组非涨停稀疏L1/Elastic残差及等权集成各12幅度，以及消融。')
            text = text.replace('49项5635800行CDF与147冷前缀核对', '37项5635800行CDF与111冷前缀核对')
            text = text.replace('登记第119轮88项非涨停残差HGB与完整父方案组合验证并发布完整榜与全量QA',
                                '登记第133轮40项稀疏L1和Elastic残差完整验证并发布完整榜与QA44')
        compile(text, str(A / name), 'exec')
        result[name] = text
    assert len(result) == 8
    return result


def main():
    ready_path = A / 'nonflag_SparseGram40_selected_release_v1_20261007/selected_candidate_ready_for_registration.json'
    ready = read(ready_path)
    assert ready['status'] == 'passed_actual40_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot = read(A / 'nonflag_SparseGram40_official_comparison_v1_20261007/verification.json')
    assert len(pilot['records']) == 40 and pilot['best'] == ready['best']
    path = A / 'nonflag_SparseGram40_round133_source_admission_v1_20261007.json'
    proof = read(path)
    assert proof['status'] == 'passed_actual37_controls_and24_prospective133_complete_source_schema_paths_and_graph_routes'
    for p, d in proof['input_sha256'].items(): assert sha(p) == d, p
    generated = generate(pilot['actual_comparison_parent_round'])
    for name, text in generated.items():
        assert not (A / name).exists()
        assert hashlib.sha256(text.encode()).hexdigest() == proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name, text in generated.items(): (A / name).write_text(text, encoding='utf8', newline='\n')
    create(A / 'nonflag_SparseGram40_round133_source_preparation_v1_20261007.json', {
        'status': 'passed_actual40_sealed_candidate_and_admitted_full133_QA44_sources',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'round': 133, 'scored_records': 40,
        'actual_comparison_parent_round': pilot['actual_comparison_parent_round'],
        'input_sha256': {str(p): sha(p) for p in [Path(__file__), ready_path, path, *[A / n for n in generated]]},
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__': main()
