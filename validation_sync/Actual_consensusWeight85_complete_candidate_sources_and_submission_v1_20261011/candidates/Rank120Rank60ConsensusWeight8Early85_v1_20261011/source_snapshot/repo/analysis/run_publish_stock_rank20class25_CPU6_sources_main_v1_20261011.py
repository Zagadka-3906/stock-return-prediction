from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed()
 for n in ['actual_stock_rank20class25_balanced_BCE_CPU_v1_20261011','StockRank20Class25Embedding_actual_mature_fixture_CPU_v1_20261011','actual_stock_rank20class25_embedding_eleven_parent_callbacks_CPU_v1_20261011']:closed(n)
 template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py';paths=[Path(__file__),template,A/'actual_observer113_class25_sources_admission_v1_20261011.json',A/'stock_rank20class10_latest_qualified183_predeclared17_sources_v1_20261011.json',A/'run_publish_class10_after183_completed17_main_v1_20261011.py']
 for name in ['stock_rank20class25_BCE_own6_sources_admission_v1_20261011.json','stock_rank20class25_balanced_BCE_actual_CPU_controls_v1_20261011.json','stock_rank20class25_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json']:
  p=A/name;paths.append(p)
  for pp,d in read(p)['input_sha256'].items():
   assert sha(pp)==d,pp
   if Path(pp).suffix in ('.py','.json'):paths.append(Path(pp))
 text=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7','StockRank20Class25_actual_CPU6')
 start=text.index('    paths=');end=text.index('    import publish_classifier',start);text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
 start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start);manifest={'status':'actual_top25_mature20_BCE_independent_CPU6_gradient49153_and_callback11_passed_before_GPU','classification_fraction':.25,'positive_class_weight':3.,'own6_full5_official46_not_claimed_complete':True,'new_fits_by_publication':0,'new_scores_by_publication':0,'test_labels_read':False};text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
 p=A/'publish_frozen_StockRank20Class25_actual_CPU6_main_v1_20261011.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');assert allowed();runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
