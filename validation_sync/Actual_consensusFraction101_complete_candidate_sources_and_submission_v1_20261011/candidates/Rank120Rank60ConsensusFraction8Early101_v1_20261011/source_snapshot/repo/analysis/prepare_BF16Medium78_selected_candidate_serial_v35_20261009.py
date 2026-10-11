from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from bind_future_import_namespaces_v35_20261009 import execute
if __name__=='__main__':execute(153,'prepare_BF16Medium78_selected_candidate_v1_20261009.py')
