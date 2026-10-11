"""Version the FM router and waiting workflows without rewriting frozen evidence."""
from pathlib import Path
import ast
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def clone(old, new, replacements):
    source, target = A / old, A / new
    data = source.read_text(encoding='utf-8')
    for previous, updated in replacements:
        assert previous in data, (old, previous)
        data = data.replace(previous, updated)
    ast.parse(data)
    if target.exists():
        assert target.read_bytes() == data.encode('utf-8'), target
    else:
        target.write_text(data, encoding='utf-8', newline='')
    return {'original_source': str(source), 'original_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'new_source': str(target), 'new_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}


def main():
    rows = []
    rows.append(clone('factorization_machine_model_sources_20261005.py', 'factorization_machine_model_sources_v2_20261005.py', [
        ('Route matched LightGBM leaf models and every inherited native family.', 'Route actual FM weights and every inherited native family by their saved kind.'),
        ("bundle['kind']=='lightgbm_factorization_machine'", "bundle['kind']=='factorization_machine'")]))
    rows.append(clone('factorization_machine_scheme_runtime_20261005.py', 'factorization_machine_scheme_runtime_v2_20261005.py', [
        ('factorization_machine_model_sources_20261005', 'factorization_machine_model_sources_v2_20261005'),
        ('factorization_machine_future_qa_20261005', 'factorization_machine_future_qa_v2_20261005')]))
    rows.append(clone('predict_factorization_machine_scheme_20261005.py', 'predict_factorization_machine_scheme_codec_v2_20261005.py', [
        ('factorization_machine_model_sources_20261005.py', 'factorization_machine_model_sources_v2_20261005.py'),
        ('factorization_machine_scheme_runtime_20261005.py', 'factorization_machine_scheme_runtime_v2_20261005.py'),
        ('factorization_machine_search_engine_v2_20261005.py', 'factorization_machine_search_engine_v4_20261005.py')]))
    rows.append(clone('predict_factorization_machine_scheme_v3_20261005.py', 'predict_factorization_machine_scheme_v4_20261005.py', [
        ('predict_factorization_machine_scheme_20261005', 'predict_factorization_machine_scheme_codec_v2_20261005'),
        ('factorization_machine_search_engine_v3_20261005', 'factorization_machine_search_engine_v4_20261005'),
        ('predict_factorization_machine_scheme_v3_20261005', 'predict_factorization_machine_scheme_v4_20261005'),
        ("{ns.NUMBER}_v3.py", "{ns.NUMBER}_v4.py")]))
    rows.append(clone('factorization_machine_search_engine_v3_20261005.py', 'factorization_machine_search_engine_v4_20261005.py', [
        ('factorization_machine_scheme_runtime_20261005', 'factorization_machine_scheme_runtime_v2_20261005'),
        ('factorization_machine_future_qa_20261005', 'factorization_machine_future_qa_v2_20261005'),
        ('factorization_machine_search_generator_preflight_v3_20261005', 'factorization_machine_search_generator_preflight_v4_20261005'),
        ('predict_factorization_machine_scheme_v3_20261005', 'predict_factorization_machine_scheme_v4_20261005'),
        ("{number}_v3.py", "{number}_v4.py"), ("{number}_v3_pipeline.py", "{number}_v4_pipeline.py"),
        ('factorization_machine_model_sources_20261005', 'factorization_machine_model_sources_v2_20261005'),
        ('run_factorization_machine_round_v3_20261005', 'run_factorization_machine_round_v4_20261005'),
        ('verify_factorization_machine_search_generators_v3_20261005', 'verify_factorization_machine_search_generators_v4_20261005')]))
    rows.append(clone('run_factorization_machine_round_v3_20261005.py', 'run_factorization_machine_round_v4_20261005.py', [
        ('factorization_machine_future_qa_20261005', 'factorization_machine_future_qa_v2_20261005'),
        ('factorization_machine_search_generator_preflight_v3_20261005', 'factorization_machine_search_generator_preflight_v4_20261005'),
        ('factorization_machine_quality_run_20261005', 'factorization_machine_quality_run_v4_20261005'),
        ("{number}_v3", "{number}_v4"),
        ('predict_factorization_machine_scheme_v3_20261005', 'predict_factorization_machine_scheme_v4_20261005')]))
    for number in (73, 74):
        replacements = [('factorization_machine_search_engine_v3_20261005', 'factorization_machine_search_engine_v4_20261005')]
        if number == 74:
            replacements.append(('optimize_training_round73_v3', 'optimize_training_round73_v4'))
        rows.append(clone(f'optimize_training_round{number}_v3.py', f'optimize_training_round{number}_v4.py', replacements))
        rows.append(clone(f'run_training_round{number}_v3_pipeline.py', f'run_training_round{number}_v4_pipeline.py', [
            ('run_factorization_machine_round_v3_20261005', 'run_factorization_machine_round_v4_20261005')]))
    rows.append(clone('verify_factorization_machine_search_generators_v3_20261005.py', 'verify_factorization_machine_search_generators_v4_20261005.py', [
        ('factorization_machine_search_generator_preflight_v3_20261005', 'factorization_machine_search_generator_preflight_v4_20261005'),
        ("{n}{suffix}", "{n}{suffix}"),
        ("'_v3'", "'_v4'"), ("'_v3_pipeline'", "'_v4_pipeline'"),
        ("{number}_v3", "{number}_v4"),
        ('factorization_machine_scheme_runtime_20261005', 'factorization_machine_scheme_runtime_v2_20261005')]))
    rows.append(clone('verify_factorization_machine_full_future_20261005.py', 'verify_factorization_machine_full_future_v2_20261005.py', [
        ('factorization_machine_future_qa_20261005', 'factorization_machine_future_qa_v2_20261005'),
        ('factorization_machine_model_sources_20261005', 'factorization_machine_model_sources_v2_20261005'),
        ('factorization_machine_future_run_20261005', 'factorization_machine_future_run_v2_20261005'),
        ('                info = bank.train_one(name, 2025)', "                fit_existed = (bank.OUT / name / 'info_2025.json').exists()\n                info = bank.train_one(name, 2025)"),
        ("checks.append({'model': name,", "checks.append({'model': name, 'fit_artifact_existed_before_this_execution': fit_existed,"),
        ("'actual_fulltraining_fits': len(checks),", "'actual_fulltraining_fits': len(checks),\n        'new_fulltraining_fits_this_execution': sum(not row['fit_artifact_existed_before_this_execution'] for row in checks),\n        'original_failed_fullfuture_evidence_preserved': True,")]))
    rows.append(clone('publish_factorization_machine_completed_native_20261005.py', 'publish_factorization_machine_completed_native_v2_20261005.py', [
        ('factorization_machine_future_qa_20261005', 'factorization_machine_future_qa_v2_20261005'),
        ('factorization_machine_native_github_run_20261005', 'factorization_machine_native_github_run_v2_20261005'),
        ('factorization_machine_native_github_state_20261005', 'factorization_machine_native_github_state_v2_20261005')]))
    rows.append(clone('refresh_optimization_boundary_evidence_v7_20261005.py', 'refresh_optimization_boundary_evidence_v8_20261005.py', [
        ('factorization_machine_future_qa_20261005', 'factorization_machine_future_qa_v2_20261005'),
        ('factorization_machine_search_generator_preflight_v3_20261005', 'factorization_machine_search_generator_preflight_v4_20261005')]))
    rows.append(clone('monitor_actual_optimization_progress_v8_20261005.py', 'monitor_actual_optimization_progress_v9_20261005.py', [
        ('refresh_optimization_boundary_evidence_v7_20261005', 'refresh_optimization_boundary_evidence_v8_20261005'),
        ('actual_optimization_monitor_run_v8_20261005', 'actual_optimization_monitor_run_v9_20261005'),
        ('factorization_machine_future_qa_20261005', 'factorization_machine_future_qa_v2_20261005'),
        ('factorization_machine_search_generator_preflight_v3_20261005', 'factorization_machine_search_generator_preflight_v4_20261005')]))
    with (A / 'factorization_machine_v4_router_source_repair_20261005.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'created_versioned_router_and_unstarted_workflow_repairs',
                   'original_frozen_sources_not_modified': True, 'actual30_annual_fits_not_restarted': True,
                   'source_revisions': rows, 'planned_records_preserved': {'73': 124, '74': 138},
                   'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
    print(json.dumps({'created_sources': len(rows), 'new_quality_scores': 0}), flush=True)


if __name__ == '__main__':
    main()
