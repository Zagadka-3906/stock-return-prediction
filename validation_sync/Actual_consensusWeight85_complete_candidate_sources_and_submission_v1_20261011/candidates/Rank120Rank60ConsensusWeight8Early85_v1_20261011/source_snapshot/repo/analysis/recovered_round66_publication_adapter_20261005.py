"""Include both the failed original scope and actual passed recovery in the export."""
from pathlib import Path


def install(sync):
    original = sync.snapshot

    def snapshot(number):
        manifest, payload = original(number)
        if number != 66:
            return manifest, payload
        assert manifest['scientific_evidence']['actual_recovery_scope_required'] is True
        relative = Path('validation_sync/round66')
        directory = sync.ROOT / 'analysis/optimization_20261003_r66'
        for name in ('provenance_scope_execution_recovery_v3_20261005.json',
                     'recovery_frozen_execution_v3_20261005.json'):
            source = directory / name
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data)
            destination = (relative / name).as_posix()
            payload[destination] = data
            manifest['local_input_source_sha256'][source.relative_to(sync.ROOT).as_posix()] = sync.sha(data)
            manifest['exported_files'][destination] = {'bytes': len(data), 'sha256': sync.sha(data)}
        passed = sync.read(directory / 'provenance_scope_execution_recovery_v3_20261005.json')
        failed = sync.read(directory / 'provenance_scope_execution.json')
        assert passed['status'] == 'passed' and failed['status'] == 'failed'
        manifest['original_failed_scope_retained_and_actual_recovery_passed'] = True
        payload[(relative / 'manifest.json').as_posix()] = sync.encoded(manifest)
        payload[(relative / 'README.md').as_posix()] += (
            '\n第66轮原始来源解析因候选文件尚未生成而失败；原协议和失败证明保持原样。'
            '实际恢复的完整执行证明为 `provenance_scope_execution_recovery_v3_20261005.json`，'
            '恢复冻结来源为 `recovery_frozen_execution_v3_20261005.json`。'
            '只有实际恢复的全部科学检查和最终全量哈希复核通过后，才导出本目录。\n').encode('utf-8')
        return manifest, payload

    sync.snapshot = snapshot
    return original
