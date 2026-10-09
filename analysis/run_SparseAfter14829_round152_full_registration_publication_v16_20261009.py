from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from sparse150152_publication_safe_receivers_v16_20261009 import execute
if __name__=='__main__':execute(152,'run_SparseAfter14829_round152_full_registration_v2_20261009.py')
