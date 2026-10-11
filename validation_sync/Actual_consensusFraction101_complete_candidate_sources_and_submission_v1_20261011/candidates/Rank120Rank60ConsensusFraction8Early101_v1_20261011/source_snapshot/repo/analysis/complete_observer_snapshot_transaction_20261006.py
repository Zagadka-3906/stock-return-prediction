"""Keep intermediate observer layers private until the complete update succeeds."""
from pathlib import Path
from contextlib import contextmanager
import copy
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = {ROOT / 'analysis' / name for name in (
    'ongoing_optimization_state.json', 'resume_optimization_20261004.json',
    'actual_optimization_monitor_state_20261005.json')}


@contextmanager
def transaction():
    import atomic_optimization_observer_writes_20261005 as atomic
    original_read, original_write_text, original_atomic = Path.read_text, Path.write_text, atomic.write
    pending, bindings = {}, []

    def read_text(path, *args, **kwargs):
        resolved = Path(path).resolve()
        if resolved in pending:
            return json.dumps(pending[resolved], ensure_ascii=False)
        return original_read(path, *args, **kwargs)

    def write(path, value):
        resolved = Path(path).resolve()
        if resolved in PUBLIC:
            pending[resolved] = copy.deepcopy(value)
        else:
            original_atomic(path, value)

    def write_text(path, data, *args, **kwargs):
        resolved = Path(path).resolve()
        if resolved in PUBLIC:
            pending[resolved] = json.loads(data)
            return len(data)
        return original_write_text(path, data, *args, **kwargs)

    def commit(generation):
        assert set(pending) == PUBLIC, 'Every complete public state is required.'
        for value in pending.values():
            value['complete_observer_generation'] = generation
            value['intermediate_observer_layers_not_published'] = True
        for path in sorted(PUBLIC):
            original_atomic(path, pending[path])

    try:
        Path.read_text, Path.write_text, atomic.write = read_text, write_text, write
        for name, module in tuple(sys.modules.items()):
            if name.startswith('monitor_actual_optimization_progress_') and callable(getattr(module, 'write', None)):
                bindings.append((module, module.write))
                module.write = write
        yield pending, commit
    finally:
        for module, original in reversed(bindings):
            module.write = original
        Path.read_text, Path.write_text, atomic.write = original_read, original_write_text, original_atomic
