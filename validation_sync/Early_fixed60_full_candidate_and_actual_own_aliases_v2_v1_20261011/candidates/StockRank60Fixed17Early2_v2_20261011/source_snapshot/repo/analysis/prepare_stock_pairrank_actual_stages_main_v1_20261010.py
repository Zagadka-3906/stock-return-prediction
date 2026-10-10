from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from handoff_ready_goss_full_execution_20261006 import start_service
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    source=A/'publish_stock_rank_wide32_capacity_stages_main_v2_20261010.py'
    text=source.read_text(encoding='utf8').replace('stock_rank_wide32','stock_pairrank').replace('StockRankWide32Embedding1024','StockPairRankEmbeddingSmall512').replace('StockRankWide32_capacity','StockPairRank_objective').replace('wide1024','small512')
    text=text.replace("A/'stock_identity_embedding32_network_v1_20261010.py',A/'stock_rank_wide32_explicit_architecture_recovery_v1_20261010.json'","A/'stock_identity_embedding_network_v1_20261010.py',A/'same_day_ranknet_loss_v1_20261010.py',A/'same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json'")
    # Previous replacements alter the recovery identifier, so use its actual new spelling.
    text=text.replace("A/'stock_identity_embedding32_network_v1_20261010.py',A/'stock_pairrank_explicit_architecture_recovery_v1_20261010.json'","A/'stock_identity_embedding_network_v1_20261010.py',A/'same_day_ranknet_loss_v1_20261010.py',A/'same_day_ranknet_loss_actual_CPU_controls_v1_20261010.json'")
    text=text.replace("'stock_rank_wide' in folder.name.lower() or 'stockrankwide' in folder.name.lower()","'stock_pairrank' in folder.name.lower() or 'stockpairrank' in folder.name.lower()")
    text=text.replace("('*stock_rank_wide*20261010.py','*stock_rank_wide*20261010.json')","('*stock_pairrank*20261010.py','*stock_pairrank*20261010.json')")
    text=text.replace('stock_pairrank_embedding_native_stage_and_fast17_sources_admission_v1_20261010.json','stock_pairrank_embedding_own32_controls46_sources_admission_v1_20261010.json')
    text=text.replace("'original16_architecture_refusal_preserved':True","'date_local_pair_loss_independent_CPU_passed':True")
    text=text.replace('保存一日排名股票身份32维与1024网络64轮独立容量试验：','保存同日成对排序目标股票身份16维与120特征512网络32轮独立试验：')
    path=A/'publish_stock_pairrank_objective_stages_main_v1_20261010.py'
    assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n')
    name='actual_StockPairRank_objective_stages_main_v1_20261010'
    assert allowed()
    row=start_service(name,path.name,[],{str(path):sha(path),str(source):sha(source)})
    create(A/(name+'_activation.json'),row);print(row,flush=True)
if __name__=='__main__':main()
