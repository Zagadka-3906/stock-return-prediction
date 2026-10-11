"""Publish the actual complete49 score/control evidence only after its worker passes."""
from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed

def main():
 assert allowed();closed('actual_rank60_rank20_after183_mixed49_screen_v1_20261011')
 folder=Path('E:/赛题五_本机临时/StockRank60Rank20_after183_higher_allocation49_screen_v1_20261011');proof=read(folder/'verification.json')
 assert len(proof['records'])==proof['new_quality_score_records']==49
 assert (proof['actual_nonidentity_full_controls'],proof['actual_nonidentity_prefix_controls'])==(48,144)
 for p,d in proof['input_sha256'].items():assert sha(p)==d,p
 template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py'
 paths=[Path(__file__),template,folder/'verification.json',folder/'frozen_before_any_new_controls_or_scores.json',A/'rank60_rank20_after183_mixed49_predeclared_sources_admission_v1_20261011.json',A/'rank60_rank20_mixed_actual_twelve_parent_callbacks_CPU_controls_v1_20261011.json',A/'rank60_rank20_mixed_after_qualified183_native_stage_v1_20261011.py',A/'predict_rank60_rank20_mixed_complete_qualified183_scheme_v1_20261011.py',A/'run_rank60_rank20_after183_mixed49_screen_v1_20261011.py']
 for row in proof['records']:
  p=folder/f"case{row['case']:03d}_official.json";assert read(p)==row
  control=folder/f"case{row['case']:03d}_controls.json";assert sha(control)==row['control_sha256']
  capsule=Path(row['official_score_cache']['official_metrics_source']);assert sha(capsule)==row['official_metric_capsule_sha256'] and read(capsule)['metrics']==row['metrics']
  paths.extend([p,control,capsule])
 for pat in ['blend*_controls.json']:paths.extend(folder.glob(pat))
 paths.extend(Path(p) for p in proof['input_sha256'] if Path(p).suffix in ('.py','.json') and Path(p).stat().st_size<20*1024**2)
 prefix='Rank60Rank20_after183_completed49';s=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7',prefix).replace('from owned_idle_publication_wait_runtime_v1_20261010 import hold','from owned_idle_publication_wait_reboot_identity_v2_20261011 import hold')
 start=s.index('    paths=');end=s.index('    import publish_classifier',start);s=s[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+s[end:]
 start=s.index("    payload[(prefix/'manifest.json').as_posix()]");end=s.index('    out=Path(',start)
 manifest={'status':'actual49_TRAIN_only20_60_mixed_raw_scores_after_exact_qualified183_passed','actual_scored_records':49,'actual_nonidentity_full_controls':48,'actual_nonidentity_prefix_controls':144,'best':proof['best'],'new_fits_by_publication':0,'new_scores_by_publication':0,'selected_future_candidate_and_full_board_registration_pending':True,'test_labels_read':False}
 s=s[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+s[end:]
 s=s.replace('新十日平均收益排名股票身份模型：7项独立均值排名与严格成熟未来投毒CPU检查通过；原生与独立解码器冻结，尚未训练或评分','已完成49项成熟20/60混合信号与完整183融合的TRAIN官方评分；48项全量Pandas和144项前缀检查通过；未来候选与完整榜资格待核验')
 driver=A/'publish_frozen_Rank60Rank20_after183_completed49_main_v1_20261011.py';assert not driver.exists();compile(s,str(driver),'exec');driver.write_text(s,encoding='utf8',newline='\n');assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
