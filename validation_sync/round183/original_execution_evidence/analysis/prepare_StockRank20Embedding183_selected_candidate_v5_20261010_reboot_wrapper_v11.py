from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_reboot_complete_candidate_v11_20261011 import execute
if __name__=='__main__':execute('prepare_StockRank20Embedding183_selected_candidate_v5_20261010.py')
