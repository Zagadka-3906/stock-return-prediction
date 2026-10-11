"""Upload each completed new120 validation stage only after its real owned service passes."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();old=A/'run_stock_rank60_objective_actual_stages_main_v1_20261011.py';s=old.read_text(encoding='utf8').replace('stock_rank60','stock_rank120').replace('StockRank60','StockRank120').replace('rank60','rank120').replace('mature60','mature120').replace('mean60','mean120').replace('stockrank20class25','stockrank120').replace('六十日','一百二十日')
 before="('native42_official46',['actual_stock_rank120_embedding_six_state_native42_v1_20261011','actual_stock_rank120_embedding_after175_large_allocation29_screen_v1_20261011'])"
 assert s.count(before)==1;s=s.replace(before,"('native42',['actual_stock_rank120_embedding_six_state_native42_v1_20261011'])")
 start=s.index("  if stage=='native42_official46':");end=s.index("  text=template.read_text",start);s=s[:start]+s[end:]
 s=s.replace("'actual_mean120_maturity_CPU7_boundary12_and_fixture49153_passed':True","'actual_mean120_maturity_CPU7_boundary12_and_fixture49153_passed':True,'official33_scores_published_by_separate_completed_stage':True")
 p=A/'run_stock_rank120_objective_actual_stages_main_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
 assert allowed();r=start_service('actual_stock_rank120_objective_stages_main_v1_20261011',p.name,[],{str(p):sha(p),str(old):sha(old),str(Path(__file__)):sha(__file__)})
 create(A/'actual_stock_rank120_objective_stages_main_activation_v1_20261011.json',r)
 print({'actual120_stage_main_publication_queued_only_after_real_completed_stage':True},flush=True)
if __name__=='__main__':main()
