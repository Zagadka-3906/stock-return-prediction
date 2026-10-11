from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from recover_HuberSparse150_serial_publication_v18_20261009 import execute
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute('publish_HuberSparse59_evidence_v1_20261009.py',p.parse_args().phase)
