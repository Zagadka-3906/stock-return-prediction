"""Prepare37 measured comparisons plus qualified175/189 anchors, then qualify winner."""
from pathlib import Path
from datetime import datetime
import sys

A = Path(__file__).resolve().parent
ROOT = A.parent
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

PLAN = 'near_protected_complete39_after189_plan_v1_20261011.json'
NORMAL = 'normalize_completed_near_protected39_after189_v1_20261011.py'
COMPUTE = 'compute_near_protected39_selected_native14_v1_20261011.py'
QUAL = 'qualify_near_protected39_selected_native14_v1_20261011.py'


def save(name, text):
    path = A / name
    assert not path.exists(), path
    compile(text, str(path), 'exec')
    path.write_text(text, encoding='utf8', newline='\n')
    return path


def once(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)


def main():
    assert allowed()
    declaration = read(A / 'rank5_rank20_near_protected37_predeclared_plan_v1_20261011.json')
    family = {
        'name': 'near_protected37', 'actual_service': declaration['actual_service'],
        'main_receipt': 'near_protected37_official37_main_receipt_v1_20261011.json',
        'output': declaration['output'], 'banks': declaration['banks'],
        'member_names': ['Rank20_ID16_Cross120_seed20261009_e64', 'Rank5_ID16_Cross120_seed20261009_e64'],
        'native_stage_module': declaration['native_stage_module'],
        'component_weight_field': 'rank5_weight', 'component_weights': declaration['component_weights'],
        'label_horizons': [20, 5], 'training_windows': [252, 252],
        'stage_kind': declaration['stage_kind'], 'signal_name': 'near_protected_two_horizon_raw_average',
    }
    create(A / PLAN, {'status': 'predeclared39_normalization_without_rescoring_future_parent189_not_yet_claimed_qualified',
                      'at_local': datetime.now().isoformat(), 'expected_records': 39,
                      'fully_qualified_anchors': [175, 189],
                      'actual_previous_complete_family': 'MixedObjectiveWindow189_complete149_family_v3_20261011',
                      'families': [family], 'new_quality_scores': 0, 'new_native_fits': 0,
                      'full190_factory_not_yet_created': True, 'test_labels_read': False})
    normal_source = A / 'normalize_completed_three_cached_mixed149_after188_v1_20261011.py'
    text = normal_source.read_text(encoding='utf8')
    text = text.replace('three_cached_mixed_complete149_after188', 'near_protected_complete39_after189')
    text = text.replace('three_cached_mixed_stage_selector_and_CPU11_sources_admission_v2_20261011', 'near_protected_stage_selector_and_CPU11_sources_admission_v1_20261011')
    text = text.replace('three_cached_mixed_actual_eleven_parent_callbacks_CPU_controls_v2_20261011', 'near_protected_actual_eleven_parent_callbacks_CPU_controls_v1_20261011')
    text = text.replace('==149', '==39').replace('[175,188]', '[175,189]').replace('(175,188)', '(175,189)')
    text = text.replace('anchors[188]', 'anchors[189]')
    text = text.replace("'actual_comparison_parent_round':188", "'actual_comparison_parent_round':189")
    text = text.replace('==49', '==37').replace('==(48,144)', '==(36,108)')
    text = text.replace('full_count+=48;prefix_count+=144', 'full_count+=36;prefix_count+=108')
    text = text.replace('==(149,144,432)', '==(39,36,108)')
    text = text.replace("'expected_scored_records':149", "'expected_scored_records':39")
    text = text.replace("'actual_nonidentity_full_controls':144", "'actual_nonidentity_full_controls':36")
    text = text.replace("'actual_nonidentity_prefix_controls':432", "'actual_nonidentity_prefix_controls':108")
    text = text.replace("cfg['kind']=='CDF'", "cfg['kind'] in ('valid_pool_protection_v1','official_Top_protection_v2')")
    text = text.replace("codec=None if identity else 'CDF'", "codec=None if identity else cfg['kind']")
    text = text.replace('normalized149', 'normalized39').replace('complete149', 'complete39')
    text = text.replace('Normalize147 measured TRAIN comparisons and qualified175/188 anchors', 'Normalize37 measured TRAIN comparisons and qualified175/189 anchors')
    normal = save(NORMAL, text)
    qualified_source = A / 'qualify_three_cached_mixed149_selected_native14_v1_20261011.py'
    text = qualified_source.read_text(encoding='utf8')
    text = text.replace('three_cached_mixed149_selected_native14', 'near_protected39_selected_native14')
    text = text.replace('normalize_completed_three_cached_mixed149_after188_v1_20261011', Path(NORMAL).stem)
    text = text.replace('actual_three_cached_mixed149_after186_normalization_v1_20261011', 'actual_near_protected39_after189_normalization_v1_20261011')
    text = text.replace('three_cached_mixed_complete149_after188', 'near_protected_complete39_after189')
    text = text.replace('pilot149', 'pilot39').replace('==149', '==39').replace('(144,432)', '(36,108)')
    text = text.replace('three_cached_mixed_stage_selector_and_CPU11_sources_admission_v2_20261011', 'near_protected_stage_selector_and_CPU11_sources_admission_v1_20261011')
    text = text.replace('fully_qualified_anchor149', 'fully_qualified_anchor39').replace('full189', 'full190')
    compute = save(COMPUTE, text)
    wrapper = '''"""Reuse verified identical37 native14 controls, or execute changed39 selection."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from compute_near_protected39_selected_native14_v1_20261011 import OUT

def main():
    assert allowed();closed('actual_near_protected39_after189_normalization_v1_20261011')
    pointer=A/'actual_near_protected_complete39_after189_location_v1_20261011.json'
    pilot_path=Path(read(pointer)['output'])/'pilot39.json';pilot=read(pilot_path);best=pilot['best'];cfg=best['configuration']
    assert len(pilot['records'])==39
    if cfg['model'] is None:
        from compute_near_protected39_selected_native14_v1_20261011 import main as compute
        compute();return
    closed('actual_rank5_rank20_near_protected_selected_native14_v1_20261011')
    source=Path('E:/赛题五_本机临时/rank5_rank20_near_protected_selected_native14_v1_20261011/verification.json')
    previous=read(source);old=previous['best']['configuration']
    keys=('role','weight','sign','protect_fraction','rank5_weight')
    identical=old['kind']==cfg['codec'] and all(old[k]==cfg[k] for k in keys)
    if not identical:
        from compute_near_protected39_selected_native14_v1_20261011 import main as compute
        compute();return
    assert (previous['actual_native_cases'],previous['actual_cold_cases'],len(previous['prefit_rejections']))==(14,14,7)
    assert previous['actual_saved_states']==12
    for row in previous['records']:
        spec=row['configuration']
        assert spec['codec']==cfg['codec'] and spec['recipe']==cfg['recipe']
        assert all(spec[k]==cfg[k] for k in keys if k!='sign')
        assert spec['sign'] in (-1.,1.) and spec['original_complete_parent_round']==175
        assert row['native_independent_and_cold_bits_exact']
    pins={**pilot['input_sha256'],**previous['input_sha256'],str(source):sha(source),str(pointer):sha(pointer),str(pilot_path):sha(pilot_path),str(Path(__file__)):sha(__file__)}
    for p,d in pins.items():assert sha(p)==d,p
    assert allowed();OUT.mkdir(exist_ok=False)
    create(OUT/'pilot39.json',{**pilot,'input_sha256':pins,'normalization_source':str(pilot_path)})
    create(OUT/'verification.json',{'status':'passed_selected_near_protected39_six_pairs14_native14_cold7_prefit_refusals','best':best,'input_sha256':pins,'records':previous['records'],'prefit_rejections':previous['prefit_rejections'],'actual_saved_states':12,'actual_native_cases':14,'actual_cold_cases':14,'new_native_cases_by_this_qualifier':0,'qualification_mode':'verified_existing_identical_spec_parent175_native14','verified_native_source':str(source),'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,'full190_candidate_and_registration_pending':True})
    create(A/'actual_near_protected39_selected_native14_location_v1_20261011.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()
'''
    qualified = save(QUAL, wrapper)
    # Both paths must expose the same qualified39 status; the fallback was inherited.
    assert "'passed_selected_near_protected39_six_pairs14_native14_cold7_prefit_refusals'" in compute.read_text(encoding='utf8')
    assert "'passed_selected_fully_qualified_anchor39_no_new_native_stage_claimed'" in compute.read_text(encoding='utf8')
    paths = [Path(__file__), normal_source, qualified_source, normal, compute, qualified, A / PLAN,
             A / 'near_protected_stage_selector_and_CPU11_sources_admission_v1_20261011.json']
    proof = A / 'near_protected39_normalization_native14_sources_admission_v1_20261011.json'
    create(proof, {'status': 'compiled39_comparison_with175189_and_exact_native14_reuse_or_changed_selection_compute',
                   'input_sha256': {str(p): sha(p) for p in paths}, 'expected_records': 39,
                   'expected_full_controls': 36, 'expected_prefix_controls': 108,
                   'actual189_complete_not_yet_claimed': True, 'full190_factory_not_yet_created': True,
                   'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False})
    for name, driver in [('actual_near_protected39_after189_normalization_v1_20261011', normal),
                         ('actual_near_protected39_selected_native14_v1_20261011', qualified)]:
        assert allowed()
        row = start_service(name, driver.name, [], {str(driver): sha(driver), str(proof): sha(proof)})
        create(A / (name + '_activation.json'), row)
    print({'complete39_normalization_and_selected_qualification_queued': True,
           'new_quality_scores': 0, 'full190_factory_created': False}, flush=True)


if __name__ == '__main__':
    main()
