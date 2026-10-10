"""Predeclare larger two-seed rank changes with protected upper tails, using qualified TRAIN raw predictions."""
from pathlib import Path
import sys, importlib
A=Path(__file__).resolve().parent; ROOT=A.parent
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def once(text,old,new):
    assert text.count(old)==1,(old,text.count(old))
    return text.replace(old,new)

def main():
    assert allowed()
    source=A/'run_rank20_two_seed_after175_complement49_screen_v1_20261010.py'
    signal=A/'rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json'
    tensor=A/'rank20_two_seed_actual_six_population_and_weights_CPU_v1_20261010.json'
    assert read(signal)['status'].startswith('passed_actual3_')
    assert read(tensor)['status'].startswith('passed')
    text=source.read_text(encoding='utf8')
    start=text.index('def cases():');end=text.index('\ndef main():',start)
    cases="""def cases():
    rows=[{'kind':'anchor175','role':None,'weight':0.,'sign':1.,'protect_fraction':None,'second_seed_weight':None}]
    for blend in (.25,.5,.75):
        for kind in ('valid_pool_protection_v1','official_Top_protection_v2'):
            for sign in (-1.,1.):
                for weight in (.016,.064,.25):
                    rows.append({'kind':kind,'role':'nonflag_valid','weight':weight,'sign':sign,'protect_fraction':.15,'second_seed_weight':blend})
    assert len(rows)==37;return rows

"""
    text=text[:start]+cases+text[end:]
    text=once(text,'def main():\n    assert allowed()\n',"def main():\n    assert allowed()\n    closed('actual_rank20_two_seed_after175_complement49_screen_v1_20261010')\n    closed('actual_rank20_two_seed_native84_v1_20261010')\n")
    replacements={
        'StockRank20TwoSeed_after175_complement49_screen_v1_20261010':'StockRank20TwoSeed_after175_protected_tail37_screen_v1_20261011',
        'rank20_two_seed_complement49_predeclared_plan_v1_20261010':'rank20_two_seed_protected_tail37_predeclared_plan_v1_20261011',
        'frozen49_':'frozen37_', 'rank20_two_seed49_training_only':'rank20_two_seed_protected37_training_only',
        "'expected_cases':49":"'expected_cases':37", "'new_quality_score_records':49":"'new_quality_score_records':37",
        "'actual_nonidentity_full_controls':48":"'actual_nonidentity_full_controls':36",
        "'actual_nonidentity_prefix_controls':144":"'actual_nonidentity_prefix_controls':108",
        'passed49_':'passed37_', 'CDF_tiny_weights_and_protected_tail_official_comparisons':'two_seed_larger_weights_both_signs_protected_tail_official_comparisons',
    }
    for old,new in replacements.items():
        assert old in text,old
        text=text.replace(old,new)
    driver=A/'run_rank20_two_seed_after175_protected_tail37_screen_v1_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec')
    driver.write_text(text,encoding='utf8',newline='\n')
    module=importlib.import_module(driver.stem);rows=module.cases()
    assert len(rows)==37 and len({repr(c) for c in rows})==37
    assert {c['kind'] for c in rows[1:]}=={'valid_pool_protection_v1','official_Top_protection_v2'}
    assert {c['sign'] for c in rows[1:]}=={-1.,1.}
    plan=A/'rank20_two_seed_protected_tail37_predeclared_plan_v1_20261011.json'
    create(plan,{'status':'predeclared37_before_any_protected_two_seed_official_score',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,driver,signal,tensor]},
        'cases':rows,'baseline_round':175,'planned_official_records':37,'planned_full_controls':36,'planned_prefix_controls':108,
        'source_of_hypothesis':'TRAIN negative small-weight Rank20 complement motivates larger both-sign rank perturbations while preserving upper tail; adaptive selection bias uncorrected',
        'previous_CDF49_not_repeated':True,'models_reused':12,'new_training_by_screen':0,
        'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,'submission_qualified':False,
        'new_stage_native_qualification_and_full_candidate_pipeline_pending':True})
    assert allowed()
    name='actual_rank20_two_seed_after175_protected_tail37_screen_v1_20261011'
    row=start_service(name,driver.name,[],{str(driver):sha(driver),str(plan):sha(plan)})
    create(A/(name+'_activation.json'),row)
    print({'planned_cases':37,'training_reused':True,'official_scores_pending':True},flush=True)

if __name__=='__main__':main()
