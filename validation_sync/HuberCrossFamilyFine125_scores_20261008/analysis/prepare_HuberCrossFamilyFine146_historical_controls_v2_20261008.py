"""Use the actual139 boundary winner to prepare untested signed fine weights on complete136."""
from pathlib import Path
import json
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def save_source(name, text):
    path = A / name
    compile(text, str(path), 'exec')
    with path.open('x', encoding='utf-8', newline='') as stream:
        stream.write(text)
    return path


def replace_once(text, before, after):
    assert text.count(before) == 1, before
    return text.replace(before, after)


def main():
    quality = A / 'HuberCrossFamily112_official_comparison_v1_20261008/verification.json'
    previous_plan = A / 'HuberCrossFamily112_round139_plan_v1_20261008.json'
    scored, plan = read(quality), read(previous_plan)
    winner = scored['best']
    assert len(scored['records']) == 112
    assert winner['configuration']['group'] == 4 and winner['configuration']['share'] == .5
    assert winner['configuration']['weight'] == .0025
    assert .0025 == min(c['amplitude'] for c in plan['new_cases'] if c['amplitude'] > 0)
    shares = [.25, .375, .5, .625, .75]
    magnitudes = [.00025, .0005, .00075, .001, .00125, .0015,
                  .00175, .002, .00225, .00275, .003, .00325]
    cases = [{'group': 4, 'share': share, 'amplitude': direction * amplitude}
             for share in shares for direction in (1, -1) for amplitude in magnitudes]
    old = {(c['group'], c['share'], c['amplitude']) for c in plan['new_cases']}
    assert len(cases) == len({(c['group'], c['share'], c['amplitude']) for c in cases}) == 120
    assert not old.intersection((c['group'], c['share'], c['amplitude']) for c in cases)
    heads = {h: plan['heads'][h] for h in winner['ordered_native_components']}
    assert set(heads) == {'huber_d010', 'huber_d025', 'bayes_diagonal'}
    parent = read(ROOT / 'candidates/optimization_20261003_r136/verification.json')
    assert parent['status'] == 'passed'
    assert 'nonflag_CPU_HuberCrossFamily_complete_parent_CDF' not in parent['whole_scheme_graph']
    assert read(A / 'optimization_20261003_r136/full_registration_execution.json')['status'] == 'passed'
    proposal = A / 'HuberCrossFamilyFine125_round146_proposal_v1_20261008.json'
    preserved = read(proposal)
    assert preserved['new_cases'] == cases and preserved['heads'] == heads
    assert preserved['scientific_stage_base_round'] == 136
    assert preserved['actual139_official_winner']['score'] == winner['connected_final_score']
    # Revalidate actual existing native evidence, preserving the limited2025 training-row scope.
    huber_path = Path('E:/赛题五_本机临时/nonflag_HuberIRLS64_bank10_v1_20261008/verification.json')
    huber = read(huber_path)
    assert huber['actual_native_fits'] == 10 and huber['actual_full_OOF_heads'] == 2
    cross_path = Path(read(A / 'actual_CrossFamily_bank30_synthetic_location_v1_20261008.json')['output']) / 'verification.json'
    cross = read(cross_path)
    records, pins = [], {str(p): sha(p) for p in [Path(__file__), proposal, huber_path, cross_path]}
    for head, row in heads.items():
        oof = Path(row['folder']) / 'oof_verification.json'
        proof = read(oof)
        assert proof['rows'] == 5635800
        if 'days' in proof: assert proof['days'] == 1212
        assert not proof['test_labels_read']
        pins[str(oof)] = sha(oof)
        pins[row['oof']] = sha(row['oof'])
        for year in range(2021, 2026):
            info_path = Path(row['infos'][str(year)])
            info = read(info_path)
            assert info['year'] == year and info['last_training_label_date'] < info['exclusive_cutoff']
            assert info['last_training_label_end'] <= info['exclusive_cutoff']
            for path, digest in ((info['native_model_path'], info['native_model_sha256']),
                                 (info['independent_' + row['state_kind'] + '_state_path'],
                                  info['independent_' + row['state_kind'] + '_state_sha256'])):
                assert sha(path) == digest
                pins[path] = digest
            pins[str(info_path)] = sha(info_path)
            if head.startswith('huber_'):
                native = next(r for r in huber['actual_models'] if r['name'] == info['name'] and r['year'] == year)
                assert native['native_reload_independent_all_prediction_bits_exact']
                actual_rows = native['prediction_control_rows']
            else:
                native = next(r for r in cross['actual_native_replay_records'] if r['head'] == head and r['year'] == year)
                assert native['full_saved_reloaded_independent_bits_exact']
                actual_rows = native['actual_rows']
            records.append({'head': head, 'year': year, 'actual_rows': actual_rows,
                            'full_saved_reloaded_independent_bits_exact': True,
                            'control_scope': 'own_full_nonflag_annual_OOF' if year < 2025 else 'own1000_training_rows_no_future_X',
                            'actual2025_future_X_read': False})
    assert len(records) == 15
    audit = Path('E:/赛题五_本机临时/HuberCrossFamilyFine15_existing_native_evidence_v1_20261008')
    assert not audit.exists()
    audit.mkdir()
    create(audit / 'verification.json', {'status': 'passed_actual15_existing_native_evidence_rehash_with2025_scope_retained',
        'actual_model_count': 15, 'actual_full_OOF_heads': 3, 'actual_native_replay_records': records,
        'input_sha256': pins, 'new_native_replay_claimed': False, 'new_native_fits': 0,
        'new_quality_scores': 0, 'test_labels_read': False})
    audit_pointer = A / 'actual_HuberCrossFamilyFine_bank15_location_v1_20261008.json'
    create(audit_pointer, {'output': str(audit), 'verification_sha256': sha(audit / 'verification.json'),
                         'new_native_fits': 0, 'new_future_inference': 0})
    codec_text = (A / 'HuberCrossFamily_complete_parent_CDF_v1_20261008.py').read_text(encoding='utf-8-sig')
    codec_text = replace_once(codec_text, 'assert group in range(len(GROUPS)) and share in (.25, .5, .75)',
                              'assert group == 4 and share in (.25, .375, .5, .625, .75)')
    codec_text = replace_once(codec_text, 'assert np.isfinite(amplitude) and 0. <= amplitude <= .1',
                              'assert np.isfinite(amplitude) and -.00325 <= amplitude <= .00325')
    codec = save_source('HuberCrossFamilyFine_complete_parent_CDF_v1_20261008.py', codec_text)
    stage_text = (A / 'HuberCrossFamily_complete_parent_native_stage_v1_20261008.py').read_text(encoding='utf-8-sig')
    stage_text = stage_text.replace('from HuberCrossFamily_complete_parent_CDF_v1_20261008 import',
                                    'from HuberCrossFamilyFine_complete_parent_CDF_v1_20261008 import')
    stage_text = replace_once(stage_text, "assert spec['amplitude']>0. and spec['amplitude']<=.1 and spec['share'] in (.25,.5,.75)",
                              "assert 0.<abs(spec['amplitude'])<=.00325 and spec['share'] in (.25,.375,.5,.625,.75)")
    stage = save_source('HuberCrossFamilyFine_complete_parent_native_stage_v1_20261008.py', stage_text)
    full_text = (A / 'verify_CrossFamilyFine121_full_historical_controls_v1_20261008.py').read_text(encoding='utf-8-sig')
    full_text = full_text.replace('CrossFamilyFine', 'HuberCrossFamilyFine').replace('parent134', 'parent136').replace('round145', 'round146')
    full_text = full_text.replace('_r134/', '_r136/').replace('round134_receipt', 'round136_receipt')
    full_text = full_text.replace('==134', '==136').replace(':134', ':136').replace('exact134', 'exact136')
    full_text = replace_once(full_text, "{'ridge_l001','ridge_l025','rff_g00625','rff_g0125'}", "{'huber_d010','huber_d025','bayes_diagonal'}")
    full_text = full_text.replace('actual_CrossFamily_bank30_synthetic_location_v1_20261008.json', audit_pointer.name)
    full_text = replace_once(full_text, "audit['actual_model_count']==30 and audit['actual_full_OOF_heads']==6",
                             "audit['actual_model_count']==15 and audit['actual_full_OOF_heads']==3")
    full_text = full_text.replace('len(selected)==20', 'len(selected)==15').replace('revalidated\':20', "revalidated':15")
    full = save_source('verify_HuberCrossFamilyFine121_full_historical_controls_v1_20261008.py', full_text)
    hook_text = (A / 'verify_CrossFamilyFine30_native_historical_hooks_v1_20261008.py').read_text(encoding='utf-8-sig')
    hook_text = hook_text.replace('CrossFamilyFine', 'HuberCrossFamilyFine').replace('round145', 'round146')
    hook_text = hook_text.replace('CrossFamily91_parent134_historical_full_controls_v1_20261008',
                                  'HuberCrossFamily109_current_parent_controls_v18_20261008')
    hook_text = hook_text.replace('_r134/', '_r136/').replace('actual_CrossFamily91_parent134_location_v1_20261008.json',
                                                            'actual_HuberCrossFamily109_current_parent_location_v18_20261008.json')
    hook_text = replace_once(hook_text, "read(proof)['actual_full_cases']==91 and read(proof)['actual_cold_cases']==273",
                             "read(proof)['actual_full_cases']==109 and read(proof)['actual_cold_cases']==327")
    hook_text = replace_once(hook_text, "'state_kind':kind,'path':info['native_model_path']",
                             "'state_kind':row['native_stage_state_kind'],'path':info['native_model_path']")
    hook_text = hook_text.replace('len(records)}/15', 'len(records)}/30').replace('actual15_historical', 'actual30_historical')
    hook = save_source('verify_HuberCrossFamilyFine30_native_historical_hooks_v1_20261008.py', hook_text)
    sources = [Path(__file__), proposal, audit_pointer, audit / 'verification.json', codec, stage, full, hook]
    controls_pins = {str(p): sha(p) for p in sources}
    create(A / 'HuberCrossFamilyFine146_historical_receiver_preparation_v1_20261008.json',
           {'status': 'prepared_signed_fine_Huber_controls_only_no146_quality_admission',
            'input_sha256': controls_pins, 'actual_existing_model_records_revalidated': 15,
            'full_cases_planned': 121, 'cold_controls_planned': 363, 'native_hooks_planned': 30,
            'historical_controls_not_a_complete146_candidate': True, 'new_quality_scores': 0, 'test_labels_read': False})
    launches = {
        'native': start('HuberCrossFamilyFine30_actual_native_historical_controls_v1_20261008', hook.name, [], controls_pins),
        'full': start('HuberCrossFamilyFine121_actual_full_historical_controls_v1_20261008', full.name, [], controls_pins)}
    create(A / 'HuberCrossFamilyFine146_historical_hidden_launches_v1_20261008.json',
           {'status': 'started_actual_historical_only_controls', 'launches': launches,
            'input_sha256': controls_pins, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'started', 'workers': {k: r['owned_worker_pid'] for k, r in launches.items()}}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
