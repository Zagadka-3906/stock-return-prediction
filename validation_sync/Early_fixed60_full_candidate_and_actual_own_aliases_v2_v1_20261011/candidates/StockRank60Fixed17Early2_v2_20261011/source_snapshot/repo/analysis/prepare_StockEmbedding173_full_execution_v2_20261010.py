"""Exact173/36/QA84 execution routes; never dispatch the new scope before completed172."""
from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from prepare_stock_embedding173_full_registry_sources_v2_20261010 import route,source_paths
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def actual_routes(text):
    text=route(text).replace('full133','full36')
    text=text.replace('stock_embedding173_full_registry_sources_preparation_v1_20261010.json','stock_embedding173_full_registry_sources_preparation_v2_20261010.json')
    text=text.replace('prepare_stock_embedding173_selected_candidate_v2_20261010.py','prepare_StockEmbedding173_selected_candidate_v1_20261010.py').replace('seal_stock_embedding173_selected_candidate_v1_20261010.py','seal_StockEmbedding173_selected_candidate_v1_20261010.py')
    text=text.replace("closed('Frontier233171_complete233_family_v2_20261010')","closed('Frontier133172_complete133_family_v2_20261010')")
    text=text.replace("closed('actual_cross120_recent252_return_own_controls_and_training_queue_v2_20261010')","closed('actual_stock_embedding_checkpoint_yield_training_queue_v5_20261010')\n    closed('actual_stock_embedding_six_state_native42_v2_20261010')")
    text=text.replace('actual_frontier133_selected_native14_location_v1_20261010.json','actual_stock_embedding36_selected_native14_location_v1_20261010.json')
    text=text.replace('(128,384)','(32,96)').replace('in (169,170,172)','in (170,172)')
    return text
def main():
    assert allowed();inputs=[];outputs=[]
    originals=['run_Frontier133172_full_registration_v2_20261010.py','verify_Frontier133172_full133_preflight_v2_20261010.py','run_Frontier133172_complete_family_v2_20261010.py']
    names=['run_StockEmbedding173_full_registration_v2_20261010.py','verify_StockEmbedding173_full36_preflight_v2_20261010.py','run_StockEmbedding173_complete_family_v2_20261010.py']
    for old,new in zip(originals,names):
        p=A/old;inputs.append(p);outputs.append(save(new,actual_routes(p.read_text(encoding='utf8'))))
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/'optimize_training_round173.py');assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(173,172,(456,))
    for p in [*source_paths(),*outputs]:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    for p in outputs:importlib.import_module(p.stem)
    family=outputs[2].read_text(encoding='utf8')
    assert "closed('StockEmbedding36_selected_native14_v1_20261010')" in family
    assert 'prepare_StockEmbedding173_selected_candidate_v1_20261010.py' in family
    assert 'seal_StockEmbedding173_selected_candidate_v1_20261010.py' in family
    preflight=outputs[1].read_text(encoding='utf8')
    assert '(32,96)' in preflight and 'actual_stock_embedding36_selected_native14_location_v1_20261010.json' in preflight
    assert 'actual_comparison_parent_round\']==172' in preflight
    create(A/'stock_embedding173_actual_execution_routes_admission_v2_20261010.json',{'status':'compiled_actual173_family36_preflight_register_QA84_routes_and_imported_execution_drivers','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_embedding173_candidate_sources_preparation_v1_20261010.json',A/'stock_embedding173_full_registry_sources_preparation_v2_20261010.json']},'expected_records':36,'expected_full_board':16748,'QA':84,'new_quality_scores':0,'new_native_fits':0,'actual_future_dispatch':False})
    print('PASS imported actual full173 drivers, selected36 routes, scalar173/172/wave456, QA84 and E-only outputs',flush=True)
if __name__=='__main__':main()
