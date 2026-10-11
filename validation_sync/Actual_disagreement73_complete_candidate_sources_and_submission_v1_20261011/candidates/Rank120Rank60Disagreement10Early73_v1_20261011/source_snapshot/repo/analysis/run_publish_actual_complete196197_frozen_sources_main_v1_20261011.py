from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
if __name__=='__main__':
 assert allowed();template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py';paths=[Path(__file__),template,A/'actual_observer114_complete196197_sources_admission_v1_20261011.json',A/'route_class10_latest183_complete196_exact_v3_20261011.py']
 for name in ['stock_rank20class10_latest183_complete196_exact_routes_v3_20261011.json','stock_rank20class25_embedding197_full_execution_sources_admission_v1_20261011.json','stock_rank20class25_complete197_pipeline_before_scores_sources_v1_20261011.json']:
  p=A/name;paths.append(p)
  for pp,d in read(p)['input_sha256'].items():
   assert sha(pp)==d,pp
   if Path(pp).suffix in ('.py','.json'):paths.append(Path(pp))
 text=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7','Actual_complete196197_frozen_routes')
 start=text.index('    paths=');end=text.index('    import publish_classifier',start);text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
 start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start);manifest={'status':'compiled_actual19619_and19748_before_official_scores_or_selected_future','round196':{'records':19,'anchors':[183,195],'QA':107,'board':17967,'wave':479},'round197':{'records':48,'anchors':[175,196],'QA':108,'board':18015,'wave':480},'full_inference_QA_and_main_not_claimed_complete':True,'new_fits_by_publication':0,'new_scores_by_publication':0,'test_labels_read':False};text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
 p=A/'publish_frozen_actual_complete196197_routes_main_v1_20261011.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');assert allowed();runpy.run_path(str(p),run_name='__main__')
