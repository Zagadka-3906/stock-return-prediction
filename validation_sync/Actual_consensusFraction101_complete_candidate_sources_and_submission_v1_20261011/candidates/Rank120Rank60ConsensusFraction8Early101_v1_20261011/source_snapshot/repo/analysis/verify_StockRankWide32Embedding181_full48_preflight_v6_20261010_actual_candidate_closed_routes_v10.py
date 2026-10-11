from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_actual_candidate_closed_and180_continuation_v10_20261011 import execute
if __name__=='__main__':execute('verify_StockRankWide32Embedding181_full48_preflight_v6_20261010.py')
