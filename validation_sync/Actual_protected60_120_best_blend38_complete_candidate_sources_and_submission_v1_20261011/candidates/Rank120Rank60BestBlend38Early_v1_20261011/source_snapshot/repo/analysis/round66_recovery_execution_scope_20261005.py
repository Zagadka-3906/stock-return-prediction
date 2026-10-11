"""Resume an existing frozen protocol while preserving its failed execution proof."""
from pathlib import Path
from functools import wraps
from types import SimpleNamespace
import json
import sys

from locked_read_hash_cache_20261004 import LockedReadHashCache, fresh_sha


class RecoveryExecutionScope:
    def __init__(self, module, sources, metadata, analysis_root, additional_sources):
        self.module, self.analysis_root = module, Path(analysis_root).resolve()
        self.proto = Path(module.OUT) / 'protocol.json'
        self.extra = {str(Path(p).resolve()): fresh_sha(p) for p in (*sources, *additional_sources)}
        self.metadata = dict(metadata, recovery_execution=True)
        self.old_freeze, self.old_dump = module.freeze, module.dump
        self.cache, self.bindings = None, []

    def install(self):
        @wraps(self.old_freeze)
        def freeze():
            self.old_freeze()
            original = json.loads(self.proto.read_text(encoding='utf-8-sig'))
            assert self.proto.parent.name == 'optimization_20261003_r66'
            combined = dict(original['input_sha256'])
            for source, digest in self.extra.items():
                assert source not in combined or combined[source] == digest, source
                combined[source] = digest
            scope = self.proto.parent / 'recovery_frozen_execution_v3_20261005.json'
            with scope.open('x', encoding='utf-8') as stream:
                json.dump({'status': 'frozen_before_actual_recovery_execution',
                           'input_sha256': combined, 'original_protocol_sha256': fresh_sha(self.proto),
                           'effective_execution_driver': self.metadata,
                           'original_frozen_protocol_not_changed': True,
                           'new_quality_scores': 0, 'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
            self.cache = LockedReadHashCache(combined)
            self.cache.__enter__()
            seen = set()
            for _, namespace in sorted(sys.modules.copy().items()):
                file = getattr(namespace, '__file__', None)
                if not file or Path(file).resolve().parent != self.analysis_root:
                    continue
                for obj in (namespace, *[v for v in vars(namespace).values() if isinstance(v, SimpleNamespace)]):
                    if id(obj) not in seen and callable(getattr(obj, 'sha', None)):
                        self.bindings.append((obj, obj.sha))
                        seen.add(id(obj))
                        obj.sha = self.cache.sha
        self.module.freeze = freeze
        return self

    def close(self, failed=False):
        for obj, function in self.bindings:
            obj.sha = function
        self.module.freeze, self.module.dump = self.old_freeze, self.old_dump
        if self.cache is None:
            return {'scope_started': False, 'recovery_execution': True}
        report = {'scope_started': True, 'sha_bindings': len(self.bindings),
                  'cache_hits': self.cache.hits, 'nonsealed_paths_rehashed': self.cache.fresh_calls,
                  'failed': bool(failed), 'recovery_execution': True,
                  'original_failed_scope_retained': True,
                  'original_protocol_sha256': fresh_sha(self.proto)}
        try:
            if not failed:
                self.cache.reverify()
                report['all_original_and_recovery_inputs_fully_rehashed_andmatched'] = True
        finally:
            self.cache.close()
        assert all(obj.sha is function for obj, function in self.bindings)
        assert self.module.freeze is self.old_freeze and self.module.dump is self.old_dump
        report['all_sha_bindings_restored'] = True
        return report
