"""Extend the original cost producer with actual artifacts from the new kernel bank."""
from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    import refresh_expanded_stacking_research_evidence_20261004 as original
    original.main()
    from locked_read_hash_cache_20261004 import fresh_sha
    storage = read(ROOT / 'analysis/nystrom_tuning_storage_20261005.json')
    bank = Path(storage['output_directory'])
    protocol = read(bank / 'protocol.json')
    cost_path = ROOT / 'analysis/optimization_fit_cost_evidence_20261004.json'
    cost = read(cost_path)
    configs, new_models, bindings = protocol['configurations'], [], {}
    assert len(configs) == 10 and protocol['expected_annual_fits'] == 50
    for name, cfg in configs.items():
        details = []
        for year in range(2020, 2025):
            info_path = bank / name / f'info_{year}.json'
            if not info_path.exists():
                continue
            info = read(info_path)
            assert info['status'] == 'passed' and info['configuration'] == cfg
            assert info['model'] == name and info['year'] == year and info['new_model_fits'] == 1
            meta = info['training_meta']
            assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive']
            bindings[str(info_path.resolve())] = fresh_sha(info_path)
            details.append({'year': year, 'mature_training_rows': meta['rows'],
                'fit_seconds': info['fit_seconds'], 'artifact_elapsed_seconds': info['elapsed_seconds'],
                'actual_new_fits': 1, 'source': str(info_path.resolve()),
                'model_sha256': info['model_sha256'], 'prediction_sha256': info['prediction_sha256']})
        model = {'model': name, 'kind': 'ridge_nystrom', 'target': cfg['target'],
            'annual_artifacts': len(details), 'new_annual_fits': len(details),
            'fit_seconds_total': sum(row['fit_seconds'] for row in details), 'annual_details': details,
            'all_five_annual_outputs_complete': len(details) == 5,
            'expanded_basis_columns': 63 + cfg['landmark_components'],
            'source_bank': str(bank), 'configuration': cfg}
        full = bank / name / 'info_2025.json'
        if full.exists():
            info = read(full)
            assert info['status'] == 'passed' and info['configuration'] == cfg and info['new_model_fits'] == 1
            model['fulltraining'] = {'status': 'passed', 'mature_training_rows': info['training_meta']['rows'],
                'fit_seconds': info['fit_seconds'], 'elapsed_seconds': info['elapsed_seconds'],
                'actual_new_fits': 1, 'source': str(full.resolve()),
                'test_prediction_not_generated_during_fit': info['fulltraining_only_test_prediction_not_generated']}
            bindings[str(full.resolve())] = fresh_sha(full)
        new_models.append(model)
    cost['models'] = [row for row in cost['models'] if row['model'] not in configs] + new_models
    names = [row['model'] for row in cost['models']]
    assert len(names) == len(set(names))
    families = {}
    for model in cost['models']:
        family = families.setdefault(model['kind'], {'configurations': 0, 'new_annual_fits': 0, 'fit_seconds_total': 0.})
        family['configurations'] += 1
        family['new_annual_fits'] += model['new_annual_fits']
        family['fit_seconds_total'] += model['fit_seconds_total']
    cost.update(configurations=len(names), families=families,
        native_child_annual_fits=sum(row['new_annual_fits'] for row in cost['models'] if row['kind'] not in ('past_oof_ridge', 'neural_ensemble')),
        total_actual_new_annual_fits=sum(row['new_annual_fits'] for row in cost['models']),
        fully_completed_five_year_configurations=sum(row['annual_artifacts'] == 5 for row in cost['models']),
        fulltraining_artifacts_ready=sum('fulltraining' in row for row in cost['models']),
        native_backbone_configurations_fully_trained=sum(row['annual_artifacts'] == 5 and row['kind'] not in ('past_oof_ridge', 'neural_ensemble') for row in cost['models']),
        nystrom_tuning_actual_annual_fits=sum(row['new_annual_fits'] for row in new_models),
        nystrom_tuning_actual_fulltraining_artifacts=sum('fulltraining' in row for row in new_models),
        nystrom_tuning_declared_configurations=10, nystrom_tuning_info_source_sha256=bindings,
        generated_at_local=datetime.now().isoformat(timespec='seconds'),
        supplemental_cost_source='analysis/refresh_nystrom_tuning_cost_evidence_20261005.py',
        global_resource_exhaustion_established=False)
    write(cost_path, cost)
    path = ROOT / 'analysis/next_experiment_directions_20261003.json'
    directions = read(path)
    directions.update(total_new_individual_and_virtual_configurations=cost['configurations'],
        fully_completed_five_year_configurations=cost['fully_completed_five_year_configurations'],
        new_annual_oof_fits_completed=cost['total_actual_new_annual_fits'],
        native_child_annual_oof_fits_completed=cost['native_child_annual_fits'],
        nystrom_tuning_actual_annual_fits=cost['nystrom_tuning_actual_annual_fits'],
        nystrom_tuning_actual_fulltraining_artifacts=cost['nystrom_tuning_actual_fulltraining_artifacts'])
    write(path, directions)
    print(json.dumps({'configurations': cost['configurations'], 'actual_annual_fits': cost['total_actual_new_annual_fits'],
        'new_kernel_annual_fits': cost['nystrom_tuning_actual_annual_fits'],
        'fulltraining_artifacts': cost['fulltraining_artifacts_ready']}, ensure_ascii=False), flush=True)
