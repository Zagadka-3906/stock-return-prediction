from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed();template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py';paths=[Path(__file__),template,A/'owned_idle_publication_wait_reboot_identity_v2_20261011.py',A/'publish_explicit_parent_training_round_external_frozen_v3_20261011.py',A/'actual_external_frozen_publication183184_capsule_controls_v3_20261011.json']
 for name in ['completed_score_parent_chain_recovery31_routes_v1_20261011.json','new_objectives_exact_source_recovery34_routes_v1_20261011.json','stock_rank20class10_complete195_actual_parent34_pipeline_sources_v1_20261011.json']:
  p=A/name;d=read(p);paths.append(p)
  for pp,digest in d['input_sha256'].items():
   assert sha(pp)==digest,pp
   if Path(pp).suffix in ('.py','.json'):paths.append(Path(pp))
 for pattern in ('*resume29*py','*bridge30*py','*bridge30*json','*recovery31*py','*recovery34*py','*observer112*json','*monitor*v112*py'):
  paths.extend(A.glob(pattern))
 text=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7','Actual_parent3134_frozen_runtime')
 start=text.index('    paths=');end=text.index('    import publish_classifier',start);text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
 start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
 manifest={'status':'actual_frozen_runtime_recovery3134_and_133_existing_score_capsules_verified','new_fits':0,'new_scores':0,'actual_183184_frozen_score_capsules_verified':133,'completed_future_or_QA_or_main_not_claimed_by_sources_publication':True,'live_science_preserved':True,'deadline':'2026-10-11T13:00:00+08:00','test_labels_read':False}
 text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
 p=A/'publish_frozen_actual_parent3134_runtime_sources_main_v1_20261011.py';assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');assert allowed();runpy.run_path(str(p),run_name='__main__')
if __name__=='__main__':main()
