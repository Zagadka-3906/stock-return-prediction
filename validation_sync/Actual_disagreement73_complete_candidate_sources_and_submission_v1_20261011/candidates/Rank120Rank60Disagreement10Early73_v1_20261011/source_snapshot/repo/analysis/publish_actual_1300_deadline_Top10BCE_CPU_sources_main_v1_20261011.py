from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
 assert allowed();closed('actual_stock_rank20class10_balanced_BCE_CPU_v1_20261011');closed('StockRank20Class10Embedding_actual_mature_fixture_CPU_v1_20261011');closed('actual_stock_rank20class10_embedding_eleven_parent_callbacks_CPU_v1_20261011')
 template=A/'publish_Rank10_actual_maturity7_sources_main_v1_20261011.py';paths=[Path(__file__),template,ROOT/'AGENTS.md',A/'activate_user_requested_stop1300_v1_20261011.py',A/'user_requested_stop1300_v1_20261011.py',A/'user_requested_stop1300_until_manual_continue_v1_20261011/deadline_extension_verification.json',A/'user_requested_stop1300_until_manual_continue_v1_20261011/actual_schedule_activation.json',A/'user_requested_stop1300_until_manual_continue_v1_20261011/actual_1100_guard_retirement.json',A/'user_requested_stop1300_until_manual_continue_v1_20261011/schedule.json',A/'actual_observer110_deadline13_and_classification_sources_admission_v1_20261011.json']
 for pattern in ('*stock_rank20class10*20261011.py','*stock_rank20class10*20261011.json','*rank20class10*20261011.py','*rank20class10*20261011.json'):paths.extend(A.glob(pattern))
 for pp in [A/'stock_rank20class10_BCE_own6_sources_admission_v1_20261011.json',A/'stock_rank20class10_balanced_BCE_actual_CPU_controls_v1_20261011.json',A/'stock_rank20class10_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261011.json']:
  for name,d in read(pp)['input_sha256'].items():
   assert sha(name)==d,name
   if Path(name).suffix in ('.py','.json'):paths.append(Path(name))
 text=template.read_text(encoding='utf8').replace('Rank10_actual_maturity7','Actual_1300_deadline_Top10BCE_CPU_sources')
 start=text.index('    paths=');end=text.index('    import publish_classifier',start);text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']]\n'+text[end:]
 start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
 manifest={'status':'actual13_deadline_and_Top10_mature20_binary_BCE_CPU6_fixture49153_callback11_passed_before_complete_own6_or_scores','deadline':'2026-10-11T13:00:00+08:00','old11_guard_exact_identity_retired':True,'actual_binary_loss_and_gradient_cases':6,'actual_mature_fixture_rows':49153,'actual_callback_checks':11,'own6_full5_official46_and_full195_not_completed':True,'new_fits_by_publication':0,'new_scores_by_publication':0,'test_labels_read':False}
 text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
 driver=A/'publish_Actual_1300_deadline_Top10BCE_CPU_sources_main_v1_20261011.py';assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n');assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
