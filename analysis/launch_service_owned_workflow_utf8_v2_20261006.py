"""Explicit UTF-8 script loading for a hidden Windows PowerShell service launcher."""
from pathlib import Path
import base64
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def launch(definition):
    definition = Path(definition).resolve()
    assert definition.is_relative_to(ROOT / 'analysis')
    assert not (definition.parent / 'launch_result.json').exists()
    source = ROOT / 'analysis/launch_service_owned_windows_workflow_20261006.ps1'
    # Windows PowerShell5 parses BOM-less script files using a legacy code page.
    # Decode the unchanged source explicitly, then bind its actual parameter.
    command = ("$PSDefaultParameterValues['Get-Content:Encoding']='utf8'; "
        + '& ([ScriptBlock]::Create([IO.File]::ReadAllText(' + quote(source)
        + ', [Text.Encoding]::UTF8))) -DefinitionPath ' + quote(definition))
    encoded = base64.b64encode(command.encode('utf-16-le')).decode('ascii')
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-EncodedCommand', encoded],
        cwd=ROOT, stdin=subprocess.DEVNULL, startupinfo=startup,
        creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True,
        text=True, encoding='utf-8', errors='replace', timeout=30)
    assert result.returncode == 0, result.stderr
    receipt = json.loads((definition.parent / 'launch_result.json').read_text(encoding='utf-8-sig'))
    assert receipt['ReturnValue'] == 0
    return receipt
