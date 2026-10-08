from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from recover_Joint147_actual_scorer_upstream_v6_20261008 import execute
if __name__=='__main__':execute('verify_JointCrossHuberOrder185_round147_sources_v2_20261008.py')
