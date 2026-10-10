"""Freeze a distinct protected-tail native stage and validate only the actual TRAIN37 winner."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def once(text,old,new):
    assert text.count(old)==1,(old,text.count(old));return text.replace(old,new)

def main():
    assert allowed()
    original=A/'rank20_two_seed_after_qualified_parent_native_stage_v1_20261010.py'
    text=original.read_text(encoding='utf8')
    text=text.replace('rank20_two_seed_after_complete_qualified_parent_v1_20261010','rank20_two_seed_protected_after_complete_qualified_parent_v1_20261011')
    text=once(text,'    import BF16Medium153_complete_parent_rank_CDF_v1_20261009 as codec',"    import protected_upper_tail_rank_permutation_v1_20261010 as valid_tail\n    import protected_official_top_rank_permutation_v2_20261010 as top_tail")
    text=once(text,"    assert spec['recipe']==RECIPE and spec['codec']=='CDF'","    assert spec['recipe']==RECIPE and spec['codec'] in ('valid_pool_protection_v1','official_Top_protection_v2')\n    assert spec['role']=='nonflag_valid' and spec['protect_fraction']==.15\n    codec=valid_tail if spec['codec']=='valid_pool_protection_v1' else top_tail")
    text=text.replace("spec['stage_kind']=='rank20_two_seed_raw_average'","spec['stage_kind']=='rank20_two_seed_raw_average_protected_tail'")
    text=once(text,"    args=(context.dates,context.flags,context.valid,spec['role'],spec['weight'],spec['sign'])","    args=(context.dates,context.flags,context.valid,spec['weight'],spec['protect_fraction'],spec['sign'])")
    start=text.index('    cohort=codec.selected(');end=text.index('    for member in members:assert ns.sha',start)
    text=text[:start]+"    codec.assert_invariants(parent,value,context.dates,context.flags,context.valid,spec['protect_fraction'])\n"+text[end:]
    text=text.replace("'codec':'CDF'","'codec':spec['codec']")
    stagepath=A/'rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011.py'
    assert not stagepath.exists();compile(text,str(stagepath),'exec');stagepath.write_text(text,encoding='utf8',newline='\n')
    stage=importlib.import_module(stagepath.stem)
    source=A/'verify_rank20_two_seed_six_pair_states_native84_v1_20261010.py'
    verify=source.read_text(encoding='utf8')
    verify=once(verify,"    assert allowed();closed('actual_stock_rank20seed10_embedding_after175_large_allocation29_screen_v1_20261010')","    assert allowed();closed('actual_rank20_two_seed_after175_protected_tail37_screen_v1_20261011')\n    closed('StockRank20LongEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009')")
    verify=verify.replace('rank20_two_seed_after_qualified_parent_native_stage_v1_20261010','rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011')
    verify=verify.replace('rank20_two_seed_six_pair_states_native84_v1_20261010','rank20_two_seed_protected_selected_native14_v1_20261011')
    verify=once(verify,"    pins={str(p):sha(p) for p in sources}","    pointer=A/'actual_StockRank20TwoSeed_after175_protected_tail37_screen_location_v1_20261011.json'\n    proofpath=Path(read(pointer)['output'])/'verification.json';proof=read(proofpath)\n    assert proof['new_quality_score_records']==37\n    best=min(proof['records'],key=lambda r:(-r['connected_final_score'],r['configuration']['kind']!='anchor175',r['case']))\n    sources += [pointer,proofpath,A/'rank20_two_seed_protected_tail37_predeclared_plan_v1_20261011.json']\n    pins={str(p):sha(p) for p in sources}")
    verify=once(verify,'    frame=pl.read_parquet(framepath',"    create(OUT/'selected_before_native14.json',{'best':best,'input_sha256':pins,'selection_from_TRAIN_only':True,'actual_future_X_read':False})\n    if best['configuration']['kind']=='anchor175':\n        create(OUT/'verification.json',{'status':'passed_actual_qualified175_anchor_reuse_no_new_native_stage','input_sha256':pins,'best':best,'actual_native_cases':0,'actual_cold_cases':0,'new_quality_scores':0,'actual_future_X_read':False,'submission_qualified':False})\n        create(A/'actual_rank20_two_seed_protected_selected_native14_location_v1_20261011.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json')})\n        return\n    frame=pl.read_parquet(framepath")
    start=verify.index('            for blend in (.25,.5,.75):');end=verify.index('            bad=SimpleNamespace',start)
    region=verify[start:end]
    body=region[region.index('                        assert allowed()'):]
    body='\n'.join(line[12:] if line.startswith('            ') else line for line in body.split('\n'))
    old="                        spec={'recipe':stage.RECIPE,'codec':'CDF','stage_kind':'rank20_two_seed_raw_average','role':role,'weight':.0003125,'protect_fraction':None,'sign':sign,'original_complete_parent_round':175,'first2020_active':True,'position':'after_complete_qualified_parent','decay':None,'second_seed_weight':blend}"
    old=old[12:]
    new="            c=best['configuration']\n            spec={'recipe':stage.RECIPE,'codec':c['kind'],'stage_kind':'rank20_two_seed_raw_average_protected_tail','role':c['role'],'weight':c['weight'],'protect_fraction':c['protect_fraction'],'sign':c['sign'],'original_complete_parent_round':175,'first2020_active':True,'position':'after_complete_qualified_parent','decay':None,'second_seed_weight':c['second_seed_weight']}"
    body=once(body,old,new)
    verify=verify[:start]+body+verify[end:]
    verify=verify.replace("'expected_native':84,'expected_cold':84","'expected_native':7,'expected_cold':7")
    verify=verify.replace('len(records)==84','len(records)==7').replace("'actual_native_cases':84,'actual_cold_cases':84","'actual_native_cases':7,'actual_cold_cases':7")
    verify=verify.replace('native84_cold84','selected_native7_cold7').replace('/84;','/7;').replace('frozen_before_native84.json','frozen_before_selected_native14.json')
    verify=verify.replace('actual_rank20_two_seed_native84_location_v1_20261010','actual_rank20_two_seed_protected_selected_native14_location_v1_20261011')
    verify=once(verify,"'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False}","'best':best,'submission_qualified':False,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False}")
    driver=A/'verify_rank20_two_seed_protected_selected_native14_v1_20261011.py'
    assert not driver.exists();compile(verify,str(driver),'exec');driver.write_text(verify,encoding='utf8',newline='\n')
    admission=A/'rank20_two_seed_protected_selected_native14_sources_admission_v1_20261011.json'
    create(admission,{'status':'compiled_distinct_protected_stage_and_selected7_cold7_before_any_future_inference',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,source,stagepath,driver]},
        'graph_key':stage.GRAPH_KEY,'expected_scored_records':37,'expected_selected_native_cases':7,'expected_selected_cold_cases':7,
        'waits_long504_full5_to_avoid_overlapping_GPU':True,'new_quality_scores':0,'test_labels_read':False,'actual_future_X_read':False})
    assert allowed()
    name='actual_rank20_two_seed_protected_selected_native14_v1_20261011'
    row=start_service(name,driver.name,[],{str(driver):sha(driver),str(admission):sha(admission)})
    create(A/(name+'_activation.json'),row)
    print({'selected_only_native14_queued':True,'new_fits':0,'future_submission_pipeline_pending':True},flush=True)

if __name__=='__main__':main()
