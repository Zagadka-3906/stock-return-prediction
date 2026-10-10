from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_verified_Dual25_recovery_dependencies_v7_20261010 import execute
if __name__=='__main__':execute('run_StockRank20Embedding180_full_registration_v5_20261010.py')
