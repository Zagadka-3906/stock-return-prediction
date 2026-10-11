"""Use an explicitly verified current PowerShell runtime and hide its console."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def launch(definition, powershell):
    definition, powershell = Path(definition).resolve(), Path(powershell).resolve()
    assert definition.is_relative_to(ROOT / 'analysis') and powershell.name.lower() == 'pwsh.exe'
    assert powershell.is_file() and not (definition.parent / 'launch_result.json').exists()
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    kwargs = dict(cwd=ROOT, stdin=subprocess.DEVNULL, startupinfo=startup,
        creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True,
        text=True, encoding='utf-8', errors='replace', timeout=30)
    version = subprocess.run([str(powershell), '--version'], **kwargs)
    assert version.returncode == 0 and version.stdout.startswith('PowerShell 7.'), version.stdout
    source = ROOT / 'analysis/launch_service_owned_windows_workflow_20261006.ps1'
    result = subprocess.run([str(powershell), '-NoProfile', '-NonInteractive', '-File',
        str(source), '-DefinitionPath', str(definition)], **kwargs)
    assert result.returncode == 0, result.stderr
    receipt = json.loads((definition.parent / 'launch_result.json').read_text(encoding='utf-8-sig'))
    assert receipt['ReturnValue'] == 0
    return {'actual_verified_runtime': version.stdout.strip(), 'actual_runtime_path': str(powershell),
            'actual_launch_result': receipt, 'CREATE_NO_WINDOW': True, 'SW_HIDE': True}
