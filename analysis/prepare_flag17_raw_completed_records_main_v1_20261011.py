from pathlib import Path
import sys,ast,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
p=A/'run_publish_rank120_after183_completed33_main_v1_20261011.py';s=p.read_text(encoding='utf8')
for old,new in [('actual_stock_rank120_embedding_after183_direct_allocation33','actual_stock_rank60_flag17_after183_direct17'),('StockRank120EmbeddingSmall512_after183_direct_allocation33_screen','StockRank60FlagOnly_after183_direct17_screen'),('stock_rank120_after183_direct33_predeclared_sources','rank60_flag17_raw_sources_predeclared'),('Rank120_after183_actual33','Rank60FlagOnly_after183_actual17')]:s=s.replace(old,new)
for old,new in [(33,17),(32,16),(96,48)]:s=re.sub(r'(?<!\d)'+str(old)+r'(?!\d)',str(new),s)
q=A/'run_publish_rank60_flag17_after183_completed17_main_v1_20261011.py';ast.parse(s);assert not q.exists();q.write_text(s,encoding='utf8',newline='\n')
assert allowed();i=start_service('actual_rank60_flag17_completed17_main_v1_20261011',q.name,[],{str(q):sha(q),str(p):sha(p)});create(A/'actual_rank60_flag17_completed17_main_activation_v1_20261011.json',i)
print('Independent all17 raw official records main publisher queued, regardless of candidate gain',flush=True)
