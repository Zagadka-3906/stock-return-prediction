from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py'
 phases=[('restart_CPU',['actual_stock_rank120_embedding_small512_restart_v1_20261011','StockRank120EmbeddingSmall512_independent_small_CPU_v1_20261011']),('own6_full5',['StockRank120EmbeddingSmall512_independent_full5_GPU_controls_v1_20261011']),('native42',['actual_stock_rank120_embedding_six_state_native42_v1_20261011'])]
 for stage,deps in phases:
  for name in deps:closed(name)
  assert allowed();paths=[Path(__file__),template,ROOT/'后续选模标准.md',A/'stock_identity_embedding_network_v1_20261010.py']
  for pattern in ('*stock_rank120*20261011.py','*stock_rank120*20261011.json','*rank120*20261011.py','*rank120*20261011.json'):paths.extend(A.glob(pattern))
  for base in [A/'service_owned_workflows_20261006',Path('E:/赛题五_本机临时'),Path('E:/赛题五_本机临时/GPU实测_20261009')]:
   for folder in base.iterdir():
    if folder.is_dir() and ('stock_rank120' in folder.name.lower() or 'stockrank120' in folder.name.lower()):paths.extend(p for p in folder.rglob('*.json') if 'tmp' not in p.relative_to(folder).parts and p.stat().st_size<20*1024**2)
  paths=[p for p in dict.fromkeys(paths) if p.name not in ('actual_stage.json','state.json','best_so_far.json','checkpoint_manifest.json','progress.json')]
  # Freeze completed score capsules separately from large raw prediction files.
  text=template.read_text(encoding='utf8');start=text.index('    paths=');end=text.index('    import publish_classifier',start)
  text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
  text=text.replace('Rank10_actual_maturity7',f'StockRank120_objective_{stage}')
  text=text.replace(repr(str(template)).replace('Rank10_actual_maturity7',f'StockRank120_objective_{stage}'),repr(str(template)))
  start=text.index('    paths=');end=text.index('    import publish_classifier',start)
  text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
  start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
  manifest={'status':'actual_completed_mature120_Huber_stage_only','stage':stage,'new_scores_by_publication':0,'submission_qualification_pending':True,'actual_future_X_read':False,'test_labels_read':False,'actual_mean120_maturity_CPU7_boundary12_and_fixture49153_passed':True,'official33_scores_published_by_separate_completed_stage':True}
  text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
  text=text.replace('新十日平均收益排名股票身份模型：7项独立均值排名与严格成熟未来投毒CPU检查通过；原生与独立解码器冻结，尚未训练或评分','一百二十日成熟平均收益排名股票身份模型：保存实际完成阶段 '+stage+'；完整提交资格单独核实')
  driver=A/f'publish_frozen_StockRank120_objective_{stage}_main_v1_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
  assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
