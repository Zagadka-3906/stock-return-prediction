"""Prepare the protected37 replay route and execute its actual11 parent callbacks."""
from pathlib import Path
import importlib, runpy, sys

A = Path(__file__).resolve().parent
ROOT = A.parent
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed


def save(name, text):
    path = A / name
    assert not path.exists(), path
    compile(text, str(path), 'exec')
    path.write_text(text, encoding='utf8', newline='\n')
    return path


def main():
    assert allowed()
    source = A / 'predict_three_cached_mixed_complete_qualified_parent_scheme_v2_20261011.py'
    text = source.read_text(encoding='utf8')
    start, stop = text.index('def select_stage(graph):'), text.index('\ndef predict(')
    selector = '''def select_stage(graph):
    import rank5_rank20_near_protected_after_qualified_parent_native_stage_v1_20261011 as stage
    assert stage.GRAPH_KEY in graph
    spec=graph[stage.GRAPH_KEY]
    assert spec['recipe']==stage.RECIPE
    assert spec['codec'] in ('valid_pool_protection_v1','official_Top_protection_v2')
    assert spec['rank5_weight'] in (.03125,.0625,.125)
    assert spec['role']=='nonflag_valid' and spec['protect_fraction']==.15
    return stage,stage.GRAPH_KEY,'rank5_weight'

'''
    text = text[:start] + selector + text[stop:]
    text = text.replace('native_reload_two_independent_decoders_scalar_mix_and_Pandas_CDF_bits_exact', 'native_reload_two_independent_decoders_scalar_mix_and_Pandas_protected_sort_bits_exact')
    text = text.replace('rank5_rank20_mixed_complete_parent_native_replay_verification.json', 'rank5_rank20_near_protected_complete_parent_native_replay_verification.json')
    text = text.replace('passed_actual_complete175_mixed_horizon_two_full_native_independent_scalar_mix_and_cold80', 'passed_actual_complete175_near_protected_two_full_native_independent_scalar_mix_and_cold80')
    predictor = save('predict_near_protected_complete_qualified_parent_scheme_v1_20261011.py', text)
    module = importlib.import_module(predictor.stem)
    stage = importlib.import_module('rank5_rank20_near_protected_after_qualified_parent_native_stage_v1_20261011')
    rows = []
    for codec in ('valid_pool_protection_v1', 'official_Top_protection_v2'):
        for ratio in (.03125, .0625, .125):
            spec = {'recipe': stage.RECIPE, 'codec': codec, 'rank5_weight': ratio,
                    'role': 'nonflag_valid', 'protect_fraction': .15}
            chosen, key, field = module.select_stage({stage.GRAPH_KEY: spec})
            assert chosen is stage and key == stage.GRAPH_KEY and field == 'rank5_weight'
            rows.append(spec)
    good = rows[0]
    bad = [{}, {stage.GRAPH_KEY: {**good, 'recipe': 'wrong'}},
           {stage.GRAPH_KEY: {**good, 'codec': 'CDF'}},
           {stage.GRAPH_KEY: {**good, 'rank5_weight': 0.}},
           {stage.GRAPH_KEY: {**good, 'protect_fraction': .5}},
           {stage.GRAPH_KEY: {**good, 'role': 'all'}}]
    for graph in bad:
        try:
            module.select_stage(graph)
        except AssertionError:
            pass
        else:
            raise AssertionError('Unplanned protected selector configuration accepted')
    original = A / 'verify_three_cached_mixed_actual_eleven_parent_callbacks_CPU_v2_20261011.py'
    text = original.read_text(encoding='utf8')
    text = text.replace(source.stem, predictor.stem)
    text = text.replace('three_cached_mixed_actual_eleven_parent_callbacks_CPU_controls_v2_20261011', 'near_protected_actual_eleven_parent_callbacks_CPU_controls_v1_20261011')
    text = text.replace('two_seed_stage_last', 'near_protected_stage_last')
    cpu = save('verify_near_protected_actual_eleven_parent_callbacks_CPU_v1_20261011.py', text)
    runpy.run_path(str(cpu), run_name='__main__')
    proof = A / 'near_protected_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json'
    assert len(read(proof)['records']) == 11
    paths = [Path(__file__), source, predictor, original, cpu, proof, Path(stage.__file__)]
    create(A / 'near_protected_stage_selector_and_CPU11_sources_admission_v1_20261011.json', {
        'status': 'passed6_protected_codec_ratio_selectors6_bad_refusals_and11_actual_parent_callbacks_CPU_only',
        'input_sha256': {str(p): sha(p) for p in paths}, 'actual_selector_controls': rows,
        'actual_bad_input_refusals': len(bad), 'actual_parent_callback_CPU_count': 11,
        'new_native_fits': 0, 'new_quality_scores': 0,
        'actual_future_X_read': False, 'test_labels_read': False,
        'native_and_full_future_candidate_qualification_pending': True})
    print({'actual_selector_checks': len(rows), 'bad_input_refusals': len(bad), 'actual_parent_callbacks': 11}, flush=True)


if __name__ == '__main__':
    main()
