"""Start scientific training only after genuine codec and source admission processes close."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
def main():
    f=A/'service_owned_workflows_20261006/nonflag_residual_HGB10_training_admission'
    while not (f/'native_launch.json').exists() or owned(read(f/'native_launch.json')):time.sleep(10)
    assert read(f/'service_execution.json')['status']=='passed'
    from train_nonflag_residual_HGB_bank10_20261007 import main as actual
    actual()
if __name__=='__main__':main()
