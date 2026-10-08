"""Avoid competing with ongoing143 full candidate inference; then execute fresh40 own-window fits."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
def main():
    service=A/'service_owned_workflows_20261006/ConeRidgeFine68_selected_candidate_preparation_v1_20261008'
    while owned(read(service/'native_launch.json')):time.sleep(10)
    assert read(service/'service_execution.json')['status']=='passed'
    from train_nonflag_ConeRidgeAlpha8_64_bank40_v2_20261008 import main as bank
    bank()
if __name__=='__main__':main()
