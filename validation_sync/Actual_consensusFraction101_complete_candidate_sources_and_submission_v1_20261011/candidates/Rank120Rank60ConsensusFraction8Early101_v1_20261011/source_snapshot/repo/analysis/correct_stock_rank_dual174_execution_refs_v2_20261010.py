"""Use fresh drivers for literal execution references before any scientific dispatch."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed()
    mapping={'run_StockRankDual174_full_registration_v1_20261010':'run_StockRankDual174_full_registration_v2_20261010','run_StockRankDual174_complete_family_v1_20261010':'run_StockRankDual174_complete_family_v2_20261010','run_StockRankDual174_complete_family_v3_20261010':'run_StockRankDual174_complete_family_v2_20261010','verify_StockRankDual174_full36_preflight_v3_20261010':'verify_StockRankDual174_full44_preflight_v2_20261010','verify_StockRankDual174_full44_preflight_v1_20261010':'verify_StockRankDual174_full44_preflight_v2_20261010','stock_rank_dual174_full_family_preflight_v3_20261010':'stock_rank_dual174_full_family_preflight_v2_20261010','stock_rank_dual174_full_family_preflight_v1_20261010':'stock_rank_dual174_full_family_preflight_v2_20261010'}
    import re
    sources=[A/'run_StockRankDual174_full_registration_v1_20261010.py',A/'run_StockRankDual174_complete_family_v1_20261010.py',A/'verify_StockRankDual174_full44_preflight_v1_20261010.py'];outputs=[]
    for source in sources:
        text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],source.read_text(encoding='utf8'))
        dest=A/(mapping[source.stem]+'.py');assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n');outputs.append(dest);importlib.import_module(dest.stem)
    assert not Path('E:/赛题五_本机临时/第174轮_20261010').exists()
    retire(read(A/'service_owned_workflows_20261006/StockRankDual174_complete44_family_v1_20261010/native_launch.json'),'Verified childless selected14 wait superseded by fresh execution2 references; no selected scientific output, score or inference began.')
    family=A/'run_StockRankDual174_complete_family_v2_20261010.py'
    row=start_service('StockRankDual174_complete44_family_v2_20261010',family.name,[],{str(family):sha(family)})
    create(A/'actual_StockRankDual174_complete44_family_activation_v2_20261010.json',row)
    create(A/'stock_rank_dual174_actual_execution_refs_admission_v2_20261010.json',{'status':'passed_fresh_compiled_imported_full174_drivers_with_exact_existing_execution2_source_literals_before_selected14_dispatch','input_sha256':{str(p):sha(p) for p in [Path(__file__),*sources,*outputs]},'actual_service':row,'scientific_outputs_restarted':0,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False})
    print({'actual_full174_family_version':2,'scientific_dispatch_started':False},flush=True)
if __name__=='__main__':main()
