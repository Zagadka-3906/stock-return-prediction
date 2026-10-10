"""Test the new interaction model against qualified170 without waiting for later CPU grids."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();original=A/'run_stock_embedding_after172_high_impact17_screen_v1_20261010.py';text=original.read_text(encoding='utf8')
    text=text.replace("closed('Frontier133172_complete133_family_v2_20261010')","closed('Cross120170_complete132_family_v5_20261010')\n    closed('actual_stock_embedding_six_state_native42_v2_20261010')")
    text=text.replace('round172_receipt.json','round170_receipt.json').replace("release['scored_records']==133","release['scored_records']==132")
    text=text.replace('optimization_20261003_r172','optimization_20261003_r170').replace('anchor172','anchor170').replace("'parent_round':172","'parent_round':170").replace('complete_parent172','complete_parent170').replace('after172','after170')
    text=text.replace('actual_Cross120RecentReturn252_after170_high_impact17_screen_location_v1_20261010.json','actual_StockEmbeddingSmall512_after170_high_impact17_screen_location_v1_20261010.json')
    text=text.replace("    paths=[Path(__file__)","    actual_native_pointer=A/'actual_stock_embedding_six_state_native42_location_v1_20261010.json'\n    actual_native_folder=Path(read(actual_native_pointer)['output']);actual_native_proof=read(actual_native_folder/'verification.json')\n    assert actual_native_proof['actual_saved_states']==6 and actual_native_proof['actual_native_cases']==42 and actual_native_proof['actual_cold_cases']==42\n    paths=[actual_native_pointer,actual_native_folder/'verification.json',Path(__file__)")
    screen=save('run_stock_embedding_after170_fast17_screen_v1_20261010.py',text)
    module=importlib.import_module(screen.stem);cases=module.cases();assert len(cases)==17
    plan=A/'stock_embedding_after170_predeclared_fast17_selection_plan_v1_20261010.json'
    create(plan,{'status':'predeclared_before_any_stock_embedding_quality_scores_fast170_complement_to_later172_screen','cases':cases,'fully_qualified_parent':170,'nonidentity_full_controls':16,'nonidentity_cold_controls':48,'official_training_only_scores':17,'actual_six_state_native42_prerequisite':True,'future_X_read':False,'test_labels_read':False,'original_later172_screen_preserved':True,'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,screen,A/'stock_embedding_after172_predeclared17_selection_plan_v1_20261010.json']}})
    original=A/'publish_stock_embedding17_completion_v49_20261010.py';pub=original.read_text(encoding='utf8')
    pub=pub.replace('actual_stock_embedding_after172_high_impact17_screen_v1_20261010','actual_stock_embedding_after170_fast17_screen_v1_20261010').replace('StockEmbeddingSmall512_after172_high_impact17_screen_v1_20261010','StockEmbeddingSmall512_after170_high_impact17_screen_v1_20261010')
    pub=pub.replace('stock_embedding_after172_predeclared17_selection_plan_v1_20261010.json',plan.name).replace('run_stock_embedding_after172_high_impact17_screen_v1_20261010.py',screen.name)
    pub=pub.replace('stock_embedding17_completion','stock_embedding17_after170_completion').replace('v49_20261010','v51_20261010')
    pub=pub.replace("    paths=[Path(__file__)","    native=Path(read(A/'actual_stock_embedding_six_state_native42_location_v1_20261010.json')['output'])\n    assert read(native/'verification.json')['actual_native_cases']==42\n    paths=[*native.glob('*.json'),Path(__file__)")
    publisher=save('publish_stock_embedding_after170_fast17_completion_v51_20261010.py',pub)
    for name,driver,receipt in [('actual_stock_embedding_after170_fast17_screen_v1_20261010',screen,'actual_stock_embedding_after170_fast17_screen_activation_v1_20261010.json'),('actual_stock_embedding_after170_fast17_completion_main_v51_20261010',publisher,'actual_stock_embedding_after170_fast17_completion_main_activation_v51_20261010.json')]:
        assert allowed();row=start_service(name,driver.name,[],{str(driver):sha(driver),str(plan):sha(plan)});create(A/receipt,row)
    print('Actual native42 then fast17 against qualified170 queued; later172 confirmation retained',flush=True)
if __name__=='__main__':main()
