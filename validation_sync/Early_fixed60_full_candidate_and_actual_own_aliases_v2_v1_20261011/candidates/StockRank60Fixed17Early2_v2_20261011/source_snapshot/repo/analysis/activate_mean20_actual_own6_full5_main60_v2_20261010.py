"""Publish actual six mature own fits and five complete independent validation panels."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();closed('actual_stock_forward20_embedding_own_training_queue_v1_20261010');closed('StockForward20EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009')
    bank=Path('E:/赛题五_本机临时/stock_forward20_embedding_small512_BF16_bank6_v1_20261010')
    own=read(bank/'verification.json');assert own['actual_native_fits']==6
    pointer=A/'actual_StockForward20EmbeddingSmall512_full5_independent_location_v1_20261009.json';full=Path(read(pointer)['output']);proof=read(full/'verification.json')
    paths=[Path(__file__),pointer,bank/'verification.json',full/'verification.json',*[bank/str(y)/'info.json' for y in range(2020,2026)],*full.glob('*.json')]
    for y in range(2020,2026):
        info=read(bank/str(y)/'info.json');assert info['configuration']['epochs']==64 and info['configuration']['label_horizon_trading_days']==20
        assert info['training_meta']['last_label_end']<info['training_meta']['cutoff_exclusive']
    for p in [*own['input_sha256'],*proof['input_sha256']]:
        path=Path(p)
        if path.suffix in ('.json','.py'):paths.append(path)
    for job in ['actual_stock_forward20_embedding_small512_bank6_v1_20261010','actual_stock_forward20_embedding_own_training_queue_v1_20261010','StockForward20EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009']:
        folder=A/'service_owned_workflows_20261006'/job;paths += [p for p in folder.glob('*.json') if p.name in ('native_launch.json','service_execution.json','job_definition.json')]
    paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
    source=A/'publish_StockMean20_actual_mature_GPU_and179_sources_main_v57_20261010.py';text=source.read_text(encoding='utf8');begin=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',begin)
    text=text[:begin]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    text=text.replace('StockMean20_mature_GPU_sources_and179_routes_v57','StockMean20_actual_own6_full5_v60').replace('StockMean20_mature_GPU_sources_and179_routes_main_v57','StockMean20_actual_own6_full5_main_v60').replace('StockMean20_mature_GPU_sources_and179_routes_main_receipt_v57','StockMean20_actual_own6_full5_main_receipt_v60')
    text=text.replace('passed_actual49153_mature_mean20_fixture_and_GPU32_wide2_restart_compiled48_QA90_sources_annual_training_and_quality_pending','passed_actual6_own64_mature_mean20_identity_cross120_models_and_complete5635800_independent_native_replays_with10_cold_prefixes_quality_pending')
    text=text.replace('保存股票身份与120维特征二十日收益目标的实际成熟49153样本和GPU重启检查，以及179轮48项验证源码；年度评分和未来推理尚待完成','保存股票身份与120维特征二十日收益目标的实际六年度64轮成熟训练、5635800行独立重放及10个冷启动前缀；官方质量评分仍待完成')
    publisher=A/'publish_StockMean20_actual_own6_full5_main_v60_20261010.py';assert not publisher.exists();compile(text,str(publisher),'exec');publisher.write_text(text,encoding='utf8',newline='\n')
    proofpath=A/'StockMean20_actual_own6_full5_main_sources_admission_v60_20261010.json';create(proofpath,{'status':'verified_actual6_mature_mean20_own64_models_and_full5_proofs_before_main_publication','input_sha256':{str(p):sha(p) for p in [Path(__file__),publisher,*paths]},'actual_native_fits':6,'new_quality_scores':0,'test_labels_read':False})
    assert allowed();row=start_service('actual_StockMean20_own6_full5_main_v60_20261010',publisher.name,[],{str(publisher):sha(publisher),str(proofpath):sha(proofpath)});create(A/'actual_StockMean20_own6_full5_main_v60_20261010_activation.json',row)
    print({'actual_own6_full5_main60_started':True,'official_scores_pending':True},flush=True)
if __name__=='__main__':main()
