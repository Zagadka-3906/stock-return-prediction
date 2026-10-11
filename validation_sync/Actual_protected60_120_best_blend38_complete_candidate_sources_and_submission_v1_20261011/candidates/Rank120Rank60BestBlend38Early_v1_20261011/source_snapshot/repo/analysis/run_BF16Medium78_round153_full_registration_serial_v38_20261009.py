from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from bind_future_import_namespaces_v38_20261009 import execute
if __name__=='__main__':execute(153,'run_BF16Medium78_round153_full_registration_v3_20261009.py')
