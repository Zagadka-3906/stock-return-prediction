from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from recover_actual146_candidate_state_dispatch_v6_20261008 import full
if __name__=='__main__':full()
