"""Count composite artifacts separately from the native fits that produced their parents."""
from pathlib import Path
from datetime import datetime
import json
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def write(path,value):
    temporary=Path(path).with_suffix('.ensemble_cost.tmp')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temporary.replace(path)
def main():
    import refresh_linear_leaf_cost_evidence_20261005 as previous
    from atomic_optimization_observer_writes_20261005 import operational_writes
    with operational_writes('refresh_linear_leaf_cost_evidence_20261005'):
        previous.main()
    from locked_read_hash_cache_20261004 import fresh_sha
    plan=read(ROOT/'analysis/linear_leaf_ensemble_complete_search_plan_20261005.json')
    bank=Path(read(ROOT/'analysis/linear_leaf_ensemble_storage_20261005.json')['output_directory'])
    cost_path=ROOT/'analysis/optimization_fit_cost_evidence_20261004.json'
    cost=read(cost_path);configs=plan['model_configurations'];models=[];bindings={}
    for name,cfg in configs.items():
        details=[]
        for year in range(2020,2025):
            source=bank/name/f'info_{year}.json'
            if not source.exists():continue
            info=read(source)
            assert info['status']=='passed' and info['configuration']==cfg and info['new_model_fits']==0
            assert info['actual80_day_native_composite_prefix_bit_identical'] and info['model_reload_bit_identical']
            meta=info['training_meta'];assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
            details.append({'year':year,'actual_new_fits':0,'fit_seconds':0.,'artifact_elapsed_seconds':info['elapsed_seconds'],'mature_training_rows':meta['rows'],'source':str(source),'model_sha256':info['model_sha256'],'prediction_sha256':info['prediction_sha256']})
            bindings[str(source)]=fresh_sha(source)
        row={'model':name,'kind':'linear_leaf_ensemble','target':cfg['target'],'configuration':cfg,'source_bank':str(bank),'annual_artifacts':len(details),'new_annual_fits':0,'annual_details':details,'fit_seconds_total':0.,'all_five_annual_outputs_complete':len(details)==5,'native_parent_fits_counted_once_in_parent_rows':True,'actual_virtual_artifact_construction_not_training':True}
        source=bank/name/'info_2025.json'
        if source.exists():
            info=read(source);assert info['status']=='passed' and info['configuration']==cfg and info['new_model_fits']==0
            row['fulltraining']={'status':'passed','actual_new_fits':0,'mature_training_rows':info['training_meta']['rows'],'fit_seconds':0.,'elapsed_seconds':info['elapsed_seconds'],'source':str(source),'test_prediction_not_generated_during_fit':info['fulltraining_only_test_prediction_not_generated'],'virtual_bundle_not_new_fit':True}
            bindings[str(source)]=fresh_sha(source)
        models.append(row)
    cost['models']=[row for row in cost['models'] if row['model'] not in configs]+models
    assert len({row['model'] for row in cost['models']})==len(cost['models'])
    families={}
    for row in cost['models']:
        entry=families.setdefault(row['kind'],{'configurations':0,'new_annual_fits':0,'fit_seconds_total':0.})
        entry['configurations']+=1;entry['new_annual_fits']+=row['new_annual_fits'];entry['fit_seconds_total']+=row['fit_seconds_total']
    virtual=('past_oof_ridge','neural_ensemble','linear_leaf_ensemble')
    cost.update(configurations=len(cost['models']),families=families,total_actual_new_annual_fits=sum(row['new_annual_fits'] for row in cost['models']),native_child_annual_fits=sum(row['new_annual_fits'] for row in cost['models'] if row['kind'] not in virtual),fully_completed_five_year_configurations=sum(row['annual_artifacts']==5 for row in cost['models']),native_backbone_configurations_fully_trained=sum(row['annual_artifacts']==5 and row['kind'] not in virtual for row in cost['models']),fulltraining_artifacts_ready=sum('fulltraining' in row for row in cost['models']),linear_leaf_ensemble_declared_configurations=len(configs),linear_leaf_ensemble_actual_virtual_annual_outputs=sum(row['annual_artifacts'] for row in models),linear_leaf_ensemble_actual_new_annual_fits=0,linear_leaf_ensemble_actual_virtual_final_bundles=sum('fulltraining' in row for row in models),linear_leaf_ensemble_actual_new_final_fits=0,linear_leaf_ensemble_info_source_sha256=bindings,supplementary_composite_cost_source=str(Path(__file__).relative_to(ROOT)),generated_at_local=datetime.now().isoformat(timespec='seconds'),global_resource_exhaustion_established=False)
    write(cost_path,cost)
    path=ROOT/'analysis/next_experiment_directions_20261003.json';directions=read(path)
    directions.update(total_new_individual_and_virtual_configurations=cost['configurations'],new_annual_oof_fits_completed=cost['total_actual_new_annual_fits'],native_child_annual_oof_fits_completed=cost['native_child_annual_fits'],fully_completed_five_year_configurations=cost['fully_completed_five_year_configurations'],linear_leaf_ensemble_declared_configurations=len(configs),linear_leaf_ensemble_actual_virtual_annual_outputs=cost['linear_leaf_ensemble_actual_virtual_annual_outputs'],linear_leaf_ensemble_actual_new_annual_fits=0,linear_leaf_ensemble_actual_virtual_final_bundles=cost['linear_leaf_ensemble_actual_virtual_final_bundles'])
    write(path,directions)
    print(json.dumps({key:cost[key] for key in ('configurations','total_actual_new_annual_fits','linear_leaf_ensemble_actual_virtual_annual_outputs','linear_leaf_ensemble_actual_new_annual_fits','linear_leaf_ensemble_actual_virtual_final_bundles')},ensure_ascii=False),flush=True)
