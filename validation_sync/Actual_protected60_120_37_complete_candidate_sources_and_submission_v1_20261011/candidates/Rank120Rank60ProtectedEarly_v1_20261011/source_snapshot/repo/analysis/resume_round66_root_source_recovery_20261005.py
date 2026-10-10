"""Run the original R66 grid with guarded source resolution and a separate scope."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def main():
    run_path = ROOT / 'analysis/round66_root_source_recovery_run_20261005.json'
    run = json.loads(run_path.read_text(encoding='utf-8'))
    from locked_read_hash_cache_20261004 import fresh_sha
    for source, expected in run['input_sha256'].items():
        assert fresh_sha(source) == expected, source
    import optimize_training_round50 as roots
    from standalone_root_source_adapter_20261005 import install
    restore = install(roots)
    import optimize_training_round66_v2 as module
    # Preserve the immutable failed scope and write only the new execution result.
    original_dump = module.dump

    def dump(path, value, *args, **kwargs):
        path = Path(path)
        if path == module.OUT / 'provenance_scope_execution.json':
            path = module.OUT / 'provenance_scope_execution_recovery_v3_20261005.json'
        return original_dump(path, value, *args, **kwargs)

    module.dump = dump
    import frozen_provenance_execution_scope_20261004 as scoped
    from round66_recovery_execution_scope_20261005 import RecoveryExecutionScope
    original_scope = scoped.FrozenProvenanceExecutionScope
    additional = [Path(__file__), run_path, ROOT / 'analysis/standalone_root_source_adapter_20261005.py',
                  ROOT / 'analysis/round66_recovery_execution_scope_20261005.py',
                  ROOT / 'analysis/standalone_root_source_adapter_preflight_20261005/verification.json',
                  module.OUT / 'provenance_scope_execution.json']

    def scope(namespace, sources, metadata, analysis_root):
        assert namespace is module
        return RecoveryExecutionScope(namespace, sources, metadata, analysis_root, additional)

    scoped.FrozenProvenanceExecutionScope = scope
    try:
        from run_nystrom_tuning_round_v2_20261005 import main as original
        original(66)
    finally:
        scoped.FrozenProvenanceExecutionScope = original_scope
        module.dump = original_dump
        restore()


if __name__ == '__main__':
    main()
