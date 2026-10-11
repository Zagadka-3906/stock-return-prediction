from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('actual_rank120_rank60_after183_consensus8_screen80_v1_20261011')
 folder=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_consensus8_screen80_v1_20261011');proof=read(folder/'verification.json');assert len(proof['records'])==8 and proof['actual_nonidentity_full_controls']==7 and proof['actual_nonidentity_prefix_controls']==21
 template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py';paths=[Path(__file__),template,folder/'verification.json',folder/'frozen_before_any_new_controls_or_scores.json',A/'rank120_rank60_consensus8_predeclared_sources80_v1_20261011.json']
 for p,d in proof['input_sha256'].items():
  assert sha(p)==d,p
  if Path(p).suffix in ('.py','.json'):paths.append(Path(p))
 for r in proof['records']:
  p=Path(r['official_score_cache']['official_metrics_source']);assert sha(p)==r['official_metric_capsule_sha256'] and read(p)['metrics']==r['metrics'];paths.extend([p,folder/f"case{r['case']:03d}_official.json",folder/f"case{r['case']:03d}_controls.json"])
 text=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7','Rank120Rank60Consensus_after183_actual8_81')
 start=text.index('    paths=');end=text.index('    import publish_classifier',start);text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
 start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
 manifest={'status':'actual8_disagreement_CDF_continuous_TRAIN_official_scores_completed_after_qualified183','parent_round':183,'actual_nonidentity_full_Pandas_controls':7,'actual_prefix_controls':21,'best_S':proof['best']['connected_final_score'],'submission_qualification_pending':True,'new_fits_by_publication':0,'new_scores_by_publication':0,'test_labels_read':False}
 text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
 p=A/'publish_frozen_Rank120Rank60Consensus_after183_actual8_81_main_v1_20261011.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');assert allowed();runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
