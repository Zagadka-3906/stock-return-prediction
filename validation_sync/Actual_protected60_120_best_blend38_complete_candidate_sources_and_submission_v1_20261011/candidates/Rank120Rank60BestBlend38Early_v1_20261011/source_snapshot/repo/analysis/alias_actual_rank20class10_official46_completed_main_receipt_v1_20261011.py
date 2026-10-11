from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
if __name__=='__main__':
 assert allowed();closed('actual_stock_rank20class10_objective_stages_main_v2_20261011')
 p=A/'StockRank20Class10_objective_native42_official46_sources_main_receipt_v1_20261011.json';r=read(p);assert r['status']=='pushed_and_remote_head_verified' and r['branch']=='main'
 create(A/'StockRank20Class10_objective_native42_official46_main_receipt_v1_20261011.json',{**r,'actual_receipt_source':str(p),'actual_receipt_sha256':sha(p),'new_scores':0})
