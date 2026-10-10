"""Freeze the new identity/cross120/mean20 family before any actual future inference."""
from pathlib import Path
import sys,re,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
NAMES=['register_StockForward20Embedding179_round179_artifacts_v2_20261010.py','publish_StockForward20Embedding179_round179_full_validation_v2_20261010.py','optimize_training_round179.py','finalize_training_round179.py','lossless_ranking_runtime_adapter_round179_v2_20261008.py','build_lossless_ranking_display_round179_v2_20261008.py','verify_lossless_ranking_display_round179_v2_20261008.py','collect_full_lossless_round179_qa90_20261010.py']
EXTRAS=['normalize_completed_stock_forward20_embedding_complete48_after178_v4_20261010.py','qualify_stock_forward20_embedding48_selected_native14_v4_20261010.py','stock_forward20_embedding179_storage_v1_20261010.py','prepare_StockForward20Embedding179_selected_candidate_v4_20261010.py','seal_StockForward20Embedding179_selected_candidate_v1_20261010.py','run_StockForward20Embedding179_complete_family_v5_20261010.py','run_StockForward20Embedding179_full_registration_v4_20261010.py','verify_StockForward20Embedding179_full48_preflight_v4_20261010.py','run_StockForward20Embedding179_selected_candidate_feature_cache_v5_20261010.py','stock_forward20_embedding179_candidate_sources_preparation_v4_20261010.json','stock_forward20_embedding179_full_registry_sources_preparation_v2_20261010.json','stock_forward20_embedding_complete48_after178_selection_plan_v1_20261010.json','predict_stock_forward20_embedding_complete_qualified_parent_scheme_v1_20261010.py','stock_forward20_embedding_actual_ten_parent_callbacks_CPU_controls_v1_20261010.json','stock_forward20_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json','prepare_stock_forward20_embedding_full5_native42_screen46_v1_20261010.py','exact_verified_feature120_memoization_runtime_v1_20261010.py']
def source_paths():
    from prepare_StockForward5Embedding178_complete48_pipeline_v1_20261010 import source_paths as older
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*older()]))
def route(text):
    mapping={'StockForward5Embedding178':'StockForward20Embedding179','stock_forward5_embedding178':'stock_forward20_embedding179','StockRank5Embedding177_complete48_family_v4':'StockForward5Embedding178_complete48_family_v5','stock_forward5_embedding':'stock_forward20_embedding','StockForward5Embedding':'StockForward20Embedding','Forward5Mean':'Forward20Mean','return5mean':'return20mean','nine_parent':'ten_parent','171':'173','177':'178','178':'179','16966':'17014','qa89':'qa90','QA89':'QA90','qa_v89':'qa_v90','wave461':'wave462','461':'462'}
    text=re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    text=text.replace("'QA':89","'QA':90").replace('(179,178,(462,))','(179,178,(462,))')
    text=text.replace('五日','二十日').replace('forward5_return_Huber','forward20_return_Huber')
    return text
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();plan=A/'stock_forward20_embedding_complete48_after178_selection_plan_v1_20261010.json'
    assert read(plan)['expected_records']==48 and read(plan)['fully_qualified_anchors']==[173,178]
    inputs=[];outputs=[]
    pairs=[('normalize_completed_stock_forward5_embedding_complete48_after177_v4_20261010.py',EXTRAS[0]),('qualify_stock_forward5_embedding48_selected_native14_v4_20261010.py',EXTRAS[1]),('stock_forward5_embedding178_storage_v1_20261010.py',EXTRAS[2]),('prepare_StockForward5Embedding178_selected_candidate_v4_20261010.py',EXTRAS[3]),('seal_StockForward5Embedding178_selected_candidate_v1_20261010.py',EXTRAS[4])]
    for old,new in pairs:
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        if new==EXTRAS[0]:text=re.sub(r'        actual_aliases=\{[^\n]*\}', '        actual_aliases={}',text)
        outputs.append(save(new,text))
    create(A/EXTRAS[9],{'status':'compiled48_mean20_identity_cross120_selected_sources_before_future','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,plan]},'parent_rounds':[173,178],'expected_records':48,'full_controls':44,'prefix_controls':132,'new_quality_scores':0,'actual_future_inference_pending':True,'test_labels_read':False})
    from prepare_StockForward5Embedding178_complete48_pipeline_v1_20261010 import NAMES as originals
    for old,new in zip(originals,NAMES):
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        text=text.replace('prepare_StockForward20Embedding179_complete48_pipeline_v1','prepare_StockForward20Embedding179_complete48_pipeline_v1')
        text=text.replace('近期252日成熟样本独立64轮训练','近期252日且标签严格完整成熟的样本独立64轮训练')
        outputs.append(save(new,text))
    create(A/EXTRAS[10],{'status':'compiled8_exact48_registry_QA90_main_before_future','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'expected_records':48,'expected_full_board':17014,'new_quality_scores':0,'test_labels_read':False})
    for old,new in [('run_StockForward5Embedding178_complete_family_v5_20261010.py',EXTRAS[5]),('run_StockForward5Embedding178_full_registration_v4_20261010.py',EXTRAS[6]),('verify_StockForward5Embedding178_full48_preflight_v4_20261010.py',EXTRAS[7]),('run_StockForward5Embedding178_selected_candidate_feature_cache_v5_20261010.py',EXTRAS[8])]:
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        # Keep the actual prior family's immutable routes; do not invent transformed historical files.
        text=re.sub(r'^    extra \+= .*\n','',text,flags=re.M)
        text=re.sub(r'^    sources \+= .*\n','',text,flags=re.M)
        begin=text.find('    base_source_paths=routes.source_paths\n');end=text.find('    sources=routes.source_paths();',begin)
        if begin>=0:
            assert end>begin;text=text[:begin]+text[end:]
        outputs.append(save(new,text))
    for p in source_paths():assert p.is_file(),p
    for p in outputs:importlib.import_module(p.stem)
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/'optimize_training_round179.py');assert(opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(179,178,(462,))
    storage=importlib.import_module(Path(EXTRAS[2]).stem);assert len(storage.OUTPUTS)==6 and storage.EBASE.name=='第179轮_20261010'
    assert 'assert number == 179' in (A/EXTRAS[2]).read_text(encoding='utf8')
    for name in (EXTRAS[0],EXTRAS[6]):assert "closed('StockForward5Embedding178_complete48_family_v5_20261010')" in (A/name).read_text(encoding='utf8')
    proof=A/'stock_forward20_embedding179_full_execution_sources_admission_v1_20261010.json'
    create(proof,{'status':'compiled_complete48_mean20_identity_cross120_QA90_before_future','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,plan]},'expected_records':48,'expected_full_board':17014,'parent_rounds':[173,178],'actual_parent_service':'StockForward5Embedding178_complete48_family_v5_20261010','new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    for name,p in [('actual_stock_forward20_embedding48_after178_normalization_queue_v4_20261010',A/EXTRAS[0]),('StockForward20Embedding48_selected_native14_v4_20261010',A/EXTRAS[1]),('StockForward20Embedding179_complete48_family_v5_20261010',A/EXTRAS[5])]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'complete48_mean20_family_queued':True,'future_inference_pending':True},flush=True)
if __name__=='__main__':main()
