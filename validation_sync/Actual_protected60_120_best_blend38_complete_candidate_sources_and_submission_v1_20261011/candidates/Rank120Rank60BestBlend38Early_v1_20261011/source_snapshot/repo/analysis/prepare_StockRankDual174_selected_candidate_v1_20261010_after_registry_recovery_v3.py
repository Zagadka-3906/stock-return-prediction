from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_verified_Dual25_recovery_dependencies_v3_20261010 import execute
if __name__=='__main__':execute('prepare_StockRankDual174_selected_candidate_v1_20261010.py')
