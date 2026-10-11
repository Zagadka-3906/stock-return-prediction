"""Publish the declared mixed-horizon experiment and separately its actual49 completed scores."""
from pathlib import Path
import sys,runpy,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    for phase in ['sources','official49']:
        assert allowed()
        if phase=='official49':closed('actual_rank5_rank20_after175_mixed_horizon49_screen_v2_20261011')
        paths=[Path(__file__),template,ROOT/'后续选模标准.md',A/'monitor_reboot_optimization_v95_20261011.py',A/'prepare_rank5_rank20_mixed_horizon49_v1_20261011.py',A/'run_rank5_rank20_after175_mixed_horizon49_screen_v1_20261011.py',A/'run_rank5_rank20_after175_mixed_horizon49_screen_v2_20261011.py',A/'rank5_rank20_mixed_horizon49_predeclared_plan_v1_20261011.json',A/'mixed_horizon49_actual_rank5_native_dependency_recovery_v2_20261011.json',A/'rank20_two_seed_raw_signal_v1_20261010.py',A/'rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json']
        for filename in ['complete180_registered_continuation_routes_v12_20261011.json','complete180_registered_continuation_routes_v13_20261011.json']:
            path=A/filename;proof=read(path);paths.append(path)
            for p,d in proof['input_sha256'].items():assert sha(p)==d,p
            paths.extend(Path(p) for p in proof['input_sha256'])
        if phase=='official49':
            out=Path('E:/赛题五_本机临时/StockRank5Rank20_after175_mixed_horizon49_screen_v2_20261011');proof=read(out/'verification.json')
            assert len(proof['records'])==49 and proof['actual_nonidentity_full_controls']==48 and proof['actual_nonidentity_prefix_controls']==144
            paths.extend(p for p in out.glob('*.json') if p.name not in ['actual_stage.json','best_so_far.json'])
            paths.extend(Path(p) for p in proof['input_sha256'] if Path(p).suffix.lower() in ['.json','.py','.md'])
            for row in proof['records']:paths.append(Path(row['official_score_cache']['official_metrics_source']))
        paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
        name='mixed_horizon49_registered13_'+phase+'_v1_20261011';mainname='mixed_horizon49_registered13_'+phase+'_main_v1_20261011';receiptname='mixed_horizon49_registered13_'+phase+'_main_receipt_v1_20261011'
        text=template.read_text(encoding='utf8').replace('StockRank20_actual_own6_full5_v66_20261010',name).replace('StockRank20_actual_own6_full5_main_v66_20261010',mainname).replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010',receiptname).replace('main_publisher_v11_20261010','main_publisher_reboot_v12_20261011')
        start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start);text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
        start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
        manifest={'status':'predeclared49_mixed_horizon_sources' if phase=='sources' else 'passed_actual49_mixed_horizon_TRAIN_official_scores','phase':phase,'label_horizons':[20,5],'training_populations_equal_not_claimed':True,'official_records':0 if phase=='sources' else 49,'full_independent_controls':0 if phase=='sources' else 48,'prefix_controls':0 if phase=='sources' else 144,'new_model_fits':0,'future_candidate_qualification_pending':True,'new_scores_by_publication':0,'test_labels_read':False,'global_exhaustion_proven':False}
        text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
        text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('保存五日与二十日排名目标现成模型的49项互补融合'+phase+'及第180轮已登记接续和版本别名证据；完整未来资格待验证'),text);assert count==1
        target=A/('publish_'+name+'_payload_main.py');assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n');assert allowed();runpy.run_path(str(target),run_name='__main__')
if __name__=='__main__':main()
