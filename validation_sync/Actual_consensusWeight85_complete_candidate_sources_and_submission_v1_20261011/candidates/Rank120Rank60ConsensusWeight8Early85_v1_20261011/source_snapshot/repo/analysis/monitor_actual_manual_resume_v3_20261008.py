"""Lightweight actual service and committed-round observer for this manual continuation."""
from pathlib import Path
from datetime import datetime
import json
import re
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
import psutil
from run_dependency_queue_v3_20261006 import read, owned
from atomic_optimization_observer_writes_20261005 import write


def update():
    observed = {}
    names = ['main_publisher_v8_20261008', 'nonflag_ReverseBayes40_round132_full_registration_v1',
        'actual_GPU_resource_controls_main_publication_v1_20261008',
        'actual_neural_BF16_micro8192_bank6_v1_20261008', 'actual_neural_BF16_micro8192_bank6_v2_20261008',
        'actual_SparseGram133_complete_dependency_queue_v1_20261008',
        'nonflag_SparseGram40_round133_source_admission_v1', 'nonflag_SparseGram40_full37_controls_main_publication_v1',
        'nonflag_SparseGram40_official_comparison_v1', 'nonflag_SparseGram40_scores_main_publication_v1',
        'nonflag_SparseGram40_selected_candidate_preparation_v1', 'nonflag_SparseGram40_selected_candidate_sealing_v1',
        'nonflag_SparseGram40_round133_full_registration_v1',
        'nonflag_SparseGram40_round133_full_registration_recovery_v3_20261008',
        'nonflag_SparseGram40_round133_full_registration_resume_v4_20261008',
        'actual_deadline_and_full_training_handoff_main_publication_v3_20261008',
        'actual_ReverseBayesFine134_complete_dependency_queue_v3_20261008',
        'nonflag_ReverseBayesFine40_actual_full37_controls_v1_20261008',
        'nonflag_ReverseBayesFine40_round134_source_admission_v1',
        'nonflag_ReverseBayesFine40_full37_controls_main_publication_v1',
        'nonflag_ReverseBayesFine40_official_comparison_v1',
        'nonflag_ReverseBayesFine40_scores_main_publication_v1',
        'nonflag_ReverseBayesFine40_selected_candidate_preparation_v1',
        'nonflag_ReverseBayesFine40_selected_candidate_sealing_v1',
        'nonflag_ReverseBayesFine40_round134_full_registration_v1',
        'BF16_independent_small_CPU_preflight_v1_20261008',
        'BF16_independent_full5_GPU_controls_v1_20261008',
        'BF16_independent_full5_GPU_controls_v2_20261008']
    for name in names:
        folder = A / 'service_owned_workflows_20261006' / name
        if not (folder / 'native_launch.json').exists(): continue
        row = read(folder / 'native_launch.json')
        active = owned(row)
        value = {'actual_live_worker': active, 'pid': row['owned_worker_pid'],
                 'creation_time': row['owned_worker_creation_time'], 'driver': row['original_driver']}
        if active:
            process = psutil.Process(row['owned_worker_pid'])
            value.update(actual_process_status=process.status(), RSS_GiB=round(process.memory_info().rss / 2**30, 3))
        elif (folder / 'service_execution.json').exists(): value['terminal'] = read(folder / 'service_execution.json')
        observed[name] = value
    qualified = []
    for number in (128, 129, 130, 131, 132, 133, 134):
        folder = A / f'optimization_20261003_r{number}'
        receipt = A / f'github_validation_sync_main_20261005/round{number}_receipt.json'
        if not (folder / 'full_registration_execution.json').exists() or not receipt.exists(): continue
        full, transport = read(folder / 'full_registration_execution.json'), read(receipt)
        if full['status'] == 'passed' and transport['status'] == 'pushed_and_remote_head_verified':
            selected = read(folder / 'selection.json')
            qualified.append({'round': number, 'official_score': selected['winner']['metrics']['final_score'],
                              'main_commit': transport['commit'], 'connected_records': transport['connected_records']})
    best = min(qualified, key=lambda r: (-r['official_score'], r['round']))
    latest = max(qualified, key=lambda r: r['round'])
    pending = {}
    for number, base in [(132, 'nonflag_ReverseBayes40'), (133, 'nonflag_SparseGram40'), (134, 'nonflag_ReverseBayesFine40')]:
        folder = A / (base + '_official_comparison_v1_20261007')
        if (folder / 'actual_stage.json').exists(): pending[str(number)] = read(folder / 'actual_stage.json')
        if (folder / 'verification.json').exists():
            proof = read(folder / 'verification.json')
            pending[str(number)] = {'official_comparisons_complete': len(proof['records']),
                    'best_official_score': proof['best']['connected_final_score'],
                    'full_registration_complete': any(r['round'] == number for r in qualified)}
    bank = Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_v2_20261008')
    annual = []
    for year in range(2020, 2026):
        path = bank / str(year) / 'info.json'
        if path.exists(): annual.append({'year': year, 'status': read(path)['status'], 'model_sha256': read(path)['model_sha256']})
    state = {'status': 'active_actual_manual_continuation', 'at_local': datetime.now().isoformat(timespec='seconds'),
        'progress_monitor': str(Path(__file__)), 'best_fully_qualified': best, 'latest_fully_qualified_round': latest,
        'actual_user_deadline': read(A/'actual_user_submission_deadline_and_priority_20261008.json')['deadline_local'], 'qualified_recent_rounds': qualified,
        'official_comparison_progress': pending, 'new_BF16_completed_annual_models': annual,
        'new_BF16_expected_annual_models': 6, 'actual_services': observed,
        'available_RAM_GiB': round(psutil.virtual_memory().available / 2**30, 3),
        'expired_20261007_stop_guard_not_restarted': True, 'global_boundary_not_established': True}
    if (bank / 'actual_stage.json').exists(): state['new_BF16_actual_stage'] = read(bank / 'actual_stage.json')
    log = A / 'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/stdout.log'
    if log.exists():
        with log.open('rb') as stream:
            stream.seek(max(0, log.stat().st_size - 32768))
            tail = stream.read().decode('utf8', errors='replace')
        annual_starts=list(re.finditer(r'Actual new BF16 annual (\d+):',tail))
        epoch_year=int(annual_starts[-1].group(1)) if annual_starts else state.get('new_BF16_actual_stage',{}).get('year')
        if annual_starts:tail=tail[annual_starts[-1].end():]
        epochs = re.findall(r'BF16 micro8192 epoch (\d+)/(\d+) loss=([\d.eE+-]+) fit_seconds=([\d.]+)', tail)
        saved = re.findall(r'durable_epoch=(\d+) checkpoint_seconds=([\d.]+)', tail)
        if epochs:
            epoch, total, loss, seconds = epochs[-1]
            state['new_BF16_latest_actual_epoch'] = {'year': epoch_year, 'completed_epoch': int(epoch), 'total_epochs': int(total),
                'training_loss': float(loss), 'fit_seconds': float(seconds),
                'durable_saved_epoch': int(saved[-1][0]) if saved else None,
                'checkpoint_seconds': float(saved[-1][1]) if saved else None,
                'validation_quality_or_full_annual_speedup_not_inferred_from_training_loss': True}
    write(A / 'actual_manual_resume_progress_20261008.json', state)
    lines = ['# 本次继续工作的实际进度', '', '更新时间：' + state['at_local'], '',
             f"已完整合格的最好方案：第{best['round']}轮，官方S={best['official_score']:.17g}，最新完整榜{latest['connected_records']}条。", '',
             '截止时间：'+state['actual_user_deadline'], '',
             f'新BF16年度模型：已完成{len(annual)}/6；完整年度评分尚待模型与方案全部验证。', '',
             '最新比较：']
    for number, value in pending.items(): lines.append(f'- 第{number}轮：' + json.dumps(value, ensure_ascii=False))
    if 'new_BF16_latest_actual_epoch' in state:
        lines += ['', '最新实际训练轮次：' + json.dumps(state['new_BF16_latest_actual_epoch'], ensure_ascii=False)]
    lines += ['', '实际进程：']
    for name, value in observed.items():
        status = value.get('actual_process_status', value.get('terminal', {}).get('status', 'missing_terminal'))
        lines.append(f'- {name}：{status}，PID {value["pid"]}')
    target = A / 'actual_manual_resume_progress_20261008.md'
    temporary = target.with_suffix('.md.part')
    temporary.write_text('\n'.join(lines) + '\n', encoding='utf8', newline='\n')
    temporary.replace(target)


def main():
    while True:
        update()
        time.sleep(10)


if __name__ == '__main__': main()
