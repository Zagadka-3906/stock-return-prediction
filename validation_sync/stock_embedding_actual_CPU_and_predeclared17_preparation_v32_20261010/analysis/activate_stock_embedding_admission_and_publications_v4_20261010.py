"""Perform lightweight restart admission now; protect pending candidate GPU inference."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    old=A/'run_stock_embedding_small512_own_training_queue_v3_20261010.py';text=old.read_text(encoding='utf8')
    text=text.replace('    closed(predecessor)',"    closed('actual_frontier133_2020_TRAIN_native42_controls_v1_20261010')\n    closed('actual_cross120_recent252_return_own_controls_and_training_queue_v2_20261010')\n    assert not (A/'service_owned_workflows_20261006/Frontier233171_selected_candidate_preparation_v1_20261010/native_launch.json').exists()\n    assert not Path('E:/赛题五_本机临时/Dual120Consensus_after169_high_impact193_screen_v1_20261010/verification.json').exists()")
    text=text.replace('    for name,driver in tasks:\n        if not allowed():return',"    for name,driver in tasks:\n        if not allowed():return\n        if name=='actual_stock_embedding_small512_bank6_v1_20261010':\n            write(OUT/'state.json',{'status':'restart_and_independent_CPU_admission_complete_waiting_actual172_seal_before_six_fits','actual_service':predecessor,'new_quality_scores':0})\n            closed(predecessor)\n            if not allowed():return")
    queue=save('run_stock_embedding_small512_own_training_queue_v4_20261010.py',text)
    fixture=Path(read(A/'actual_stock_embedding_mature_fixture_location_v1_20261010.json')['output'])
    paths=[Path(__file__),queue,A/'stock_embedding_after172_predeclared17_selection_plan_v1_20261010.json',fixture/'verification.json',A/'actual_stock_embedding_mature_fixture_location_v1_20261010.json',A/'run_stock_embedding_after172_high_impact17_screen_v1_20261010.py',A/'actual_stock_embedding_own_training_queue_activation_v4_20261010.json',A/'actual_stock_embedding17_screen_activation_v1_20261010.json']
    for proof in ('stock_embedding_small512_sources_admission_v1_20261010.json','stock_embedding_actual_full5_routes_admission_v2_20261010.json','stock_embedding_E_cache_safe_runtime_admission_v3_20261010.json'):
        paths += [A/proof,*[Path(p) for p in read(A/proof)['input_sha256']]]
    paths += [A/'verify_stock_embedding_mature_fixture_and_CPU_v2_20261010.py']
    original=A/'publish_frontier133172_native_controls_and_full_pipeline_v31_20261010.py';pub=original.read_text(encoding='utf8')
    begin=pub.index('    from prepare_frontier233171_full_registry_sources_v1_20261010 import source_paths');end=pub.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    replacement='    paths=[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']\n'
    pub=pub[:begin]+replacement+pub[end:]
    pub=pub.replace('frontier133172_native_controls_and_full_pipeline_v31','stock_embedding_actual_CPU_and_predeclared17_preparation_v32').replace('frontier133172_native_controls_and_full_pipeline_main_v31','stock_embedding_actual_CPU_and_predeclared17_preparation_main_v32')
    pub=pub.replace('frontier133172_native_controls_and_full_pipeline_main_receipt_v31','stock_embedding_actual_CPU_and_predeclared17_preparation_main_receipt_v32')
    pub=pub.replace('passed_actual_own_return120_six_full5_native42_and_new_single_leaf42_native84_cold_controls133_full_pipeline_queued','passed_actual_mature49153_stock_identity_mapping_and_independent_CPU10017_four_prefixes_new_GPU_restart_and_17_quality_cases_queued')
    pub=pub.replace('保存一日收益120维六年度完整独立检查与新单模型阶段42项原生84项冷启动控制、133比较及完整172冻结推理QA83流程，正式候选资格待完成','保存新股票身份嵌入小网络的49153行成熟训练映射与10017行CPU独立推理、未知股票与四个前缀检查，以及预声明17项提分快速验证队列')
    pubpath=save('publish_stock_embedding_actual_CPU_preparation_v32_20261010.py',pub)
    original=A/'publish_cross120_return1d81_completion_v47_20261010.py';pub=original.read_text(encoding='utf8')
    begin=pub.index("    closed('actual_Cross120RecentReturn252_after169_high_impact81_screen_v2_20261010')");end=pub.index('    for row in proof[\'records\']:',begin)
    replacement="""    closed('actual_stock_embedding_after172_high_impact17_screen_v1_20261010')
    screen=Path('E:/赛题五_本机临时/StockEmbeddingSmall512_after172_high_impact17_screen_v1_20261010')
    proof=read(screen/'verification.json');assert len(proof['records'])==proof['new_quality_score_records']==17
    assert proof['actual_nonidentity_full_controls']==16 and proof['actual_nonidentity_prefix_controls']==48
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    paths=[Path(__file__),A/'stock_embedding_after172_predeclared17_selection_plan_v1_20261010.json',A/'run_stock_embedding_after172_high_impact17_screen_v1_20261010.py',*screen.glob('*.json')]
    for admission in ('stock_embedding_small512_sources_admission_v1_20261010.json','stock_embedding_actual_full5_routes_admission_v2_20261010.json','stock_embedding_E_cache_safe_runtime_admission_v3_20261010.json'):
        paths += [A/admission,*[Path(p) for p in read(A/admission)['input_sha256'] if Path(p).suffix=='.py']]
    bank=Path(read(A/'actual_stock_embedding_small512_bank6_location_v1_20261010.json')['output']);assert read(bank/'verification.json')['actual_native_fits']==6
    paths += [bank/'verification.json',*bank.glob('*/info.json')]
    pointer=A/'actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json'
    paths += [pointer,*Path(read(pointer)['output']).glob('*.json')]
"""
    pub=pub[:begin]+replacement+pub[end:]
    pub=pub.replace('actual_Cross120RecentReturn252_after169_high_impact81_screen_v2_20261010','actual_stock_embedding_after172_high_impact17_screen_v1_20261010')
    pub=pub.replace('cross120_return1d81_completion','stock_embedding17_completion').replace('v47_20261010','v49_20261010')
    pub=pub.replace("create(A/'stock_embedding17_completion_main_receipt_v40_20261010.json',receipt);",'')
    pub=pub.replace('passed81_actual_own120_one_day_return_TRAIN_official_records80_full240_cold_controls_candidate_freeze_and_full_registration_pending','passed17_actual_stock_embedding_TRAIN_official_records16_full48_cold_controls_selected_stage_candidate_freeze_and_full_registration_pending').replace("'scored_records':81","'scored_records':17")
    pub=pub.replace('保存独立120维一天收益模型六次训练与81项真实TRAIN官方评分、完整80项和240个因果前缀控制','保存新股票身份嵌入模型六年度训练独立检查和17项真实TRAIN官方评分、16项完整及48项因果前缀控制')
    completion=save('publish_stock_embedding17_completion_v49_20261010.py',pub)
    for module in (queue,pubpath,completion,A/'run_stock_embedding_after172_high_impact17_screen_v1_20261010.py'):
        importlib.import_module(module.stem)
    create(A/'stock_embedding_actual_queue_and_publication_routes_admission_v4_20261010.json',{'status':'compiled_and_imported_actual_stock_embedding_queue17_and_safe_main_publishers','input_sha256':{str(p):sha(p) for p in [Path(__file__),queue,pubpath,completion]},'new_quality_scores':0})
    tasks=[('actual_stock_embedding_own_training_queue_v4_20261010',queue,'actual_stock_embedding_own_training_queue_activation_v4_20261010.json'),('actual_stock_embedding_after172_high_impact17_screen_v1_20261010',A/'run_stock_embedding_after172_high_impact17_screen_v1_20261010.py','actual_stock_embedding17_screen_activation_v1_20261010.json'),('actual_stock_embedding17_completion_main_v49_20261010',completion,'actual_stock_embedding17_completion_publication_activation_v49_20261010.json')]
    for name,driver,activation in tasks:
        assert allowed();row=start_service(name,driver.name,[],{str(driver):sha(driver)});create(A/activation,row)
    assert allowed();row=start_service('actual_stock_embedding_actual_CPU_preparation_main_v32_20261010',pubpath.name,[],{str(pubpath):sha(pubpath)});create(A/'actual_stock_embedding_CPU_preparation_main_activation_v32_20261010.json',row)
    print('Started actual hidden restart admission; annual fits gated by172 seal,17 screening and main publication queued',flush=True)
if __name__=='__main__':main()
