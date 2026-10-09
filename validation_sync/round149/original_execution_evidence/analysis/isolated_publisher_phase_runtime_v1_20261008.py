"""Give each publisher phase its own exclusive file-backed Git directory in this process only."""
from pathlib import Path
from contextlib import contextmanager


@contextmanager
def installed_phase(phase):
    assert phase in ('controls','scores')
    import verified_TLS_Git_retry_runtime_v2_20261008 as runtime
    original=runtime.installed
    def scoped(folder):
        return original(Path(folder)/('phase_'+phase+'_scope_v1'))
    runtime.installed=scoped
    try:yield
    finally:runtime.installed=original
