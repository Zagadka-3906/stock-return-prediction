from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from route_verified_canonical_publication_and_failed_chain38_v1_20261011 import execute
if __name__=='__main__':execute('stock_rank20long_embedding_small512_BF16_native_v1_20261010.py')
