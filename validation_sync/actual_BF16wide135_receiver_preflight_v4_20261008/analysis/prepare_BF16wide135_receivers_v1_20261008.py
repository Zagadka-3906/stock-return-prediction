"""Prepare fresh seal/full-QA receivers before new quality observations; never alter pinned original sources."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create


def main():
    source_seal=A/'seal_nonflag_ReverseBayesFine40_selected_candidate_v1_20261007.py'
    seal=source_seal.read_text(encoding='utf8').replace('nonflag_ReverseBayesFine40','BF16wide40')
    seal=seal.replace('BF16wide40_selected_candidate_preparation_v1','BF16wide40_selected_candidate_preparation_v1_20261008')
    seal=seal.replace('BF16wide40_selected_release_v1_20261007','BF16wide40_selected_release_v1_20261008')
    seal=seal.replace('BF16wide40_official_comparison_v1_20261007','BF16wide40_official_comparison_v1_20261008')
    seal=seal.replace("A/'nonflag_residual_EmpiricalBayes64_bank10_20261007/verification.json'","A/'BF16wide40_actual_controls_index_v1_20261008.json'")
    seal=seal.replace("candidate/'nonflag_residual_ReverseBayes64_native_replay_verification.json'","candidate/'BF16_complete_parent_native_replay_verification.json'")
    seal=seal.replace('passed_actual_complete_parent_and_nonflag_ReverseBayes64_two_full_replays_independent_and_cold80','passed_actual_complete_parent_and_BF16_two_full_native_independent_replays_and_cold80')
    seal=seal.replace("if __name__=='__main__':main()","if __name__=='__main__':\n    from BF16wide135_storage_v1_20261008 import installed_transfer\n    with installed_transfer():main()")
    source_driver=A/'run_nonflag_ReverseBayesFine40_round134_full_registration_v3_20261008.py'
    driver=source_driver.read_text(encoding='utf8')
    from prepare_BF16wide40_round135_sources_v1_20261008 import convert
    driver=convert(driver)
    driver=driver.replace('Register28 actual numerical-order scores and its sealed winner, full QA30, and main.',
        'Register40 actual complete-parent neural comparisons, sealed winner, full QA46 and main.')
    start=driver.index("    for name in (");end=driver.index('        service=',start)
    driver=driver[:start]+"    for name in ('BF16wide40_official_comparison_v1_20261008','BF16wide40_scores_main_publication_v1_20261008',\n        'BF16wide40_selected_candidate_sealing_v1_20261008','nonflag_ReverseBayesFine40_round134_full_registration_v1'):\n"+driver[end:]
    driver=driver.replace('prepare_BF16wide40_round135_sources_v3_20261008','prepare_BF16wide40_round135_sources_v1_20261008')
    driver=driver.replace('BF16wide40_round135_source_preparation_v1_20261007','BF16wide40_round135_source_preparation_v1_20261008')
    driver=driver.replace('BF16wide40_round135_actual_registration_v1_20261007','BF16wide40_round135_actual_registration_v1_20261008')
    start=driver.index('    import ast\n');end=driver.index('    create(A/',start)
    driver=driver[:start]+"    from prepare_BF16wide40_round135_sources_v1_20261008 import source_paths\n    ns={'sources':source_paths()}\n    assert all(p.is_file() for p in ns['sources'])\n"+driver[end:]
    driver=driver.replace('BF16wide40_actual_source_paths_before_registration_20261007','BF16wide40_actual_source_paths_before_registration_20261008')
    driver=driver.replace('(112,132,133)','(112,133,134)')
    driver=driver.replace("ROOT/'tmp/BF16wide40_full135_20261007'","Path('E:/赛题五_本机临时/第135轮_20261008/tmp/full135')")
    driver=driver.replace("'完整父方案的反向贝叶斯残差幅度加密'","'完整父方案与BF16宽网络排序融合'")
    driver=driver.replace("'预定40项完整官方比较：三个合格锚点、36项反向贝叶斯幅度加密和一个消融'","'预定40项：三个合格锚点、36项宽网络融合、零权重恒等对照'")
    driver=driver.replace('failed_preserved_HGB_quarter_numeric28_full119_registration','failed_preserved_BF16wide40_full135_registration')
    driver=driver.replace("with installed(A/'run_BF16wide40_round135_full_registration_v2_file_IO_20261008'):main()",
        "from BF16wide135_storage_v1_20261008 import installed_transfer\n    with installed(A/'run_BF16wide40_round135_full_registration_v1_file_IO_20261008'),installed_transfer():main()")
    outputs={A/'seal_BF16wide40_selected_candidate_v1_20261008.py':seal,A/'run_BF16wide40_round135_full_registration_v1_20261008.py':driver}
    for p,t in outputs.items():assert not p.exists();compile(t,str(p),'exec')
    for p,t in outputs.items():p.write_text(t,encoding='utf8',newline='\n')
    print('Fresh135 seal and full-QA46 receiver sources prepared before quality scores.',flush=True)


if __name__=='__main__':main()
