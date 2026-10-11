from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_new_objectives_exact_source_recovery34_v1_20261011 import installed
if __name__=='__main__':
 closed,start,data=installed()
 runpy.run_path(str(A/'qualify_stock_rank20class10_embedding48_selected_native14_v1_20261011_canonical_terminal_wrapper_v1_20261011.py'),run_name='__main__')
