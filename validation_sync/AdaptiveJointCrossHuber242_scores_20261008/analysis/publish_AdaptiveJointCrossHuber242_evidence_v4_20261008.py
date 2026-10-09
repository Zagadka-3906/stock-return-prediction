from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from recover_Adaptive148_own_full_service_identity_v4_20261008 import execute
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute('publish_AdaptiveJointCrossHuber242_evidence_v2_20261008.py',p.parse_args().phase)
