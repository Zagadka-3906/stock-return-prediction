from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from verify_future_service_and_data_namespaces_v22_20261009 import execute
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute(153,'publish_BF16Medium78_evidence_v2_20261009.py',p.parse_args().phase)
