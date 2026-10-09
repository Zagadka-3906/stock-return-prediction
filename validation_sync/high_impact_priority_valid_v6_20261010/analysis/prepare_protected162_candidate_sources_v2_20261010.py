"""Prepare exclusive protected162 storage and a truthful complete157 candidate replay."""
from pathlib import Path
import ast,hashlib,sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha

def change(text,old,new,count=1):
    assert text.count(old)==count,(old,text.count(old),count)
    return text.replace(old,new)

def generate():
    storage=(A/'BF16FlagAfter152157_storage_v1_20261009.py').read_text(encoding='utf8')
    storage=storage.replace('第157轮_20261009','第162轮_20261010').replace('BF16FlagAfter15222_v1_20261009','TailProtected162_v1_20261010').replace('optimization_20261003_r157','optimization_20261003_r162').replace('BF16FlagAfter15222_selected_release_v1_20261009','TailProtected162_selected_release_v1_20261010').replace('round157','round162').replace('v68_20261009','v73_20261010').replace("EBASE/'QA68'","EBASE/'QA73'").replace('number == 157','number == 162')
    # There is no second official comparison output: the real76 pilot is in the native-control folder.
    tree=ast.parse(storage)
    node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUTPUTS' for t in n.targets))
    import prepare_BF16Seed10_80_round155_sources_v1_20261009 as template
    storage=template.previous.replace_node(storage,node.value,"{ROOT/'candidates/TailProtected162_v1_20261010':EBASE/'candidate',ROOT/'candidates/optimization_20261003_r162':EBASE/'registered_candidate',ROOT/'analysis/TailProtected162_selected_release_v1_20261010':EBASE/'selected_release',ROOT/'analysis/lossless_ranking_display_v2_20261006/round162':EBASE/'display',ROOT/'analysis/lossless_ranking_display_qa_v73_20261010':EBASE/'QA73'}")
    s=(A/'prepare_BF16FlagAfter15222_selected_candidate_v1_20261009.py').read_text(encoding='utf8')
    s=s.replace('BF16FlagAfter15222','TailProtected162').replace('BF16FlagAfter152157_storage_v1_20261009','protected162_storage_v2_20261010').replace('TailProtected162_selected_release_v1_20261009','TailProtected162_selected_release_v1_20261010').replace('TailProtected162_v1_20261009','TailProtected162_v1_20261010')
    s=change(s,"GRAPH_KEY='BF16_flag_after152157_complete_parent_rank_CDF'","GRAPH_KEY='protected_tail_after_complete157_native_v1_20261010'")
    s=change(s,"    closed('TailProtected162_official_comparison_v3_20261009')\n    closed('TailProtected162_scores_main_publication_v1_20261009')","    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed\n    assert allowed()\n    closed('TailProtected162_selected_native14_v1_20261010')")
    s=change(s,'    from BF16Medium153_complete_parent_rank_CDF_v1_20261009 import transform\n    from neural_BF16_medium2048_seed09_e64_native_v1_20261009 import CONFIG','    import importlib\n    import protected_tail_after157_native_stage_v1_20261010 as native_stage')
    s=change(s,"    empty(OUT);empty(CANDIDATE)","    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import OUT as native_out\n    empty(OUT);empty(CANDIDATE)")
    s=change(s,"pilot_path=A/'TailProtected162_official_comparison_v1_20261009/verification.json'","pilot_path=native_out/'pilot76.json'")
    s=s.replace('passed_actual22_BF16_flag_after152157_complete_parent_rank_CDF_full_official_comparisons','passed_normalized76_actual_complete_training_only_official_records')
    s=change(s,"    from prepare_BF16FlagAfter152157_core_drafts_v1_20261009 import best_key","    def best_key(r):return (-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case'])")
    s=change(s,'assert parent_number in (152,153,154,155,156)','assert parent_number in (157,160,161)')
    begin=s.index("    admission=A/'TailProtected162_round157_source_admission_v1_20261009.json'")
    end=s.index('    pins={**protocol_pins',begin)
    s=s[:begin]+"    sources=[Path(__file__),A/'protected162_storage_v2_20261010.py',A/'predict_protected_tail_after157_complete_scheme_v1_20261010.py',A/'protected_tail_after157_native_stage_v1_20261010.py',A/'seal_protected162_selected_candidate_v2_20261010.py',A/'protected162_candidate_sources_preparation_v2_20261010.json',native_out/'verification.json',pilot_path,parent_candidate/'manifest.json',parent_candidate/'source_package_verification.json',parent_release/'full_registration_execution.json']\n"+s[end:]
    s=change(s,'assert parent_number==152 and','assert parent_number==157 and')
    s=change(s,"    bank=Path(read(A/'actual_BF16_medium2048_seed09_e64_bank6_location_v1_20261009.json')['output'])","    recipes={'seed09':'neural_BF16_medium2048_seed09_e64_bank6_v1_20261009','seed10':'neural_BF16_medium2048_seed10_e64_bank6_v1_20261009','drop05':'neural_BF16_medium2048_drop05_seed09_e64_bank6_v1_20261009'}\n    bank=Path('E:/赛题五_本机临时')/recipes[cfg['recipe']]\n    CONFIG=importlib.import_module(native_stage.BACKENDS[cfg['recipe']][0]).CONFIG\n    transform=importlib.import_module(native_stage.CODECS[cfg['codec']]).transform")
    s=s.replace('第157轮_20261009/pre_inference_source_freeze_v14','第162轮_20261010/pre_inference_source_freeze_v1')
    s=change(s,"    neural_folder=Path(read(A/'actual_BF16Medium153_full5_independent_location_v1_20261009.json')['output'])","    # Resolve saved raw-panel locations from the actual recipe's passed own-independent proof.\n    own_pointer={'seed09':'actual_BF16Medium153_full5_independent_location_v1_20261009.json','seed10':'actual_BF16TwoSeed154_seed10_full5_independent_location_v1_20261009.json','drop05':'actual_BF16Drop05_156_full5_independent_location_v1_20261009.json'}[cfg['recipe']]\n    neural_folder=Path(read(A/own_pointer)['output'])")
    s=change(s,"transform(raw,neural,dates,flags,valid,cfg['role'],cfg['weight'],cfg['sign'])","transform(raw,neural,dates,flags,valid,cfg['weight'],cfg['protect_fraction'],cfg['sign'])")
    s=change(s,"scoring=A/'BF16FlagAfter152157_D_scoring_v1_20261009/selected/scoring_validation_only'","scoring=A/'TailProtected162_D_scoring_v1_20261010/selected/scoring_validation_only'")
    s=change(s,"'actual6_mature_native_and_full_independent_controls':str(neural_folder/'verification.json')","'actual6_mature_native_and_full_independent_controls':str(neural_folder/'verification.json'),'actual_selected14_native14_cold7_prefit_controls':str(native_out/'verification.json')")
    s=change(s,"'transformation':'inverseCDF_parent((1-weight)*parent_day_average_rank_over_N+weight*neural_day_average_rank_over_N)'","'transformation':'per-day protected-tail parent-value permutation by mature neural ranks; official_Top_v2 additionally applies documented oneULP cutoff-tie lift','codec_module':native_stage.CODECS[cfg['codec']] ")
    s=change(s,'    from predict_BF16FlagAfter152157_complete_parent_scheme_v1_20261009 import predict','    from predict_protected_tail_after157_complete_scheme_v1_20261010 import predict')
    s=s.replace('expected_scored_records=22','expected_scored_records=76').replace("'scored_records':22","'scored_records':76").replace("len(pilot['records'])==22","len(pilot['records'])==76").replace('all22','all76').replace('by_all22','by_all76').replace('anchor22','anchor76')
    s=change(s,"'invalid_signal_bits_preserved':True","'invalid_signal_bits_preserved':True,'selected_native14_source':str(native_out/'verification.json')")
    s=change(s,"        from predict_protected_tail_after157_complete_scheme_v1_20261010 import predict","        assert allowed()\n        from predict_protected_tail_after157_complete_scheme_v1_20261010 import predict")
    seal=(A/'seal_ReusedNN160Quality19_selected_candidate_cold80_v2_20261010.py').read_text(encoding='utf8')
    seal=seal.replace('ReusedNN160Quality19','TailProtected162').replace('ReusedNN160Stage_storage_v1_20261009','protected162_storage_v2_20261010').replace('TailProtected162_selected_candidate_preparation_v1_20261009','TailProtected162_selected_candidate_preparation_v1_20261010').replace('TailProtected162_selected_release_v1_20261009','TailProtected162_selected_release_v1_20261010').replace('anchor19','anchor76').replace('actual19','actual76')
    seal=change(seal,"candidate/'ReusedNN160Stage_complete_parent_native_replay_verification.json'","candidate/'protected_tail_after157_complete_parent_native_replay_verification.json'")
    seal=seal.replace('passed_actual_complete152_and_medium153_two_full_native_independent_replays_and_cold80','passed_actual_complete157_protected_tail_two_full_native_independent_replays_and_cold80')
    seal=change(seal,"        A/'TailProtected162_actual_controls_index_v1_20261009.json',\n        A/'TailProtected162_official_comparison_v1_20261009/verification.json'","        Path('E:/赛题五_本机临时/protected_tail_selected_native14_v1_20261010/pilot76.json'),\n        Path('E:/赛题五_本机临时/protected_tail_selected_native14_v1_20261010/verification.json')")
    seal=change(seal,"assert ready['status']=='passed_actual_selected_new_TailProtected162_candidate_inference'","assert ready['status']=='passed_actual_selected_new_TailProtected162_candidate_inference'")
    # Match the original candidate-preparer's precise successful selected-inference status.
    s=s.replace('TailProtected162_selected_release_v1_20261009','TailProtected162_selected_release_v1_20261010')
    seal=seal.replace('passed_actual19_selected','passed_actual76_selected')
    output={'protected162_storage_v2_20261010.py':storage,'prepare_protected162_selected_candidate_v2_20261010.py':s,'seal_protected162_selected_candidate_v2_20261010.py':seal}
    for name,text in output.items():compile(text,str(A/name),'exec')
    return output

def main():
    output=generate()
    for name,text in output.items():
        assert not (A/name).exists(),name
        (A/name).write_text(text,encoding='utf8',newline='\n')
    create(A/'protected162_candidate_sources_preparation_v2_20261010.json',{'status':'passed_three_exclusive_candidate_sources_compiled_before_future_inference','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*(A/n for n in output)]},'actual_candidate_inference_performed':False,'actual_future_X_read':False,'new_quality_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
