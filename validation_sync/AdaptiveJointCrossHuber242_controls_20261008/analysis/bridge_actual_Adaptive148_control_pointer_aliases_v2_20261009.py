from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from resume_pending148_verified_gates_v5_20261009 import execute
if __name__=='__main__':execute('bridge_actual_Adaptive148_control_pointer_aliases_v1_20261008.py')
