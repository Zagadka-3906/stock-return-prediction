from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('actual_rank10_rank20_after175_higher_allocation49_screen_v1_20261011')
 folder=Path('E:/赛题五_本机临时/StockRank10Rank20_after175_higher_allocation49_screen_v1_20261011');proof=read(folder/'verification.json')
 assert len(proof['records'])==49 and proof['new_quality_score_records']==49 and proof['actual_nonidentity_full_controls']==48 and proof['actual_nonidentity_prefix_controls']==144
 paths=[Path(__file__),A/'prepare_rank10_rank20_higher_allocation49_v1_20261011.py',A/'run_rank10_rank20_after175_higher_allocation49_screen_v1_20261011.py',A/'rank10_rank20_higher_allocation49_predeclared_sources_admission_v1_20261011.json',folder/'verification.json',folder/'frozen_before_any_new_controls_or_scores.json',*folder.glob('case*_official.json'),*folder.glob('case*_controls.json')]
 for p,d in proof['input_sha256'].items():
  assert sha(p)==d,p
  if Path(p).suffix in ('.py','.json'):paths.append(Path(p))
 for row in proof['records']:
  p=Path(row['official_score_cache']['official_metrics_source']);assert sha(p)==row['official_metric_capsule_sha256'];paths.append(p)
 template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py';paths.append(template)
 text=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7','Rank10Rank20_higher49_actual_official')
 start=text.index('    paths=');end=text.index('    import publish_classifier',start)
 text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
 start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
 manifest={'status':'actual49_cached_rank10_rank20_higher_allocation_training_only_official_scores_completed','actual_scored_records':49,'actual_full_independent_controls':48,'actual_prefix_controls':144,'new_fits':0,'new_scores_by_publication':0,'selected_native14_and_future_qualification_pending':True,'test_labels_read':False,'future_X_read_for_selection':False,'best_S':proof['best']['connected_final_score']}
 text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
 text=text.replace('新十日平均收益排名股票身份模型：7项独立均值排名与严格成熟未来投毒CPU检查通过；原生与独立解码器冻结，尚未训练或评分','缓存十日与二十日排序预测融合：49项连续五年官方评分，48全量Pandas与144因果前缀检查完成；完整提交资格另行核实')
 driver=A/'publish_Rank10Rank20_higher49_actual_official_main_v1_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
 assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
