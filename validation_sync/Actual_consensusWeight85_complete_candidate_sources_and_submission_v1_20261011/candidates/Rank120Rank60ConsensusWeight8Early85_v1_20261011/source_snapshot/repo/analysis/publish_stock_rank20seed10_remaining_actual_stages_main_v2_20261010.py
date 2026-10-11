"""Serialize actual immutable capacity sources/controls/scores onto verified GitHub main."""
from pathlib import Path
import sys,re,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha,read
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def main():
    assert allowed()
    phases=[('restart_CPU',('actual_stock_rank20seed10_embedding_small512_restart_actual_fixture_v2_20261010','StockRank20Seed10EmbeddingSmall512_independent_small_CPU_v1_20261009')),('own6_full5',('StockRank20Seed10EmbeddingSmall512_independent_full5_GPU_controls_v1_20261009',)),('native42_official46',('actual_stock_rank20seed10_embedding_six_state_native42_v1_20261010','actual_stock_rank20seed10_embedding_after175_large_allocation29_screen_v1_20261010'))]
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    for stage,dependencies in phases:
        for name in dependencies:closed(name)
        assert allowed()
        paths=[Path(__file__),A/'recover_seed10_actual_fixture_dependency_v2_20261010.py',A/'seed10_actual_fixture_dependency_recovery_sources_v2_20261010.json',template,ROOT/'后续选模标准.md',A/'stock_identity_embedding_network_v1_20261010.py',A/'recent252_rank20_mature_training_population_v1_20261010.py',A/'recent252_rank20_mature_population_actual_CPU_controls_v1_20261010.json',A/'prepare_rank20_seed10_own64_controls46_v1_20261010.py']
        for pattern in ('*stock_rank20seed10*20261010.py','*stock_rank20seed10*20261010.json'):
            paths.extend(A.glob(pattern))
        for base in [A/'service_owned_workflows_20261006',Path('E:/赛题五_本机临时'),Path('E:/赛题五_本机临时/GPU实测_20261009')]:
            for folder in base.iterdir():
                if folder.is_dir() and ('stock_rank20seed10' in folder.name.lower() or 'stockrank20seed10' in folder.name.lower()):
                    paths.extend(p for p in folder.rglob('*.json') if 'tmp' not in p.relative_to(folder).parts and p.stat().st_size<20*1024**2)
        paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
        # Exclude observer files: these change while a publication waits for the mutex.
        paths=[p for p in paths if p.name not in ('actual_stage.json','state.json','best_so_far.json')]
        text=template.read_text(encoding='utf8')
        start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
        text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
        text=text.replace('StockRank20_actual_own6_full5_v66_20261010',f'StockRank20Seed10_objective_{stage}_v1_20261010').replace('StockRank20_actual_own6_full5_main_v66_20261010',f'StockRank20Seed10_objective_{stage}_main_v1_20261010').replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010',f'StockRank20Seed10_objective_{stage}_main_receipt_v1_20261010')
        start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
        manifest={'status':'actual_immutable_capacity_stage_records_only','stage':stage,'configuration':read(A/'stock_rank20seed10_embedding_own64_controls46_sources_admission_v1_20261010.json')['configuration'],'actual_future_X_read':False,'submission_qualification_pending':True,'new_quality_scores_by_publication':0,'unchanged_mature_rank20_population_controls_explicitly_reused':True,'independent_seed':20261010}
        text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
        text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('保存独立种子20261010的20日排名目标股票身份16维与120特征512网络64轮试验：'+stage+'；仅记录实际已完成验证'),text);assert count==1
        driver=A/f'publish_StockRank20Seed10_objective_{stage}_main_v1_20261010.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
        assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
