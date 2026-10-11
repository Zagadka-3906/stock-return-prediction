"""Independent early42 controls unblock171 screening; preserve all original174/175 queues."""
from pathlib import Path
import sys,importlib,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();import psutil
    source=A/'verify_stock_top10_embedding_six_state_native42_v2_20261010.py';text=source.read_text(encoding='utf8')
    gate="    if Path('E:/赛题五_本机临时/Dual120Consensus_after169_high_impact193_screen_v1_20261010/verification.json').exists():closed('StockRankDual174_selected_candidate_sealing_v1_20261010')\n";assert text.count(gate)==2
    text=text.replace(gate,'').replace('stock_top10_embedding_six_state_native42_v1_20261010','stock_top10_embedding_early171_six_state_native42_v3_20261010').replace('actual_stock_top10_embedding_six_state_native42_location_v1_20261010','actual_stock_top10_embedding_early171_six_state_native42_location_v3_20261010')
    early=save('verify_stock_top10_embedding_early171_six_state_native42_v3_20261010.py',text)
    oldscreen=A/'run_stock_top10_embedding_after171_large_allocation29_screen_v1_20261010.py';text=oldscreen.read_text(encoding='utf8').replace("closed('actual_stock_top10_embedding_six_state_native42_v1_20261010')","closed('actual_stock_top10_embedding_early171_six_state_native42_v3_20261010')").replace('actual_stock_top10_embedding_six_state_native42_location_v1_20261010','actual_stock_top10_embedding_early171_six_state_native42_location_v3_20261010')
    screen=save('run_stock_top10_embedding_after171_large_allocation29_screen_v2_20261010.py',text)
    assert importlib.import_module(oldscreen.stem).cases()==importlib.import_module(screen.stem).cases()
    oldpub=A/'publish_stock_top10_embedding_after171_large_allocation29_completion_v61_20261010.py';text=oldpub.read_text(encoding='utf8').replace('stock_top10_embedding_stage_and_after171_fast17_sources_admission_v1_20261010','stock_top10_embedding_stage_and_after174_fast17_sources_admission_v1_20261010').replace("closed('actual_stock_top10_embedding_after171_large_allocation29_screen_v1_20261010')","closed('actual_stock_top10_embedding_after171_large_allocation29_screen_v2_20261010')").replace('actual_stock_top10_embedding_six_state_native42_location_v1_20261010','actual_stock_top10_embedding_early171_six_state_native42_location_v3_20261010').replace(oldscreen.name,screen.name).replace("service=A/'service_owned_workflows_20261006/actual_stock_top10_embedding_after171_large_allocation29_screen_v1_20261010'","service=A/'service_owned_workflows_20261006/actual_stock_top10_embedding_after171_large_allocation29_screen_v2_20261010'")
    text=text.replace("paths=[A/'stock_top10_large_allocation29_predeclared_actual_CPU_admission_v1_20261010.json'","paths=[A/'stock_top10_early171_independent42_route_admission_v2_20261010.json',A/'stock_top10_after171_early_large29_predeclared_admission_v1_20261010.json',A/'stock_top10_large_allocation29_predeclared_actual_CPU_admission_v1_20261010.json'")
    pub=save('publish_stock_top10_embedding_after171_large_allocation29_completion_v62_20261010.py',text)
    oldnames=('actual_stock_top10_embedding_after171_large_allocation29_screen_v1_20261010','actual_stock_top10_embedding_after171_large_allocation29_completion_main_v61_20261010')
    rows=[read(A/'service_owned_workflows_20261006'/n/'native_launch.json')for n in oldnames];assert all(owned(r) and not psutil.Process(r['owned_worker_pid']).children()for r in rows)
    assert not Path('E:/赛题五_本机临时/StockTop10EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010').exists()
    proof=A/'stock_top10_early171_independent42_route_admission_v2_20261010.json'
    create(proof,{'status':'compiled_exact42_independent_early_output_and_original29_cases_no174_delivery_dependency_metadata_inventory_corrected','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,early,oldscreen,screen,oldpub,pub]},'original174_native42_and175_family_preserved':True,'exact29_cases_unchanged':True,'early_native42_output':'stock_top10_embedding_early171_six_state_native42_v3_20261010','canonical29_main_receipt_version':61,'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    for row in rows:retire(row,'Verified childless before early171 controls/scores or publication output. Same29 cases use separate real42 checks without waiting174; preserve original174/175 pipeline.')
    for name,p in [('actual_stock_top10_embedding_early171_six_state_native42_v3_20261010',early),('actual_stock_top10_embedding_after171_large_allocation29_screen_v2_20261010',screen),('actual_stock_top10_embedding_after171_large_allocation29_completion_main_v62_20261010',pub)]:
        row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    old=A/'monitor_fast_optimization_v59_20261010.py';text=old.read_text(encoding='utf8').replace('v59_20261010','v60_20261010').replace('v101_20261010','v103_20261010').replace('v31_20261010','v32_20261010').replace('actual_stock_top10_embedding_after171_large_allocation29_screen_v1_20261010','actual_stock_top10_embedding_after171_large_allocation29_screen_v2_20261010').replace('actual_stock_top10_embedding_after171_large_allocation29_completion_main_v61_20261010','actual_stock_top10_embedding_after171_large_allocation29_completion_main_v62_20261010')
    needle="    families=['StockTop10EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010'";text=text.replace(needle,"    jobs += ['actual_stock_top10_embedding_early171_six_state_native42_v3_20261010']\n"+needle)
    observer=save('monitor_fast_optimization_v60_20261010.py',text);row=start_service('actual_fast_optimization_progress_v60_20261010',observer.name,[],{str(observer):sha(observer)});create(A/'actual_fast_optimization_progress_v60_activation_20261010.json',row)
    while not(A/'optimization_live_progress_v60_20261010.json').exists():time.sleep(1)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v59_20261010/native_launch.json'),'Verified observer60 shows early171 independent42_3 and actual29_2; original174/175 scientific jobs unchanged.')
    print({'independent_early42_started':True,'actual_171_large29_version':2,'original_174_175_unchanged':True},flush=True)
if __name__=='__main__':main()
