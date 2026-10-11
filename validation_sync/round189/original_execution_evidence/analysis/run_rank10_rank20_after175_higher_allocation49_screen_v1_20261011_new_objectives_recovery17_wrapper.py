from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_new_objectives_exact_source_recovery17_v1_20261011 import execute
if __name__=='__main__':execute('run_rank10_rank20_after175_higher_allocation49_screen_v1_20261011.py')
