"""Main-only sources, completed near-pure49, long-window49 and actual native14 phases."""
from pathlib import Path
import sys,re,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    admission=A/'cached_mixed_near_pure_and_long_window49_admission_v1_20261011.json';data=read(admission)
    native=A/'mixed_horizon_native14_predictor_CPU11_sources_admission_v1_20261011.json'
    phases=[('native14',None)]
    for phase,screen in phases:
        assert allowed()
        if screen:closed(screen['service'])
        if phase=='native14':closed('actual_rank5_rank20_mixed_selected_native14_v1_20261011')
        paths=[Path(__file__),template,ROOT/'后续选模标准.md',admission,native]
        for proofpath in [admission,native]:
            proof=read(proofpath)
            for p,d in proof['input_sha256'].items():assert sha(p)==d,p
            paths.extend(Path(p) for p in proof['input_sha256'])
        if screen:
            folder=Path(screen['output']);proof=read(folder/'verification.json')
            assert len(proof['records'])==49 and proof['actual_nonidentity_full_controls']==48 and proof['actual_nonidentity_prefix_controls']==144
            paths.extend(p for p in folder.glob('*.json') if p.name not in ('actual_stage.json','best_so_far.json'))
            paths.extend(Path(p) for p in proof['input_sha256'] if Path(p).suffix.lower() in ('.json','.py','.md'))
            paths.extend(Path(row['official_score_cache']['official_metrics_source']) for row in proof['records'])
        if phase=='native14':
            folder=Path('E:/赛题五_本机临时/rank5_rank20_mixed_selected_native14_v1_20261011');proof=read(folder/'verification.json')
            if proof['best']['configuration']['kind']!='anchor175':assert proof['actual_native_cases']==proof['actual_cold_cases']==14 and len(proof['prefit_rejections'])==7
            paths.extend(p for p in folder.glob('*.json'));paths.extend(Path(p) for p in proof['input_sha256'] if Path(p).suffix.lower() in ('.json','.py','.md'))
        paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
        stem='additional_cached_mixed_'+phase+'_recovery14_v2_20261011';mainstem='additional_cached_mixed_'+phase+'_main_recovery14_v2_20261011';receiptstem='additional_cached_mixed_'+phase+'_main_receipt_recovery14_v2_20261011'
        text=template.read_text(encoding='utf8').replace('StockRank20_actual_own6_full5_v66_20261010',stem).replace('StockRank20_actual_own6_full5_main_v66_20261010',mainstem).replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010',receiptstem).replace('main_publisher_v11_20261010','main_publisher_reboot_v12_20261011')
        start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start);text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
        start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
        manifest={'status':'actual_phase_evidence_preserved','phase':phase,'official_score_records':49 if screen else 0,'actual_full_Pandas_controls':48 if screen else 0,'actual_prefix_controls':144 if screen else 0,'native14_actual_only':phase=='native14','CPU_callback_count':11,'new_fits':0,'new_scores_by_publication':0,'training_populations_equal_not_claimed':True,'future_candidate_qualification_pending':True,'test_labels_read':False,'global_exhaustion_proven':False}
        text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
        text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('保存缓存模型小比例跨目标融合、252与504日窗口融合和各自实际独立控制：'+phase+'；未完成未来资格不记通过'),text);assert count==1
        target=A/('publish_'+stem+'_payload_main.py');assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');assert allowed();runpy.run_path(str(target),run_name='__main__')
if __name__=='__main__':main()
