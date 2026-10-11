from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_new_objectives_exact_source_recovery18_v1_20261011 import execute
if __name__=='__main__':execute('run_Rank10Rank20Higher193_full_registration_v4_20261011.py')
