"""Publish declared88 sources first, then actual normalized and selected controls, on verified main."""
from pathlib import Path
import sys,re,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def main():
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    admission=A/'rank20_two_seed_complete88_normalization_native14_sources_admission_v1_20261011.json'
    for stage,deps in [('sources',()),('normalized_selected14',('actual_rank20_two_seed88_after186_normalization_v1_20261011','actual_rank20_two_seed88_selected_native14_v1_20261011'))]:
        assert allowed()
        for name in deps:closed(name)
        data=read(admission)
        for p,d in data['input_sha256'].items():assert sha(p)==d,p
        paths=list(dict.fromkeys([Path(__file__),template,admission,*[Path(p) for p in data['input_sha256']]]))
        if stage=='normalized_selected14':
            for pointername in ['actual_rank20_two_seed_complete88_after186_location_v1_20261011.json','actual_rank20_two_seed88_selected_native14_location_v1_20261011.json']:
                pointer=A/pointername;folder=Path(read(pointer)['output']);paths += [pointer,*folder.glob('*.json')]
        assert all(p.is_file() for p in paths)
        text=template.read_text(encoding='utf8')
        # Namespace only the transport template, before adding exact scientific file paths.
        text=text.replace('StockRank20_actual_own6_full5_v66_20261010',f'Rank20_two_seed88_{stage}_v1_20261011').replace('StockRank20_actual_own6_full5_main_v66_20261010',f'Rank20_two_seed88_{stage}_main_v1_20261011').replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010',f'Rank20_two_seed88_{stage}_main_receipt_v1_20261011')
        start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
        text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
        start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
        manifest={'status':'immutable_two_seed88_stage_records','stage':stage,'expected_records':88,'anchors':[175,186],
            'new_quality_scores_by_publication':0,'full187_candidate_registry_pipeline_pending':True,'actual_future_X_read':False,'test_labels_read':False}
        if stage=='normalized_selected14':
            pointer=A/'actual_rank20_two_seed88_selected_native14_location_v1_20261011.json';folder=Path(read(pointer)['output'])
            pilot=read(folder/'pilot88.json');verification=read(folder/'verification.json')
            assert len(pilot['records'])==88 and pilot['best']==verification['best']
            manifest.update(actual_normalized_records=88,best_TRAIN_score=pilot['best']['connected_final_score'],
                actual_native_cases=verification.get('actual_native_cases',0),actual_cold_cases=verification.get('actual_cold_cases',0),
                selected_anchor_reuse=pilot['best']['configuration']['model'] is None)
        text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
        text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('保存双种子49项及头部保护37项与175/186锚点的88项统一选模：'+stage+'；未来完整候选资格尚待完成'),text);assert count==1
        driver=A/f'publish_Rank20_two_seed88_{stage}_payload_main_v1_20261011.py'
        assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
        assert allowed();runpy.run_path(str(driver),run_name='__main__')

if __name__=='__main__':main()
