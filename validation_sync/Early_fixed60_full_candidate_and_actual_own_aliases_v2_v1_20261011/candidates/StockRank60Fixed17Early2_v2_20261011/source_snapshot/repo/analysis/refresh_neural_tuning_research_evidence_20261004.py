"""Refresh mutable research/cost ledgers from completed immutable model metadata."""
from pathlib import Path
import json
from datetime import datetime
ROOT=Path(__file__).resolve().parents[1]


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    bank=ROOT/'analysis/neural_tuning_bank_20261004';protocol=read(bank/'protocol.json')
    configs=protocol['configurations'];complete=(bank/'oof_audit.json').exists();now=datetime.now().isoformat(timespec='seconds')
    new_models=[];completed=0
    for name,cfg in configs.items():
        details=[]
        for year in (2020,2021,2022,2023,2024):
            path=bank/name/f'info_{year}.json'
            if not path.exists():continue
            info=read(path);assert info['status']=='passed' and info['configuration']==cfg
            details.append({'year':year,'mature_training_rows':info['training_meta']['rows'],
                 'fit_seconds':info['fit_seconds'],'artifact_elapsed_seconds':info['elapsed_seconds'],
                 'actual_new_fits':1,'source':str(path.resolve())});completed+=1
        model={'model':name,'kind':'mlp','target':'y_rank','annual_artifacts':len(details),
               'new_annual_fits':len(details),'fit_seconds_total':sum(row['fit_seconds'] for row in details),
               'annual_details':details,'all_five_annual_models_complete':len(details)==5}
        full=bank/name/'info_2025.json'
        if full.exists():
            info=read(full);model['fulltraining']={'status':info['status'],'mature_training_rows':info['training_meta']['rows'],
                'fit_seconds':info['fit_seconds'],'elapsed_seconds':info['elapsed_seconds'],'source':str(full.resolve()),
                'test_prediction_not_generated_during_fit':info['fulltraining_only_test_prediction_not_generated']}
        new_models.append(model)
    assert not complete or completed==25
    cost_path=ROOT/'analysis/optimization_fit_cost_evidence_20261004.json';cost=read(cost_path)
    cost['models']=[model for model in cost['models'] if model['model'] not in configs]+new_models
    families={}
    for model in cost['models']:
        family=families.setdefault(model['kind'],{'configurations':0,'new_annual_fits':0,'fit_seconds_total':0.})
        family['configurations']+=1;family['new_annual_fits']+=model['new_annual_fits'];family['fit_seconds_total']+=model['fit_seconds_total']
    cost.update({'generated_at_local':now,'configurations':len(cost['models']),'families':families,
           'native_child_annual_fits':sum(model['new_annual_fits'] for model in cost['models'] if model['kind'] not in ('past_oof_ridge','neural_ensemble')),
           'learned_meta_annual_fits':sum(model['new_annual_fits'] for model in cost['models'] if model['kind']=='past_oof_ridge'),
           'total_actual_new_annual_fits':sum(model['new_annual_fits'] for model in cost['models']),
           'neural_tuning_completed_annual_fits':completed,'neural_tuning_expected_annual_fits':25,
           'neural_tuning_all_annual_controls_complete':complete,'queued_rounds':list(range(24,37)),
           'fully_completed_five_year_configurations':sum(model['annual_artifacts']==5 for model in cost['models']),
           'fulltraining_artifacts_ready':sum('fulltraining' in model for model in cost['models']),
           'neural_tuning_resource_samples':'analysis/neural_tuning_resource_observations_20261004/samples.jsonl',
           'global_resource_exhaustion_established':False})
    write(cost_path,cost)
    direction_path=ROOT/'analysis/next_experiment_directions_20261003.json';directions=read(direction_path)
    directions['directions']=[item for item in directions['directions'] if item.get('priority')!=10]+[{
        'priority':10,'method':'Matched neural rank-target offsets and learning rates',
        'reason':'All ordinary512-wide rank-MSE banks retained learning rate0.001 and historical float32 target shift-0.5; direct centered provided rank targets and lower/higher rates have not received matched complete-output comparisons.',
        'prespecified_grid':{'rank_training_offsets':[-.5,0.],'learning_rates':[.0005,.001,.002]},
        'reused_control':'rank512_e32; offset-0.5/lr0.001','new_configurations':5,
        'expected_annual_fits':25,'completed_annual_fits':completed,
        'status':'All25 annual models, maturity controls and raw-prefix/reload checks complete' if complete else f'{completed}/25 annual models complete; remaining fits and controls running',
        'execution_status':'queued_for_validation' if complete else 'training_running_then_validation_queued',
        'queued_rounds':[35,36],'expected_official_records':{'35':92,'36':118},
        'required_controls':['historical fitter matched control state and predictions exact','actual float32 fit-target SHA records','same raw training matrices, keys and provided targets','five mature-label folds and poisoned-future refits','fixed padded inference and complete-output cold-prefix checks','full mapped official CSV scoring, frozen scheme, then candidate inference'],
        'target_interpretation':'Both affine targets are valid; original shift is not classified as leakage or an invalid model.',
        'preflight':'analysis/neural_tuning_preflight_20261004/verification.json',
        'full_baseline_and_shift_controls':'analysis/neural_tuning_round_baselines_qa_20261004/verification.json',
        'resource_observations':'analysis/neural_tuning_resource_observations_20261004',
        'test_labels_read':False}]
    directions.update({'updated_at_local':now,'new_annual_oof_fits_completed':cost['total_actual_new_annual_fits'],
           'native_child_annual_oof_fits_completed':cost['native_child_annual_fits'],
           'total_new_individual_and_virtual_configurations':cost['configurations'],
           'fully_completed_five_year_configurations':cost['fully_completed_five_year_configurations'],
           'planned_neural_tuning_configurations':5,'global_resource_exhaustion_established':False})
    directions['prospective_parallel_official_scoring_four']['additional_prospective_rounds']=[35,36]
    write(direction_path,directions)
    print(json.dumps({'completed_neural_tuning_fits':completed,'total_actual_new_annual_fits':cost['total_actual_new_annual_fits'],
                      'five_year_configurations_complete':cost['fully_completed_five_year_configurations'],
                      'all_tuning_controls_complete':complete,'global_resource_exhaustion_established':False}))


if __name__=='__main__':main()
