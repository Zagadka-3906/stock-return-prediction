from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_complete_registered180_v12_20261011 import execute
if __name__=='__main__':execute('run_StockRank20LongEmbedding188_complete_family_v1_20261011.py')
