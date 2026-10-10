"""Publish the compiled48/QA97 candidate flow and preserved unlaunched admission failure on main."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    assert allowed()
    source=A/'publish_seed10_complete48_source_capsules_main_v2_20261011.py'
    text=source.read_text(encoding='utf8')
    text=text.replace('seed10_complete48_normalization_native14_sources_admission_v1_20261011.json','stock_rank20seed10_embedding186_full_execution_sources_admission_v2_20261011.json')
    text=text.replace('publish_seed10_complete48_sources_main_v1_20261011.py','prepare_StockRank20Seed10Embedding186_complete48_pipeline_v1_20261011.py')
    text=text.replace('seed10_source_capsules_case_collision_recovery_v2_20261011.json','seed10_full186_source_admission_recovery_v2_20261011.json')
    text=text.replace('Seed10_complete48_sources','Seed10_full186_sources')
    text=text.replace('frozen48_normalization_and_native14_sources_actual11_callback_CPU_only',
        'compiled_full186_candidate_registry_QA97_sources_actual11_callback_CPU_only')
    text=text.replace("'complete186_future_pipeline_not_created':True","'complete186_future_pipeline_created':True,'complete186_qualification_pending':True,'QA':97,'expected_full_board':17402")
    text=text.replace("'冻结独立种子20261010的48项统一选模与原生资格源码，保存11项实际父方案回调CPU检查；未来推理尚未派发'",
        "'冻结独立种子20261010第186轮48项完整候选与QA97登记流程；复用全部完成评分，未来推理尚待资格，保留原源码准入失败'")
    text=text.replace('publish_Seed10_full186_sources_payload_main_v2_20261011.py','publish_Seed10_full186_sources_payload_main_v1_20261011.py')
    needle='    assert all(p.is_file() for p in paths)';assert text.count(needle)==1
    text=text.replace(needle,"    paths += [A/'prepare_seed10_full186_sources_main_v1_20261011.py',A/'recover_seed10_full186_source_admission_v2_20261011.py']\n    paths += [Path(p) for p in read(A/'seed10_full186_source_admission_recovery_v2_20261011.json')['input_sha256']]\n"+needle)
    driver=A/'publish_seed10_full186_source_capsules_main_v1_20261011.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    assert allowed()
    name='actual_Seed10_full186_source_capsules_main_v1_20261011'
    row=start_service(name,driver.name,[],{str(driver):sha(driver),str(Path(__file__)):sha(__file__)})
    create(A/(name+'_activation.json'),row)
    print({'full186_sources_and_original_admission_failure_main_queued':True},flush=True)

if __name__=='__main__':main()
