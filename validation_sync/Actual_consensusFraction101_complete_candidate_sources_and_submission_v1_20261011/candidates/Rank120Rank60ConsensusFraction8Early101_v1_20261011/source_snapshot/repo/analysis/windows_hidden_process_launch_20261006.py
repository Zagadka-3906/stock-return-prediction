"""Create background console processes without conflicting console flags."""
import subprocess


def launch(arguments, **kwargs):
    kwargs.setdefault('stdin', subprocess.DEVNULL)
    flags = kwargs.pop('creationflags', 0)
    flags &= ~(subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_CONSOLE)
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    return subprocess.Popen(arguments, creationflags=flags | subprocess.CREATE_NO_WINDOW,
                            startupinfo=startup, **kwargs)
