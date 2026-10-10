"""Update resource/research ledgers from immutable matched CatBoost metadata."""
from pathlib import Path
import json
from datetime import datetime
ROOT=Path(__file__).resolve().parents[1]


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    bank=ROOT/'analysis/catboost_tuning_bank_20261004';protocol=read(bank/'protocol.json')
    configs=protocol['configurations'];complete=(bank/'oof_audit.json').exists();now=datetime.now().isoformat(timespec='seconds')
    models=[];completed=0
    for name,cfg in configs.items():
        details=[]
        for year in (2020,2021,2022,2023,2024):
            path=bank/name/f'info_{year}.json'
            if not path.exists():continue
            info=read(path);assert info['status']=='passed' and info['configuration']==cfg
            details.append({'year':year,'mature_training_rows':info['training_meta']['rows'],'fit_seconds':info['fit_seconds'],
                 'artifact_elapsed_seconds':info['elapsed_seconds'],'actual_new_fits':1,'source':str(path.resolve())});completed+=1
        model={'model':name,'kind':'catboost','target':'y_rank','annual_artifacts':len(details),'new_annual_fits':len(details),
               'fit_seconds_total':sum(row['fit_seconds'] for row in details),'annual_details':details,
               'all_five_annual_models_complete':len(details)==5,'gpu_refit_bit_deterministic':False}
        full=bank/name/'info_2025.json'
        if full.exists():
            info=read(full);model['fulltraining']={'status':info['status'],'mature_training_rows':info['training_meta']['rows'],
                 'fit_seconds':info['fit_seconds'],'elapsed_seconds':info['elapsed_seconds'],'source':str(full.resolve()),
                 'test_prediction_not_generated_during_fit':info['fulltraining_only_test_prediction_not_generated']}
        models.append(model)
    assert not complete or completed==25
    cost_path=ROOT/'analysis/optimization_fit_cost_evidence_20261004.json';cost=read(cost_path)
    cost['models']=[model for model in cost['models'] if model['model'] not in configs]+models;families={}
    for model in cost['models']:
        family=families.setdefault(model['kind'],{'configurations':0,'new_annual_fits':0,'fit_seconds_total':0.})
        family['configurations']+=1;family['new_annual_fits']+=model['new_annual_fits'];family['fit_seconds_total']+=model['fit_seconds_total']
    cost.update({'generated_at_local':now,'configurations':len(cost['models']),'families':families,
        'native_child_annual_fits':sum(model['new_annual_fits'] for model in cost['models'] if model['kind'] not in ('past_oof_ridge','neural_ensemble')),
        'learned_meta_annual_fits':sum(model['new_annual_fits'] for model in cost['models'] if model['kind']=='past_oof_ridge'),
        'total_actual_new_annual_fits':sum(model['new_annual_fits'] for model in cost['models']),
        'catboost_tuning_completed_annual_fits':completed,'catboost_tuning_expected_annual_fits':25,'catboost_tuning_all_annual_controls_complete':complete,
        'fully_completed_five_year_configurations':sum(model['annual_artifacts']==5 for model in cost['models']),
        'fulltraining_artifacts_ready':sum('fulltraining' in model for model in cost['models']),
        'queued_rounds':list(range(24,39)),'catboost_tuning_resource_samples':'analysis/catboost_tuning_resource_observations_20261004/samples.jsonl',
        'global_resource_exhaustion_established':False})
    resource_summary=ROOT/'analysis/catboost_tuning_resource_observations_20261004/summary.json'
    if resource_summary.exists():
        resources=read(resource_summary)
        cost.update({'catboost_tuning_resource_summary':'analysis/catboost_tuning_resource_observations_20261004/summary.json',
              'catboost_tuning_resource_summary_status':resources['status'],
              'catboost_tuning_sampled_minimum_available_ram_GiB':resources['minimum_available_ram_bytes_sampled']/2**30,
              'catboost_tuning_sampled_maximum_gpu_memory_MiB':resources['maximum_gpu_memory_mib_sampled']})
    write(cost_path,cost)
    direction_path=ROOT/'analysis/next_experiment_directions_20261003.json';directions=read(direction_path)
    directions['directions']=[item for item in directions['directions'] if item.get('priority')!=11]+[{
        'priority':11,'method':'Matched CatBoost learning rate, iteration budget, leaf regularization and depth',
        'reason':'Earlier CatBoost only compared three target/depth configurations. Its15 actual annual fits cost232 seconds, leaving justified capacity to test matched optimization axes.',
        'new_configurations':5,'expected_annual_fits':25,'completed_annual_fits':completed,
        'prespecified_controls':{'learning_rate_iterations':[[.025,600],[.025,1200]],'l2_leaf_reg':[1.,100.],'depth':[10]},
        'reused_control':'cat_rank6_e600; seed20261013, depth6,lr0.05,600 iterations,l2_leaf_reg10',
        'status':'All25 annual models, CPU maturity controls and frozen serial inference checks complete' if complete else f'{completed}/25 annual models complete; fitting and verification running',
        'execution_status':'queued_for_validation' if complete else 'training_running_then_validation_queued',
        'queued_rounds':[37,38],'expected_official_records':{'37':92,'38':118},
        'preflight':'analysis/catboost_tuning_preflight_20261004/verification.json',
        'full_baseline_and_shift_controls':'analysis/catboost_tuning_round_baselines_qa_20261004/verification.json',
        'resource_observations':'analysis/catboost_tuning_resource_observations_20261004',
        'gpu_refit_bit_deterministic':False,'test_labels_read':False}]
    directions.update({'updated_at_local':now,'new_annual_oof_fits_completed':cost['total_actual_new_annual_fits'],
        'native_child_annual_oof_fits_completed':cost['native_child_annual_fits'],'total_new_individual_and_virtual_configurations':cost['configurations'],
        'fully_completed_five_year_configurations':cost['fully_completed_five_year_configurations'],'planned_catboost_tuning_configurations':5,
        'new_backbone_configurations_fully_trained':sum(model['annual_artifacts']==5 for model in cost['models'] if model['kind'] not in ('past_oof_ridge','neural_ensemble')),
        'new_backbone_configurations_trained':sum(model['annual_artifacts']==5 for model in cost['models'] if model['kind'] not in ('past_oof_ridge','neural_ensemble')),
        'global_resource_exhaustion_established':False})
    directions['prospective_parallel_official_scoring_four']['additional_prospective_rounds']=[35,36,37,38]
    write(direction_path,directions)
    print(json.dumps({'catboost_tuning_annual_fits':completed,'total_actual_new_annual_fits':cost['total_actual_new_annual_fits'],
               'five_year_configurations_complete':cost['fully_completed_five_year_configurations'],'all_tuning_controls_complete':complete}))


if __name__=='__main__':main()
