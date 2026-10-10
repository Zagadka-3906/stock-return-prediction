"""Test the complete new classifier on an already qualified anchor without waiting for174."""
from pathlib import Path
import sys,importlib,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    release=read(A/'github_validation_sync_main_20261005/round171_receipt.json');assert release['status']=='pushed_and_remote_head_verified' and release['scored_records']==233
    source=A/'run_stock_top10_embedding_after174_large_allocation29_screen_v1_20261010.py';text=source.read_text(encoding='utf8')
    wait="    closed('actual_stock_top10_embedding_after174_fast17_screen_v1_20261010')\n";assert text.count(wait)==1;text=text.replace(wait,'')
    text=text.replace('StockRankDual174_complete44_family_v2_20261010','Frontier233171_complete233_family_v2_20261010').replace("release['scored_records']==44","release['scored_records']==233").replace('174','171')
    screen=save('run_stock_top10_embedding_after171_large_allocation29_screen_v1_20261010.py',text)
    module=importlib.import_module(screen.stem);assert module.cases()==importlib.import_module(source.stem).cases() or all({**r,'kind':'anchor174'}==s for r,s in zip(module.cases()[:1],importlib.import_module(source.stem).cases()[:1]))
    expected=importlib.import_module(source.stem).cases();actual=module.cases();assert len(actual)==29 and actual[1:]==expected[1:] and actual[0]['kind']=='anchor171'
    proof=A/'stock_top10_after171_early_large29_predeclared_admission_v1_20261010.json'
    create(proof,{'status':'compiled_exact_same29_classifier_weights_on_already_fully_qualified171_independent_of_pending174','input_sha256':{str(p):sha(p) for p in (Path(__file__),source,screen,A/'github_validation_sync_main_20261005/round171_receipt.json',A/'stock_top10_large_allocation29_predeclared_actual_CPU_admission_v1_20261010.json')},'cases':actual,'classifier_own6_full5_native42_required_before_scores':True,'current_qualified_parent':171,'new_fits':0,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False,'must_compare_with_complete175_in_followup_selection':True})
    sourcepub=A/'publish_stock_top10_embedding_after174_large_allocation29_completion_v60_20261010.py';text=sourcepub.read_text(encoding='utf8').replace('174','171').replace('v60_20261010','v61_20261010')
    pub=save('publish_stock_top10_embedding_after171_large_allocation29_completion_v61_20261010.py',text)
    for name,p in [('actual_stock_top10_embedding_after171_large_allocation29_screen_v1_20261010',screen),('actual_stock_top10_embedding_after171_large_allocation29_completion_main_v61_20261010',pub)]:
        row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    old=A/'monitor_fast_optimization_v58_20261010.py';text=old.read_text(encoding='utf8').replace('v58_20261010','v59_20261010').replace('v99_20261010','v101_20261010').replace('v30_20261010','v31_20261010')
    needle="    families=['StockTop10EmbeddingSmall512_after174_large_allocation29_screen_v1_20261010'";assert text.count(needle)==1
    text=text.replace(needle,"    jobs += ['actual_stock_top10_embedding_after171_large_allocation29_screen_v1_20261010','actual_stock_top10_embedding_after171_large_allocation29_completion_main_v61_20261010']\n    families=['StockTop10EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010','StockTop10EmbeddingSmall512_after174_large_allocation29_screen_v1_20261010'")
    needle="('StockTop10EmbeddingSmall512_after174_high_impact17_screen_v1_20261010',17)";text=text.replace(needle,"('StockTop10EmbeddingSmall512_after171_large_allocation29_screen_v1_20261010',29),('StockTop10EmbeddingSmall512_after174_large_allocation29_screen_v1_20261010',29),"+needle)
    observer=save('monitor_fast_optimization_v59_20261010.py',text);row=start_service('actual_fast_optimization_progress_v59_20261010',observer.name,[],{str(observer):sha(observer)});create(A/'actual_fast_optimization_progress_v59_activation_20261010.json',row)
    while not (A/'optimization_live_progress_v59_20261010.json').exists():time.sleep(1)
    retire(read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_v58_20261010/native_launch.json'),'Verified observer59 shows early29 actual171 anchor as separate family; full175 unchanged and no scientific worker stopped.')
    print({'early_actual171_large29_queue_started':True,'actual_official_scores':0,'observer':59,'final175_pipeline_unchanged':True},flush=True)
if __name__=='__main__':main()
