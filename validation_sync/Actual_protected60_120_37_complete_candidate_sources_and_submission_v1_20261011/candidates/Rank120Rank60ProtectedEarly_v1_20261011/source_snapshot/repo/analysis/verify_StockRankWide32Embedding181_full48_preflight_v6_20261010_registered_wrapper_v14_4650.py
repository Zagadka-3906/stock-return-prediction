from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_verified4650_recovery_v14_20261011 import execute
if __name__=='__main__':execute('verify_StockRankWide32Embedding181_full48_preflight_v6_20261010.py')
