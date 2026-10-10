"""Freeze stronger-parent interactions; wait for actual new own6/full5/native42 before scoring."""
from pathlib import Path
import sys,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    source=A/'run_Huber010_high_impact65_screen_v1_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace('huber010','topweightedhuber010').replace('Huber010161','TopWeightedHuber010165').replace('Huber010_high_impact65','TopWeighted_after163_high_impact65')
    text=text.replace('optimization_20261003_r157','optimization_20261003_r163').replace('anchor157','anchor163').replace('cumulative157','cumulative163').replace('parent157','parent163').replace('parent_round\':157','parent_round\':163')
    text=text.replace('full_parent157','full_parent163').replace('complete_parent157','complete_parent163')
    driver=A/'run_TopWeighted_after163_high_impact65_screen_v1_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    create(A/'TopWeighted_after163_high_impact65_frozen_intent_v1_20261010.json',{'status':'frozen65_interactions_with_current_complete163_before_new_model_training_completes','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver,A/'neural_BF16_medium2048_topweightedhuber010_seed09_e64_frontier_v1_20261010.json',A/'optimization_20261003_r163/selected_validation.npy',A/'optimization_20261003_r163/calibrated_csv_official.json',ROOT/'后续选模标准.md']},'actual_scheme_base_round':163,'new_quality_scores':0,'actual_future_X_read':False,'actual_annual_models_not_claimed_by_intent':True,'own6_fits_full5_native42_required_before_first_new_score':True,'cases':__import__('run_TopWeighted_after163_high_impact65_screen_v1_20261010').cases(),'test_labels_read':False})
    row=start_service('actual_TopWeighted_after163_high_impact65_screen_v1_20261010',driver.name,[],{str(driver):sha(driver),str(Path(__file__)):sha(Path(__file__))})
    create(A/'TopWeighted_after163_highimpact65_actual_hidden_queue_v1_20261010.json',row);print(row,flush=True)
if __name__=='__main__':main()
