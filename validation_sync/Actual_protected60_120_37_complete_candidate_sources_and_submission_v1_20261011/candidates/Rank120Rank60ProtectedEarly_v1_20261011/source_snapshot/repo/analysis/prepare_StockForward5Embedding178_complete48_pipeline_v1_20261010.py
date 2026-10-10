"""Complete48 forward5-return comparisons, selected freeze, full inference, QA89, main."""
from pathlib import Path
import sys,re,io,tokenize,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
MAPPING={
 'StockRank5Embedding177':'StockForward5Embedding178','stock_rank5_embedding177':'stock_forward5_embedding178',
 'stock_rank5_embedding_complete48_after176':'stock_forward5_embedding_complete48_after177',
 'normalize_completed_stock_rank5_embedding_complete48_after176':'normalize_completed_stock_forward5_embedding_complete48_after177',
 'StockRank5Embedding48':'StockForward5Embedding48','stock_rank5_embedding48':'stock_forward5_embedding48',
 'stock_rank5_embedding_actual_eight_parent_callbacks_CPU_controls_v1':'stock_forward5_embedding_actual_nine_parent_callbacks_CPU_controls_v1',
 'stock_rank5_embedding16_cross120_rank5mean_recent252_small512_BF16_e64':'stock_forward5_embedding16_cross120_return5mean_recent252_small512_BF16_e64',
 'rank_MLP512_StockEmbedding16_Cross120Recent252Rank5Mean_seed09_e64':'rank_MLP512_StockEmbedding16_Cross120Recent252Forward5Mean_seed09_e64',
 'stock_rank5_embedding_rank5mean_direct':'stock_forward5_embedding_return5mean_direct',
 'StockRank5EmbeddingSmall512':'StockForward5EmbeddingSmall512','stock_rank5_embedding':'stock_forward5_embedding',
 'round177':'round178','_r177':'_r178','_r176':'_r177','第177轮':'第178轮',
 'qa88':'qa89','QA88':'QA89','qa_v88':'qa_v89','wave460':'wave461',
}
def route(text):
    text=re.sub('|'.join(re.escape(k) for k in sorted(MAPPING,key=len,reverse=True)),lambda m:MAPPING[m.group()],text)
    text=tokenize.untokenize([t._replace(string={'177':'178','176':'177','88':'89','460':'461'}.get(t.string,t.string)) if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])
    text=text.replace('[171,176]','[171,177]').replace('(171,176)','(171,177)').replace("'assert number == 177'","'assert number == 178'").replace('anchors[176]','anchors[177]')
    text=text.replace("closed('StockTop10Embedding176_complete31_family_v2_20261010')","closed('StockRank5Embedding177_complete48_family_v2_20261010')")
    text=text.replace('existing_own_stock_Top10_BCE_native_bank_fits','existing_own_stock_forward5_return_Huber_native_bank_fits')
    return text
NAMES=['register_StockForward5Embedding178_round178_artifacts_v2_20261010.py','publish_StockForward5Embedding178_round178_full_validation_v2_20261010.py','optimize_training_round178.py','finalize_training_round178.py','lossless_ranking_runtime_adapter_round178_v2_20261008.py','build_lossless_ranking_display_round178_v2_20261008.py','verify_lossless_ranking_display_round178_v2_20261008.py','collect_full_lossless_round178_qa89_20261010.py']
EXTRAS=['prepare_StockForward5Embedding178_complete48_pipeline_v1_20261010.py','prepare_StockForward5Embedding178_selected_candidate_v2_20261010.py','seal_StockForward5Embedding178_selected_candidate_v1_20261010.py','stock_forward5_embedding178_storage_v1_20261010.py','stock_forward5_embedding178_candidate_sources_preparation_v2_20261010.json','normalize_completed_stock_forward5_embedding_complete48_after177_v2_20261010.py','qualify_stock_forward5_embedding48_selected_native14_v2_20261010.py','stock_forward5_embedding_complete48_after177_selection_plan_v1_20261010.json','run_stock_forward5_embedding_after171_large_allocation29_screen_v1_20261010.py','predict_stock_forward5_embedding_complete_qualified_parent_scheme_v1_20261010.py','stock_forward5_embedding_actual_nine_parent_callbacks_CPU_controls_v1_20261010.json','stock_forward5_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json','prepare_stock_forward5_embedding_full5_native42_and_screen46_v1_20261010.py']
def source_paths():
    from prepare_StockRank5Embedding177_complete48_pipeline_v1_20261010 import source_paths as older
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*older()]))
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();inputs=[];outputs=[]
    plan=A/'stock_forward5_embedding_complete48_after177_selection_plan_v1_20261010.json';assert read(plan)['expected_records']==48
    pairs=[('normalize_completed_stock_rank5_embedding_complete48_after176_v2_20261010.py','normalize_completed_stock_forward5_embedding_complete48_after177_v2_20261010.py'),('qualify_stock_rank5_embedding48_selected_native14_v2_20261010.py','qualify_stock_forward5_embedding48_selected_native14_v2_20261010.py'),('stock_rank5_embedding177_storage_v1_20261010.py','stock_forward5_embedding178_storage_v1_20261010.py'),('prepare_StockRank5Embedding177_selected_candidate_v2_20261010.py','prepare_StockForward5Embedding178_selected_candidate_v2_20261010.py'),('seal_StockRank5Embedding177_selected_candidate_v1_20261010.py','seal_StockForward5Embedding178_selected_candidate_v1_20261010.py')]
    for old,new in pairs:
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8')).replace('actual_stock_forward5_embedding48_after176_normalization_queue_v2','actual_stock_forward5_embedding48_after177_normalization_queue_v2');outputs.append(save(new,text))
    for p in outputs:importlib.import_module(p.stem)
    storage=importlib.import_module(outputs[2].stem);assert len(storage.OUTPUTS)==6 and storage.EBASE.name=='第178轮_20261010'
    create(A/'stock_forward5_embedding178_candidate_sources_preparation_v2_20261010.json',{'status':'compiled_exact48_forward5_return_e64_two_grids171177_anchors_selected14_frozen_candidate_sources','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,plan]},'expected_records':48,'parent_rounds':[171,177],'full_controls':44,'prefix_controls':132,'new_native_fits':0,'new_quality_scores':0,'actual_future_inference_pending':True,'test_labels_read':False})
    from prepare_StockRank5Embedding177_complete48_pipeline_v1_20261010 import NAMES as originals
    for old,new in zip(originals,NAMES):
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8')).replace("['rank5_tiny_and_protected17','rank5_large29','qualified171','qualified176']","['forward5_return_tiny_and_protected17','forward5_return_large29','qualified171','qualified177']")
        if new==NAMES[1]:
            lines=text.splitlines();idx=[i for i,line in enumerate(lines) if "payload[(prefix/'README.md').as_posix()] +=" in line];assert len(idx)==1
            lines[idx[0]]="    payload[(prefix/'README.md').as_posix()] += ('\\n第178轮：股票身份嵌入与五日平均收益Huber目标，六年度近期252日成熟样本独立64轮训练；17项小权重及保护融合、29项大权重及全有效股票融合，与完整171及177两个锚点共48条TRAIN官方记录统一选择。44项全量Pandas控制、132个因果前缀；最高官方S优先和物理模型SHA去重。胜出新方案六状态14原生、14冷启动、7拟合前拒绝检查，冻结后两次1599600行完整独立推理及cold80；锚点如实复用。完整榜16966条、六视图QA89及GitHub main；未使用测试标签。\\n').encode('utf8')"
            text='\n'.join(lines)+'\n'
        outputs.append(save(new,text))
    for p in source_paths():assert p.is_file(),p
    create(A/'stock_forward5_embedding178_full_registry_sources_preparation_v2_20261010.json',{'status':'compiled8_exact48_registry_QA89_main_sources_selected_inference_pending','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'expected_records':48,'expected_full_board':16966,'new_quality_scores':0,'test_labels_read':False})
    for old,new in [('run_StockRank5Embedding177_complete_family_v2_20261010.py','run_StockForward5Embedding178_complete_family_v2_20261010.py'),('run_StockRank5Embedding177_full_registration_v2_20261010.py','run_StockForward5Embedding178_full_registration_v2_20261010.py'),('verify_StockRank5Embedding177_full48_preflight_v2_20261010.py','verify_StockForward5Embedding178_full48_preflight_v2_20261010.py')]:
        p=A/old;inputs.append(p);text=route(p.read_text(encoding='utf8'))
        text=text.replace("publish(178,'股票身份五日排名48项完整验证','conditional_flag_residual_causal_checks.json',['实际17项保护及29项大权重融合与完整171和176锚点；连续官方S优先'])","publish(178,'股票身份五日收益48项完整验证','conditional_flag_residual_causal_checks.json',['实际17项保护及29项大权重融合与完整171和177锚点；连续官方S优先'])")
        # Exact-S ties remain eligible according to the declared physical-complexity tie break.
        text=text.replace("best['connected_final_score']>baseline['final_score']","best['connected_final_score']>=baseline['final_score']")
        outputs.append(save(new,text))
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/'optimize_training_round178.py');assert(opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(178,177,(461,))
    for p in outputs[-3:]:importlib.import_module(p.stem)
    proof=A/'stock_forward5_embedding178_full_execution_sources_admission_v2_20261010.json'
    create(proof,{'status':'compiled_complete48_family_preflight_runtime_QA89_before_future_dispatch','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs]},'expected_records':48,'expected_full_board':16966,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    tasks=[('actual_stock_forward5_embedding48_after177_normalization_queue_v2_20261010',outputs[0]),('StockForward5Embedding48_selected_native14_v2_20261010',outputs[1]),('StockForward5Embedding178_complete48_family_v2_20261010',A/'run_StockForward5Embedding178_complete_family_v2_20261010.py')]
    for name,p in tasks:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(proof):sha(proof)});create(A/(name+'_activation.json'),row)
    print({'complete48_forward5_queues_started':True,'full_board':16966,'actual_future_dispatch_not_started':True},flush=True)
if __name__=='__main__':main()
