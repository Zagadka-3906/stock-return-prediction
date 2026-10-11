"""Compact read-only progress from completed proofs and live local processes."""
from pathlib import Path
from datetime import datetime
import json
import psutil
ROOT=Path(__file__).resolve().parents[1]


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    registry=ROOT/read(ROOT/'analysis/ongoing_optimization_state.json')['active_run_registry']
    entries=read(registry);rounds=[]
    for entry in entries:
        n=entry['round'];folder=ROOT/f'analysis/optimization_20261003_r{n}'
        state=ROOT/f'analysis/ongoing_optimization_r{n}_state.json'
        payload=read(state) if state.exists() else {}
        waves={path.stem:len(read(path)['results']) for path in folder.glob('wave*_results.json')}
        rows=[row for path in folder.glob('wave*_results.json') for row in read(path)['results'].values()]
        rounds.append({'round':n,'root_pid_live':psutil.pid_exists(entry['pid']),
            'status':payload.get('status'),'stage':payload.get('stage'),'wave_records':waves,
            'best_saved_partial_score':max((r['connected_final_score'] for r in rows),default=None),
            'published':(ROOT/f'results/optimization_20261003_r{n}.json').exists()})
    banks={}
    for name in ('neural_tuning','catboost_tuning','expanded_stacking','additive_ridge','fourier_ridge','nonlinear_stacking','fourier_tuning'):
        bank=ROOT/f'analysis/{name}_bank_20261004'
        banks[name]={'annual_artifacts':len(list(bank.glob('*/info_202[0-4].json'))),
                     'fulltraining_artifacts':len(list(bank.glob('*/info_2025.json'))),
                     'oof_audit_status':read(bank/'oof_audit.json')['status'] if (bank/'oof_audit.json').exists() else None}
    resources={}
    for name in ('expanded_future','additive_ridge','fourier_ridge','nonlinear_stacking','nonlinear_stacking_recovery','fourier_tuning'):
        folder=f'{name.removesuffix("_recovery")}_resource_observations_recovery_20261004' if name.endswith('_recovery') else f'{name}_resource_observations_20261004'
        out=ROOT/'analysis'/folder;samples=out/'samples.jsonl'
        if not samples.exists():continue
        lines=samples.read_text(encoding='utf-8').splitlines();records=[]
        for line in lines:
            try:records.append(json.loads(line))
            except json.JSONDecodeError:pass  # Ignore a live partially written final line.
        resources[name]={'sample_count':len(records),'last_sample':records[-1] if records else None,
            'minimum_available_ram_GiB_sampled':min((r['available_ram_bytes']/2**30 for r in records),default=None),
            'maximum_gpu_memory_miB_sampled':max((r['gpu_last_sample']['memory_used_mib'] for r in records if r['gpu_last_sample']),default=None),
            'summary_status':read(out/'summary.json')['status'] if (out/'summary.json').exists() else 'running'}
    future=ROOT/'analysis/expanded_stacking_future_pipelines_qa_20261004/verification.json'
    board=read(ROOT/'results/all_model_rankings_20261003.json')
    print(json.dumps({'at_local':datetime.now().isoformat(timespec='seconds'),
        'available_ram_GiB':psutil.virtual_memory().available/2**30,'rounds':rounds,
        'banks':banks,'expanded_future_qa':read(future)['status'] if future.exists() else 'pending',
        'board_records':board['summary']['connected_exact_records'],'resources':resources},ensure_ascii=False))


if __name__=='__main__':main()
