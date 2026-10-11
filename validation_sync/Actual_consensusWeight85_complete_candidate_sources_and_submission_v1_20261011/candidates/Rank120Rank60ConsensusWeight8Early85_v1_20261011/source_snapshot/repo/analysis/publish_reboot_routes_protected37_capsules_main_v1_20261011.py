"""Publish recovery sources and all completed37 scientific records, without duplicate scoring."""
from pathlib import Path
import sys,runpy,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed();closed('actual_rank20_two_seed_protected_selected_native14_reboot_v2_20261011')
    proof=A/'reboot_complete_candidate_routes_v11_20261011.json';d=read(proof)
    paths=[Path(__file__),proof,A/'monitor_reboot_optimization_v94_20261011.py',A/'two_seed_protected37_completed_pointer_recovery_v2_20261011.json',A/'actual_StockRank20TwoSeed_after175_protected_tail37_screen_location_v1_20261011.json',ROOT/'后续选模标准.md',*[Path(p) for p in d['input_sha256']]]
    for p,h in d['input_sha256'].items():assert sha(p)==h,p
    for folder in [Path('E:/赛题五_本机临时/StockRank20TwoSeed_after175_protected_tail37_screen_v1_20261011'),Path('E:/赛题五_本机临时/rank20_two_seed_protected_selected_native14_v1_20261011')]:
        paths.extend(p for p in folder.rglob('*.json') if 'tmp' not in p.relative_to(folder).parts and p.name not in ('best_so_far.json','actual_stage.json','state.json'))
    for name in ['actual_rank20_two_seed_after175_protected_tail37_screen_v1_20261011','actual_rank20_two_seed_protected37_completed_admission_v2_20261011','actual_rank20_two_seed_protected_selected_native14_reboot_v2_20261011','StockRank20Embedding180_complete48_family_actual_resume_v10_20261011']:
        folder=A/'service_owned_workflows_20261006'/name;paths.extend(p for p in folder.glob('*.json'))
    paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths)
    template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py';paths.append(template)
    text=template.read_text(encoding='utf8')
    for old,new in [('StockRank20_actual_own6_full5_v66_20261010','reboot_routes_and_protected37_v1_20261011'),('StockRank20_actual_own6_full5_main_v66_20261010','reboot_routes_and_protected37_main_v1_20261011'),('StockRank20_actual_own6_full5_main_receipt_v66_20261010','reboot_routes_and_protected37_main_receipt_v1_20261011')]:text=text.replace(old,new)
    text=text.replace('main_publisher_v11_20261010','main_publisher_reboot_v12_20261011')
    start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
    manifest={'status':'passed_actual37_protected_scores_and_selected_native_controls_with_evidence_based_reboot_routes','official_scored_records':37,'full_independent_controls':36,'prefix_controls':108,'new_scores_by_recovery':0,'new_fits_by_recovery':0,'complete180_188_future_qualification_pending':True,'global_exhaustion_proven':False,'original_failures_preserved':True,'test_labels_read':False}
    text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
    text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('保存双种子头部保护37项实际官方评分和36项完整108项前缀验证、原生资格与重启后180—188候选继续路由；保留原失败'),text);assert count==1
    target=A/'publish_reboot_routes_protected37_payload_main_v1_20261011.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    assert allowed();runpy.run_path(str(target),run_name='__main__')
if __name__=='__main__':main()
