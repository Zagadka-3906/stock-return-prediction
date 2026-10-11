"""Publish the fixed82 source plan and each real41-case terminal result separately onto main."""
from pathlib import Path
import sys,re,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import create,sha,read
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    for stage,parent,version in [('after174',174,69),('after175',175,70)]:
        assert allowed()
        if parent:
            closed(f'actual_stock_rank20_embedding_after{parent}_tiny_CDF41_screen_v1_20261010')
            folder=Path(f'E:/赛题五_本机临时/StockRank20EmbeddingSmall512_after{parent}_tiny_CDF41_screen_v1_20261010')
            proof=read(folder/'verification.json');assert len(proof['records'])==41 and proof['actual_nonidentity_full_controls']==40 and proof['actual_nonidentity_prefix_controls']==120
        paths=[Path(__file__),template,A/'prepare_rank20_tiny_CDF82_after174175_v1_20261010.py',A/'rank20_tiny_CDF82_after174175_predeclared_plan_v1_20261010.json',A/'run_stock_rank20_embedding_after174_tiny_CDF41_screen_v1_20261010.py',A/'run_stock_rank20_embedding_after175_tiny_CDF41_screen_v1_20261010.py',ROOT/'后续选模标准.md',A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json']
        if parent:
            paths.extend(p for p in folder.rglob('*.json') if p.name not in ('actual_stage.json','best_so_far.json') and 'tmp' not in p.relative_to(folder).parts)
            service=A/f'service_owned_workflows_20261006/actual_stock_rank20_embedding_after{parent}_tiny_CDF41_screen_v1_20261010';paths.extend(service/n for n in ('job_definition.json','native_launch.json','service_execution.json'))
            def collect(value):
                if isinstance(value,dict):
                    for k,v in value.items():collect(k);collect(v)
                elif isinstance(value,list):
                    for v in value:collect(v)
                elif isinstance(value,str) and len(value)<500 and value.startswith(('D:','E:')):
                    p=Path(value)
                    if p.suffix in ('.json','.py','.md') and p.is_file() and p.stat().st_size<20*1024**2:paths.append(p)
            collect(proof)
            for p in list(paths):
                if p.suffix=='.json':collect(read(p))
        paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
        text=template.read_text(encoding='utf8');start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
        text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
        namespace=f'Rank20_tinyCDF82_{stage}_v{version}_20261010';receipt=f'Rank20_tinyCDF41_after{parent}_main_receipt_v{version}_20261010' if parent else 'Rank20_tinyCDF82_sources_main_receipt_v68_20261010'
        text=text.replace('StockRank20_actual_own6_full5_v66_20261010',namespace).replace('StockRank20_actual_own6_full5_main_v66_20261010',namespace+'_main').replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010',receipt)
        start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
        manifest={'status':'actual_TRAIN_only_tiny_CDF_stage_metadata','stage':stage,'parent_round':parent,'predeclared_total_cases':82,'actual_quality_records':41 if parent else 0,'new_native_fits':0,'submission_qualified':False,'actual_future_X_read':False,'test_labels_read':False}
        text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
        text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('保存20日排名与174/175的82项微权重互补：'+stage+'；实际已完成TRAIN记录与完整及冷启动检查'),text);assert count==1
        driver=A/f'publish_{namespace}_main.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
        assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
