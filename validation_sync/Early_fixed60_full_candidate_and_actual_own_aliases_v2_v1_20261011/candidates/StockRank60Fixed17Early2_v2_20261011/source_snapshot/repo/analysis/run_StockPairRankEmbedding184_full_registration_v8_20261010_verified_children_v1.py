from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_StockPairRank184_exact_verified_children_v1_20261010 import execute
if __name__=='__main__':execute('run_StockPairRankEmbedding184_full_registration_v8_20261010.py')
