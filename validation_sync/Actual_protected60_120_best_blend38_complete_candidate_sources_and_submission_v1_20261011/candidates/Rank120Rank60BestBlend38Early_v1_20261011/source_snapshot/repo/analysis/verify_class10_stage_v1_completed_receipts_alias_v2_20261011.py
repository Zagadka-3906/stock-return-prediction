from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('actual_stock_rank20class10_objective_stages_main_v1_20261011');rows=[]
 for stage in ('restart_CPU','own6_full5','native42_official46'):
  p=A/f'StockRank20Class10_objective_{stage}_sources_main_receipt_v1_20261011.json';r=read(p);assert r['status']=='pushed_and_remote_head_verified' and r['branch']=='main';rows.append({'source':str(p),'sha256':sha(p),'receipt':r})
 create(A/'stock_rank20class10_actual_completed_v1_publication_alias_v2_20261011.json',{'status':'passed_actual_all3_completed_v1_receipts_metadata_alias_only','receipts':rows,'new_fits':0,'new_scores':0,'no_new_publication':True})
if __name__=='__main__':main()
