from pathlib import Path
import sys,ast,re
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
old=A/'prepare_StockRank60Seed10Direct204_complete35_pipeline_v1_20261011.py'
s=old.read_text(encoding='utf8').replace('StockRank60Seed10','StockRank60Window504').replace('stock_rank60seed10','stock_rank60window504')
s=re.sub(r'(?<!\d)(204|203|487|115|18298)(?!\d)',lambda m:{'204':'206','203':'205','487':'489','115':'117','18298':'18372'}[m.group()],s)
s=s.replace("PARENT='Rank120Rank60Protected205_complete39_family_v1_20261011'","PARENT='Rank60TwoSeedProtected205_complete39_family_v2_20261011'")
s=s.replace("('seed09_e64','seed10_e64')","('seed09_e64','seed09_e64')")
s=s.replace("CONFIG['seed']==20261010","CONFIG['seed']==20261009")
s=s.replace(" s=s.replace('owned_idle_publication_wait_runtime", " s=s.replace('recent252','recent504').replace('Recent252','Recent504')\n s=s.replace('owned_idle_publication_wait_runtime",1)
s=s.replace("EXTRAS[17]=template.EXTRAS[17]", "EXTRAS[13]='stock_rank60window504_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json'\nEXTRAS[17]=template.EXTRAS[17]")
s=s.replace("  outputs.append(save(A/aliases[name],text))", "  text=text.replace('stock_rank60_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json','stock_rank60window504_actual_twelve_parent183_callbacks_CPU_controls_v2_20261011.json')\n  outputs.append(save(A/aliases[name],text))")
s=s.replace('rank60_seed10_pure33','rank60_window504_pure33').replace('actual33_seed10','actual33_window504')
p=A/'prepare_StockRank60Window504Direct206_complete35_pipeline_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
create(A/'rank60window504_complete206_factory_sources_admission_v1_20261011.json',{'status':'prospective206_own_window504_bank_and_callbacks_after_actual205_v2_parent_all_gates_retained','input_sha256':{str(old):sha(old),str(p):sha(p)},'new_fits_or_scores':0})
print(p,flush=True)
