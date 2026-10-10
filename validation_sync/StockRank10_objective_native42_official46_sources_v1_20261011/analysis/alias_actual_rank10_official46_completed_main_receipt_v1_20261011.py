from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('actual_stock_rank10_objective_stages_main_v3_20261011')
 p=A/'StockRank10_objective_native42_official46_sources_main_receipt_v1_20261011.json';r=read(p)
 assert r['status']=='pushed_and_remote_head_verified' and r['branch']=='main'
 create(A/'StockRank10_objective_native42_official46_main_receipt_v1_20261011.json',r)
 create(A/'rank10_official46_main_receipt_filename_alias_v1_20261011.json',{'status':'passed_actual_completed46_main_receipt_byte_equivalent_metadata_alias','source':str(p),'source_sha256':sha(p),'commit':r['commit'],'new_publication_or_score_claimed':False})
if __name__=='__main__':main()
