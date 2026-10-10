"""New36-record selected recipe, complete parent routing, pre-future freeze and E-only outputs."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
RECIPE='stock_embedding16_cross120_return1d_recent252_small512_BF16_e24'
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def route(text):
    pairs=[('frontier133_after_complete_qualified_parent_native_stage_v1_20261010','stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010'),('predict_frontier133_complete_qualified_parent_scheme_v1_20261010','predict_stock_embedding_complete_qualified_parent_scheme_v1_20261010'),('qualify_frontier133_selected_native14_v1_20261010','qualify_stock_embedding36_selected_native14_v1_20261010'),('normalize_completed_frontier133_after171_v1_20261010','normalize_completed_stock_embedding36_after172_v1_20261010'),('Frontier133172','StockEmbedding173'),('frontier133172','stock_embedding173'),('frontier133_selected_native14','stock_embedding36_selected_native14'),('frontier133_after_complete_qualified_parent_v1_20261010','stock_embedding_after_complete_qualified_parent_v1_20261010'),('frontier133_complete_parent_native_replay_verification','stock_embedding_complete_parent_native_replay_verification'),('passed_actual_complete_qualified_parent_frontier133_two_full','passed_actual_complete_qualified_parent_stock_embedding_two_full'),('pilot133','pilot36'),('normalized133','normalized36'),('anchor133','anchor36'),('actual133','actual36'),('all133','all36')]
    for old,new in pairs:text=text.replace(old,new)
    return text
def main():
    assert allowed();inputs=[];outputs=[]
    old=A/'frontier133172_storage_v1_20261010.py';inputs.append(old);text=route(old.read_text(encoding='utf8'))
    text=text.replace('第172轮','第173轮').replace('r172','r173').replace('round172','round173').replace('number == 172','number == 173').replace('qa_v83','qa_v84').replace('QA83','QA84')
    storage=save('stock_embedding173_storage_v1_20261010.py',text);outputs.append(storage)
    old=A/'prepare_frontier133172_selected_candidate_v2_20261010.py';inputs.append(old);text=route(old.read_text(encoding='utf8'))
    text=text.replace("closed('Frontier133_selected_native14_v1_20261010')","closed('StockEmbedding36_selected_native14_v1_20261010')")
    text=text.replace("len(pilot['records'])==133","len(pilot['records'])==36").replace('parent_number in (169,170,171)','parent_number in (170,172)').replace('parent_number in (169,170)','parent_number in (170,172)')
    text=text.replace("own_pointer={'cross120recent252returnhuber050':'actual_BF16Cross120RecentReturn252Huber050175_full5_independent_location_v1_20261009.json','cross120recent252forward5huber050':'actual_BF16Cross120Recent252Forward5Huber050173_full5_independent_location_v1_20261009.json','cross120recent252rank5huber050':'actual_BF16Cross120Recent252Rank5Huber050174_full5_independent_location_v1_20261009.json'}[cfg['recipe']]","own_pointer='actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json'\n    assert cfg['recipe']=="+repr(RECIPE))
    begin=text.index("        if cfg['stage_kind']=='cross120_causal_smoothing':");end=text.index('\n        selected=transform(',begin)
    text=text[:begin]+"        assert cfg['stage_kind']=='stock_embedding_return1d_direct' and cfg['decay'] is None\n"+text[end:]
    text=text.replace('第172轮','第173轮').replace('expected_scored_records=133','expected_scored_records=36').replace("'scored_records':133","'scored_records':36").replace('selected_by_all133','selected_by_all36')
    candidate=save('prepare_StockEmbedding173_selected_candidate_v1_20261010.py',text);outputs.append(candidate)
    old=A/'seal_frontier133172_selected_candidate_v1_20261010.py';inputs.append(old);text=route(old.read_text(encoding='utf8'))
    seal=save('seal_StockEmbedding173_selected_candidate_v1_20261010.py',text);outputs.append(seal)
    #Exact actual graph keys and imported modules, independent of display numbers.
    c=importlib.import_module(candidate.stem);s=importlib.import_module(storage.stem)
    from stock_embedding_after_complete_qualified_parent_native_stage_v1_20261010 import GRAPH_KEY
    assert c.GRAPH_KEY==GRAPH_KEY and len(s.OUTPUTS)==6 and s.EBASE.name=='第173轮_20261010'
    assert 'number == 173' in storage.read_text(encoding='utf8')
    assert 'Frontier133_selected_native14' not in candidate.read_text(encoding='utf8')
    create(A/'stock_embedding173_candidate_sources_preparation_v1_20261010.json',{'status':'compiled36_selected_candidate_freeze_native_stock_stage_and_six_E_output_routes','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,A/'stock_embedding_complete36_and_selected14_sources_admission_v1_20261010.json']},'expected_records':36,'parent_rounds':[170,172],'new_native_fits':0,'new_quality_scores':0,'actual_selected_full_future_and_registration_pending':True})
    print('Compiled actual173 selected36 candidate and E-only six outputs; no future data read or output allocated',flush=True)
if __name__=='__main__':main()
