from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
def main():
 assert allowed();old=A/'prepare_actual_observer111_parent3133_v1_20261011.py';new=A/'prepare_actual_observer112_parent3134_v1_20261011.py';assert not new.exists()
 s=old.read_text(encoding='utf8').replace('v111','v112').replace('v110','v111').replace('.110.tmp','.111.tmp').replace('.111.tmp','.112.tmp').replace('recovery33','recovery34').replace('parent3133','parent3134').replace('handoff_v195','handoff_v200').replace('handoff_v200','handoff_v201')
 s=s.replace(" names=[current_name(n) for n in names]"," names=[current_name(n).replace('recovery33_','recovery34_') for n in names]")
 s=s.replace("'actual_parent3133_frozen_publication_runtime_sources_main_v1_20261011'","'actual_parent3134_frozen_publication_runtime_sources_main_v1_20261011'")
 s=s.replace(" names += [n for n,_", " names+=['actual_stock_rank20class10_complete195_factory_v1_20261011','StockRank20Class10Embedding195_complete48_family_v1_20261011','actual_stock_rank20class10_embedding48_after194_normalization_queue_v1_20261011','StockRank20Class10Embedding48_selected_native14_v1_20261011']\n names += [n for n,_")
 # The existing111 handoff is200, and source prep's first replace must point to that actual filename.
 s=s.replace(".replace('handoff_v201','handoff_v200')",".replace('handoff_v200','handoff_v201')")
 compile(s,str(new),'exec');new.write_text(s,encoding='utf8',newline='\n');runpy.run_path(str(new),run_name='__main__')
 p=A/'run_publish_actual_parent3134_runtime_sources_main_v1_20261011.py';assert allowed();row=start_service('actual_parent3134_frozen_publication_runtime_sources_main_v1_20261011',p.name,[],{str(p):sha(p)});create(A/'actual_parent3134_frozen_publication_runtime_sources_main_activation_v1_20261011.json',row)
if __name__=='__main__':main()
