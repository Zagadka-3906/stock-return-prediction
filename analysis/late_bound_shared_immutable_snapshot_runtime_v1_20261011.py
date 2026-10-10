"""Bind a verified shared-board reader only after the actual publisher import."""
from contextlib import contextmanager, ExitStack
from pathlib import Path
from types import FunctionType
from shared_immutable_board_snapshot_runtime_v2_20261011 import installed as shared
from run_dependency_queue_v3_20261006 import create


@contextmanager
def installed(receiver, module_name, log):
    previous = receiver.main
    assert isinstance(previous, FunctionType)
    globals_copy = dict(previous.__globals__)
    builtins_copy = dict(previous.__builtins__)
    original_import = builtins_copy['__import__']
    seen, events = set(), []
    with ExitStack() as stack:
        def importing(name, *args, **kwargs):
            module = original_import(name, *args, **kwargs)
            if name == module_name and name not in seen:
                seen.add(name)
                stack.enter_context(shared(module, Path(log).with_name('shared_snapshot_scope_execution.json')))
                events.append({'module': name, 'shared_reader_bound_after_actual_publisher_import': True})
            return module
        builtins_copy['__import__'] = importing
        globals_copy['__builtins__'] = builtins_copy
        clone = FunctionType(previous.__code__, globals_copy, previous.__name__, previous.__defaults__, previous.__closure__)
        clone.__kwdefaults__ = previous.__kwdefaults__
        clone.__annotations__ = previous.__annotations__
        receiver.main = clone
        try:
            yield events
        finally:
            assert receiver.main is clone
            receiver.main = previous
    path = Path(log)
    path.parent.mkdir(parents=True, exist_ok=True)
    create(path, {'status': 'late_shared_immutable_snapshot_binding_and_receiver_restoration_completed',
                  'events': events, 'original_receiver_code_unchanged': True,
                  'new_quality_scores': 0, 'new_native_fits': 0, 'test_labels_read': False})
