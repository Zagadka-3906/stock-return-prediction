"""Version the progress observer to refresh boundary evidence on new proof files."""
from pathlib import Path
from datetime import datetime
import ast
import json
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from locked_read_hash_cache_20261004 import fresh_sha


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def create(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def main():
    analysis = ROOT / 'analysis'
    out = analysis / 'actual_progress_monitor_v2_handoff_20261005'
    out.mkdir(exist_ok=True)
    old_path = analysis / 'monitor_actual_optimization_progress_20261005.py'
    new_path = analysis / 'monitor_actual_optimization_progress_v2_20261005.py'
    old_run_path = analysis / 'actual_optimization_monitor_run_20261005.json'
    old_run = read(old_run_path)
    for path, digest in old_run['input_sha256'].items():
        assert fresh_sha(path) == digest, path
    text = old_path.read_text(encoding='utf-8')
    text = text.replace('refresh_optimization_boundary_evidence_20261004 as boundary', 'refresh_optimization_boundary_evidence_20261005 as boundary')
    text = text.replace('analysis/monitor_actual_optimization_progress_20261005.py', 'analysis/monitor_actual_optimization_progress_v2_20261005.py')
    text = text.replace('actual_optimization_monitor_run_20261005.json', 'actual_optimization_monitor_run_v2_20261005.json')
    text = text.replace("closed_changed = prior.get('latest_completed_round') != latest\n    if closed_changed:",
        "proof_names = ['neural_width_frontier_20261004/verification.json', 'neural_width_frontier_scope_audit_20261004.json', 'official_worker_frontier_execution_20261004/verification.json', 'official_worker_frontier_scope_audit_20261004.json', 'nystrom_ridge_bank_20261004/oof_audit.json', 'nystrom_ridge_bank_20261004/training_execution_scope.json', 'nystrom_ridge_resource_scope_audit_20261004.json', 'nystrom_ridge_future_models_qa_20261004/verification.json', 'nystrom_ridge_future_resource_scope_audit_20261004.json', 'nystrom_ridge_complete_scheme_preflight_20261004/verification.json', 'latest_graph_joint_axes_scope_audit_20261005/verification.json']\n    proof_paths = [ROOT / 'analysis' / name for name in proof_names]\n    boundary_key = [latest, [(str(p.relative_to(ROOT)), p.stat().st_size, p.stat().st_mtime_ns) for p in proof_paths if p.exists()]]\n    closed_changed = prior.get('boundary_key') != boundary_key\n    if closed_changed:")
    text = text.replace("'cost_inventory_key': cost_inventory_key,", "'cost_inventory_key': cost_inventory_key,\n        'boundary_key': boundary_key,")
    text = text.replace("if once or state['latest_completed_round'] >= 62:", "if once or state['latest_completed_round'] >= 63:")
    assert text != old_path.read_text(encoding='utf-8')
    ast.parse(text)
    with new_path.open('x', encoding='utf-8') as stream:
        stream.write(text)
    names = [new_path, old_path, analysis / 'refresh_optimization_boundary_evidence_20261005.py',
        analysis / 'refresh_continuous_progress_20261004.py', analysis / 'refresh_optimization_boundary_evidence_20261004.py',
        analysis / 'capture_actual_optimization_checkpoint_20261004.py', analysis / 'refresh_expanded_stacking_research_evidence_20261004.py']
    inputs = {str(p.resolve()): fresh_sha(p) for p in names}
    create(out / 'frozen_before_handoff.json', {'status': 'frozen_before_progress_monitor_handoff',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'previous_monitor': old_run,
        'input_sha256': inputs, 'reason': 'Include new proven graph-search gap and refresh resource boundaries when real proofs arrive.',
        'scientific_jobs_not_restarted': True, 'goal_status_not_modified': True})
    parent = psutil.Process(old_run['pid'])
    tree = [parent, *parent.children(recursive=True)]
    owned = [p for p in tree if any('monitor_actual_optimization_progress_20261005.py' in arg for arg in p.cmdline())]
    assert owned
    # The observer writes only mutable reports. Preserve its last state before stopping it.
    create(out / 'previous_monitor_state.json', read(analysis / 'actual_optimization_monitor_state_20261005.json'))
    for process in reversed(owned):
        process.terminate()
    psutil.wait_procs(owned, timeout=5)
    assert not any(p.is_running() for p in owned)
    for path, digest in inputs.items():
        assert fresh_sha(path) == digest, path
    stdout = analysis / 'run_logs/actual_progress_monitor_v2_20261005.stdout.log'
    stderr = analysis / 'run_logs/actual_progress_monitor_v2_20261005.stderr.log'
    with stdout.open('x') as output, stderr.open('x') as error:
        process = subprocess.Popen([sys.executable, '-B', '-X', 'utf8', str(new_path.relative_to(ROOT))],
            cwd=ROOT, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    record = {'pid': process.pid, 'script': new_path.relative_to(ROOT).as_posix(), 'script_args': [],
        'launched_at_local': datetime.now().isoformat(timespec='seconds'), 'stdout': str(stdout), 'stderr': str(stderr),
        'input_sha256': inputs, 'previous_monitor_pid': old_run['pid'],
        'previous_monitor_manifest_preserved': str(old_run_path), 'goal_status_not_modified': True,
        'new_scientific_jobs': 0, 'test_labels_read': False}
    create(analysis / 'actual_optimization_monitor_run_v2_20261005.json', record)
    create(out / 'handoff_verification.json', {'status': 'passed', 'new_monitor_pid': process.pid,
        'only_verified_owned_old_progress_monitor_stopped': True, 'original_monitor_source_preserved': True,
        'all_scientific_processes_unchanged': True, 'goal_status_not_modified': True, 'test_labels_read': False})
    print(json.dumps({'status': 'passed', 'new_monitor_pid': process.pid, 'new_scientific_jobs': 0}), flush=True)


if __name__ == '__main__':
    main()
