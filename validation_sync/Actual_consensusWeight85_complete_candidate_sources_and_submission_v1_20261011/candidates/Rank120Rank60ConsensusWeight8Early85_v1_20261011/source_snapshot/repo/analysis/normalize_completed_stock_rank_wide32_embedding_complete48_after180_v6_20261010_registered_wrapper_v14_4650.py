from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_verified4650_recovery_v14_20261011 import execute
if __name__=='__main__':execute('normalize_completed_stock_rank_wide32_embedding_complete48_after180_v6_20261010.py')
