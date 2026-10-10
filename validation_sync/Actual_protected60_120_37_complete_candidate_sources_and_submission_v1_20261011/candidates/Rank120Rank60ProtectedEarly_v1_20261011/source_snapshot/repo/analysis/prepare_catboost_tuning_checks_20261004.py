"""Wait for the frozen training bank, then verify both prospective constructions."""
from pathlib import Path
import json
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]


def main():
    gate=ROOT/'analysis/catboost_tuning_bank_20261004/oof_audit.json'
    last=time.monotonic()
    while not gate.exists():
        time.sleep(10)
        if time.monotonic()-last>=50:
            print('Waiting for all25 mature annual models; no validation scoring performed.',flush=True);last=time.monotonic()
    proof=json.loads(gate.read_text(encoding='utf-8-sig'));assert proof['status']=='passed'
    for script,proof_name in (
        ('preflight_final_roles_round37_v2.py','final_roles_round37_preflight_v2'),
        ('preflight_standalone_round38_v2.py','standalone_round38_preflight_v2')):
        destination=ROOT/f'analysis/{proof_name}/verification.json'
        if destination.exists():assert json.loads(destination.read_text(encoding='utf-8-sig'))['status']=='passed';continue
        print('Checking '+script,flush=True)
        subprocess.run([sys.executable,'-B','-X','utf8',str(ROOT/'analysis'/script)],cwd=ROOT,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert json.loads(destination.read_text(encoding='utf-8-sig'))['status']=='passed'
    print('Both prospective CatBoost-tuning preflights passed; scoring waits for complete predecessor rounds.',flush=True)


if __name__=='__main__':main()
