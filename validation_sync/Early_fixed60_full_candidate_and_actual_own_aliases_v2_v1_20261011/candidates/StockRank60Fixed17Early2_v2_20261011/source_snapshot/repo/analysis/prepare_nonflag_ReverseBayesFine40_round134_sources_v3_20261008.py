"""Predeclare complete negative Bayesian amplitude-refinement routes for all possible parents."""
from pathlib import Path
import hashlib
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from prepare_protected_upper_pool_HGB66_round115_sources_20261007 import substitute
from nonflag_ReverseBayesFine40_round134_mapping_v1_20261008 import convert
import prepare_nonflag_SparseGram40_round133_sources_v1_20261007 as base
NAMES = {name: convert(name) for name in base.NAMES.values()}


def generate(parent):
    assert parent in (112, 132, 133)
    overrides = {'_r112': f'_r{parent}', 'round112_receipt.json': f'round{parent}_receipt.json',
        'PREVIOUS_NUMBER = 112': f'PREVIOUS_NUMBER = {parent}',
        'explicit_comparison_parent_round=112': f'explicit_comparison_parent_round={parent}',
        "'explicit_parent_round': 112": f"'explicit_parent_round': {parent}"}
    result = {NAMES[name]: substitute(convert(text), overrides) for name, text in base.generate(112).items()}
    for name, text in result.items():
        if name.startswith('build_lossless_'):
            before='    assert not out.exists()\n    out.mkdir(parents=True)'
            after='    from admit_empty_E_display_junction_v1_20261008 import ensure\n    ensure(out, number)'
            assert text.count(before)==1
            text=text.replace(before,after)
        if name.startswith('lossless_ranking_runtime_'):
            before='    assert not display.exists() and not qa_folder.exists()'
            after='    assert not qa_folder.exists()\n    from admit_empty_E_display_junction_v1_20261008 import ensure\n    ensure(display, number, create=False)'
            assert text.count(before)==1
            text=text.replace(before,after)
        if name.startswith('register_'):
            legacy="assert pilot['status'] == 'passed_actual40_nonflag_Ridge_full_official_comparisons'"
            actual="assert pilot['status'] == 'passed_actual40_nonflag_ReverseBayes64_full_official_comparisons'"
            assert text.count(legacy)==1
            original=text
            text=text.replace(legacy,actual)
            import ast
            assert ast.dump(ast.parse(text.replace(actual,legacy)))==ast.dump(ast.parse(original))
            marker="    pins = {**read(RELEASE / 'protocol.json')['input_sha256']"
            assert text.count(marker)==1
            extra="    sources += [A/'prepare_nonflag_ReverseBayesFine40_round134_sources_v3_20261008.py', A/'run_nonflag_ReverseBayesFine40_round134_full_registration_v3_20261008.py', A/'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json']\n"
            extra += "    sources += [A/'admit_empty_E_display_junction_v1_20261008.py', A/'actual_ReverseBayesFine134_empty_E_receiver_preparation_v3_20261008.json']\n"
            text=text.replace(marker,extra+marker)
        if name.startswith('publish_'):
            text = text.replace('112、131、132合格锚点，两组非涨停稀疏L1/Elastic残差及等权集成各12幅度',
                                '112、132、133合格锚点，两组反向贝叶斯残差及等权集成各12幅度')
            text = text.replace('登记第133轮40项', '登记第134轮40项')
        compile(text, str(A / name), 'exec')
        result[name] = text
    assert len(result) == 8
    return result


def main():
    ready_path = A / 'nonflag_ReverseBayesFine40_selected_release_v1_20261007/selected_candidate_ready_for_registration.json'
    ready = read(ready_path)
    assert ready['status'] == 'passed_actual40_selected_candidate_full_graph_and_metrics_and_source_bytes' and ready['sealed_candidate_complete']
    pilot = read(A / 'nonflag_ReverseBayesFine40_official_comparison_v1_20261007/verification.json')
    assert len(pilot['records']) == 40 and pilot['best'] == ready['best']
    path = A / 'nonflag_ReverseBayesFine40_round134_source_admission_v1_20261007.json'
    proof = read(path)
    assert proof['status'] == 'passed_actual37_controls_and24_prospective134_complete_source_schema_paths_and_graph_routes'
    for p, d in proof['input_sha256'].items(): assert sha(p) == d, p
    generated = generate(pilot['actual_comparison_parent_round'])
    for name, text in generated.items():
        assert not (A / name).exists()
        assert hashlib.sha256(text.encode()).hexdigest() == proof['generated_source_sha256'][str(pilot['actual_comparison_parent_round'])][name]
    for name, text in generated.items(): (A / name).write_text(text, encoding='utf8', newline='\n')
    create(A / 'nonflag_ReverseBayesFine40_round134_source_preparation_v1_20261007.json', {
        'status': 'passed_actual40_sealed_candidate_and_admitted_full134_QA45_sources',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'round': 134, 'scored_records': 40,
        'actual_comparison_parent_round': pilot['actual_comparison_parent_round'],
        'input_sha256': {str(p): sha(p) for p in [Path(__file__), ready_path, path, *[A / n for n in generated]]},
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})


if __name__ == '__main__': main()
