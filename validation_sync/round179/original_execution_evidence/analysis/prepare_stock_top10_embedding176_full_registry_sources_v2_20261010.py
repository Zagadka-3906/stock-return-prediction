"""Full31 follow-up registry, immutable16870-record board, QA87 and main publication."""
from pathlib import Path
import sys,io,tokenize,re,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
NAMES=['register_StockTop10Embedding176_round176_artifacts_v2_20261010.py','publish_StockTop10Embedding176_round176_full_validation_v2_20261010.py','optimize_training_round176.py','finalize_training_round176.py','lossless_ranking_runtime_adapter_round176_v2_20261008.py','build_lossless_ranking_display_round176_v2_20261008.py','verify_lossless_ranking_display_round176_v2_20261008.py','collect_full_lossless_round176_qa87_20261010.py']
EXTRAS=['prepare_Top10_followup176_selection_candidate_and_storage_v1_20261010.py','prepare_StockTop10Embedding176_selected_candidate_v2_20261010.py','seal_StockTop10Embedding176_selected_candidate_v1_20261010.py','stock_top10_embedding176_storage_v1_20261010.py','stock_top10_embedding176_candidate_sources_preparation_v2_20261010.json','normalize_completed_stock_top10_embedding_followup31_after175_v2_20261010.py','qualify_stock_top10_embedding31_selected_native14_v2_20261010.py','stock_top10_embedding_followup31_after175_selection_plan_v1_20261010.json','run_stock_top10_embedding_after171_large_allocation29_screen_v2_20261010.py','verify_stock_top10_embedding_early171_six_state_native42_v3_20261010.py','stock_top10_early171_independent42_route_admission_v2_20261010.json','stock_top10_after171_early_large29_predeclared_admission_v1_20261010.json']
def source_paths():
    from prepare_stock_top10_embedding175_full_registry_sources_v2_20261010 import source_paths as older
    return list(dict.fromkeys([Path(__file__),*[A/n for n in NAMES+EXTRAS],*older()]))
def route(text):
    from prepare_Top10_followup176_selection_candidate_and_storage_v1_20261010 import route as scientific
    text=scientific(text)
    mapping={'round175':'round176','_r175':'_r176','_r174':'_r175','qa86':'qa87','QA86':'QA87','qa_v86':'qa_v87','wave458':'wave459','verify_StockTop10Embedding176_full47_preflight_v2_20261010':'verify_StockTop10Embedding176_full31_preflight_v2_20261010','passed_complete47_actual':'passed_complete31_actual','full36_registration':'full31_registration'}
    text=re.sub('|'.join(re.escape(k)for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text)
    text=tokenize.untokenize([t._replace(string={'175':'176','174':'175','47':'31','86':'87','458':'459','44':'28','132':'84'}.get(t.string,t.string))if t.type==tokenize.NUMBER else t for t in tokenize.generate_tokens(io.StringIO(text).readline)])
    text=text.replace("'assert number == 175'","'assert number == 176'").replace('in (175,)','in (171,175)')
    text=text.replace("closed('StockRankDual174_complete44_family_v2_20261010')","closed('StockTop10Embedding175_complete47_family_v2_20261010')").replace("closed('actual_stock_top10_embedding_six_state_native42_v1_20261010')","closed('actual_stock_top10_embedding_early171_six_state_native42_v3_20261010')")
    return text
def main():
    from run_dependency_queue_v3_20261006 import create,sha
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    from prepare_stock_top10_embedding175_full_registry_sources_v2_20261010 import NAMES as originals
    assert allowed();inputs=[];outputs=[]
    for old,new in zip(originals,NAMES):
        source=A/old;inputs.append(source);text=route(source.read_text(encoding='utf8'))
        if new==NAMES[0]:text=text.replace("['classifier_tiny_and_protected17','classifier_large_allocation29','qualified174']","['early171_classifier_large29','qualified171','qualified175']")
        if new==NAMES[1]:
            lines=text.splitlines();found=[i for i,line in enumerate(lines)if "payload[(prefix/'README.md').as_posix()] +="in line];assert len(found)==1
            lines[found[0]]="    payload[(prefix/'README.md').as_posix()] += ('\\n第176轮：第171轮完整基线上的29项Top10分类大权重及全有效股票融合，与完整合格171及175两个锚点共31条TRAIN官方记录统一选择。28项全量Pandas控制、84个因果前缀；最高官方S优先和物理模型SHA去重。新胜出方案六状态14原生、14冷启动、7拟合前拒绝检查，冻结后两次1599600行完整独立推理和cold80；锚点如实复用。完整榜16870条、六视图QA87及GitHub main；未使用测试标签。\\n').encode('utf8')"
            text='\n'.join(lines)+'\n'
        p=A/new;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');outputs.append(p)
    for p in source_paths():assert p.exists(),p
    create(A/'stock_top10_embedding176_full_registry_sources_preparation_v2_20261010.json',{'status':'compiled8_exact31_full_registry_QA87_main_sources_selected_full_inference_pending','input_sha256':{str(p):sha(p)for p in [Path(__file__),*inputs,*outputs]},'expected_records':31,'expected_full_board':16870,'new_quality_scores':0,'test_labels_read':False})
    pairs=[('run_StockTop10Embedding175_complete_family_v2_20261010.py','run_StockTop10Embedding176_complete_family_v2_20261010.py'),('run_StockTop10Embedding175_full_registration_v2_20261010.py','run_StockTop10Embedding176_full_registration_v2_20261010.py'),('verify_StockTop10Embedding175_full47_preflight_v2_20261010.py','verify_StockTop10Embedding176_full31_preflight_v2_20261010.py')]
    for old,new in pairs:
        source=A/old;inputs.append(source);text=route(source.read_text(encoding='utf8'))
        if new.startswith('run_StockTop10Embedding176_full_registration'):
            text=text.replace("publish(176,'Top10分类共47项完整验证','conditional_flag_residual_causal_checks.json',['实际17项原筛选、29项大权重融合和第174轮合格基线；连续官方S优先'])","publish(176,'提前分类29项与两完整锚点共31项验证','conditional_flag_residual_causal_checks.json',['实际171基线29项分类筛选及完整171和175锚点；连续官方S优先'])")
        p=A/new;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');outputs.append(p)
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/'optimize_training_round176.py');assert(opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(176,175,(459,))
    for p in outputs[-3:]:importlib.import_module(p.stem)
    family=A/'run_StockTop10Embedding176_complete_family_v2_20261010.py';pre=A/'verify_StockTop10Embedding176_full31_preflight_v2_20261010.py';runtime=A/'run_StockTop10Embedding176_full_registration_v2_20261010.py'
    assert 'StockTop10Embedding31_selected_native14_v2_20261010' in family.read_text(encoding='utf8') and "'assert number == 176'" in pre.read_text(encoding='utf8')
    assert "closed('StockTop10Embedding175_complete47_family_v2_20261010')"in runtime.read_text(encoding='utf8')
    proof=A/'stock_top10_embedding176_full_execution_sources_admission_v2_20261010.json'
    create(proof,{'status':'compiled_exact31_family2_preflight2_runtime2_QA87_source_inventory_before_future_dispatch','input_sha256':{str(p):sha(p)for p in [Path(__file__),*inputs,*outputs]},'expected_records':31,'expected_full_board':16870,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    from handoff_ready_goss_full_execution_20261006 import start_service
    row=start_service('StockTop10Embedding176_complete31_family_v2_20261010',family.name,[],{str(family):sha(family),str(proof):sha(proof)})
    create(A/'actual_StockTop10Embedding176_complete31_family_activation_v2_20261010.json',row);print({'actual_full176_31_queue_started':True,'QA':87,'future_dispatch_not_started':True},flush=True)
if __name__=='__main__':main()
