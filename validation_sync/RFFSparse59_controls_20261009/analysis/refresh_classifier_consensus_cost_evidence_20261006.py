"""Count verified virtual composites without inventing any native estimator fit."""
from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    from atomic_optimization_observer_writes_20261005 import write
    from locked_read_hash_cache_20261004 import fresh_sha
    bank = A / 'classifier_consensus_bank_20261005'
    future = A / 'classifier_consensus_future_qa_20261005'
    if not (bank / 'construction_execution_scope.json').exists():
        return
    assert read(bank / 'construction_execution_scope.json')['status'] == 'passed'
    configs = read(A / 'classifier_consensus_complete_search_plan_20261005.json')['configurations']
    rows, bindings = [], {}
    for name, cfg in configs.items():
        details, final = [], None
        for year in range(2020, 2026):
            path = bank / name / f'info_{year}.json'
            if not path.exists():
                continue
            info = read(path)
            assert info['status'] == 'passed' and info['configuration'] == cfg and info['new_model_fits'] == 0
            model = bank / name / f'model_{year}.joblib'
            assert fresh_sha(model) == info['model_sha256']
            bindings[str(path)] = fresh_sha(path)
            meta = info['training_meta']
            assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive']
            detail = {'year': year, 'actual_new_fits': 0, 'mature_training_rows': meta['rows'],
                'fit_seconds': 0., 'artifact_elapsed_seconds': info['elapsed_seconds'],
                'source': str(path), 'model_sha256': info['model_sha256']}
            if year < 2025:
                assert info['model_reload_bit_identical'] and info['actual_cold80_day_native_ensemble_bit_identical']
                assert fresh_sha(bank / name / f'raw_{year}.parquet') == info['prediction_sha256']
                details.append(detail)
            else:
                final = {'status': 'passed', **detail}
        row = {'model': name, 'kind': 'classifier_consensus', 'target': 'y_rank',
            'configuration': cfg, 'source_bank': str(bank), 'annual_artifacts': len(details),
            'new_annual_fits': 0, 'annual_details': details, 'fit_seconds_total': 0.,
            'virtual_artifact_not_new_native_fit': True,
            'virtual_construction_seconds': sum(d['artifact_elapsed_seconds'] for d in details),
            'unique_native_parent_fits_counted_in_original_family_only': True}
        if final is not None:
            row['fulltraining'] = final
        rows.append(row)
    cost_path = A / 'optimization_fit_cost_evidence_20261004.json'
    cost = read(cost_path)
    native_fits_before = cost['total_actual_new_annual_fits']
    cost['models'] = [r for r in cost['models'] if r['model'] not in configs] + rows
    assert len({r['model'] for r in cost['models']}) == len(cost['models'])
    families, virtual = {}, ('past_oof_ridge', 'neural_ensemble', 'linear_leaf_ensemble', 'classifier_consensus')
    for row in cost['models']:
        family = families.setdefault(row['kind'], {'configurations': 0, 'new_annual_fits': 0, 'fit_seconds_total': 0.})
        family['configurations'] += 1
        family['new_annual_fits'] += row['new_annual_fits']
        family['fit_seconds_total'] += row['fit_seconds_total']
    cost.update(configurations=len(cost['models']), families=families,
        total_actual_new_annual_fits=sum(r['new_annual_fits'] for r in cost['models']),
        native_child_annual_fits=sum(r['new_annual_fits'] for r in cost['models'] if r['kind'] not in virtual),
        fully_completed_five_year_configurations=sum(r['annual_artifacts'] == 5 for r in cost['models']),
        native_backbone_configurations_fully_trained=sum(r['annual_artifacts'] == 5 and r['kind'] not in virtual for r in cost['models']),
        fulltraining_artifacts_ready=sum('fulltraining' in r for r in cost['models']),
        classifier_consensus_virtual_annual_outputs=sum(r['annual_artifacts'] for r in rows),
        classifier_consensus_virtual_final_artifacts=sum('fulltraining' in r for r in rows),
        classifier_consensus_new_native_fits=0,
        classifier_consensus_info_source_sha256=bindings,
        classifier_consensus_fullfuture_status=read(future / 'verification.json')['status'] if (future / 'verification.json').exists() else 'pending',
        generated_at_local=datetime.now().isoformat(timespec='seconds'),
        supplementary_consensus_cost_source=str(Path(__file__).relative_to(ROOT)))
    assert cost['total_actual_new_annual_fits'] == native_fits_before
    write(cost_path, cost)
    print(json.dumps({'status': 'updated_actual_virtual_composites_without_new_native_fits',
        'configurations': cost['configurations'], 'actual_native_annual_fit_count_unchanged': native_fits_before,
        'virtual_annual_outputs': cost['classifier_consensus_virtual_annual_outputs']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
