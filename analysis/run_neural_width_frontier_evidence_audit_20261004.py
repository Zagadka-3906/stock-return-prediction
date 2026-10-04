"""Audit GPU controls after CPU capacity jobs finish, preserving benchmark background."""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]

def main():
    gates=[ROOT/'analysis/neural_width_frontier_20261004/verification.json',
        ROOT/'analysis/official_worker_frontier_execution_20261004/verification.json',
        ROOT/'analysis/official_worker_frontier_scope_audit_20261004.json']
    while True:
        try:values=[json.loads(p.read_text(encoding='utf-8-sig')) for p in gates]
        except (FileNotFoundError,json.JSONDecodeError):time.sleep(10);continue
        assert values[0]['status'] in ('passed','failed') and all(v['status']=='passed' for v in values[1:]);break
    import audit_neural_width_frontier_scope_20261004 as audit
    audit.main()

if __name__=='__main__':main()
