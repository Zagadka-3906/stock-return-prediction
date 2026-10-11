from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_reboot_complete_candidate_v11_20261011 import execute
if __name__=='__main__':execute('run_StockRank20LongEmbedding188_full_registration_v1_20261011_reboot_services_v11.py')
