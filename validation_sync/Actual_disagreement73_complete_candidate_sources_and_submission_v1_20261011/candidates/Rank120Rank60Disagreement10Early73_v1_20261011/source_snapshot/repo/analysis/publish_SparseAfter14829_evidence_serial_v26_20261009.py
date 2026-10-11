from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from bind_future_import_namespaces_v26_20261009 import execute
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute(152,'publish_SparseAfter14829_evidence_v1_20261009.py',p.parse_args().phase)
