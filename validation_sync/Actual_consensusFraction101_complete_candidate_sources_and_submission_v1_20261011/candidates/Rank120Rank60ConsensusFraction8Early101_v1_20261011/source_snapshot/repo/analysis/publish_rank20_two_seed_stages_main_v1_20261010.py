"""Publish the ensemble's declared sources and, separately, its actual completed official49 records."""
from pathlib import Path
import sys,re,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    for stage,dependencies in [('sources',()),('official49',('actual_rank20_two_seed_after175_complement49_screen_v1_20261010',))]:
        assert allowed()
        for name in dependencies:closed(name)
        paths=[Path(__file__),template,ROOT/'后续选模标准.md',
            A/'prepare_rank20_two_seed_complement49_v1_20261010.py',A/'run_rank20_two_seed_after175_complement49_screen_v1_20261010.py',
            A/'rank20_two_seed_raw_signal_v1_20261010.py',A/'rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json',
            A/'rank20_two_seed_complement49_predeclared_plan_v1_20261010.json']
        for base in [A/'service_owned_workflows_20261006',Path('E:/赛题五_本机临时')]:
            for folder in base.iterdir():
                if folder.is_dir() and ('rank20twoseed' in folder.name.lower() or 'rank20_two_seed' in folder.name.lower()):
                    paths.extend(p for p in folder.rglob('*.json') if 'tmp' not in p.relative_to(folder).parts and p.stat().st_size<20*1024**2)
        paths=list(dict.fromkeys(p for p in paths if p.name not in ('actual_stage.json','state.json','best_so_far.json')))
        assert all(p.is_file() for p in paths)
        text=template.read_text(encoding='utf8')
        start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
        text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
        text=text.replace('StockRank20_actual_own6_full5_v66_20261010',f'Rank20_two_seed_{stage}_v1_20261010').replace('StockRank20_actual_own6_full5_main_v66_20261010',f'Rank20_two_seed_{stage}_main_v1_20261010').replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010',f'Rank20_two_seed_{stage}_main_receipt_v1_20261010')
        start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
        manifest={'status':'actual_immutable_two_seed_stage_records_only','stage':stage,'seeds':[20261009,20261010],
            'baseline_round':175,'planned_official_records':49,'new_quality_scores_by_publication':0,
            'actual_future_X_read':False,'submission_qualified':False,'independent_scalar_CPU_controls_passed':True}
        if stage=='official49':
            pointer=A/'actual_StockRank20TwoSeed_after175_complement49_screen_location_v1_20261010.json'
            verification=read(Path(read(pointer)['output'])/'verification.json')
            assert verification['new_quality_score_records']==49
            manifest['actual_scored_records']=49;manifest['best_TRAIN_score']=verification['best']['connected_final_score']
        text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
        text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('保存20日排名独立双种子平均集成：'+stage+'；预声明49项TRAIN官方比较，未完成的不记为完成'),text);assert count==1
        driver=A/f'publish_Rank20_two_seed_{stage}_main_v1_20261010.py'
        assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
        assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
