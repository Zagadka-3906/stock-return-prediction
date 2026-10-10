"""Publish the actual callback CPU checks and frozen seed10 normalization/qualification sources."""
from pathlib import Path
import sys,re,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    admission=A/'stock_rank20seed10_embedding186_full_execution_sources_admission_v2_20261011.json'
    proof=read(admission)
    paths=list(dict.fromkeys([Path(__file__),A/'prepare_StockRank20Seed10Embedding186_complete48_pipeline_v1_20261011.py',A/'seed10_full186_source_admission_recovery_v2_20261011.json',template,admission,*[Path(p) for p in proof['input_sha256']]]))
    paths += [A/'prepare_seed10_full186_sources_main_v1_20261011.py',A/'recover_seed10_full186_source_admission_v2_20261011.py']
    paths += [Path(p) for p in read(A/'seed10_full186_source_admission_recovery_v2_20261011.json')['input_sha256']]
    paths += [Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\recover_seed10_full186_publication_template_literal_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\seed10_full186_publication_literal_recovery_v2_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_Seed10_full186_source_capsules_main_v1_20261011\\service_execution.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\service_owned_workflows_20261006\\actual_Seed10_full186_source_capsules_main_v1_20261011\\stderr.log', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_Seed10_full186_sources_payload_main_v1_20261011.py']]
    assert all(p.is_file() for p in paths)
    text=template.read_text(encoding='utf8')
    text=text.replace('StockRank20_actual_own6_full5_v66_20261010','Seed10_full186_sources_v2_20261011').replace('StockRank20_actual_own6_full5_main_v66_20261010','Seed10_full186_sources_main_v2_20261011').replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010','Seed10_full186_sources_main_receipt_v2_20261011')
    start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
    manifest={'status':'compiled_full186_candidate_registry_QA97_sources_actual11_callback_CPU_only','expected_records':48,
        'anchors':[175,185],'actual_callback_CPU_checks':11,'selected_native14_pending':True,'complete186_future_pipeline_created':True,'complete186_qualification_pending':True,'QA':97,'expected_full_board':17402,
        'actual_future_X_read':False,'test_labels_read':False,'new_quality_scores':0,'new_native_fits':0}
    text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
    text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('冻结独立种子20261010第186轮48项完整候选与QA97登记流程；复用全部完成评分，未来推理尚待资格，保留原源码准入失败'),text);assert count==1
    driver=A/'publish_Seed10_full186_sources_payload_main_v2_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
