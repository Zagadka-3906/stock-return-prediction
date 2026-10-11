"""Correct unexecuted receipt destination and use fresh actual publisher/normalizer versions."""
from pathlib import Path
import sys,copy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def main():
    assert allowed()
    original=A/'publish_stock_dual_embedding_after173_completion_v56_20261010.py';text=original.read_text(encoding='utf8')
    text=text.replace('stock_rank_embedding17_after170_completion_main_receipt_v55_20261010.json','stock_dual_embedding25_after173_completion_main_receipt_v57_20261010.json')
    text=text.replace('stock_dual_embedding25_after173_completion_v56_20261010','stock_dual_embedding25_after173_completion_v57_20261010').replace('stock_dual_embedding25_after173_completion_main_v56_20261010','stock_dual_embedding25_after173_completion_main_v57_20261010')
    dest=A/'publish_stock_dual_embedding_after173_completion_v57_20261010.py';assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n')
    assert 'create(A/\'stock_dual_embedding25_after173_completion_main_receipt_v57_20261010.json\'' in text
    plan=copy.deepcopy(read(A/'stock_rank_dual44_after173_selection_plan_v1_20261010.json'));family=plan['families'][1]
    family.update(publisher='actual_stock_dual_embedding_after173_completion_main_v57_20261010',main_receipt='stock_dual_embedding25_after173_completion_main_receipt_v57_20261010.json')
    planpath=A/'stock_rank_dual44_after173_selection_plan_v2_20261010.json';create(planpath,plan)
    src=A/'normalize_stock_rank_and_dual44_after173_v1_20261010.py';text=src.read_text(encoding='utf8').replace('stock_rank_dual44_after173_selection_plan_v1_20261010.json',planpath.name)
    norm=A/'normalize_stock_rank_and_dual44_after173_v2_20261010.py';assert not norm.exists();compile(text,str(norm),'exec');norm.write_text(text,encoding='utf8',newline='\n')
    assert not Path('E:/赛题五_本机临时/stock_rank_dual_complete44_after173_v1_20261010').exists()
    assert not Path('E:/赛题五_本机临时/stock_dual_embedding25_after173_completion_main_v56_20261010').exists()
    for old in ('actual_stock_dual_embedding_after173_completion_main_v56_20261010','actual_stock_rank_dual44_after173_normalization_v1_20261010'):
        retire(read(A/'service_owned_workflows_20261006'/old/'native_launch.json'),'Verified childless pre-output dispatcher superseded to preserve existing rank17 receipt and point complete44 at corrected main57; scientific scores and cases unchanged.')
    launched=[]
    for name,driver in [('actual_stock_dual_embedding_after173_completion_main_v57_20261010',dest),('actual_stock_rank_dual44_after173_normalization_v2_20261010',norm)]:
        assert allowed();row=start_service(name,driver.name,[],{str(driver):sha(driver)});create(A/(name+'_activation.json'),row);launched.append(row)
    create(A/'stock_dual25_receipt_and_complete44_actual_wait_recovery_v2_20261010.json',{'status':'passed_fresh_actual_publish57_and_normalize44_v2_routes_no_scientific_outputs_restarted','actual_services':launched,'plan':str(planpath),'all44_score_cases_unchanged':True,'new_quality_scores':0,'new_fits':0,'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,dest,src,norm,planpath]}})
    print({'corrected_main_publisher':57,'actual_complete44_normalizer':2},flush=True)
if __name__=='__main__':main()
