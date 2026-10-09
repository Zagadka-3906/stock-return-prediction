"""Hide actual stdlib and multiprocessing Windows children in the calling workflow."""
import os
import subprocess


def install():
    assert os.name == 'nt'
    import _winapi
    original = _winapi.CreateProcess
    events = []

    def create_process(application, command, process_attributes, thread_attributes,
                       inherit_handles, creationflags, environment, directory, startup):
        effective = creationflags & ~(subprocess.CREATE_NEW_CONSOLE | subprocess.DETACHED_PROCESS)
        effective |= subprocess.CREATE_NO_WINDOW
        if startup is not None:
            startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup.wShowWindow = subprocess.SW_HIDE
        result = original(application, command, process_attributes, thread_attributes,
            inherit_handles, effective, environment, directory, startup)
        events.append({'pid': result[2], 'original_creationflags': creationflags,
            'effective_creationflags': effective, 'CREATE_NO_WINDOW': True, 'SW_HIDE': True})
        return result

    _winapi.CreateProcess = create_process

    def restore():
        assert _winapi.CreateProcess is create_process
        _winapi.CreateProcess = original
        return list(events)

    return restore
