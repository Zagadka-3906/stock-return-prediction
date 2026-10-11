"""Publish actual completed rank20 six-state training and complete independent full5 evidence."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('actual_stock_rank20_embedding_own_training_queue_v1_20261010');closed('StockRank20EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009')
    bank=Path('E:/赛题五_本机临时/stock_rank20_embedding_small512_BF16_bank6_v1_20261010');own=read(bank/'verification.json');assert own['actual_native_fits']==6
    pointer=A/'actual_StockRank20EmbeddingSmall512_full5_independent_location_v1_20261009.json';full=Path(read(pointer)['output']);proof=read(full/'verification.json');assert proof['rows_days_stocks']==[5635800,1212,4650] and len(proof['records'])==5
    paths=[Path(__file__),pointer,bank/'verification.json',full/'verification.json',*[bank/str(y)/'info.json' for y in range(2020,2026)],*full.glob('*.json')]
    for year in range(2020,2026):
        info=read(bank/str(year)/'info.json');cfg=info['configuration'];assert cfg['target']=='y_rank_20mean' and cfg['epochs']==64 and cfg['label_horizon_trading_days']==20
        assert info['training_meta']['last_label_end']<info['training_meta']['cutoff_exclusive']
    for p in [*own['input_sha256'],*proof['input_sha256']]:
        path=Path(p)
        if path.suffix in ('.py','.json'):paths.append(path)
    for name in ['actual_stock_rank20_embedding_small512_bank6_v1_20261010','actual_stock_rank20_embedding_own_training_queue_v1_20261010','StockRank20EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009']:
        folder=A/'service_owned_workflows_20261006'/name;paths += [p for p in folder.glob('*.json') if p.name in ('service_execution.json','native_launch.json','job_definition.json')]
    paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
    source=A/'publish_complete_future_child_routes_main_v64_20261010.py';text=source.read_text(encoding='utf8');begin=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    text=text[:begin]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    text=text.replace('Complete_future_child_routes_v64','StockRank20_actual_own6_full5_v66').replace('Complete_future_child_routes_main_v64','StockRank20_actual_own6_full5_main_v66').replace('Complete_future_child_routes_main_receipt_v64','StockRank20_actual_own6_full5_main_receipt_v66')
    text=text.replace('verified_actual_current_dependency_handles_and_all15_unstarted_child_entry_types_including_cache_selected_candidate_own_closed_routes_before_future_dispatch_existing174_registry_preserved','passed_actual_six_own64_mature_rank20_identity_cross120_models_and_complete5635800_native_independent_forecasts_with10_cold_prefixes_quality_pending')
    text=text.replace('保存待执行流程15类封装与完整登记子入口、缓存嵌套候选的显式依赖、22个真实等待任务核验；174正在登记且未重启，科学控制和模型数学不变','保存实际股票身份与120维特征二十日排名目标六年度64轮成熟训练、5635800行独立解码和10个冷启动前缀；官方评分尚待完成')
    publisher=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py';assert not publisher.exists();compile(text,str(publisher),'exec');publisher.write_text(text,encoding='utf8',newline='\n')
    assert allowed();row=start_service('actual_StockRank20_own6_full5_main_v66_20261010',publisher.name,[],{str(publisher):sha(publisher)});create(A/'actual_StockRank20_own6_full5_main_v66_20261010_activation.json',row)
    print({'actual_rank20_own6_and5635800_independent_proofs_main66_queued':True,'official_scores_pending':True},flush=True)
if __name__=='__main__':main()
