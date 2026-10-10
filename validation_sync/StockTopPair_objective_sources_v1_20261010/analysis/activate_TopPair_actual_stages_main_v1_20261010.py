from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    source=A/'publish_stock_pairrank_objective_stages_main_v1_20261010.py'
    text=source.read_text(encoding='utf8').replace('stock_pairrank','stock_toppair').replace('stockpairrank','stocktoppair').replace('StockPairRankEmbedding','StockTopPairEmbedding').replace('StockPairRank_objective','StockTopPair_objective').replace('same_day_ranknet_loss','same_day_top_ranknet_loss')
    text=text.replace("('*stock_toppair*20261010.py','*stock_toppair*20261010.json')","('*stock_toppair*20261010.py','*stock_toppair*20261010.json','*TopPair*20261010.py','*TopPair*20261010.json')")
    text=text.replace('保存同日成对排序目标股票身份16维与120特征512网络32轮独立试验：','保存Top组训练权重十倍同日排序目标股票身份16维与120特征512网络32轮独立试验：')
    p=A/'publish_stock_toppair_objective_stages_main_v1_20261010.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n')
    assert allowed();name='actual_StockTopPair_objective_stages_main_v1_20261010';row=start_service(name,p.name,[],{str(p):sha(p)})
    create(A/(name+'_activation.json'),row);print(row,flush=True)
if __name__=='__main__':main()
