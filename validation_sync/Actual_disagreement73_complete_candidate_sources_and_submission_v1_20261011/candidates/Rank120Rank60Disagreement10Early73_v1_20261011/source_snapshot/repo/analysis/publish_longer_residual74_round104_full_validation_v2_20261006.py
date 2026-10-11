"""Preserve the original complete publication and add the actual handle-limit recovery."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
SOURCE=A/'publish_longer_residual74_round104_full_validation_20261006.py'


def main():
    text=SOURCE.read_text(encoding='utf-8')
    before='    for path in extra:'
    assert text.count(before)==1
    text=text.replace(before,
        "    extra += [RECOVERY_PUBLISHER_SOURCE,\n"
        "        A / 'run_longer_residual74_round104_full_registration_v2_20261006.py',\n"
        "        A / 'win32_read_handle_hash_cache_20261006.py',\n"
        "        A / 'win32_read_handle_hash_cache_full104_preflight_20261006.json',\n"
        "        A / 'optimization_20261003_r104/full_registration_failure.json',\n"
        "        A / 'optimization_20261003_r104/frozen_before_actual_full_registration_v2.json',\n"
        "        A / 'optimization_20261003_r104/actual_main7_idle_before_and_after_hold_v2.json']\n"
        "    extra += list((A / 'service_owned_workflows_20261006/longer_residual74_round104_full_registration').glob('*.json'))\n"
        "    extra += list((A / 'service_owned_workflows_20261006/longer_residual74_round104_full_registration').glob('*.log'))\n"+before)
    namespace={'__file__':__file__,'__name__':'actual_full104_native_read_handle_recovery_publication',
        'RECOVERY_PUBLISHER_SOURCE':Path(__file__)}
    exec(compile(text,str(SOURCE),'exec'),namespace)
    namespace['main']()


if __name__=='__main__':main()
