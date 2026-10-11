from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from recover_Joint147_actual_scorer_upstream_v6_20261008 import execute
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('controls','scores'));execute('publish_JointCrossHuberOrder185_evidence_v4_20261008.py',parser.parse_args().phase)
