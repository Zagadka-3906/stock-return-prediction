from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from bind_future151to153_serial_receivers_v21_20261009 import execute
if __name__=='__main__':execute(153,'run_BF16Medium78_official_comparison_v2_20261009.py')
