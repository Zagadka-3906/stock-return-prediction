from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from Pure149_chunked_publication_receiver_runtime_v15_20261009 import execute
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute('publish_PureRFFHuber128_evidence_v2_20261008.py',p.parse_args().phase)
