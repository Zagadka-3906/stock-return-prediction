from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_StockTopPair185_exact_verified_children_v1_20261010 import execute
if __name__=='__main__':execute('prepare_StockTopPairEmbedding185_selected_candidate_v8_20261010.py')
