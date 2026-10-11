"""Declare37 larger protected-sort variants of the measured near-pure horizon blend."""
from pathlib import Path
import ast, importlib, sys
from datetime import datetime

A = Path(__file__).resolve().parent
ROOT = A.parent
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

PLAN = 'rank5_rank20_near_protected37_predeclared_plan_v1_20261011.json'
OUT_NAME = 'Rank5Rank20_after175_near_protected37_screen_v1_20261011'
DRIVER = 'run_rank5_rank20_after175_near_protected37_screen_v1_20261011.py'
STAGE = 'rank5_rank20_near_protected_after_qualified_parent_native_stage_v1_20261011.py'
RECIPE = 'stock_rank5_rank20_near_pure_protected_label_horizon_ID16_cross120_recent252_e64'
SERVICE = 'actual_rank5_rank20_after175_near_protected37_screen_v1_20261011'


def save(name, text):
    path = A / name
    assert not path.exists(), path
    compile(text, str(path), 'exec')
    path.write_text(text, encoding='utf8', newline='\n')
    return path


def main():
    assert allowed()
    original = A / 'run_rank5_rank20_after175_near_pure49_screen_v1_20261011.py'
    precursor = Path('E:/赛题五_本机临时/Rank5Rank20_after175_near_pure49_screen_v1_20261011/verification.json')
    measured = read(precursor)
    assert len(measured['records']) == 49 and measured['best']['connected_final_score'] == 0.4514130257498636
    text = original.read_text(encoding='utf8')
    first, last = text.index('def cases():'), text.index('\ndef main():')
    replacement = '''def cases():
    rows=[{'kind':'anchor175','role':None,'weight':0.,'sign':1.,'protect_fraction':None,'rank5_weight':None}]
    for blend in (.03125,.0625,.125):
        for kind in ('valid_pool_protection_v1','official_Top_protection_v2'):
            for sign in (-1.,1.):
                for weight in (.016,.064,.25):
                    rows.append({'kind':kind,'role':'nonflag_valid','weight':weight,'sign':sign,'protect_fraction':.15,'rank5_weight':blend})
    assert len(rows)==37;return rows

'''
    text = text[:first] + replacement + text[last:]
    text = text.replace('Rank5Rank20_after175_near_pure49_screen_v1_20261011', OUT_NAME)
    text = text.replace('rank5_rank20_near_pure49_predeclared_plan_v1_20261011.json', PLAN)
    text = text.replace("closed('actual_rank5_rank20_after175_mixed_horizon49_screen_v2_20261011')", "closed('actual_rank5_rank20_after175_near_pure49_screen_v1_20261011')")
    text = text.replace('stock_rank5_rank20_mixed_label_horizon_ID16_cross120_recent252_e64', RECIPE)
    text = text.replace("'expected_cases':49", "'expected_cases':37").replace("'new_quality_score_records':49", "'new_quality_score_records':37")
    text = text.replace("'actual_nonidentity_full_controls':48", "'actual_nonidentity_full_controls':36").replace("'actual_nonidentity_prefix_controls':144", "'actual_nonidentity_prefix_controls':108")
    text = text.replace('passed49_mixed_rank5_rank20_TRAIN_only_CDF_both_signs_official_comparisons', 'passed37_near_pure_horizon_protected_sort_TRAIN_only_official_comparisons')
    text = text.replace('actual_mixed_rank5_rank20_49_TRAIN_only_official_scoring', 'actual_near_pure_horizon_protected37_TRAIN_only_official_scoring')
    driver = save(DRIVER, text)
    original_stage = A / 'rank5_rank20_near_pure_after_qualified_parent_native_stage_v1_20261011.py'
    text = original_stage.read_text(encoding='utf8')
    text = text.replace('rank5_rank20_near_pure_after_complete_qualified_parent_v1_20261011', 'rank5_rank20_near_protected_after_complete_qualified_parent_v1_20261011')
    text = text.replace('stock_rank5_rank20_near_pure_label_horizon_ID16_cross120_recent252_e64', RECIPE)
    text = text.replace('    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec',
                        '    import protected_upper_tail_rank_permutation_v1_20261010 as valid_tail\n    import protected_official_top_rank_permutation_v2_20261010 as top_tail')
    text = text.replace("    assert spec['recipe']==RECIPE and spec['codec']=='CDF'", "    assert spec['recipe']==RECIPE and spec['codec'] in ('valid_pool_protection_v1','official_Top_protection_v2')\n    assert spec['role']=='nonflag_valid' and spec['protect_fraction']==.15\n    codec=valid_tail if spec['codec']=='valid_pool_protection_v1' else top_tail")
    text = text.replace("spec['stage_kind']=='rank5_rank20_mixed_raw_average'", "spec['stage_kind']=='rank5_rank20_mixed_raw_average_protected_tail'")
    text = text.replace("args=(context.dates,context.flags,context.valid,spec['role'],spec['weight'],spec['sign'])", "args=(context.dates,context.flags,context.valid,spec['weight'],spec['protect_fraction'],spec['sign'])")
    old = "    cohort=codec.selected(context.flags,context.valid,spec['role'])\n    assert np.array_equal(value[~cohort].view('u8'),np.asarray(parent,dtype=np.float64)[~cohort].view('u8'))"
    assert text.count(old) == 1
    text = text.replace(old, "    codec.assert_invariants(parent,value,context.dates,context.flags,context.valid,spec['protect_fraction'])")
    text = text.replace("'codec':'CDF'", "'codec':spec['codec']")
    text = text.replace('native_reload_two_independent_decoders_scalar_mix_and_Pandas_CDF_bits_exact', 'native_reload_two_independent_decoders_scalar_mix_and_Pandas_protected_sort_bits_exact')
    stage = save(STAGE, text)
    cases = importlib.import_module(Path(DRIVER).stem).cases()
    assert len(cases) == 37
    stage_module = importlib.import_module(Path(STAGE).stem)
    assert stage_module.RECIPE == RECIPE and len(stage_module.BACKENDS[RECIPE]) == 4
    tree = ast.parse(stage.read_text(encoding='utf8'))
    assert 'reference_meta' not in {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    paths = [Path(__file__), original, original_stage, driver, stage, precursor,
             A / 'protected_upper_tail_rank_permutation_controls_v1_20261010.json',
             A / 'protected_official_top_rank_permutation_controls_v2_20261010.json']
    pins = {str(p): sha(p) for p in paths}
    create(A / PLAN, {'status': 'predeclared37_adaptive_TRAIN_only_protected_sort_horizon_blends_before_any_new_scores',
                      'at_local': datetime.now().isoformat(), 'input_sha256': pins, 'cases': cases,
                      'actual_service': SERVICE, 'output': str(Path('E:/赛题五_本机临时') / OUT_NAME),
                      'location_pointer': str(A / ('actual_' + OUT_NAME + '_location.json')),
                      'native_stage_module': stage_module.__name__, 'native_graph_key': stage_module.GRAPH_KEY,
                      'stage_kind': 'rank5_rank20_mixed_raw_average_protected_tail', 'recipe': RECIPE,
                      'banks': ['stock_rank20_embedding_small512_BF16_bank6_v1_20261010', 'stock_rank5_embedding_small512_BF16_bank6_v1_20261010'],
                      'component_weights': [.03125, .0625, .125], 'label_horizons': [20, 5],
                      'training_windows': [252, 252], 'training_populations_equal_not_claimed': True,
                      'expected_records': 37, 'expected_nonidentity_full_controls': 36,
                      'expected_nonidentity_prefix_controls': 108, 'new_native_fits': 0,
                      'new_quality_scores_before_declaration': 0, 'future_X_read': False,
                      'test_labels_read': False, 'selection_bias_uncorrected': True,
                      'adaptive_TRAIN_search_not_blind': True, 'future_selected_native_and_candidate_pending': True,
                      'full190_registration_factory_not_yet_created': True,
                      'preceding_full189_remains_prioritized': True})
    assert not (Path('E:/赛题五_本机临时') / OUT_NAME).exists()
    assert allowed()
    row = start_service(SERVICE, DRIVER, [], {**pins, str(A / PLAN): sha(A / PLAN)})
    create(A / (SERVICE + '_activation.json'), row)
    create(A / 'near_protected37_sources_and_dispatch_admission_v1_20261011.json', {
        'status': 'compiled_independently_matured_two_horizon_protected_stage_and_dispatched37_TRAIN_cases',
        'input_sha256': {**pins, str(A / PLAN): sha(A / PLAN)},
        'actual_service_identity': row, 'native_stage_not_yet_qualified': True,
        'new_native_fits': 0, 'new_quality_scores_not_claimed_complete': True,
        'future_X_read': False, 'test_labels_read': False})
    print({'new_declared_protected_cases': 37, 'new_native_fits': 0, 'worker_pid': row['owned_worker_pid']}, flush=True)


if __name__ == '__main__':
    main()
