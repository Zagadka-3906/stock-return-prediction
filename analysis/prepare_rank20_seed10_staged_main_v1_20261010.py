"""Publish real seed10 validations in order, using the existing verified main-only publisher."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    source=A/'publish_stock_pairrank_objective_stages_main_v1_20261010.py'
    text=source.read_text(encoding='utf8')
    text=text.replace('stock_pairrank','stock_rank20seed10').replace('StockPairRank','StockRank20Seed10').replace('stockpairrank','stockrank20seed10')
    text=text.replace('after174','after175').replace('own32_controls46','own64_controls46')
    text=text.replace(",A/'same_day_ranknet_loss_v1_20261010.py',A/'same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json'",
        ",A/'recent252_rank20_mature_training_population_v1_20261010.py',A/'recent252_rank20_mature_population_actual_CPU_controls_v1_20261010.json',A/'prepare_rank20_seed10_own64_controls46_v1_20261010.py'")
    text=text.replace("'date_local_pair_loss_independent_CPU_passed':True", "'unchanged_mature_rank20_population_controls_explicitly_reused':True,'independent_seed':20261010")
    text=text.replace('保存同日成对排序目标股票身份16维与120特征512网络32轮独立试验：',
        '保存独立种子20261010的20日排名目标股票身份16维与120特征512网络64轮试验：')
    driver=A/'publish_stock_rank20seed10_objective_stages_main_v1_20261010.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    assert allowed()
    row=start_service('actual_StockRank20Seed10_objective_stages_main_v1_20261010',driver.name,[],{str(source):sha(source),str(driver):sha(driver),str(Path(__file__)):sha(__file__)})
    create(A/'actual_StockRank20Seed10_objective_stages_main_v1_20261010_activation.json',row)
    print({'stages':['sources','restart_CPU','own6_full5','native42_official46'],'main_only':True,'actual_scores_not_claimed_complete':True},flush=True)
if __name__=='__main__':main()
