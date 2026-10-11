"""Protected original146 mathematical receiver; actual5 operational source closure and full contexts."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from prepare_actual146_full_context_receiver_v5_20261008 import execute
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute('publish_HuberCrossFamilyFine125_evidence_v3_20261008.py',p.parse_args().phase)
