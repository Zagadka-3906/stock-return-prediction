"""Count actual completed memory-layout fits and retain earlier native/virtual costs."""
from pathlib import Path
from datetime import datetime
import json
import math

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path,value):
    temporary = Path(path).with_suffix('.memory_cost.tmp')
    temporary.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temporary.replace(path)


def measurements(path):
    if not Path(path).exists():
        return []
    data = Path(path).read_bytes()
    return [json.loads(line) for line in data.splitlines() if line.strip() and line.rstrip().endswith(b'}')]


def main():
    import refresh_gradient_sampling_cost_evidence_20261005 as previous
    from atomic_optimization_observer_writes_20261005 import operational_writes
    with operational_writes('refresh_gradient_sampling_cost_evidence_20261005'):
        previous.main()
    from locked_read_hash_cache_20261004 import fresh_sha
    plan = read(A / 'memory_efficient_neural_complete_search_plan_20261005.json')
    bank = Path(read(A / 'memory_efficient_neural_storage_20261005.json')['output_directory'])
    future = A / 'memory_efficient_neural_future_qa_20261005'
    configs = plan['model_configurations']
    actual_measurements = measurements(bank / 'actual_native_fit_measurements.jsonl') + measurements(future / 'actual_native_fit_measurements.jsonl')
    cost_path = A / 'optimization_fit_cost_evidence_20261004.json'
    cost = read(cost_path)
    rows,bindings = [],{}
    for name,cfg in configs.items():
        details = []
        row = {'model':name,'kind':'mlp','method_family':'memory_efficient_neural','target':cfg['target'],
            'configuration':cfg,'source_bank':str(bank),'pilot_fits_excluded_from_full_fit_count':True}
        for year in range(2020,2026):
            path = bank / name / f'info_{year}.json'
            if not path.exists():
                continue
            info = read(path)
            assert info['status']=='passed' and info['configuration']==cfg and info['year']==year and info['model']==name
            meta = info['training_meta']
            assert meta['last'] < meta['cutoff_exclusive'] and meta['last_label_end'] <= meta['cutoff_exclusive']
            completed = [m for m in actual_measurements if m['configuration']==cfg and m['actual_training_rows']==meta['rows']
                and m.get('status')=='completed_original_requested_epochs' and m['context'].get('year')==year]
            assert len(completed)==1,(name,year,'Actual complete32epoch resource record required.')
            fit = completed[0]
            assert fit['requested_epochs']==fit['completed_epochs']==32 and fit['parameter_count']==168894465
            assert fit['planned_native_optimizer_steps']==math.ceil(meta['rows']/32768)*32 and fit['returned_state_all_finite']
            bindings[str(path)] = fresh_sha(path)
            if year<2025:
                details.append({'year':year,'actual_new_fits':1,'fit_seconds':info['fit_seconds'],
                    'artifact_elapsed_seconds':info['elapsed_seconds'],'mature_training_rows':meta['rows'],
                    'actual_completed_epochs':fit['completed_epochs'],'actual_parameter_count':fit['parameter_count'],
                    'source':str(path),'model_sha256':info['model_sha256'],'prediction_sha256':info['prediction_sha256']})
            else:
                row['fulltraining'] = {'status':'passed','actual_new_fits':1,'mature_training_rows':meta['rows'],
                    'fit_seconds':info['fit_seconds'],'elapsed_seconds':info['elapsed_seconds'],'source':str(path),
                    'actual_completed_epochs':32,'actual_parameter_count':168894465,
                    'test_prediction_not_generated_during_fit':info['fulltraining_only_test_prediction_not_generated']}
        row.update(annual_artifacts=len(details),new_annual_fits=len(details),annual_details=details,
            fit_seconds_total=sum(item['fit_seconds'] for item in details),all_five_annual_outputs_complete=len(details)==5)
        rows.append(row)
    cost['models'] = [row for row in cost['models'] if row['model'] not in configs] + rows
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
        memory_efficient_neural_declared_configurations=3,
        memory_efficient_neural_actual_annual_fits=sum(row['new_annual_fits'] for row in rows),
        memory_efficient_neural_actual_fulltraining_artifacts=sum('fulltraining' in row for row in rows),
        memory_efficient_neural_info_source_sha256=bindings,
        supplementary_memory_layout_cost_source=str(Path(__file__).relative_to(ROOT)),
        generated_at_local=datetime.now().isoformat(timespec='seconds'),global_resource_exhaustion_established=False)
    write(cost_path,cost)
    directions_path=A/'next_experiment_directions_20261003.json'
    directions=read(directions_path)
    directions.update(total_new_individual_and_virtual_configurations=cost['configurations'],
        new_annual_oof_fits_completed=cost['total_actual_new_annual_fits'],native_child_annual_oof_fits_completed=cost['native_child_annual_fits'],
        fully_completed_five_year_configurations=cost['fully_completed_five_year_configurations'],
        memory_efficient_neural_declared_configurations=3,
        memory_efficient_neural_actual_annual_fits=cost['memory_efficient_neural_actual_annual_fits'],
        memory_efficient_neural_actual_fulltraining_artifacts=cost['memory_efficient_neural_actual_fulltraining_artifacts'])
    write(directions_path,directions)
    print(json.dumps({'configurations':cost['configurations'],'actual_annual_fits':cost['total_actual_new_annual_fits'],
        'memory_efficient_neural_actual_annual_fits':cost['memory_efficient_neural_actual_annual_fits']},ensure_ascii=False),flush=True)
