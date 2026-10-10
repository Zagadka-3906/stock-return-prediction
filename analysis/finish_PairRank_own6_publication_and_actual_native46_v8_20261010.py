from pathlib import Path
import sys,time,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    f=A/'service_owned_workflows_20261006/actual_StockPairRank_objective_stages_main_v1_20261010'
    row=read(f/'native_launch.json')
    while owned(row):assert allowed();time.sleep(10)
    assert read(A/'StockPairRank_objective_own6_full5_main_receipt_v1_20261010.json')['status']=='pushed_and_remote_head_verified'
    runpy.run_path(str(A/'publish_stock_pairrank_objective_remaining_native46_main_v2_20261010_actual_native_admission_v8.py'),run_name='__main__')
if __name__=='__main__':main()
