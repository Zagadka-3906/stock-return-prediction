from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from recover_Joint147_publisher_phase_scratch_v7_20261008 import execute
if __name__=='__main__':execute('run_JointCrossHuberOrder185_round147_full_registration_v5_20261008.py')
