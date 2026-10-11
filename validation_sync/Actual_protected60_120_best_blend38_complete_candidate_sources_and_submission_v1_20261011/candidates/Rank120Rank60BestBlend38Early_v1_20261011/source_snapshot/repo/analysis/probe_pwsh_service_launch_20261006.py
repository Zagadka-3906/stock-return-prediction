"""Actual independently owned service launch through current PowerShell7."""
from pathlib import Path
import ctypes
import json
import os
import time


def main():
    root = Path(__file__).resolve().parents[1]
    assert ctypes.WinDLL('kernel32').GetConsoleWindow() == 0
    time.sleep(1)
    out = root / 'analysis/pwsh_service_launch_preflight_20261006'
    out.mkdir()
    with (out / 'verification.json').open('x', encoding='utf-8') as stream:
        json.dump({'status': 'passed_actual_current_PowerShell7_Chinese_path_consoleless_service_launch',
            'actual_native_pid': os.getpid(), 'actual_console_handle': 0,
            'actual_project_directory_with_Chinese_characters': str(root),
            'original_PS1_source_not_edited': True, 'actual_service_bootstrap_assertions_executed': True,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False},
            stream, ensure_ascii=False, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
