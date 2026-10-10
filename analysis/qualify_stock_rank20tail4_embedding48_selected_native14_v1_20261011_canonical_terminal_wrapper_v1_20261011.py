from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
if __name__=='__main__':
 assert allowed();m=importlib.import_module('qualify_stock_rank20tail4_embedding48_selected_native14_v1_20261011');m.closed=closed;m.main()
