"""Freeze mixed-horizon replay sources with independent maturity for each model population."""
from pathlib import Path
import sys,importlib,time,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();original=A/'rank20_two_seed_after_qualified_parent_native_stage_v1_20261010.py'
    s=original.read_text(encoding='utf8').replace('rank20_two_seed_after_complete_qualified_parent_v1_20261010','rank5_rank20_mixed_after_complete_qualified_parent_v1_20261011').replace('stock_rank20_two_seed_ID16_cross120_recent252_e64','stock_rank5_rank20_mixed_label_horizon_ID16_cross120_recent252_e64').replace('stock_rank20seed10_embedding','stock_rank5_embedding')
    s=s.replace('second_seed_weight','rank5_weight').replace('seed_components','horizon_components').replace('rank20_two_seed_raw_average','rank5_rank20_mixed_raw_average')
    s=s.replace("    reference_meta=members[0]['training_info']['training_meta']\n",'')
    s=s.replace("native.CONFIG['seed']==(20261009,20261010)[i]","native.CONFIG['seed']==20261009")
    start=s.index("        for key in ('training_matrix_sha256'");end=s.index('        assert ns.sha(path)',start)
    s=s[:start]+"        assert native.CONFIG['label_horizon_trading_days']==(20,5)[i]\n        assert native.CONFIG['target']==('y_rank_20mean','y_rank_5mean')[i]\n        # No equality is imposed on independently matured five-day and twenty-day training populations.\n"+s[end:]
    s=s.replace("'seed':native.CONFIG['seed'],","'seed':native.CONFIG['seed'],'label_horizon_trading_days':native.CONFIG['label_horizon_trading_days'],'training_cutoff_exclusive':meta['cutoff_exclusive'],'last_training_label_end':meta['last_label_end'],")
    stage=save('rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011.py',s)
    p=A/'predict_rank20_two_seed_complete_qualified_parent_scheme_v1_20261011.py';s=p.read_text(encoding='utf8')
    s=s.replace('import rank20_two_seed_after_qualified_parent_native_stage_v1_20261010 as cdf','import rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011 as cdf')
    s=s.replace('    import rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011 as protected\n','').replace('(cdf,protected)','(cdf,)').replace('stage=cdf if key==cdf.GRAPH_KEY else protected','stage=cdf')
    s=s.replace('second_seed_weight','rank5_weight').replace('seed_components','horizon_components').replace("member['configuration']['seed']==(20261009,20261010)[i]","member['configuration']['seed']==20261009\n        assert member['configuration']['label_horizon_trading_days']==(20,5)[i]")
    s=s.replace('RANK20_TWO_SEED_AFTER_WHOLE_QUALIFIED_PARENT','RANK5_RANK20_MIXED_AFTER_WHOLE_QUALIFIED_PARENT').replace('rank20_two_seed','rank5_rank20_mixed').replace('two_seed','mixed_horizon')
    predictor=save('predict_rank5_rank20_mixed_complete_qualified_parent_scheme_v1_20261011.py',s)
    cpu=A/'verify_rank20_two_seed_actual_eleven_parent_callbacks_CPU_v1_20261011.py';s=cpu.read_text(encoding='utf8').replace('predict_rank20_two_seed_complete_qualified_parent_scheme_v1_20261011','predict_rank5_rank20_mixed_complete_qualified_parent_scheme_v1_20261011').replace('RANK20_TWO_SEED_AFTER_WHOLE_QUALIFIED_PARENT','RANK5_RANK20_MIXED_AFTER_WHOLE_QUALIFIED_PARENT').replace('rank20_two_seed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011','rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011')
    cpu_new=save('verify_rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU_v1_20261011.py',s)
    runpy.run_path(str(cpu_new),run_name='__main__')
    template=A/'verify_rank20_two_seed_protected_selected_native14_v1_20261011.py';s=template.read_text(encoding='utf8')
    s=s.replace('rank20_two_seed_protected_selected_native14','rank5_rank20_mixed_selected_native14').replace('actual_rank20_two_seed_after175_protected_tail37_screen_v1_20261011','actual_rank5_rank20_after175_mixed_horizon49_screen_v2_20261011')
    # Finish highest-priority183 full qualification before allocating this independent new GPU stage.
    s=s.replace("    closed('StockRank20LongEmbeddingSmall512_independent_full5_GPU_controls_v1_20261009')", "    closed('StockRank20Embedding183_complete85_registered_continuation_v13_dependency_placeholder')\n    import psutil,time\n    while psutil.virtual_memory().available<12*2**30:assert allowed();time.sleep(15)")
    # Resolve the exact family name from the current immutable dependency proof, no guessed native route.
    data=read(A/'complete180_registered_continuation_routes_v13_20261011.json');canonical='StockRank20Embedding183_complete85_family_v6_20261010';actual=data['service_aliases'][canonical]
    s=s.replace('StockRank20Embedding183_complete85_registered_continuation_v13_dependency_placeholder',actual)
    s=s.replace('rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011','rank5_rank20_mixed_after_qualified_parent_native_stage_v1_20261011').replace("('stock_rank20_embedding','stock_rank20seed10_embedding')","('stock_rank20_embedding','stock_rank5_embedding')")
    s=s.replace('actual_StockRank20TwoSeed_after175_protected_tail37_screen_location_v1_20261011','actual_StockRank5Rank20_after175_mixed_horizon49_screen_location_v2_20261011').replace("proof['new_quality_score_records']==37","proof['new_quality_score_records']==49").replace('rank20_two_seed_protected_tail37_predeclared_plan_v1_20261011','rank5_rank20_mixed_horizon49_predeclared_plan_v1_20261011')
    s=s.replace("f'Rank20_ID16_Cross120_seed{(20261009,20261010)[i]}_e64'","f'Rank{(20,5)[i]}_ID16_Cross120_seed20261009_e64'").replace('seed_components','horizon_components').replace("'rank20_two_seed_raw_average_protected_tail'","'rank5_rank20_mixed_raw_average'").replace('second_seed_weight','rank5_weight')
    s=s.replace("'expected_native':7,'expected_cold':7","'expected_native':14,'expected_cold':14")
    block_start=s.index("            spec={'recipe':stage.RECIPE");block_end=s.index('            bad=SimpleNamespace',block_start)
    block=s[block_start:block_end].replace("'sign':c['sign']","'sign':sign").replace('len(records)}/7','len(records)}/14')
    s=s[:block_start]+'            for sign in (-1.,1.):\n'+''.join('    '+line if line.strip() else line for line in block.splitlines(keepends=True))+s[block_end:]
    s=s.replace('len(records)==7 and len(refusals)==7','len(records)==14 and len(refusals)==7').replace("'actual_native_cases':7,'actual_cold_cases':7","'actual_native_cases':14,'actual_cold_cases':14").replace('selected_native7_cold7','selected_native14_cold14')
    native=save('verify_rank5_rank20_mixed_selected_native14_v1_20261011.py',s)
    sources=[Path(__file__),original,p,cpu,cpu_new,stage,predictor,template,native,A/'rank5_rank20_mixed_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json',A/'complete180_registered_continuation_routes_v13_20261011.json']
    for model in ['stock_rank20_embedding','stock_rank5_embedding']:
        bank=Path('E:/赛题五_本机临时')/(model+'_small512_BF16_bank6_v1_20261010');assert read(bank/'verification.json')['actual_native_fits']==6
        for year in range(2020,2026):
            info=read(bank/str(year)/'info.json');assert sha(bank/str(year)/'model.joblib')==info['model_sha256'];assert info['training_meta']['last_label_end']<info['training_meta']['cutoff_exclusive'];sources.append(bank/str(year)/'info.json')
    proof=A/'mixed_horizon_native14_predictor_CPU11_sources_admission_v1_20261011.json'
    create(proof,{'status':'compiled_mixed_horizon_independent_maturity_native14_and_actual_CPU11_parent_callbacks','input_sha256':{str(p):sha(p) for p in sources},'actual_callback_CPU_count':11,'physical_saved_states':12,'label_horizons':[20,5],'native14_and_cold14_pending':True,'GPU_waits_actual183_family':actual,'new_fits':0,'new_scores':0,'future_candidate_qualification_pending':True,'training_populations_equal_not_claimed':True})
    assert allowed();row=start_service('actual_rank5_rank20_mixed_selected_native14_v1_20261011',native.name,[],{str(native):sha(native),str(proof):sha(proof)});create(A/'actual_rank5_rank20_mixed_selected_native14_activation_v1_20261011.json',row)
    print({'actual_parent_callback_CPU_checks':11,'mixed_horizon_native14_queued':True,'new_fits':0},flush=True)
if __name__=='__main__':main()
