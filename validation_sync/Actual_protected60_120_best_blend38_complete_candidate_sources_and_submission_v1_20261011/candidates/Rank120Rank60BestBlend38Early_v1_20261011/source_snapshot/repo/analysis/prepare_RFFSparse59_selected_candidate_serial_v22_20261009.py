from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from verify_future_service_and_data_namespaces_v22_20261009 import execute
if __name__=='__main__':execute(151,'prepare_RFFSparse59_selected_candidate_v3_20261009.py')
