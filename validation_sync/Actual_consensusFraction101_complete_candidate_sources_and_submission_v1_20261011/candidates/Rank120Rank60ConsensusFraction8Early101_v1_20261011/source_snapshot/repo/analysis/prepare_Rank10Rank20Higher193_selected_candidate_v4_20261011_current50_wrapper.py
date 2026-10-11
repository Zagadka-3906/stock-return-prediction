from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_current_publication_paths_and_prospective50_v1_20261011 import execute
if __name__=='__main__':execute('prepare_Rank10Rank20Higher193_selected_candidate_v4_20261011.py')
