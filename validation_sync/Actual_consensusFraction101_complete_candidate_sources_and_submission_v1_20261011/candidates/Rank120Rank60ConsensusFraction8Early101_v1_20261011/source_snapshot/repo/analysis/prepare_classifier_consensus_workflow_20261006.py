"""Freeze fixed candidate definitions, then launch actual complete construction."""
from pathlib import Path
from datetime import datetime
import json
import os
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))


def main():
    import build_classifier_consensus_bank_20261005 as bank
    if sys.argv[1] == 'plan':
        bank.dump(bank.PLAN, {'status': 'fixed_before_consensus_construction_and_official_quality',
            'configurations': bank.CONFIGS, 'years': list(bank.YEARS),
            'expected_virtual_annual_outputs': 30, 'expected_virtual_final_artifacts': 6,
            'new_native_fits': 0, 'reused_unique_native_annual_fits': 20,
            'reused_unique_native_final_fits': 4,
            'prospective_rounds': [89, 90], 'explicit_parent_rounds': {'89': 88, '90': 89},
            'quality_sources_implementation_and_preflight_still_pending': True,
            'scored_records_prespecified': {'89': 124, '90': 138},
            'wave_arm_counts': {'89': [73, 8, 18, 25], '90': [37, 84, 17]},
            'waves': {'89': [353, 354, 355, 356], '90': [357, 358, 359]},
            'all_original_required_rounds67_to88_retained': True,
            'validation_rows': 5635800, 'validation_days': 1212, 'validation_codes': 4650,
            'mature_original_one_day_purge_and_continuous_turnover': True,
            'all6_actual_full1599600_row_future_reload_and_cold80_required': True,
            'fixed_composites_not_learned_from_validation_or_test': True,
            'correlation_diagnostic_not_selection_gate': True,
            'past_only_return_mapping_and17_digit_written_CSV_official_scoring_required': True,
            'whole_scheme_causal_checks_candidates_and_complete_ranking_required': True,
            'sole_selection_objective': '.4 ICmean + .3 annual_excess + .3 (1 - turnover)',
            'selection_bias_uncorrected': True, 'physical_resource_boundary_established': False,
            'test_labels_read': False, 'new_quality_scores': 0}, immutable=True)
        print(json.dumps({'status': 'fixed6_consensus_candidates_and262_full_quality_records'}, ensure_ascii=False))
        return
    assert sys.argv[1] == 'launch'
    from windows_hidden_process_launch_20261006 import launch
    out = A / 'classifier_consensus_workflow_launch_20261006'
    assert not out.exists()
    assert bank.read(A / 'classifier_consensus_preflight_20261005/verification.json')['status'] == 'passed_actual_native_parent_consensus_reload_and_prefix'
    assert bank.read(A / 'classifier_consensus_direct_router_preflight_20261005/verification.json')['status'] == 'passed_actual_consensus_and_inherited_routes'
    out.mkdir()
    sources = [Path(__file__), bank.PLAN, Path(bank.__file__), bank.SOURCE, bank.parent.SOURCE,
        A / 'run_classifier_consensus_bank_20261005.py',
        A / 'verify_classifier_consensus_full_future_20261005.py',
        A / 'classifier_consensus_model_sources_20261005.py',
        A / 'classifier_consensus_future_codec_adapter_20261005.py',
        A / 'verify_classifier_consensus_preflight_20261005.py',
        A / 'classifier_consensus_preflight_20261005/verification.json',
        A / 'classifier_consensus_direct_router_preflight_20261005/verification.json',
        A / 'windows_hidden_process_launch_20261006.py']
    inputs = {str(p.resolve()): bank.sha(p) for p in sources}
    for name in ('bank', 'future'):
        bank.dump(A / f'classifier_consensus_{name}_run_20261005.json', {
            'status': 'frozen_before_actual_complete_fixed_consensus_construction',
            'input_sha256': inputs, 'new_native_fits': 0, 'test_labels_read': False}, immutable=True)
    scratch = ROOT / 'tmp/classifier_consensus_20261006'
    scratch.mkdir(parents=True, exist_ok=True)
    assert scratch.resolve().drive.upper() == 'D:'
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = str(scratch)
    jobs = {}
    for name, script in (('bank', 'run_classifier_consensus_bank_20261005.py'),
                         ('future', 'verify_classifier_consensus_full_future_20261005.py')):
        path = A / script
        with (out / f'{name}_stdout.log').open('xb') as stdout, (out / f'{name}_stderr.log').open('xb') as stderr:
            process = launch([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(path)],
                             cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
        time.sleep(.5)
        assert process.poll() is None, (out / f'{name}_stderr.log').read_text(encoding='utf-8')
        parent = psutil.Process(process.pid)
        children = [p for p in parent.children(recursive=True)
                    if p.name().lower() == 'python.exe' and p.cmdline()[1:] == parent.cmdline()[1:]]
        assert len(children) == 1
        jobs[name] = {'pid': parent.pid, 'script': str(path), 'script_args': [],
            'owned_worker_pid': children[0].pid, 'owned_worker_creation_time': children[0].create_time(),
            'stdout': str(out / f'{name}_stdout.log'), 'stderr': str(out / f'{name}_stderr.log'),
            'at_local': datetime.now().isoformat(timespec='seconds')}
        bank.dump(out / f'{name}_launch.json', jobs[name], immutable=True)
    bank.dump(out / 'verification.json', {'status': 'passed2_actual_consoleless_consensus_jobs_owned',
        'jobs': jobs, 'input_sha256': inputs, 'new_native_fits': 0,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    print(json.dumps({'status': 'actual_complete_consensus_construction_started', 'jobs': jobs}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
