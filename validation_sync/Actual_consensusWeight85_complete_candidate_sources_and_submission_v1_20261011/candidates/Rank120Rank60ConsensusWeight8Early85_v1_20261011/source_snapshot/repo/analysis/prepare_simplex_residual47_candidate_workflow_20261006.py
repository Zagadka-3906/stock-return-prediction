"""Prepare unique saved-model storage and exact repeated-addition weighted replay."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import create, sha, read


def main():
    stems = ['predict_longer_residual74_native_scheme_20261006',
        'freeze_and_infer_longer_residual74_candidate_20261006',
        'freeze_longer_residual74_candidate_sources_20261006',
        'seal_longer_residual74_candidate_source_package_20261006',
        'admit_longer_residual74_candidate_20261006',
        'wait_and_seal_longer_residual74_candidate_20261006',
        'launch_longer_residual74_candidate_workflow_20261006']
    names = {s+'.py': s.replace('longer_residual74','simplex_residual47')+'.py' for s in stems}
    changes = {
        'conditional_residual128_256_comparison74_20261006': 'residual_simplex47_official_comparison_20261006',
        'conditional_residual128_256_comparison74': 'residual_simplex47_official_comparison',
        'conditional_residual128_256_scores74_evidence_publication': 'residual_simplex47_scores_evidence_publication',
        'passed_actual74_matched128_256_residual_and_ensemble_full_official_comparisons':
            'passed_actual47_convex_simplex_residual_ensemble_full_official_comparisons',
        'longer_residual74': 'simplex_residual47',
        'qualified102_anchor_score': 'selected74_anchor_score',
        'score_gain_over_qualified102_anchor': 'score_gain_over_selected74_anchor',
        'expected_scored_records=74': 'expected_scored_records=47',
        "'scored_records': 74": "'scored_records': 47",
        '== 74': '== 47', 'all74': 'all47', 'full74': 'full47', 'actual74': 'actual47',
        'selected74-case': 'selected47-case', 'Actual74-case': 'Actual47-case',
        'owned74_candidate': 'owned47_candidate',
    }
    generated,pins,routes={},{},[]
    for old,new in names.items():
        original=(A/old).read_text(encoding='utf-8')
        text,effective=original,{}
        for before in sorted(changes,key=len,reverse=True):
            if before in text:
                text=text.replace(before,changes[before]);effective[before]=changes[before]
        if old.startswith('freeze_and_infer_'):
            before="    names = pilot['ensembles'].get(cfg['model'], [cfg['model']])"
            assert text.count(before)==1
            text=text.replace(before,
                "    ordered_entries = pilot['ensembles'].get(cfg['model'], [cfg['model']])\n"
                "    names = list(dict.fromkeys(ordered_entries))\n"
                "    repeat_counts = {name: ordered_entries.count(name) for name in names}\n"
                "    assert ordered_entries == [name for name in names for _ in range(repeat_counts[name])]\n"
                "    if cfg['model'] in pilot['ensemble_integer_weights']:\n"
                "        assert len(ordered_entries) == 4\n"
                "        assert [repeat_counts.get(name, 0) for name in pilot['ordered_unique_native_components']] == pilot['ensemble_integer_weights'][cfg['model']]\n"
                "    else:\n"
                "        assert cfg == pilot['records'][1]['configuration'] and len(ordered_entries) == 3\n")
            before="'ensemble_rule': 'declared component order sum then divide by component count',"
            assert text.count(before)==1
            text=text.replace(before,
                "'ensemble_rule': 'declared unique component order, repeat-add each native prediction, divide by total entry count',\n"
                "            'component_repeat_counts': repeat_counts, 'original_ordered_ensemble_entries': ordered_entries,")
            before="'native_component_names': names,"
            assert before in text
            text=text.replace(before,before+" 'component_repeat_counts': repeat_counts,")
        if old.startswith('predict_'):
            before="    assert 1 <= len(components) <= 4 and spec['weight'] > 0"
            assert text.count(before)==1
            text=text.replace(before,before+
                "\n    repeat_counts = spec['component_repeat_counts']\n"
                "    assert list(repeat_counts) == [c['name'] for c in components]\n"
                "    assert all(type(n) is int and 1 <= n <= 4 for n in repeat_counts.values())\n"
                "    denominator = sum(repeat_counts.values())\n"
                "    assert denominator in (3, 4)\n"
                "    assert spec['original_ordered_ensemble_entries'] == [c['name'] for c in components for _ in range(repeat_counts[c['name']])]\n")
            before="        assert cfg['weight'] == spec['weight'] and cfg['model'] == spec['model']"
            assert text.count(before)==1
            text=text.replace(before,before+"\n        assert cfg['component_repeat_counts'] == repeat_counts")
            before="            combined += primary\n            independent_combined += independent"
            assert text.count(before)==1
            text=text.replace(before,
                "            for _ in range(repeat_counts[component['name']]):\n"
                "                combined += primary\n"
                "                independent_combined += independent")
            before="        combined /= len(components)\n        independent_combined /= len(components)"
            assert text.count(before)==1
            text=text.replace(before,"        combined /= denominator\n        independent_combined /= denominator")
            text=text.replace("'native_independent_equal_mean_and_full_transform_bits_exact': True,",
                "'native_independent_ordered_weighted_mean_and_full_transform_bits_exact': True,\n"
                "            'component_repeat_counts': repeat_counts, 'actual_denominator': denominator,")
        if old.startswith('admit_'):
            before="'residual_simplex47_official_comparison', 'residual_simplex47_scores_evidence_publication')"
            assert text.count(before)==1
            text=text.replace(before,"'residual_simplex47_official_comparison',)")
            text=text.replace('waiting_for_full47_official_scores_and_main_and_memory','waiting_for_full47_official_scores_and_memory')
            before="'native_component_count_follows_selected_winner': True,"
            assert text.count(before)==1
            text=text.replace(before,before+"\n        'main_score_publication_independently_serialized_after_full105': True,")
        compile(text,str(A/new),'exec')
        generated[new]=text;pins[str(A/old)]=sha(A/old)
        routes.append({'source':old,'target':new,'explicit_route_replacements':effective})
    frozen=A/'residual_simplex47_frozen_before_hidden_launch_20261006.json'
    declared=read(frozen)
    assert declared['expected_scored_records']==47
    assert len(declared['integer_weight_triples'])==15
    evidence=[Path(__file__),frozen,A/'run_residual_simplex47_official_comparison_20261006.py',
        A/'publish_residual_simplex47_scores_20261006.py',
        A/'residual_simplex47_hidden_admission_20261006.json',
        A/'conditional_flag_residual_extrapolation_transform_20261006.py',
        A/'conditional_residual128_256_bank40_20261006/verification.json',
        A/'conditional_flag_residual_bank_20261006/verification.json']
    pins.update({str(p):sha(p) for p in evidence})
    for new in generated:
        assert not (A/new).exists(),new
    for new,text in generated.items():
        with (A/new).open('x',encoding='utf-8') as stream:stream.write(text)
        pins[str(A/new)]=sha(A/new)
    create(A/'simplex_residual47_candidate_workflow_preparation_20261006.json',{
        'status':'prepared_actual47_declared_convex_ensemble_saved_native_full_cold_and_independent_replay',
        'input_sha256':pins,'routes':routes,
        'actual_final_selection_pending_all47_original_official_scores':True,
        'integer_convex_weight_order_and_repeated_float64_addition_preserved':True,
        'saved_model_storage_and_native_controls_count_unique_components_only':True,
        'source_package_complete_all_local_Python_freeze_before_inference':True,
        'all_original_two_full1599600_and_cold372000_and_independent_CSV_controls_preserved':True,
        'main_score_publication_independent_from_candidate_admission_to_save_deadline_time':True,
        'full_ranking_registration_and_main_candidate_publication_still_required':True,
        'new_native_fits_by_preparation':0,'new_quality_scores_by_preparation':0,'test_labels_read':False})


if __name__=='__main__':main()
