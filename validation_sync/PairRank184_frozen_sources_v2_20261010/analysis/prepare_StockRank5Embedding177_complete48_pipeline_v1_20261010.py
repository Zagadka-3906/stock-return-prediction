"""Admit rank5 complete48 selection, future freeze, replay, QA88 and main sources."""
from pathlib import Path
import sys,re,io,tokenize,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

MAPPING={
 'StockTop10Embedding176':'StockRank5Embedding177','stock_top10_embedding176':'stock_rank5_embedding177',
 'stock_top10_embedding_followup31_after175':'stock_rank5_embedding_complete48_after176',
 'normalize_completed_stock_top10_embedding_followup31_after175':'normalize_completed_stock_rank5_embedding_complete48_after176',
 'StockTop10Embedding31':'StockRank5Embedding48','stock_top10_embedding31':'stock_rank5_embedding48',
 'stock_top10_embedding_after_complete_qualified_parent_native_stage_v2':'stock_rank5_embedding_after_complete_qualified_parent_native_stage_v1',
 'stock_top10_actual_six_parent_callback_CPU_controls_v1':'stock_rank5_embedding_actual_eight_parent_callbacks_CPU_controls_v1',
 'stock_top10_large_allocation29_predeclared_actual_CPU_admission_v1':'stock_rank5_embedding_actual_eight_parent_callbacks_CPU_controls_v1',
 'actual_stock_top10_embedding_early171_six_state_native42_v3':'actual_stock_rank5_embedding_six_state_native42_v1',
 'actual_stock_top10_embedding_own_training_queue_v3':'actual_stock_rank5_embedding_own_training_queue_v1',
 'stock_top10_embedding16_cross120_top10_BCE_Pos9_recent252_small512_BF16_e24':'stock_rank5_embedding16_cross120_rank5mean_recent252_small512_BF16_e64',
 'rank_MLP512_StockEmbedding16_Cross120Recent252Top10BCEPos9_seed09_e24':'rank_MLP512_StockEmbedding16_Cross120Recent252Rank5Mean_seed09_e64',
 'stock_top10_embedding_BCE_classifier_direct':'stock_rank5_embedding_rank5mean_direct',
 'StockTop10EmbeddingSmall512':'StockRank5EmbeddingSmall512','stock_top10_embedding':'stock_rank5_embedding',
 'round176':'round177','_r176':'_r177','_r175':'_r176','第176轮':'第177轮',
 'qa87':'qa88','QA87':'QA88','qa_v87':'qa_v88','wave459':'wave460',
 'pilot31':'pilot48','normalized31':'normalized48','anchor31':'anchor48','actual31':'actual48','all31':'all48','complete31':'complete48','full31':'full48',
}
def route(text):
    text=re.sub('|'.join(re.escape(k) for k in sorted(MAPPING,key=len,reverse=True)),lambda m:MAPPING[m.group()],text)
    text=tokenize.untokenize([t._replace(string={'176':'177','175':'176','31':'48','28':'44','84':'132','87':'88','459':'460','24':'64'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])
    return text.replace('[171,175]','[171,176]').replace('(171,175)','(171,176)').replace("'assert number == 176'","'assert number == 177'").replace('anchors[175]','anchors[176]').replace("closed('StockTop10Embedding175_complete47_family_v2_20261010')","closed('StockTop10Embedding176_complete31_family_v2_20261010')")

NAMES=['register_StockRank5Embedding177_round177_artifacts_v2_20261010.py','publish_StockRank5Embedding177_round177_full_validation_v2_20261010.py','optimize_training_round177.py','finalize_training_round177.py','lossless_ranking_runtime_adapter_round177_v2_20261008.py','build_lossless_ranking_display_round177_v2_20261008.py','verify_lossless_ranking_display_round177_v2_20261008.py','collect_full_lossless_round177_qa88_20261010.py']
EXTRAS=['prepare_StockRank5Embedding177_complete48_pipeline_v1_20261010.py','prepare_StockRank5Embedding177_selected_candidate_v2_20261010.py','seal_StockRank5Embedding177_selected_candidate_v1_20261010.py','stock_rank5_embedding177_storage_v1_20261010.py','stock_rank5_embedding177_candidate_sources_preparation_v2_20261010.json','normalize_completed_stock_rank5_embedding_complete48_after176_v2_20261010.py','qualify_stock_rank5_embedding48_selected_native14_v2_20261010.py','stock_rank5_embedding_complete48_after176_selection_plan_v1_20261010.json','run_stock_rank5_embedding_after171_large_allocation29_screen_v1_20261010.py','predict_stock_rank5_embedding_complete_qualified_parent_scheme_v1_20261010.py','stock_rank5_embedding_actual_eight_parent_callbacks_CPU_controls_v1_20261010.json','stock_rank5_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json']
def source_paths():
    from prepare_stock_top10_embedding176_full_registry_sources_v2_20261010 import source_paths as older
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*older()]))
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p

def main():
    assert allowed();inputs=[];outputs=[]
    plan=A/'stock_rank5_embedding_complete48_after176_selection_plan_v1_20261010.json';assert read(plan)['expected_records']==48
    pairs=[
      ('normalize_completed_stock_top10_embedding_followup31_after175_v2_20261010.py','normalize_completed_stock_rank5_embedding_complete48_after176_v2_20261010.py'),
      ('qualify_stock_top10_embedding31_selected_native14_v2_20261010.py','qualify_stock_rank5_embedding48_selected_native14_v2_20261010.py'),
      ('stock_top10_embedding176_storage_v1_20261010.py','stock_rank5_embedding177_storage_v1_20261010.py'),
      ('prepare_StockTop10Embedding176_selected_candidate_v2_20261010.py','prepare_StockRank5Embedding177_selected_candidate_v2_20261010.py'),
      ('seal_StockTop10Embedding176_selected_candidate_v1_20261010.py','seal_StockRank5Embedding177_selected_candidate_v1_20261010.py')]
    for old,new in pairs:
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        text=text.replace('actual_stock_rank5_embedding48_after175_normalization_queue_v2','actual_stock_rank5_embedding48_after176_normalization_queue_v2')
        text=text.replace('Small512_full5_independent_location_v1_20261009','Small512_full5_independent_location_v1_20261009')
        outputs.append(save(new,text))
    for p in outputs:importlib.import_module(p.stem)
    storage=importlib.import_module(outputs[2].stem);assert len(storage.OUTPUTS)==6 and storage.EBASE.name=='第177轮_20261010'
    create(A/'stock_rank5_embedding177_candidate_sources_preparation_v2_20261010.json',{'status':'compiled_exact48_rank5_e64_two_grids_and171176_anchors_selected14_frozen_candidate_sources','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,plan]},'expected_records':48,'parent_rounds':[171,176],'full_controls':44,'prefix_controls':132,'new_native_fits':0,'new_quality_scores':0,'actual_future_inference_pending':True,'test_labels_read':False})
    from prepare_stock_top10_embedding176_full_registry_sources_v2_20261010 import NAMES as originals
    for old,new in zip(originals,NAMES):
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        text=text.replace('prepare_stock_rank5_embedding177_full_registry_sources_v2_20261010','prepare_StockRank5Embedding177_complete48_pipeline_v1_20261010')
        text=text.replace("['early171_classifier_large29','qualified171','qualified175']","['rank5_tiny_and_protected17','rank5_large29','qualified171','qualified176']")
        if new==NAMES[1]:
            lines=text.splitlines();idx=[i for i,line in enumerate(lines) if "payload[(prefix/'README.md').as_posix()] +=" in line];assert len(idx)==1
            lines[idx[0]]="    payload[(prefix/'README.md').as_posix()] += ('\\n第177轮：股票身份嵌入与五日平均排名，六年度近期252日成熟样本独立64轮训练；17项小权重及保护融合、29项大权重及全有效股票融合，与完整171及176两个锚点共48条TRAIN官方记录统一选择。44项全量Pandas控制、132个因果前缀；最高官方S优先和物理模型SHA去重。胜出新方案六状态14原生、14冷启动、7拟合前拒绝检查，冻结后两次1599600行完整独立推理及cold80；锚点如实复用。完整榜16918条、六视图QA88及GitHub main；未使用测试标签。\\n').encode('utf8')"
            text='\n'.join(lines)+'\n'
        outputs.append(save(new,text))
    for p in source_paths():assert p.is_file(),p
    create(A/'stock_rank5_embedding177_full_registry_sources_preparation_v2_20261010.json',{'status':'compiled8_exact48_registry_QA88_main_sources_selected_inference_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'expected_records':48,'expected_full_board':16918,'new_quality_scores':0,'test_labels_read':False})
    for old,new in [('run_StockTop10Embedding176_complete_family_v2_20261010.py','run_StockRank5Embedding177_complete_family_v2_20261010.py'),('run_StockTop10Embedding176_full_registration_v2_20261010.py','run_StockRank5Embedding177_full_registration_v2_20261010.py'),('verify_StockTop10Embedding176_full31_preflight_v2_20261010.py','verify_StockRank5Embedding177_full48_preflight_v2_20261010.py')]:
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8')).replace('prepare_stock_rank5_embedding177_full_registry_sources_v2_20261010','prepare_StockRank5Embedding177_complete48_pipeline_v1_20261010')
        text=text.replace("publish(177,'提前分类29项与两完整锚点共31项验证','conditional_flag_residual_causal_checks.json',['实际171基线29项分类筛选及完整171和175锚点；连续官方S优先'])","publish(177,'股票身份五日排名48项完整验证','conditional_flag_residual_causal_checks.json',['实际17项保护及29项大权重融合与完整171和176锚点；连续官方S优先'])")
        outputs.append(save(new,text))
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/'optimize_training_round177.py');assert(opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(177,176,(460,))
    for p in outputs[-3:]:importlib.import_module(p.stem)
    proof=A/'stock_rank5_embedding177_full_execution_sources_admission_v2_20261010.json'
    create(proof,{'status':'compiled_complete48_family_preflight_runtime_QA88_before_future_dispatch','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'expected_records':48,'expected_full_board':16918,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    tasks=[('actual_stock_rank5_embedding48_after176_normalization_queue_v2_20261010',outputs[0]),('StockRank5Embedding48_selected_native14_v2_20261010',outputs[1]),('StockRank5Embedding177_complete48_family_v2_20261010',A/'run_StockRank5Embedding177_complete_family_v2_20261010.py')]
    for name,p in tasks:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'complete48_rank5_queues_started':True,'full_board':16918,'actual_future_dispatch_not_started':True},flush=True)
if __name__=='__main__':main()
