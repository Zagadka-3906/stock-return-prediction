from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_actual_PairRank_native42_admission_v8_20261010 import execute
if __name__=='__main__':execute('run_StockPairRankEmbedding184_complete_family_v9_20261010.py')
