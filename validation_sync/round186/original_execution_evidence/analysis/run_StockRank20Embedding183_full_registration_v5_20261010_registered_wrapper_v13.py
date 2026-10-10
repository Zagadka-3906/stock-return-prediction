from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_complete_registered180_v13_20261011 import execute
if __name__=='__main__':execute('run_StockRank20Embedding183_full_registration_v5_20261010_registered_services_v13.py')
