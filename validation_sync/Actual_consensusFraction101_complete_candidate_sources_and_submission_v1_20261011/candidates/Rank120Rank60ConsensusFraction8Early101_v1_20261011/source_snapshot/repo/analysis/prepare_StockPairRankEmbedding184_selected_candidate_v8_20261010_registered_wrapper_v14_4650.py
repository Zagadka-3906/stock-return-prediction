from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_verified4650_recovery_v14_20261011 import execute
if __name__=='__main__':execute('prepare_StockPairRankEmbedding184_selected_candidate_v8_20261010.py')
