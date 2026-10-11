"""Serial real alpha probes and40 own-window bank fits, before any candidate quality."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
def main():
    plan=read(A/'nonflag_ConeRidgeAlpha8_64_bank40_plan_v1_20261008.json')
    for path,digest in plan['input_sha256'].items():assert sha(path)==digest,path
    from verify_nonflag_ConeRidgeAlpha8_64_small_v1_20261008 import main as small
    from verify_nonflag_ConeRidgeAlpha8_64_actual200k_v1_20261008 import main as probe
    from train_nonflag_ConeRidgeAlpha8_64_bank40_v1_20261008 import main as bank
    small();probe();bank()
if __name__=='__main__':main()
