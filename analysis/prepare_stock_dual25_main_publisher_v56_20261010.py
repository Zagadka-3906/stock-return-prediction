"""Publish each real25-record complementary embedding validation when complete."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    source=A/'publish_stock_rank_embedding_after170_completion_v55_20261010.py';text=source.read_text(encoding='utf8')
    text=text.replace('actual_stock_rank_embedding_after170_fast17_screen_v1_20261010','actual_stock_dual_embedding_after173_high_impact25_screen_v1_20261010')
    text=text.replace('StockRankEmbeddingSmall512_after170_high_impact17_screen_v1_20261010','StockDualEmbedding_after173_high_impact25_screen_v1_20261010')
    text=text.replace('run_stock_rank_embedding_after170_fast17_screen_v1_20261010.py','run_stock_dual_embedding_after173_high_impact25_screen_v1_20261010.py')
    text=text.replace("==17","==25").replace("==16","==24").replace("==48","==72")
    text=text.replace("'scored_records':17","'scored_records':25").replace('passed17_actual_stock_rank_embedding_TRAIN_official_records16_full48_cold','passed25_actual_stock_dual_embedding_TRAIN_official_records24_full72_cold')
    text=text.replace('stock_rank_embedding17_after170_completion_v55_20261010','stock_dual_embedding25_after173_completion_v56_20261010').replace('stock_rank_embedding17_after170_completion_main_v55_20261010','stock_dual_embedding25_after173_completion_main_v56_20261010')
    marker='    bank=Path'
    idx=text.index(marker)
    text=text[:idx]+"    paths += [A/'stock_dual_embedding_after173_predeclared25_plan_v1_20261010.json',A/'prepare_stock_dual_embedding_after173_25_v1_20261010.py',A/'dual_target_daily_rank_consensus_v1_20261010.py']\n    return_bank=Path(read(A/'actual_stock_embedding_small512_bank6_location_v1_20261010.json')['output'])\n    paths += [return_bank/'verification.json',*return_bank.glob('*/info.json')]\n    for return_pointer in ('actual_stock_embedding_six_state_native42_location_v1_20261010.json','actual_StockEmbeddingSmall512_full5_independent_location_v1_20261009.json'):\n        paths += [A/return_pointer,*Path(read(A/return_pointer)['output']).glob('*.json')]\n"+text[idx:]
    text=text.replace('保存新股票身份嵌入模型六年度训练独立检查和17项真实TRAIN官方评分、16项完整及48项因果前缀控制','保存股票收益与排名嵌入模型互补集成25项真实TRAIN官方评分、24项完整及72项因果前缀控制')
    dest=A/'publish_stock_dual_embedding_after173_completion_v56_20261010.py';assert not dest.exists();compile(text,str(dest),'exec');dest.write_text(text,encoding='utf8',newline='\n')
    row=start_service('actual_stock_dual_embedding_after173_completion_main_v56_20261010',dest.name,[],{str(dest):sha(dest)})
    create(A/'actual_stock_dual_embedding_after173_completion_main_activation_v56_20261010.json',row)
    print({'dual25_main_publication':'queued_after_actual_completion'},flush=True)
if __name__=='__main__':main()
