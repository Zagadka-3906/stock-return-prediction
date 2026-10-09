"""Generate full76 routes before selected future inference, retaining original ranking QA."""
from pathlib import Path
import sys,time,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from prepare_protected162_candidate_sources_v2_20261010 import change

def route(text):
    pairs=[('ReusedNN160Quality19','TailProtected162'),('ReusedNN160Stage_storage_v1_20261009','protected162_storage_v2_20261010'),('round160','round162'),('r160','r162'),('qa71','qa73'),('QA71','QA73'),('v71_20261009','v73_20261010'),('第160轮_20261009','第162轮_20261010'),('round162_qa73_20261009','round162_qa73_20261010'),('TailProtected162_round162_artifacts_20261009','TailProtected162_round162_artifacts_20261010'),('TailProtected162_round162_full_validation_20261009','TailProtected162_round162_full_validation_20261010'),('TailProtected162_round162_sources_v1_20261009','protected162_full_registry_sources_v1_20261010'),('TailProtected162_selected_release_v1_20261009','TailProtected162_selected_release_v1_20261010')]
    for old,new in pairs:text=text.replace(old,new)
    return text

NAMES=['register_TailProtected162_round162_artifacts_20261010.py','publish_TailProtected162_round162_full_validation_20261010.py','optimize_training_round162.py','finalize_training_round162.py','lossless_ranking_runtime_adapter_round162_v2_20261008.py','build_lossless_ranking_display_round162_v2_20261008.py','verify_lossless_ranking_display_round162_v2_20261008.py','collect_full_lossless_round162_qa73_20261010.py']

def source_paths():
    return [Path(__file__),A/'protected162_full_registry_source_preparation_v1_20261010.json',A/'prepare_protected162_candidate_sources_v2_20261010.py',A/'protected162_candidate_sources_preparation_v2_20261010.json',A/'protected162_storage_v2_20261010.py',A/'prepare_protected162_selected_candidate_v2_20261010.py',A/'seal_protected162_selected_candidate_v2_20261010.py',A/'prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py',A/'protected_tail_after157_native_stage_v1_20261010.py',A/'predict_protected_tail_after157_complete_scheme_v1_20261010.py',A/'protected_tail_after157_native_predictor_preparation_v1_20261010.json',A/'run_protected162_complete_family_v1_20261010.py',A/'run_protected162_full_registration_v1_20261010.py',A/'owned_idle_publication_wait_runtime_v1_20261010.py',A/'lossless_chunked_safe_main_runtime_v1_20261009.py',A/'serial_main_publication_mutex_v1_20261009.py',A/'byte_exact_ranking_stream_runtime_v1_20261010.py',A/'byte_exact_publication_encoder_runtime_v1_20261010.py',*[A/n for n in NAMES]]

def generate():
    result={}
    regular=['optimize_training_round160.py','finalize_training_round160.py','lossless_ranking_runtime_adapter_round160_v2_20261008.py','build_lossless_ranking_display_round160_v2_20261008.py','verify_lossless_ranking_display_round160_v2_20261008.py','collect_full_lossless_round160_qa71_20261009.py']
    for name in regular:
        text=route((A/name).read_text(encoding='utf8'))
        text=text.replace('number == 160','number == 162').replace('(160, 71, 19)','(162, 73, 76)').replace("PREVIOUS_NUMBER = 159","PREVIOUS_NUMBER = 161").replace('optimization_20261003_r159','optimization_20261003_r161').replace('NUMBER = 160','NUMBER = 162').replace('WAVES = (443,)','WAVES = (445,)').replace("== 19","== 76")
        text=text.replace('actual_complete_parent_BF16_rank_CDF_or_exact_qualified_anchor','actual_complete157_protected_tail_permutation_or_exact_qualified_anchor')
        if name.startswith('collect_'):
            text=change(text,"qa_v{qa_version}_20261007","qa_v{qa_version}_20261010")
        result[route(name)]=text
    s=route((A/'register_BF16FlagAfter15222_round157_artifacts_20261009.py').read_text(encoding='utf8'))
    s=s.replace('BF16FlagAfter15222','TailProtected162').replace('BF16FlagAfter152157_storage_v1_20261009','protected162_storage_v2_20261010').replace('optimization_20261003_r157','optimization_20261003_r162').replace('round157','round162').replace('TailProtected162_selected_release_v1_20261009','TailProtected162_selected_release_v1_20261010')
    s=change(s,"pilot_path = A / 'TailProtected162_official_comparison_v1_20261009/verification.json'","pilot_path = Path('E:/赛题五_本机临时/protected_tail_selected_native14_v1_20261010/pilot76.json')")
    s=s.replace('passed_actual22_BF16_flag_after152157_complete_parent_rank_CDF_full_official_comparisons','passed_normalized76_actual_complete_training_only_official_records').replace('== 22','== 76')
    s=change(s,'    from prepare_TailProtected162_round162_sources_v1_20261009 import source_paths','    from prepare_protected162_full_registry_sources_v1_20261010 import source_paths')
    begin=s.index("            assert 'BF16_flag_after152157_complete_parent_rank_CDF' not in graph")
    end=s.index('        row = deepcopy',begin)
    s=s[:begin]+'''            from protected_tail_after157_native_stage_v1_20261010 import GRAPH_KEY,CODECS
            assert 'BF16_flag_after152157_complete_parent_rank_CDF' in graph and GRAPH_KEY not in graph
            assert measured['first2020_active'] and measured['ordered_native_components']==[cfg['model']]
            original=read(measured['original_screen_record'])
            assert original['metrics']==measured['metrics']
            graph[GRAPH_KEY]={**cfg,'rank_universe':cfg['universe'],'first2020_active':True,
                'position':'after_complete_qualified_parent','original_complete_parent_round':157,
                'original_complete_parent_graph_preserved':True,'codec_module':CODECS[cfg['codec']],
                'transformation':'protected-tail value permutation; official_Top_v2 adds documented oneULP cutoff-tie lift',
                'original_completed_train_only_screen_record':measured['original_screen_record'],
                'future_candidate_not_inferred_for_nonselected_comparison':True}
''' +s[end:]
    s=change(s,'row.update(wave=440','row.update(wave=445')
    s=change(s,"original_official_pilot_record=str(A / f'TailProtected162_official_comparison_v1_20261009/case{measured[\"case\"]:02d}_official.json')","original_official_pilot_record=measured.get('original_screen_record',str(pilot_path))")
    s=s.replace("r152/selection.json","r161/selection.json").replace('explicit_comparison_parent_round=152','explicit_comparison_parent_round=161').replace("'explicit_parent_round': 152","'explicit_parent_round': 161").replace("'expected_scored_records': 22","'expected_scored_records': 76").replace("'waves': [440]","'waves': [445]").replace("'wave440_results.json'","'wave445_results.json'").replace("'existing_actual_official_records': 22","'existing_actual_official_records': 76")
    s=change(s,"'original_pre_scoring_protocol': str(A / 'TailProtected162_official_comparison_v1_20261009/frozen_before_actual_full_controls_and_official_scores.json')","'original_pre_scoring_protocols': [str(A/'protected_upper_tail_screen_plan_v1_20261010.json'),str(A/'protected_official_top_screen_plan_v2_20261010.json')]")
    s=s.replace("r152/verification.json","r157/verification.json")
    s=change(s,"'actual_declared_model_ensembles': pilot['components']","'actual_declared_model_ensembles': ['seed09','seed10','drop05','complete157','qualified160','qualified161']")
    s=s.replace("A/'TailProtected162_actual_controls_index_v1_20261009.json'","Path('E:/赛题五_本机临时/protected_tail_selected_native14_v1_20261010/verification.json')")
    s=s.replace("A / 'TailProtected162_selected_release_v1_20261009/selected_candidate_ready_for_registration.json'","A / 'TailProtected162_selected_release_v1_20261010/selected_candidate_ready_for_registration.json'")
    s=s.replace('actual_all22','actual_all76').replace('all22_full','all76_full').replace('passed_actual22','passed_actual76')
    s=s.replace('BF16FlagAfter152157_complete_parent_native_replay_verification.json','protected_tail_after157_complete_parent_native_replay_verification.json')
    # Do not shadow the selected source record when constructing nonselected graphs.
    s=s.replace("            original=read(measured['original_screen_record'])\n            assert original['metrics']==measured['metrics']","            screen_original=read(measured['original_screen_record'])\n            assert screen_original['metrics']==measured['metrics']")
    result[NAMES[0]]=s
    pub=route((A/'publish_ReusedNN160Quality19_round160_full_validation_20261009.py').read_text(encoding='utf8'))
    pub=pub.replace('collect(160, 71, 19)','collect(162, 73, 76)').replace("namespace['snapshot'](160)","namespace['snapshot'](162)").replace('== 19','== 76').replace("'actual_complete_QA_version':71","'actual_complete_QA_version':73").replace('actual_complete_QA_version=71','actual_complete_QA_version=73').replace("'actual_full_QA_version': 71","'actual_full_QA_version': 73").replace("'scored_records': 19","'scored_records': 76").replace("'original_official_pilot_records_registered': 19","'original_official_pilot_records_registered': 76").replace("'round': 160","'round': 162")
    pub=change(pub,"from prepare_protected162_full_registry_sources_v1_20261010 import source_paths","from prepare_protected162_full_registry_sources_v1_20261010 import source_paths")
    pub=change(pub,"A/'TailProtected162_official_comparison_v1_20261009'","Path('E:/赛题五_本机临时/protected_tail_selected_native14_v1_20261010')")
    begin=pub.index("    for name in ('TailProtected162_official_comparison")
    end=pub.index('    for path in extra:',begin)
    pub=pub[:begin]+"    for name in ('TailProtected162_selected_native14_v1_20261010','TailProtected162_selected_candidate_preparation_v1_20261010','TailProtected162_selected_candidate_sealing_v1_20261010'):\n        folder=A/'service_owned_workflows_20261006'/name\n        extra+=list(folder.glob('*.json'))+list(folder.glob('*.log'))\n    for family in ('protected_upper_tail_screen_v1_20261010','protected_official_top_screen_v2_20261010'):\n        folder=Path('E:/赛题五_本机临时')/family\n        extra+=list(folder.glob('*.json'))\n        for row in read(folder/'verification.json')['records']:extra.append(Path(row['official_score_cache']['official_metrics_source']))\n"+pub[end:]
    begin=pub.index("    payload[(prefix/'README.md').as_posix()] +=")
    end=pub.index("    previous = sync.git",begin)
    pub=pub[:begin]+"    payload[(prefix/'README.md').as_posix()] += ('\\n第162轮：完整157之后两类保护头部的排序置换方案；74项已实际训练内评分及两个合格锚点，共76项。仅选中方案执行完整候选推理。保留原始37+37冻结计划、逐项官方分数和36+36完整、108+108截断控制，以及选中方案原生14、冷14和7项成熟截止拒绝控制。完整榜原六视图QA73与main；不读取测试标签，不声称穷尽。\\n').encode('utf8')\n"+pub[end:]
    pub=pub.replace('第160轮22项完整父方案与BF16宽网络融合并发布完整榜与QA73','第162轮76项保护头部排序方案与完整榜QA73')
    result[NAMES[1]]=pub
    assert set(result)==set(NAMES)
    for n,s in result.items():compile(s,str(A/n),'exec')
    return result

def main():
    result=generate()
    for n,s in result.items():assert not (A/n).exists();(A/n).write_text(s,encoding='utf8',newline='\n')
    create(A/'protected162_full_registry_source_preparation_v1_20261010.json',{'status':'passed_eight_complete76_routes_compiled_before_selected_future_inference','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*(A/n for n in result)]},'actual_full_QA_executed':False,'actual_future_X_read':False,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
