"""Predeclare two independently trained seeds averaged before the existing daily CDF codec."""
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
    controls=A/'rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json'
    assert read(controls)['status'].startswith('passed_actual3_')
    source=A/'run_stock_rank20seed10_embedding_after175_fast17_screen_v1_20261010.py'
    text=source.read_text(encoding='utf8')
    text=text.replace('StockRank20Seed10EmbeddingSmall512_after175_high_impact17_screen',
        'StockRank20TwoSeed_after175_complement49_screen')
    start=text.index('def cases():');end=text.index('\ndef main():',start)
    cases='''def cases():
    rows=[{'kind':'anchor175','role':None,'weight':0.,'sign':1.,'protect_fraction':None,'second_seed_weight':None}]
    for blend in (.25,.5,.75):
        for role in ('nonflag_valid','all_valid'):
            for sign in (-1.,1.):
                for weight in (.00015625,.0003125,.000625,.00125):
                    rows.append({'kind':'CDF','role':role,'weight':weight,'sign':sign,'protect_fraction':None,'second_seed_weight':blend})
    assert len(rows)==49;return rows

'''
    text=text[:start]+cases+text[end:]
    text=once(text,'def main():\n    assert allowed()\n',"def main():\n    assert allowed()\n    closed('actual_stock_rank20seed10_embedding_after175_large_allocation29_screen_v1_20261010')\n    closed('actual_stock_rank20_embedding_six_state_native42_v1_20261010')\n")
    before='    paths=[actual_native_pointer'
    additional='''    import rank20_two_seed_raw_signal_v1_20261010 as mixing
    oldpointer=A/'actual_StockRank20EmbeddingSmall512_full5_independent_location_v1_20261009.json'
    oldfull=Path(read(oldpointer)['output'])
    oldbank=Path('E:/赛题五_本机临时/stock_rank20_embedding_small512_BF16_bank6_v1_20261010')
    assert read(oldfull/'verification.json')['rows_days_stocks']==[5635800,1212,4650]
    assert read(oldbank/'verification.json')['actual_native_fits']==6
    oldnativepointer=A/'actual_stock_rank20_embedding_six_state_native42_location_v1_20261010.json'
    oldnative=Path(read(oldnativepointer)['output']);oldnativeproof=read(oldnative/'verification.json')
    assert oldnativeproof['actual_saved_states']==6 and oldnativeproof['actual_native_cases']==42 and oldnativeproof['actual_cold_cases']==42
'''
    text=once(text,before,additional+before)
    before='    pins={str(p):sha(p) for p in paths};plan=cases()'
    additional='''    paths += [oldpointer,oldfull/'verification.json',oldfull/'combined_raw.parquet',oldbank/'verification.json',
        oldnativepointer,oldnative/'verification.json',Path(mixing.__file__),A/'rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json',
        A/'rank20_two_seed_complement49_predeclared_plan_v1_20261010.json']
    for year in range(2020,2026):
        left=read(oldbank/str(year)/'info.json');right=read(bank/str(year)/'info.json')
        assert left['configuration']['seed']==20261009 and right['configuration']['seed']==20261010
        for key in ('training_matrix_sha256','training_target_sha256','first','last','days','cutoff_exclusive','last_label_end','stock_vocabulary'):
            assert left['training_meta'][key]==right['training_meta'][key],(year,key)
        assert left['model_sha256']!=right['model_sha256'],'Independent seeds must yield physically distinct actual bundles'
        paths += [oldbank/str(year)/'info.json',bank/str(year)/'info.json']
'''
    text=once(text,before,additional+before)
    before="        dates,flags,valid=[frame[k].to_numpy() for k in ('trade_date','flag_limit_up','price_valid')]"
    text=once(text,before,"        rf09=pl.read_parquet(oldfull/'combined_raw.parquet');assert rf09.select(['ts_code','trade_date']).equals(frame.select(['ts_code','trade_date']))\n"+before)
    text=once(text,"        panel=panel_cache.Panel(parent,raw,dates,flags,valid)","        raw10=raw;raw09=rf09['pred_raw'].to_numpy();active_blend=None\n        panel=None")
    before='            value=transformed(c)'
    addition='''            if i and c['second_seed_weight']!=active_blend:
                active_blend=c['second_seed_weight'];raw=mixing.combine(raw09,raw10,active_blend)
                scalar=mixing.scalar_oracle(raw09,raw10,active_blend);assert exact(raw,scalar);del scalar
                for days in (80,260,975):
                    n=days*4650;assert exact(raw[:n],mixing.combine(raw09[:n],raw10[:n],active_blend))
                    assert exact(raw[:n],mixing.scalar_oracle(raw09[:n],raw10[:n],active_blend))
                create(OUT/f'blend{active_blend}_controls.json',{'second_seed_weight':active_blend,'rows':len(raw),'actual_full_scalar_bits_exact':True,'prefix_days':[80,260,975],'future_X_read':False})
                del panel;gc.collect();panel=panel_cache.Panel(parent,raw,dates,flags,valid)
'''
    text=once(text,before,addition+before)
    text=text.replace("'recipe':'stock_rank20seed10_embedding16_cross120_rank20mean_recent252_small512_BF16_e64'",
        "'recipe':'stock_rank20_two_seed_ID16_cross120_recent252_e64'")
    text=text.replace('frozen17_','frozen49_').replace('return1d17_training_only','rank20_two_seed49_training_only')
    text=text.replace("'expected_cases':17","'expected_cases':49").replace("'new_quality_score_records':17","'new_quality_score_records':49")
    text=text.replace("'actual_nonidentity_full_controls':16","'actual_nonidentity_full_controls':48").replace("'actual_nonidentity_prefix_controls':48","'actual_nonidentity_prefix_controls':144").replace('passed17_','passed49_')
    driver=A/'run_rank20_two_seed_after175_complement49_screen_v1_20261010.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    module=importlib.import_module(driver.stem);assert len(module.cases())==49
    plan=A/'rank20_two_seed_complement49_predeclared_plan_v1_20261010.json'
    create(plan,{'status':'predeclared49_before_any_two_seed_official_score',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver,controls,A/'rank20_two_seed_raw_signal_v1_20261010.py']},
        'cases':module.cases(),'baseline_round':175,'planned_official_records':49,'planned_full_controls':48,'planned_prefix_controls':144,
        'six_fold_own_models_required_each_seed':True,'new_training_by_ensemble':0,'new_quality_scores':0,
        'source_of_hypothesis':'observed TRAIN negative rank20 complement and independent initialization; adaptive selection bias uncorrected',
        'submission_qualified':False,'actual_future_X_read':False,'test_labels_read':False})
    assert allowed();row=start_service('actual_rank20_two_seed_after175_complement49_screen_v1_20261010',driver.name,[],{str(driver):sha(driver),str(plan):sha(plan)})
    create(A/'actual_rank20_two_seed_after175_complement49_screen_v1_20261010_activation.json',row)
    print({'planned_two_seed_cases':49,'actual_scalar_CPU_controls_passed':True,'official_scores_pending':True},flush=True)
if __name__=='__main__':main()
