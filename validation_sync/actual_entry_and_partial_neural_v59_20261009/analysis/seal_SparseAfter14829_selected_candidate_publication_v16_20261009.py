from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from sparse150152_publication_safe_receivers_v16_20261009 import execute
if __name__=='__main__':execute(152,'seal_SparseAfter14829_selected_candidate_v2_20261009.py')
