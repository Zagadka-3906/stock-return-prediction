"""Bring all early171 classifier records into complete selection against qualified175."""
from pathlib import Path
import re,sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create,read
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def route(text):
    mapping={'StockTop10Embedding175':'StockTop10Embedding176','stock_top10_embedding175':'stock_top10_embedding176','stock_top10_embedding_complete47_after174':'stock_top10_embedding_followup31_after175','normalize_completed_stock_top10_embedding47_after174':'normalize_completed_stock_top10_embedding_followup31_after175','stock_top10_embedding47':'stock_top10_embedding31','StockTop10Embedding47':'StockTop10Embedding31','pilot47':'pilot31','normalized47':'normalized31','anchor47':'anchor31','actual47':'actual31','all47':'all31','第175轮':'第176轮'}
    return re.sub('|'.join(re.escape(k)for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
def main():
    assert allowed();inputs=[];outputs=[]
    plan=A/'stock_top10_embedding_followup31_after175_selection_plan_v1_20261010.json';assert read(plan)['expected_records']==31
    source=A/'normalize_completed_stock_top10_embedding47_after174_v2_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8'))
    text=text.replace("==47 and plan['fully_qualified_anchors']==[174]","==31 and plan['fully_qualified_anchors']==[171,175]").replace('for number in (174,):','for number in (171,175):').replace("closed('StockRankDual174_complete44_family_v2_20261010')","closed('StockTop10Embedding175_complete47_family_v2_20261010')").replace("closed('actual_stock_top10_embedding_six_state_native42_v1_20261010')","closed('actual_stock_top10_embedding_early171_six_state_native42_v3_20261010')")
    text=text.replace('(47,44,132)','(31,28,84)').replace('anchors[174]','anchors[175]').replace("'expected_scored_records':47","'expected_scored_records':31").replace("'actual_nonidentity_full_controls':44","'actual_nonidentity_full_controls':28").replace("'actual_nonidentity_prefix_controls':132","'actual_nonidentity_prefix_controls':84").replace("'actual_comparison_parent_round':174","'actual_comparison_parent_round':175").replace('passed_complete47_actual','passed_complete31_actual').replace("'actual_records':47","'actual_records':31")
    normal=save('normalize_completed_stock_top10_embedding_followup31_after175_v2_20261010.py',text);outputs.append(normal)
    source=A/'qualify_stock_top10_embedding47_selected_native14_v2_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8')).replace('actual_stock_top10_embedding31_after174_normalization_queue_v2','actual_stock_top10_embedding31_after175_normalization_queue_v2').replace("closed('actual_stock_top10_embedding_six_state_native42_v1_20261010')","closed('actual_stock_top10_embedding_early171_six_state_native42_v3_20261010')").replace("len(pilot['records'])==47","len(pilot['records'])==31")
    qualifier=save('qualify_stock_top10_embedding31_selected_native14_v2_20261010.py',text);outputs.append(qualifier)
    source=A/'stock_top10_embedding175_storage_v1_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8')).replace('r175','r176').replace('round175','round176').replace('number == 175','number == 176').replace('qa_v86','qa_v87').replace('QA86','QA87')
    storage=save('stock_top10_embedding176_storage_v1_20261010.py',text);outputs.append(storage)
    source=A/'prepare_StockTop10Embedding175_selected_candidate_v2_20261010.py';inputs.append(source);text=route(source.read_text(encoding='utf8')).replace("len(pilot['records'])==47","len(pilot['records'])==31").replace('parent_number in (174,)','parent_number in (171,175)').replace('expected_scored_records=47','expected_scored_records=31').replace("'scored_records':47","'scored_records':31")
    candidate=save('prepare_StockTop10Embedding176_selected_candidate_v2_20261010.py',text);outputs.append(candidate)
    source=A/'seal_StockTop10Embedding175_selected_candidate_v1_20261010.py';inputs.append(source);seal=save('seal_StockTop10Embedding176_selected_candidate_v1_20261010.py',route(source.read_text(encoding='utf8')));outputs.append(seal)
    for p in outputs:importlib.import_module(p.stem)
    c=importlib.import_module(candidate.stem);s=importlib.import_module(storage.stem);assert c.GRAPH_KEY=='stock_top10_embedding_after_complete_qualified_parent_v1_20261010' and len(s.OUTPUTS)==6 and s.EBASE.name=='第176轮_20261010'
    for p in (normal,qualifier):assert 'after174_normalization' not in p.read_text(encoding='utf8')
    proof=A/'stock_top10_embedding176_candidate_sources_preparation_v2_20261010.json'
    create(proof,{'status':'compiled_followup31_exact171_and175_anchors_selected14_candidate2_storage176_QA87_sources','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,plan]},'expected_records':31,'parent_rounds':[171,175],'full_controls':28,'prefix_controls':84,'new_native_fits':0,'new_quality_scores':0,'actual_future_inference_pending':True,'test_labels_read':False})
    for name,p in [('actual_stock_top10_embedding31_after175_normalization_queue_v2_20261010',normal),('StockTop10Embedding31_selected_native14_v2_20261010',qualifier)]:
        row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'actual31_normalization_and_selected14_queues_started':True,'candidate176_sources':'prepared','new_fits':0},flush=True)
if __name__=='__main__':main()
