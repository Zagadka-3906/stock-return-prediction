"""Preserve complete ranking and QA for all50 actual robust residual comparisons."""
from pathlib import Path
import ast
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import create, sha, read


def main():
    names = {
        'register_longer_residual74_round104_artifacts_20261006.py': 'register_robust_residual50_round105_artifacts_20261006.py',
        'optimize_training_round104.py': 'optimize_training_round105.py',
        'finalize_training_round104.py': 'finalize_training_round105.py',
        'run_longer_residual74_round104_full_registration_20261006.py': 'run_robust_residual50_round105_full_registration_20261006.py',
        'publish_longer_residual74_round104_full_validation_20261006.py': 'publish_robust_residual50_round105_full_validation_20261006.py',
        'build_lossless_ranking_display_v13_20261006.py': 'build_lossless_ranking_display_v14_20261006.py',
        'verify_lossless_ranking_display_v15_20261006.py': 'verify_lossless_ranking_display_v16_20261006.py',
        'lossless_ranking_runtime_adapter_v12_20261006.py': 'lossless_ranking_runtime_adapter_v13_20261006.py',
    }
    changes = {
        **{old.removesuffix('.py'): new.removesuffix('.py') for old, new in names.items()},
        'conditional_residual128_256_comparison74_20261006': 'robust_conditional_residual_comparison50_v2_20261006',
        'passed_actual74_matched128_256_residual_and_ensemble_full_official_comparisons':
            'passed_actual50_matched_L1_Huber_residual_and_ensemble_full_official_comparisons',
        'longer_residual74': 'robust_residual50',
        'lossless_ranking_display_qa_v15_20261006': 'lossless_ranking_display_qa_v16_20261006',
        'ranking_display_qa_v15_20261006': 'ranking_display_qa_v16_20261006',
        'collect(104, 15, 74)': 'collect(105, 16, 50)',
        "namespace['snapshot'](104)": "namespace['snapshot'](105)",
        'publish(104,': 'publish(105,', 'lossless(104)': 'lossless(105)',
        'assert number == 104': 'assert number == 105',
        'actual_complete_QA_version=15': 'actual_complete_QA_version=16',
        "'actual_full_QA_version': 15": "'actual_full_QA_version': 16",
        'round104': 'round105', '_r104': '_r105', 'NUMBER = 104': 'NUMBER = 105',
        'WAVES = (387,)': 'WAVES = (388,)', 'wave=387': 'wave=388',
        'wave387_results': 'wave388_results', "'waves': [387]": "'waves': [388]",
        "'round': 104": "'round': 105", '== 74': '== 50',
        "'expected_scored_records': 74": "'expected_scored_records': 50",
        "'existing_actual_official_records': 74": "'existing_actual_official_records': 50",
        "'existing_official_scores_registered': 74": "'existing_official_scores_registered': 50",
        "'scored_records': 74": "'scored_records': 50",
        "'original_official_pilot_records_registered': 74": "'original_official_pilot_records_registered': 50",
        "'actual_native_bank_fits': 40": "'actual_native_bank_fits': 20, 'actual_new_native_fits_recovery': 19, 'actual_original_fit_reused': 1",
        'all74': 'all50', 'actual74': 'actual50', 'Register74': 'Register50', 'the74': 'the50',
        'official74_scores': 'official50_scores', 'the74 ': 'the50 ',
        'actual_longer_residual104_complete': 'actual_robust_residual105_complete',
        '第104轮': '第105轮', '既有74项': '既有50项',
        '预定74项128与256棵树条件残差及集成官方比较': '预定50项L1与Huber条件残差及集成官方比较',
        '74项128与256棵树条件残差及集成验证': '50项L1与Huber条件残差及集成验证',
    }
    pins, generated, routes = {}, {}, []
    for old, new in names.items():
        original = (A / old).read_text(encoding='utf-8')
        text, effective = original, {}
        for before in sorted(changes, key=len, reverse=True):
            if before in text:
                text = text.replace(before, changes[before])
                effective[before] = changes[before]
        if old.startswith('register_'):
            before = "        cfg = deepcopy(measured['configuration'])"
            assert text.count(before) == 1
            text = text.replace(before, before +
                "\n        component_names = pilot['ensembles'].get(cfg['model'], [cfg['model']]) if cfg['weight'] else []\n"
                "        component_banks = {}\n"
                "        for name in component_names:\n"
                "            if name.startswith('robust_residual_'):\n"
                "                assert name.endswith('_e128')\n"
                "                component_banks[name] = A / 'robust_conditional_residual_bank20_v2_20261006'\n"
                "            else:\n"
                "                assert name.startswith('flag_residual_') and name.endswith(('_e64', '_e128', '_e256'))\n"
                "                component_banks[name] = A / ('conditional_flag_residual_bank_20261006' if name.endswith('_e64') else 'conditional_residual128_256_bank40_20261006')\n"
                "        for name, folder in component_banks.items():\n"
                "            info_path = folder / name / 'info_2025.json'\n"
                "            assert read(info_path)['name'] == name\n"
                "            pins[str(info_path)] = sha(info_path)\n")
            before = "'actual_annual_native_bank': measured['native_bank_source'],"
            assert text.count(before) == 1
            text = text.replace(before,
                "'original_pilot_native_bank_metadata': measured['native_bank_source'],\n"
                "                'actual_annual_native_component_banks': {name: str(folder) for name, folder in component_banks.items()},")
            before = "'actual40_native_bank_source': str(A / 'conditional_residual128_256_bank40_20261006/verification.json'),"
            assert text.count(before) == 1
            text = text.replace(before, before +
                "\n        'actual20_matched_L1_Huber_native_bank_source': str(A / 'robust_conditional_residual_bank20_v2_20261006/verification.json'),\n"
                "        'actual_identity_codec_recovery_preflight': str(A / 'robust_conditional_residual_codec_recovery_preflight_20261006.json'),")
            before = "'actual_all_annual_mature_native_and_independent_codec_and_prefix_controls': str(A / 'conditional_residual128_256_bank40_20261006/verification.json'),"
            assert text.count(before) == 1
            text = text.replace(before,
                "'actual_all_annual_mature_robust_native_and_independent_codec_and_prefix_controls': str(A / 'robust_conditional_residual_bank20_v2_20261006/verification.json'),\n"
                "        'actual_original74_anchor_mature_native_controls': str(A / 'conditional_residual128_256_bank40_20261006/verification.json'),")
        if old.startswith('publish_'):
            before = "    for path in extra:"
            assert text.count(before) == 1
            text = text.replace(before,
                "    robust = A / 'robust_conditional_residual_bank20_v2_20261006'\n"
                "    extra += list(robust.glob('*.json'))\n"
                "    extra += list(robust.glob('*/info_*.json'))\n"
                "    extra += list(robust.glob('*/matched_L2_reference_*_verification.json'))\n"
                "    extra += [A / 'robust_conditional_residual_codec_recovery_preflight_20261006.json',\n"
                "        A / 'robust_conditional_residual20_recovery_audit_20261006.json',\n"
                "        A / 'robust_conditional_residual_codec_recovery_v2_hidden_workflows_20261006.json',\n"
                "        A / 'robust_conditional_residual_bank_github_v2_20261006/receipt.json',\n"
                "        A / 'robust_conditional_residual_scores_github_v2_20261006/receipt.json']\n"
                "    for name in ('robust_conditional_residual_native_bank20', 'robust_conditional_residual_comparison50',\n"
                "        'robust_conditional_residual_bank20_evidence_publication', 'robust_conditional_residual_scores50_evidence_publication',\n"
                "        'robust_conditional_residual_native_bank20_v2', 'robust_conditional_residual_comparison50_v2',\n"
                "        'robust_conditional_residual_bank20_evidence_publication_v2', 'robust_conditional_residual_scores50_evidence_publication_v2'):\n"
                "        service = A / 'service_owned_workflows_20261006' / name\n"
                "        extra += list(service.glob('*.json'))\n"
                "        extra += list(service.glob('*.log'))\n"
                + before)
        if old.startswith(('build_lossless_', 'verify_lossless_', 'lossless_ranking_runtime_')):
            restored = text
            for before in sorted(effective, key=len, reverse=True):
                restored = restored.replace(effective[before], before)
            assert restored == original, 'Full ranking/browser QA logic must remain unchanged'
        compile(text, str(A / new), 'exec')
        generated[new] = text
        pins[str(A / old)] = sha(A / old)
        routes.append({'source': old, 'target': new, 'explicit_replacements': effective})
    runner = ast.parse(generated['run_robust_residual50_round105_full_registration_20261006.py'])
    for name in ('publish', 'lossless'):
        assert [n.args[0].value for n in ast.walk(runner) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name] == [105]
    publisher = ast.parse(generated['publish_robust_residual50_round105_full_validation_20261006.py'])
    assert [[a.value for a in n.args] for n in ast.walk(publisher) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'collect'] == [[105, 16, 50]]
    assert [n.args[0].value for n in ast.walk(publisher) if isinstance(n, ast.Call) and isinstance(n.func, ast.Subscript) and isinstance(n.func.slice, ast.Constant) and n.func.slice.value == 'snapshot'] == [105]
    optimizer = ast.parse(generated['optimize_training_round105.py'])
    constants = {target.id: node.value.value for node in optimizer.body if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) for target in node.targets if isinstance(target, ast.Name)}
    assert constants['NUMBER'] == 105 and constants['PREVIOUS_NUMBER'] == 100
    for new in generated:
        assert not (A / new).exists(), new
    prep = A / 'robust_residual50_candidate_workflow_preparation_20261006.json'
    pins.update(read(prep)['input_sha256'])
    pins[str(prep)] = sha(prep)
    pins[str(Path(__file__))] = sha(Path(__file__))
    admission = A / 'admit_robust_residual50_round105_full_registration_20261006.py'
    compile(admission.read_text(encoding='utf-8'), str(admission), 'exec')
    pins[str(admission)] = sha(admission)
    for new, text in generated.items():
        with (A / new).open('x', encoding='utf-8') as stream:
            stream.write(text)
        pins[str(A / new)] = sha(A / new)
    create(A / 'robust_residual50_full_registration_preparation_20261006.json', {
        'status': 'prepared_actual50_independent_parent100_branch_full105_QA16',
        'input_sha256': pins, 'routes': routes,
        'actual_AST_collect': [105, 16, 50], 'actual_AST_publish_lossless_snapshot_round': 105,
        'explicit_training_parent_round': 100,
        'selected74_anchor_and_actual_component_bank_provenance_preserved': True,
        'same_selected_saved_component_graph_and_exact_metric_capsules_required': True,
        'complete_six_views_browser45s_all_values_full_source_provenance_and_candidate_QA_preserved': True,
        'all_three_native_banks_and_actual_failures_recovery_evidence_preserved': True,
        'global_direction_or_resource_exhaustion_claimed': False,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
    })


if __name__ == '__main__':
    main()
