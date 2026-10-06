"""Version resource bindings only, before any real Nyström model fit."""
from pathlib import Path
from datetime import datetime
import ast
import json
import sys

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
    audit = analysis / 'nystrom_restart_source_audit_20261005.json'
    assert not audit.exists()
    bank = analysis / 'nystrom_ridge_bank_20261004'
    assert not list(bank.glob('*/info_202[0-4].json')) and not (bank / 'protocol.json').exists()
    old_obs = analysis / 'nystrom_ridge_resource_observations_20261004'
    old_protocol = read(old_obs / 'protocol.json')
    for path, digest in old_protocol['input_sha256'].items():
        assert fresh_sha(path) == digest, path
    rows = [json.loads(line) for line in (old_obs / 'samples.jsonl').read_text(encoding='utf-8').splitlines()]
    assert all(row['actual_completed_annual_fits'] == 0 for row in rows)
    assert not (old_obs / 'summary.json').exists()
    changes = [
        ('run_nystrom_ridge_training_20261004.py', 'run_nystrom_restart_training_20261005.py', [
            ('nystrom_ridge_resource_observations_20261004', 'nystrom_ridge_resource_observations_recovery_20261005'),
            ('nystrom_ridge_training_run_20261004.json', 'nystrom_ridge_training_run_20261005.json'),
            ('observe_nystrom_ridge_resources_20261004.py', 'observe_nystrom_restart_resources_20261005.py'),
            ('sources=[Path(__file__),', "sources=[Path(__file__),ROOT/'analysis/run_nystrom_ridge_training_20261004.py',ROOT/'analysis/nystrom_restart_source_audit_20261005.json',ROOT/'analysis/nystrom_ridge_resource_observations_recovery_20261005/recovery_binding.json',"),
        ]),
        ('audit_nystrom_ridge_resource_scope_20261004.py', 'audit_nystrom_restart_resource_scope_20261005.py', [
            ('nystrom_ridge_resource_observations_20261004', 'nystrom_ridge_resource_observations_recovery_20261005'),
            ('sources=[Path(__file__),', "sources=[Path(__file__),ROOT/'analysis/audit_nystrom_ridge_resource_scope_20261004.py',ROOT/'analysis/nystrom_restart_source_audit_20261005.json',obs/'recovery_binding.json',"),
        ]),
        ('run_nystrom_ridge_evidence_audits_20261004.py', 'run_nystrom_restart_evidence_audits_20261005.py', [
            ('nystrom_ridge_resource_observations_20261004', 'nystrom_ridge_resource_observations_recovery_20261005'),
            ('audit_nystrom_ridge_resource_scope_20261004', 'audit_nystrom_restart_resource_scope_20261005'),
        ]),
    ]
    inputs = dict(old_protocol['input_sha256'])
    records = []
    for old_name, new_name, replacements in changes:
        old = analysis / old_name
        new = analysis / new_name
        text = old.read_text(encoding='utf-8')
        for before, after in replacements:
            assert before in text, (old_name, before)
            text = text.replace(before, after)
        ast.parse(text)
        with new.open('x', encoding='utf-8') as stream:
            stream.write(text)
        records.append({'original_source': str(old), 'effective_source': str(new),
                        'replacements': replacements})
        for path in (old, new):
            inputs[str(path.resolve())] = fresh_sha(path)
    for path in (Path(__file__), analysis / 'observe_nystrom_restart_resources_20261005.py', old_obs / 'protocol.json', old_obs / 'samples.jsonl'):
        inputs[str(path.resolve())] = fresh_sha(path)
    create(audit, {'status': 'passed_pre_execution_source_binding_correction',
        'at_local': datetime.now().isoformat(timespec='seconds'),
        'original_sources_and_interrupted_sampling_files_preserved': True,
        'interrupted_pretraining_wait_samples': len(rows),
        'interrupted_last_sample_at_local': rows[-1]['at_local'],
        'actual_annual_fits_before_recovery': 0,
        'only_process_registry_and_resource_window_bindings_changed': True,
        'kernel_algorithms_configurations_and_official_score_unchanged': True,
        'source_changes': records, 'input_sha256': inputs,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'passed', 'preserved_pretraining_wait_samples': len(rows),
                      'versioned_sources': 4, 'actual_annual_fits': 0}), flush=True)


if __name__ == '__main__':
    main()
