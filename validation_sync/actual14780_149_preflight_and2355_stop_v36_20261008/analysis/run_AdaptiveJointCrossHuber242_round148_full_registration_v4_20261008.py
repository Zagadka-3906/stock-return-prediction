from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from recover_Adaptive148_own_full_service_identity_v4_20261008 import execute
if __name__=='__main__':execute('run_AdaptiveJointCrossHuber242_round148_full_registration_v2_20261008.py')
