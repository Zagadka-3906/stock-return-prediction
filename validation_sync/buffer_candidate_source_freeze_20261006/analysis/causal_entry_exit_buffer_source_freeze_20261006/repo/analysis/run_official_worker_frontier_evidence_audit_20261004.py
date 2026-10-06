"""Wait for actual completed capacity controls before claiming audited evidence."""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]

def main():
    proof=ROOT/'analysis/official_worker_frontier_execution_20261004/verification.json'
    while True:
        try:value=json.loads(proof.read_text(encoding='utf-8-sig'))
        except (FileNotFoundError,json.JSONDecodeError):time.sleep(10);continue
        assert value['status']=='passed';break
    import audit_official_worker_frontier_scope_20261004 as audit
    audit.main()

if __name__=='__main__':main()
