"""Count only saved, verified full32pass classifiers and retain all previous costs."""
from pathlib import Path
from datetime import datetime
import json

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    import refresh_memory_efficient_neural_cost_evidence_20261005 as previous
    from atomic_optimization_observer_writes_20261005 import operational_writes,write
    from locked_read_hash_cache_20261004 import fresh_sha
    with operational_writes('refresh_memory_efficient_neural_cost_evidence_20261005'):previous.main()
    configs=read(A/'streaming_rank_classifier_official_search_plan_20261005.json')['model_configurations']
    bank=Path(read(A/'streaming_rank_classifier_storage_v3_20261005.json')['output_directory'])
    fit_path=bank/'actual_native_fit_measurements.jsonl'
    measurements=[json.loads(line) for line in fit_path.read_bytes().splitlines()
                  if line.strip() and line.rstrip().endswith(b'}')] if fit_path.exists() else []
    rows,bindings=[],{}
    for name,cfg in configs.items():
        row={'model':name,'kind':'streaming_rank_classifier','method_family':'mature_rank_classification',
             'target':cfg['target'],'configuration':cfg,'source_bank':str(bank),'pilot_fits_excluded_from_full_fit_count':True}
        details=[]
        for year in range(2020,2026):
            path=bank/name/f'info_{year}.json'
            if not path.exists():continue
            info=read(path)
            assert info['status']=='passed' and info['configuration']==cfg and info['year']==year and info['model']==name
            meta=info['training_meta']
            assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
            assert meta['full_selected_row_keys_match_independent_original_filter']
            matched=[m for m in measurements if m['model']==name and m['year']==year and m['configuration']==cfg]
            assert len(matched)==1,(name,year)
            fit=matched[0]
            assert fit['status']=='completed_full_original32passes' and fit['actual_completed_epochs']==32
            assert fit['actual_training_rows']==meta['rows'] and fit['actual_rows_in_each_epoch']==[meta['rows']]*32
            assert fit['actual_native_sample_counter']==info['actual_native_sample_counter']==1+32*meta['rows']
            assert fit['coefficient_and_intercept_all_finite'] and not fit['test_data_read']
            assert fresh_sha(bank/name/f'model_{year}.joblib')==info['model_sha256']
            bindings[str(path)]=fresh_sha(path)
            detail={'year':year,'actual_new_fits':1,'actual_completed_epochs':32,
                'actual_native_sample_counter':fit['actual_native_sample_counter'],'actual_parameter_count':fit['parameter_count'],
                'mature_training_rows':meta['rows'],'fit_seconds':info['fit_seconds'],
                'artifact_elapsed_seconds':info['elapsed_seconds'],'source':str(path),'model_sha256':info['model_sha256']}
            if year<2025:
                prefix=bank/f'prefix_control_{name}_{year}.json'
                assert read(prefix)['status']=='passed' and read(prefix)['actual_saved_model_full_reload_and_cold80_day_prefix_bit_identical']
                assert info['model_reload_bit_identical'] and fresh_sha(bank/name/f'raw_{year}.parquet')==info['prediction_sha256']
                detail['prediction_sha256']=info['prediction_sha256']
                bindings[str(prefix)]=fresh_sha(prefix)
                details.append(detail)
            else:
                assert info['fulltraining_only_test_prediction_not_generated']
                row['fulltraining']={'status':'passed',**detail,'test_prediction_not_generated_during_fit':True}
        row.update(annual_artifacts=len(details),new_annual_fits=len(details),annual_details=details,
            fit_seconds_total=sum(item['fit_seconds'] for item in details),all_five_annual_outputs_complete=len(details)==5)
        rows.append(row)
    cost_path=A/'optimization_fit_cost_evidence_20261004.json'
    cost=read(cost_path)
    cost['models']=[row for row in cost['models'] if row['model'] not in configs]+rows
    assert len({row['model'] for row in cost['models']})==len(cost['models'])
    families={}
    for row in cost['models']:
        entry=families.setdefault(row['kind'],{'configurations':0,'new_annual_fits':0,'fit_seconds_total':0.})
        entry['configurations']+=1;entry['new_annual_fits']+=row['new_annual_fits'];entry['fit_seconds_total']+=row['fit_seconds_total']
    virtual=('past_oof_ridge','neural_ensemble','linear_leaf_ensemble')
    cost.update(configurations=len(cost['models']),families=families,
        total_actual_new_annual_fits=sum(row['new_annual_fits'] for row in cost['models']),
        native_child_annual_fits=sum(row['new_annual_fits'] for row in cost['models'] if row['kind'] not in virtual),
        fully_completed_five_year_configurations=sum(row['annual_artifacts']==5 for row in cost['models']),
        native_backbone_configurations_fully_trained=sum(row['annual_artifacts']==5 and row['kind'] not in virtual for row in cost['models']),
        fulltraining_artifacts_ready=sum('fulltraining' in row for row in cost['models']),
        streaming_rank_classifier_declared_configurations=4,
        streaming_rank_classifier_actual_annual_fits=sum(row['new_annual_fits'] for row in rows),
        streaming_rank_classifier_actual_fulltraining_artifacts=sum('fulltraining' in row for row in rows),
        streaming_rank_classifier_info_source_sha256=bindings,
        failed_V2_and16_small32pass_controls_not_counted_as_full_fits=True,
        supplementary_classifier_cost_source=str(Path(__file__).relative_to(ROOT)),
        generated_at_local=datetime.now().isoformat(timespec='seconds'),global_resource_exhaustion_established=False)
    write(cost_path,cost)
    path=A/'next_experiment_directions_20261003.json'
    directions=read(path)
    directions.update(total_new_individual_and_virtual_configurations=cost['configurations'],
        new_annual_oof_fits_completed=cost['total_actual_new_annual_fits'],native_child_annual_oof_fits_completed=cost['native_child_annual_fits'],
        fully_completed_five_year_configurations=cost['fully_completed_five_year_configurations'],
        streaming_rank_classifier_declared_configurations=4,
        streaming_rank_classifier_actual_annual_fits=cost['streaming_rank_classifier_actual_annual_fits'],
        streaming_rank_classifier_actual_fulltraining_artifacts=cost['streaming_rank_classifier_actual_fulltraining_artifacts'])
    write(path,directions)
    print(json.dumps({'configurations':cost['configurations'],'actual_annual_fits':cost['total_actual_new_annual_fits'],
        'actual_full_classifier_annual_fits':cost['streaming_rank_classifier_actual_annual_fits']},ensure_ascii=False),flush=True)
