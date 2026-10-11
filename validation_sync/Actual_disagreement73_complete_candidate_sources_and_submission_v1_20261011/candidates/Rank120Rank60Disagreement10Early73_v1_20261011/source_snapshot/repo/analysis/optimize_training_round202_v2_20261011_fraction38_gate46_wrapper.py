from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_fraction38_gate_only_prospective46_v1_20261011 import execute
if __name__=='__main__':execute('optimize_training_round202_v2_20261011.py')
