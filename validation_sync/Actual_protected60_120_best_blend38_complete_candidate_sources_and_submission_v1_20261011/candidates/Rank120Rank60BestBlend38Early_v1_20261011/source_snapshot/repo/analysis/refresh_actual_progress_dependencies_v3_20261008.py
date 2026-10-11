"""Refresh only the lightweight observer with actual recovery and new recipe control services."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_ready_goss_full_execution_20261006 import pair
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    old = A / 'monitor_actual_manual_resume_v2_20261008.py'
    new = A / 'monitor_actual_manual_resume_v3_20261008.py'
    text = old.read_text(encoding='utf8')
    before = "        'nonflag_SparseGram40_round133_full_registration_v1']"
    after = "        'nonflag_SparseGram40_round133_full_registration_v1',\n" \
        "        'nonflag_SparseGram40_round133_full_registration_recovery_v3_20261008',\n" \
        "        'nonflag_SparseGram40_round133_full_registration_resume_v4_20261008',\n" \
        "        'actual_deadline_and_full_training_handoff_main_publication_v3_20261008',\n" \
        "        'actual_ReverseBayesFine134_complete_dependency_queue_v3_20261008',\n" \
        "        'nonflag_ReverseBayesFine40_actual_full37_controls_v1_20261008',\n" \
        "        'nonflag_ReverseBayesFine40_round134_source_admission_v1',\n" \
        "        'nonflag_ReverseBayesFine40_full37_controls_main_publication_v1',\n" \
        "        'nonflag_ReverseBayesFine40_official_comparison_v1',\n" \
        "        'nonflag_ReverseBayesFine40_scores_main_publication_v1',\n" \
        "        'nonflag_ReverseBayesFine40_selected_candidate_preparation_v1',\n" \
        "        'nonflag_ReverseBayesFine40_selected_candidate_sealing_v1',\n" \
        "        'nonflag_ReverseBayesFine40_round134_full_registration_v1',\n" \
        "        'BF16_independent_small_CPU_preflight_v1_20261008',\n" \
        "        'BF16_independent_full5_GPU_controls_v1_20261008',\n" \
        "        'BF16_independent_full5_GPU_controls_v2_20261008']"
    assert text.count(before) == 1;text = text.replace(before, after)
    text = text.replace('for number in (128, 129, 130, 131, 132, 133):', 'for number in (128, 129, 130, 131, 132, 133, 134):')
    text = text.replace("[(132, 'nonflag_ReverseBayes40'), (133, 'nonflag_SparseGram40')]",
                        "[(132, 'nonflag_ReverseBayes40'), (133, 'nonflag_SparseGram40'), (134, 'nonflag_ReverseBayesFine40')]")
    text = text.replace("    best = min(qualified, key=lambda r: (-r['official_score'], r['round']))",
                        "    best = min(qualified, key=lambda r: (-r['official_score'], r['round']))\n    latest = max(qualified, key=lambda r: r['round'])")
    text = text.replace("'progress_monitor': str(Path(__file__)), 'best_fully_qualified': best,",
                        "'progress_monitor': str(Path(__file__)), 'best_fully_qualified': best, 'latest_fully_qualified_round': latest,\n        'actual_user_deadline': read(A/'actual_user_submission_deadline_and_priority_20261008.json')['deadline_local'],")
    needle = "        epochs = re.findall(r'BF16 micro8192 epoch"
    assert text.count(needle) == 1
    text = text.replace(needle,
        "        annual_starts=list(re.finditer(r'Actual new BF16 annual (\\d+):',tail))\n"
        "        epoch_year=int(annual_starts[-1].group(1)) if annual_starts else state.get('new_BF16_actual_stage',{}).get('year')\n"
        "        if annual_starts:tail=tail[annual_starts[-1].end():]\n" + needle)
    text = text.replace("{'completed_epoch': int(epoch), 'total_epochs': int(total),",
                        "{'year': epoch_year, 'completed_epoch': int(epoch), 'total_epochs': int(total),")
    text = text.replace("完整榜{best['connected_records']}条。", "最新完整榜{latest['connected_records']}条。")
    text = text.replace("             f'新BF16年度模型：", "             '截止时间：'+state['actual_user_deadline'], '',\n             f'新BF16年度模型：")
    compile(text, str(new), 'exec');assert not new.exists();new.write_text(text, encoding='utf8', newline='\n')
    identity_path = A / 'service_owned_workflows_20261006/actual_manual_resume_progress_monitor_v2_20261008/native_launch.json'
    row = read(identity_path);assert owned(row)
    parent, worker = pair(row)
    assert all(p.pid == worker.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True))
    proof = A / 'actual_progress_dependency_observer_replacement_v3_20261008.json'
    create(proof, {'status': 'replace_only_exact_owned_lightweight_observer_with_real_recovery_and134_dependencies',
        'original_identity': row, 'input_sha256': {str(p): sha(p) for p in [Path(__file__), old, new, identity_path]},
        'scientific_training_scoring_or_inference_workers_touched': 0})
    worker.terminate();worker.wait(timeout=10)
    if parent.is_running():parent.terminate();parent.wait(timeout=10)
    assert not owned(row)
    pins = {str(p): sha(p) for p in [new, proof]}
    current = start('actual_manual_resume_progress_monitor_v3_20261008', new.name, [], pins)
    create(A / 'actual_progress_dependency_observer_hidden_launch_v3_20261008.json', {
        'status': 'started_real_recovery_and134_and_annual_year_aware_hidden_observer', 'identity': current, 'input_sha256': pins})
    print(current['owned_worker_pid'], flush=True)


if __name__ == '__main__':main()
