"""Exact source and terminal61 TRAIN official score metadata publication, main only."""
from pathlib import Path
import sys,re,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha,read
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    folder=Path('E:/赛题五_本机临时/StockRank20EmbeddingSmall512_after174_high_impact61_screen_v1_20261010')
    for stage in ('sources','actual61'):
        assert allowed()
        if stage=='actual61':
            closed('actual_stock_rank20_embedding_after174_complement61_screen_v1_20261010')
            proof=read(folder/'verification.json');assert len(proof['records'])==61 and proof['actual_nonidentity_full_controls']==60 and proof['actual_nonidentity_prefix_controls']==180
        paths=[Path(__file__),template,A/'prepare_rank20_after174_complement61_v1_20261010.py',A/'run_stock_rank20_embedding_after174_complement61_screen_v1_20261010.py',A/'rank20_after174_complement61_predeclared_plan_v1_20261010.json',ROOT/'后续选模标准.md',A/'github_validation_sync_main_20261005/round174_receipt.json']
        if stage=='actual61':
            paths.extend(p for p in folder.rglob('*.json') if p.name not in ('actual_stage.json','best_so_far.json') and 'tmp' not in p.relative_to(folder).parts)
            for name in ('job_definition.json','native_launch.json','service_execution.json'):paths.append(A/'service_owned_workflows_20261006/actual_stock_rank20_embedding_after174_complement61_screen_v1_20261010'/name)
            def collect(value):
                if isinstance(value,dict):
                    for k,v in value.items():collect(k);collect(v)
                elif isinstance(value,list):
                    for v in value:collect(v)
                elif isinstance(value,str) and len(value)<500 and (value.startswith(('D:','E:'))):
                    p=Path(value)
                    if p.suffix in ('.json','.py','.md') and p.is_file() and p.stat().st_size<20*1024**2:paths.append(p)
            collect(proof)
            for p in list(paths):
                if p.suffix=='.json':collect(read(p))
        paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
        text=template.read_text(encoding='utf8');start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
        text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
        namespace=f'Rank20_after174_complement61_{stage}_v1_20261010'
        text=text.replace('StockRank20_actual_own6_full5_v66_20261010',namespace).replace('StockRank20_actual_own6_full5_main_v66_20261010',namespace+'_main').replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010',namespace+'_main_receipt')
        start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
        manifest={'status':'exact_actual_TRAIN_only_stage_metadata','stage':stage,'parent_round':174,'predeclared_cases':61,'actual_quality_records':61 if stage=='actual61' else 0,'new_native_fits':0,'submission_qualified':False,'actual_future_X_read':False,'test_labels_read':False}
        text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
        text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('保存20日排名与已完全验证174方案互补61项：'+stage+'；仅含实际完成的TRAIN评分与独立检查'),text);assert count==1
        driver=A/f'publish_{namespace}_main.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
        assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
