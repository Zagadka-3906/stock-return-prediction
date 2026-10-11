"""Stage the actual36-fit GOSS closure; publish canonical markers only after queue retirement."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
SOURCE = A / 'gradient_sampling_memmap_complete_bank_v3_20261006'
FUTURE = A / 'gradient_sampling_memmap_future_qa_v3_20261006'
OUT = A / 'gradient_sampling_memmap_native_promotion_20261006'
SERVICE = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_complete_workflow_v3'
RECEIPT = A / 'gradient_sampling_memmap_complete_bank_v3_github_20261006/receipt.json'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def wait_for_closure():
    from run_dependency_queue_v3_20261006 import owned
    while not (SERVICE / 'service_execution.json').exists():
        assert owned(read(SERVICE / 'native_launch.json')), 'Native worker missing without terminal evidence.'
        time.sleep(10)
    assert read(SERVICE / 'service_execution.json')['status'] == 'passed'
    while owned(read(SERVICE / 'native_launch.json')):
        time.sleep(.2)
    publication = A / 'service_owned_workflows_20261006/gradient_sampling_memmap_complete_bank_v3_publication'
    while not RECEIPT.exists():
        assert owned(read(publication / 'native_launch.json')), 'Publication missing without verified receipt.'
        time.sleep(10)
    receipt = read(RECEIPT)
    assert receipt['status'] == 'pushed_actual_controls_main_only'
    assert receipt['control_status'] == 'passed' and receipt['raw_git_blobs_verified'] > 0
    # Wait for final source re-verification before taking a read lock on the bank.
    while owned(read(publication / 'native_launch.json')):
        time.sleep(.2)
    assert read(publication / 'service_execution.json')['status'] == 'passed'
    return receipt


def stage():
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    import train_gradient_sampling_bank_20261005 as original
    assert not OUT.exists()
    audit, proof = read(SOURCE / 'oof_audit.json'), read(FUTURE / 'verification.json')
    assert audit['status'] == proof['status'] == 'passed'
    assert audit['actual_annual_fits'] == audit['actual300_round_complete_models'] == 30
    assert audit['configurations'] == original.CONFIGS and len(proof['checks']) == 6
    assert proof['actual_full_final_fits'] == 6 and proof['new_native_fits_by_this_verifier'] == 0
    assert read(SOURCE / 'training_execution_scope.json')['status'] == read(FUTURE / 'execution_scope.json')['status'] == 'passed'
    destination = Path(read(original.STORAGE)['output_directory']).resolve()
    target_future = A / 'gradient_sampling_future_qa_20261005'
    assert destination.is_relative_to(A) and destination.drive.upper() == 'D:' and destination != SOURCE
    assert not destination.exists() or not list(destination.iterdir())
    assert not target_future.exists()
    source_files = [p for p in SOURCE.rglob('*') if p.is_file() and p.suffix in ('.json', '.jsonl', '.joblib', '.parquet')]
    future_files = [p for p in FUTURE.rglob('*') if p.is_file()]
    pins = [Path(__file__), RECEIPT, SERVICE / 'service_execution.json', original.STORAGE,
        A / 'gradient_sampling_complete_search_plan_20261005.json', Path(original.__file__),
        A / 'gradient_sampling_model_sources_20261005.py', A / 'gradient_sampling_scheme_runtime_20261005.py']
    bindings = {str(p.resolve()): sha(p) for p in dict.fromkeys([*source_files, *future_files, *pins])}
    OUT.mkdir()
    create(OUT / 'frozen_before_artifact_staging.json', {'input_sha256': bindings,
        'actual_existing_annual_fits': 30, 'actual_existing_final_fits': 6,
        'copies_not_additional_fits': True, 'original262_grid_and74_75_parents_unchanged': True,
        'canonical_markers_not_exposed_until_original_scheduler_retired': True})
    copied = []
    with LockedReadHashCache(bindings) as cache:
        for name, cfg in original.CONFIGS.items():
            assert audit['entire_original_five_year_prediction_coverage'][name] == {
                **audit['entire_original_five_year_prediction_coverage'][name], 'rows': 5635800, 'days': 1212, 'codes': 4650}
            for year in range(2020, 2026):
                info = read(SOURCE / name / f'info_{year}.json')
                assert info['status'] == 'passed' and info['actual_native_boosting_iterations'] == 300
                assert info['configuration'] == cfg and info['native_objective'] == 'regression'
                label = 'rank' if cfg['target'] == 'y_rank' else 'return'
                assert info['training_meta'] == read(A / f'linear_bank_20261003/{label}_ridge_l01/info_{year}.json')['training_meta']
                assert cache.sha(SOURCE / name / f'model_{year}.joblib') == info['model_sha256']
                if year < 2025:
                    assert cache.sha(SOURCE / name / f'raw_{year}.parquet') == info['prediction_sha256']
                    assert read(SOURCE / f'boundary_control_{name}_{year}.json')['status'] == 'passed'
                    assert read(SOURCE / f'prefix_control_{name}_{year}.json')['status'] == 'passed'
                else:
                    assert info['copied_file_is_not_an_additional_native_fit']
        for check in proof['checks']:
            assert check['actual_full1599600_row_reload_bit_identical'] and check['actual_cold80_day_prefix_bit_identical']
            assert check['source_capacity_predictions_bit_identical_all1599600_rows']
            assert cache.sha(FUTURE / f"{check['model']}_raw.parquet") == check['raw_sha256']
        for base, stage_name, files in ((SOURCE, 'staged_bank', source_files), (FUTURE, 'staged_future', future_files)):
            for source in files:
                target = OUT / stage_name / source.relative_to(base)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
                digest = cache.sha(source)
                assert sha(target) == digest
                copied.append({'source': str(source), 'staged_path': str(target), 'sha256': digest, 'bytes': target.stat().st_size})
        # The original complete-scheme runtime explicitly requires these six final paths.
        for name in original.CONFIGS:
            source, target = SOURCE / name / 'model_2025.joblib', OUT / 'staged_future' / f'{name}.joblib'
            assert not target.exists()
            shutil.copyfile(source, target)
            digest = cache.sha(source)
            assert sha(target) == digest
            copied.append({'source': str(source), 'staged_path': str(target), 'sha256': digest, 'bytes': target.stat().st_size})
        cache.reverify()
    create(OUT / 'staging_verification.json', {'status': 'passed_actual36_fit_staging_no_canonical_markers_exposed',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': bindings, 'copied_artifacts': copied,
        'canonical_bank': str(destination), 'canonical_future': str(target_future),
        'actual_annual_native_fits': 30, 'actual_final_native_fits': 6,
        'new_native_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    return destination, target_future


def expose(destination, target_future, handoff_commit):
    assert read(handoff_commit)['status'] == 'retired_original_controller_and_preserved_scientific_workers'
    assert not (OUT / 'verification.json').exists()
    # The scheduler's additional promotion gate holds every dispatch until this proof exists.
    if destination.exists():
        assert not list(destination.iterdir())
        destination.rmdir()
    assert not target_future.exists()
    (OUT / 'staged_bank').rename(destination)
    (OUT / 'staged_future').rename(target_future)
    import gradient_sampling_model_sources_20261005 as router
    import gradient_sampling_scheme_runtime_20261005 as runtime
    routes = []
    for name in router.NEW_CONFIGS:
        for year in range(2020, 2026):
            path = router.model_path(name, year)
            assert path.resolve() == (destination / name / f'model_{year}.joblib').resolve()
            assert sha(path) == read(SOURCE / name / f'info_{year}.json')['model_sha256']
            routes.append({'model': name, 'year': year, 'path': str(path), 'sha256': sha(path)})
        graph = {'root': {'kind': 'standalone', 'round': 76, 'configuration': {'standalone': {'model': name}}}, 'layers': []}
        resolved = runtime.native_sources(graph)
        assert set(resolved) == {name} and Path(resolved[name]['path']).resolve() == (target_future / f'{name}.joblib').resolve()
        assert resolved[name]['sha256'] == read(SOURCE / name / 'info_2025.json')['model_sha256']
    staged = read(OUT / 'staging_verification.json')
    for row in staged['copied_artifacts']:
        path = Path(row['staged_path'])
        base, target = (OUT / 'staged_bank', destination) if path.is_relative_to(OUT / 'staged_bank') else (OUT / 'staged_future', target_future)
        assert sha(target / path.relative_to(base)) == row['sha256']
    create(OUT / 'verification.json', {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_annual_native_fits': 30, 'actual_final_native_fits': 6, 'actual_native_fits_by_promotion': 0,
        'actual_all36_original_native_routes_checked': routes,
        'actual_all6_original_complete_scheme_final_routes_checked': True,
        'byte_identical_original_configs_models_raw_predictions_and_all_future_controls_exposed': True,
        'native_main_receipt': read(RECEIPT), 'queue_handoff_commit': str(handoff_commit),
        'original262_quality_records_and74_75_parents_preserved': True,
        'complete262_quality_freeze_causal_inference_and_full_rankings_still_pending': True,
        'new_quality_scores': 0, 'test_labels_read': False, 'global_resource_boundary_established': False})
