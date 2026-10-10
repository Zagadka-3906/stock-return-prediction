"""Freeze72 new temporal interactions plus the same qualified157 anchor."""
from pathlib import Path
import sys,itertools,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    oldplan=read(A/'high_impact_cumulative_screen_plan_v2_20261010.json')
    locations={**oldplan['bank_locations'],'huber010':'actual_BF16Huber010161_full5_independent_location_v1_20261009.json'}
    locations={k:locations[k] for k in ('huber010','seed09','seed10')}
    source=A/'run_high_impact_cumulative_screen_v2_20261010.py';text=source.read_text(encoding='utf8')
    for old,new in [('high_impact_cumulative_screen_v2_20261010','causal_neural_smoothing73_screen_v1_20261010'),('high_impact_cumulative_screen_plan_v2_20261010','causal_neural_smoothing73_screen_plan_v1_20261010'),('high_impact_cumulative_screen_D_scoring_v2_20261010','causal_neural_smoothing73_D_scoring_v1_20261010'),('actual_high_impact_cumulative_screen_location_v1_20261010','actual_causal_neural_smoothing73_screen_location_v1_20261010'),('BF16Medium153_complete_parent_rank_CDF_v1_20261009','causal_neural_rank_smoothing_v1_20261010'),('passed97_train_only_high_impact_cumulative_comparisons','passed73_causal_smoothed_neural_cumulative157_comparisons')]:text=text.replace(old,new)
    text=text.replace('97','73').replace('96,','72,').replace('288','216')
    text=text.replace('last_sign=None','last_sign=None;last_decay=None')
    text=text.replace("if c['sign']!=last_sign:","if c['sign']!=last_sign or c['decay']!=last_decay:")
    text=text.replace("codec.prepare(parent,raw,dates,flags,valid,c['sign']);last_sign=c['sign']","codec.prepare(parent,raw,dates,flags,valid,c['sign'],c['decay']);last_sign=c['sign'];last_decay=c['decay']")
    text=text.replace("c['weight'],c['sign'])","c['weight'],c['sign'],c['decay'])")
    needle="    parent=np.load(A/'optimization_20261003_r157/selected_validation.npy',mmap_mode='r')";assert text.count(needle)==1
    text=text.replace(needle,"    codes=frame['ts_code'].to_numpy().reshape(1212,4650)\n    assert np.all(codes==codes[0]) and len(set(codes[0]))==4650,'Stock positions must match on every date'\n"+needle)
    driver=A/'run_causal_neural_smoothing73_screen_v1_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    cases=[{'recipe':None,'role':None,'weight':0.,'sign':1.,'decay':None}]
    for recipe,decay,role,weight in itertools.product(('huber010','seed09','seed10'),(.8,.95,.99),('nonflag_valid','all_valid'),(.016,.125,.5,1.)):
        cases.append({'recipe':recipe,'role':role,'weight':weight,'sign':1.,'decay':decay})
    assert len(cases)==73
    proof=read(A/'causal_neural_rank_smoothing_controls_v1_20261010.json');assert proof['cases']==32 and proof['prefix_cases']==96
    correction=A/'causal_neural_smoothing_synthetic_count_clarification_v1_20261010.json'
    create(correction,{'status':'clarified_original_status_label_64_192_was_a_text_error_actual_counts_are32_96','original_proof_sha256':sha(A/'causal_neural_rank_smoothing_controls_v1_20261010.json'),'actual_cases':32,'actual_prefix_cases':96,'new_validation_experiments':0})
    paths=[Path(__file__),source,driver,A/'causal_neural_rank_smoothing_v1_20261010.py',A/'causal_neural_rank_smoothing_controls_v1_20261010.json',correction,ROOT/'后续选模标准.md',A/'optimization_20261003_r157/selected_validation.npy',A/'optimization_20261003_r157/calibrated_csv_official.json',A/'connected_validation_20261002/combined_fold_frame.parquet']
    for location in locations.values():
        pointer=A/location;folder=Path(read(pointer)['output']);paths.extend([pointer,folder/'verification.json',folder/'combined_raw.parquet'])
    pins={str(p):sha(p) for p in paths}
    plan=A/'causal_neural_smoothing73_screen_plan_v1_20261010.json'
    create(plan,{'status':'frozen73_before_actual_full_controls_and_official_scoring','parent_round':157,'cases':cases,'bank_locations':locations,'input_sha256':pins,'reason':'Actual broad Huber return gain lost to turnover; constrain instability at the neural signal level before fusion, without target access','carried_states_across_2020_2024_no_annual_reset':True,'fixed_stock_slot_grid_verified_before_use':True,'new_native_fits':0,'test_labels_read':False,'future_X_read':False})
    row=start_service('actual_causal_neural_smoothing73_screen_v1_20261010',driver.name,[],{**pins,str(plan):sha(plan)})
    create(A/'causal_neural_smoothing73_actual_hidden_launch_v1_20261010.json',row);print(row,flush=True)
if __name__=='__main__':main()
