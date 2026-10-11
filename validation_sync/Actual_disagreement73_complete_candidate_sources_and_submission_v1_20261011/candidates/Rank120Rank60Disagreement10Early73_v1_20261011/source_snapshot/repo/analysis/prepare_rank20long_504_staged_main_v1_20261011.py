"""Publish the longer-window actual stages with the same verified main-only transport."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();source=A/'publish_stock_rank20seed10_objective_stages_main_v1_20261010.py'
    text=source.read_text(encoding='utf8').replace('stock_rank20seed10','stock_rank20long').replace('StockRank20Seed10','StockRank20Long').replace('stockrank20seed10','stockrank20long')
    text=text.replace('stock_rank20long_embedding_own64_controls46_sources_admission_v1_20261010','stock_rank20long_embedding_own64_native_sources_preparation_v1_20261010')
    text=text.replace('recent252_rank20_mature_training_population_v1_20261010','recent504_rank20_mature_training_population_v1_20261011')
    text=text.replace('recent252_rank20_mature_population_actual_CPU_controls_v1_20261010','recent504_rank20_mature_population_actual_CPU_controls_v1_20261011')
    text=text.replace('prepare_rank20_seed10_own64_controls46_v1_20261010','prepare_stock_rank20long_504_own64_controls46_v1_20261011')
    text=text.replace("'unchanged_mature_rank20_population_controls_explicitly_reused':True,'independent_seed':20261010",
        "'long504_mature_population_controls_independently_passed':True,'training_calendar_window':504")
    text=text.replace('保存独立种子20261010的20日排名目标股票身份16维与120特征512网络64轮试验：',
        '保存504日成熟训练窗口20日排名目标股票身份16维与120特征512网络64轮独立试验：')
    driver=A/'publish_stock_rank20long_objective_stages_main_v1_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    assert allowed();row=start_service('actual_StockRank20Long_504_objective_stages_main_v1_20261011',driver.name,[],{str(driver):sha(driver),str(Path(__file__)):sha(__file__)})
    create(A/'actual_StockRank20Long_504_objective_stages_main_v1_20261011_activation.json',row)
    print({'long504_staged_main_queued':True,'training_and_scores_not_claimed_complete':True},flush=True)
if __name__=='__main__':main()
