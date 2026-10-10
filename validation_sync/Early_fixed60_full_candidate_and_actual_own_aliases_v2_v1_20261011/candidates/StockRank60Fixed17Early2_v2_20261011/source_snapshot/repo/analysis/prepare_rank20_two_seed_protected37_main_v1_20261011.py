"""Publish frozen protected-tail source declarations and completed TRAIN37 separately on main."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    assert allowed()
    source=A/'publish_rank20_two_seed_stages_main_v1_20261010.py'
    text=source.read_text(encoding='utf8')
    replacements={
        'official49':'official37',
        'actual_rank20_two_seed_after175_complement49_screen_v1_20261010':'actual_rank20_two_seed_after175_protected_tail37_screen_v1_20261011',
        'prepare_rank20_two_seed_complement49_v1_20261010.py':'prepare_rank20_two_seed_protected_tail37_v1_20261011.py',
        'run_rank20_two_seed_after175_complement49_screen_v1_20261010.py':'run_rank20_two_seed_after175_protected_tail37_screen_v1_20261011.py',
        'rank20_two_seed_complement49_predeclared_plan_v1_20261010.json':'rank20_two_seed_protected_tail37_predeclared_plan_v1_20261011.json',
        'actual_StockRank20TwoSeed_after175_complement49_screen_location_v1_20261010.json':'actual_StockRank20TwoSeed_after175_protected_tail37_screen_location_v1_20261011.json',
        "('rank20twoseed' in folder.name.lower() or 'rank20_two_seed' in folder.name.lower())":"('protected_tail37' in folder.name.lower())",
        'Rank20_two_seed_{stage}_v1_20261010':'Rank20_two_seed_protected37_{stage}_v1_20261011',
        'Rank20_two_seed_{stage}_main_v1_20261010':'Rank20_two_seed_protected37_{stage}_main_v1_20261011',
        'Rank20_two_seed_{stage}_main_receipt_v1_20261010':'Rank20_two_seed_protected37_{stage}_main_receipt_v1_20261011',
        "'planned_official_records':49":"'planned_official_records':37",
        "['new_quality_score_records']==49":"['new_quality_score_records']==37",
        "['actual_scored_records']=49":"['actual_scored_records']=37",
        '预声明49项TRAIN官方比较':'预声明37项头部保护及双向大权重TRAIN官方比较',
    }
    for old,new in replacements.items():
        assert old in text,old;text=text.replace(old,new)
    needle="        paths=list(dict.fromkeys(p for p in paths"
    assert text.count(needle)==1
    text=text.replace(needle,"        paths += [A/'prepare_rank20_two_seed_protected37_main_v1_20261011.py',A/'rank20_two_seed_actual_six_population_and_weights_CPU_v1_20261010.json']\n"+needle)
    driver=A/'publish_rank20_two_seed_protected37_stages_main_v1_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec')
    driver.write_text(text,encoding='utf8',newline='\n')
    proof=A/'rank20_two_seed_protected37_publication_sources_v1_20261011.json'
    create(proof,{'status':'compiled_separate_sources_and_actual37_main_publication',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver]},
        'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    assert allowed()
    name='actual_Rank20_two_seed_protected37_stages_main_v1_20261011'
    row=start_service(name,driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/(name+'_activation.json'),row)
    print({'source_and_actual_score_publication_queued':True,'main_only':True},flush=True)

if __name__=='__main__':main()
