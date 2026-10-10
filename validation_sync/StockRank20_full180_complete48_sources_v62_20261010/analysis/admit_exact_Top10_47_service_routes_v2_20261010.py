"""Correct generated administrative names before normalization, selected replay or inference."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();import psutil
    oldnames=('actual_stock_top10_embedding47_after174_normalization_queue_v1_20261010','StockTop10Embedding47_selected_native14_v1_20261010')
    rows=[read(A/'service_owned_workflows_20261006'/n/'native_launch.json') for n in oldnames]
    assert all(owned(r) and not psutil.Process(r['owned_worker_pid']).children() for r in rows)
    assert not Path('E:/赛题五_本机临时/stock_top10_embedding_complete47_after174_v1_20261010').exists()
    assert not Path('E:/赛题五_本机临时/stock_top10_embedding47_selected_native14_v1_20261010').exists()
    original=A/'normalize_completed_stock_top10_embedding47_after174_v1_20261010.py';text=original.read_text(encoding='utf8').replace('passed_complete36_actual','passed_complete47_actual').replace("'actual_records':36","'actual_records':47")
    normal=save('normalize_completed_stock_top10_embedding47_after174_v2_20261010.py',text)
    q1=A/'qualify_stock_top10_embedding47_selected_native14_v1_20261010.py';text=q1.read_text(encoding='utf8')
    wrong='actual_stock_top10_embedding47_after172_normalization_queue_v1_20261010';assert text.count(wrong)==1
    text=text.replace(wrong,'actual_stock_top10_embedding47_after174_normalization_queue_v2_20261010').replace(original.stem,normal.stem)
    qualifier=save('qualify_stock_top10_embedding47_selected_native14_v2_20261010.py',text)
    c1=A/'prepare_StockTop10Embedding175_selected_candidate_v1_20261010.py';text=c1.read_text(encoding='utf8').replace(q1.stem,qualifier.stem).replace('StockTop10Embedding47_selected_native14_v1_20261010','StockTop10Embedding47_selected_native14_v2_20261010').replace(original.stem,normal.stem).replace('stock_top10_embedding175_candidate_sources_preparation_v1_20261010.json','stock_top10_embedding175_candidate_sources_preparation_v2_20261010.json')
    candidate=save('prepare_StockTop10Embedding175_selected_candidate_v2_20261010.py',text)
    for p in (normal,qualifier,candidate):importlib.import_module(p.stem)
    assert 'after172' not in qualifier.read_text(encoding='utf8') and 'actual_records\':36' not in normal.read_text(encoding='utf8')
    inputs=[Path(__file__),original,q1,c1,normal,qualifier,candidate,A/'seal_StockTop10Embedding175_selected_candidate_v1_20261010.py',A/'stock_top10_embedding175_storage_v1_20261010.py',A/'stock_top10_embedding175_candidate_sources_preparation_v1_20261010.json',A/'stock_top10_embedding_complete47_after174_selection_plan_v1_20261010.json']
    proof=A/'stock_top10_embedding175_candidate_sources_preparation_v2_20261010.json'
    create(proof,{'status':'compiled_exact47_current_route_selected14_candidate2_source_inventory_before_any_new_scientific_output','input_sha256':{str(p):sha(p) for p in inputs},'expected_records':47,'parent_rounds':[174],'full_controls':44,'prefix_controls':132,'normalization_service':'actual_stock_top10_embedding47_after174_normalization_queue_v2_20261010','selected_service':'StockTop10Embedding47_selected_native14_v2_20261010','new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    for row in rows:retire(row,'Verified childless and before output. Generated selected qualifier after172 name corrected to actual after174 normalization2; all47 cases and scientific transformations unchanged.')
    for name,driver in [('actual_stock_top10_embedding47_after174_normalization_queue_v2_20261010',normal),('StockTop10Embedding47_selected_native14_v2_20261010',qualifier)]:
        assert allowed();row=start_service(name,driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'actual_complete47_routes':2,'candidate_source':candidate.name,'no_future_dispatch':True},flush=True)
if __name__=='__main__':main()
