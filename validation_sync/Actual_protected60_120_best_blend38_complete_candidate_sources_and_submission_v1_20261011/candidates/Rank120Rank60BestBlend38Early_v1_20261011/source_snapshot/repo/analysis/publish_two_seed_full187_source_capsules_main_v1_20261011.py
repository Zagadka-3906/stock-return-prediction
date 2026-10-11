"""Publish frozen complete88 two-seed candidate/QA98 sources and the preserved source-route failure."""
from pathlib import Path
import sys,re,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    admission=A/'rank20_two_seed187_full_execution_sources_admission_v2_20261011.json'
    recovery=A/'two_seed187_exact_destination_route_recovery_v2_20261011.json'
    paths=[Path(__file__),template,admission,recovery,ROOT/'后续选模标准.md']
    for proof in (admission,recovery):
        data=read(proof)
        for p,d in data['input_sha256'].items():assert sha(p)==d,p
        paths += [Path(p) for p in data['input_sha256']]
    assert read(admission)['actual_callback_CPU_count']==11 and read(admission)['actual_models_per_nonidentity_signal']==2
    paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
    text=template.read_text(encoding='utf8')
    # Do not rewrite exact filenames already present in the scientific path list.
    text=text.replace('StockRank20_actual_own6_full5_v66_20261010','Rank20TwoSeed187_sources_v1_20261011').replace('StockRank20_actual_own6_full5_main_v66_20261010','Rank20TwoSeed187_sources_main_v1_20261011').replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010','Rank20TwoSeed187_sources_main_receipt_v1_20261011')
    start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
    manifest={'status':'compiled_full187_two_seed88_candidate_registry_QA98_sources_before_future',
        'expected_records':88,'expected_full_board':17490,'QA':98,'anchors':[175,186],
        'actual_models_per_nonidentity_signal':2,'actual_parent_callback_CPU_checks':11,
        'normalization_and_selected_native_and_full_future_qualification_pending':True,
        'new_model_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,
        'original_unlaunched_source_route_failure_preserved':True}
    text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
    text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('冻结第187轮双种子49项CDF与37项头部保护及175/186锚点的88项完整候选、双物理模型解码和QA98榜单流程；未来资格待完成'),text);assert count==1
    driver=A/'publish_Rank20TwoSeed187_sources_payload_main_v1_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    assert allowed();runpy.run_path(str(driver),run_name='__main__')

if __name__=='__main__':main()
