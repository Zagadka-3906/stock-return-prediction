"""Count actual new bank artifacts separately from the older143-config cost inventory."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import psutil

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def owned(run):
    try:
        process = psutil.Process(run['pid'])
        return any(Path(part).name == Path(run['script']).name for part in process.cmdline())
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def main():
    storage_path = ROOT / 'analysis/nystrom_tuning_storage_20261005.json'
    storage = read(storage_path)
    bank = Path(storage['output_directory'])
    protocol_path = bank / 'protocol.json'
    protocol = read(protocol_path)
    details, source_hashes = [], {str(protocol_path): sha(protocol_path), str(storage_path): sha(storage_path)}
    for name, cfg in protocol['configurations'].items():
        annual, controls, full = [], [], False
        for year in (2020, 2021, 2022, 2023, 2024, 2025):
            path = bank / name / f'info_{year}.json'
            if not path.exists():
                continue
            info = read(path)
            assert info['status'] == 'passed' and info['configuration'] == cfg
            assert info['model'] == name and info['year'] == year
            assert sha(bank / name / f'model_{year}.joblib') == info['model_sha256']
            meta = info['training_meta']
            assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive']
            source_hashes[str(path)] = sha(path)
            if year == 2025:
                full = True
                continue
            raw = bank / name / f'raw_{year}.parquet'
            assert sha(raw) == info['prediction_sha256'] and info['model_reload_bit_identical']
            annual.append(year)
            control = bank / f'prefix_control_{name}_{year}.json'
            if control.exists():
                assert read(control)['status'] == 'passed'
                controls.append(year)
                source_hashes[str(control)] = sha(control)
        details.append({'model': name, 'actual_annual_fit_years': annual,
            'actual_prefix_control_years': controls, 'actual_fulltraining_ready': full})
    runs = {key: read(ROOT / 'analysis' / filename) for key, filename in (
        ('annual_training', 'nystrom_tuning_bank_run_20261005.json'),
        ('native_future', 'nystrom_tuning_future_run_20261005.json'))}
    evidence = {'status': 'actual_artifact_progress_snapshot', 'at_local': datetime.now().isoformat(),
        'declared_new_configurations': len(details),
        'actual_annual_fits': sum(len(row['actual_annual_fit_years']) for row in details),
        'actual_prefix_controls': sum(len(row['actual_prefix_control_years']) for row in details),
        'actual_five_year_configurations': sum(len(row['actual_annual_fit_years']) == 5 for row in details),
        'actual_fulltraining_artifacts': sum(row['actual_fulltraining_ready'] for row in details),
        'expected_annual_fits': 50, 'expected_fulltraining_artifacts': 10,
        'owned_process_live_now': {key: owned(run) for key, run in runs.items()},
        'available_RAM_GiB': psutil.virtual_memory().available / 2**30,
        'scheduling_available_RAM_reserve_GiB': 14.,
        'D_free_GiB': psutil.disk_usage('D:/').free / 2**30,
        'E_free_GiB': psutil.disk_usage('E:/').free / 2**30,
        'details': details, 'source_sha256': source_hashes,
        'cost_scope': 'Supplemental new bank only; older143-config inventory excludes these new artifacts.',
        'complete_output_quality_rounds': [65, 66], 'new_quality_scores_reported_here': 0,
        'physical_or_global_method_boundary_established': False, 'test_labels_read': False}
    path = ROOT / 'analysis/nystrom_tuning_progress_20261005.json'
    temporary = path.with_suffix('.progress.tmp')
    temporary.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)
    print(json.dumps({key: evidence[key] for key in ('status', 'actual_annual_fits',
        'actual_prefix_controls', 'actual_five_year_configurations', 'actual_fulltraining_artifacts',
        'owned_process_live_now', 'available_RAM_GiB')}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
