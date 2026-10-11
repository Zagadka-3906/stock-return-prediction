from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_current_publication_paths_and_prospective53_v1_20261011 import execute
if __name__=='__main__':execute('run_StockRank20Seed10Embedding186_full_registration_v2_20261011.py')
