from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from recover_Joint147_actual_scorer_upstream_v6_20261008 import execute
if __name__=='__main__':execute('prepare_JointCrossHuberOrder185_selected_candidate_v3_20261008.py')
