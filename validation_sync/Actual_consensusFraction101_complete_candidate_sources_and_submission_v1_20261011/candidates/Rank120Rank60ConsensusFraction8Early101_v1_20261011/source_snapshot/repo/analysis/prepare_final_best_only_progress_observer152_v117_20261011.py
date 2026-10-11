from pathlib import Path
import sys,ast,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed();source=A/'monitor_verified_current_optimization_v151_20261011.py';s=source.read_text(encoding='utf8')
names=['actual_rank120_rank60_after183_consensusFraction8_screen100_v1_20261011','actual_rank120_rank60_after183_consensusFractionWeight8_screen108_v1_20261011','actual_final_fraction100_or108_best_only_full_pipeline110_v1_20261011','actual_completed_consensusFraction8_actual8_early114_main_v1_20261011','actual_completed_consensusFractionWeight8_actual8_early114_main_v1_20261011','actual_fraction100_weight108_best_only110_CPU_cleanup_sources116_main_v1_20261011']
for kind,no in [('consensusFraction8',101),('consensusFractionWeight8',109)]:
 names.extend([f'actual_rank120_rank60_{kind}_early{no}_normalization_v1_20261011',f'actual_rank120_rank60_{kind}_early{no}_selected_native14_v1_20261011'])
title={'consensusFraction8':'ConsensusFraction8','consensusFractionWeight8':'ConsensusFractionWeight8'}
for kind,no in [('consensusFraction8',101),('consensusFractionWeight8',109)]:names.extend([f'Rank120Rank60{title[kind]}Early{no}_selected_candidate_preparation_v1_20261011',f'Rank120Rank60{title[kind]}Early{no}_selected_candidate_sealing_v1_20261011'])
assert s.count(' while True:\n')==1;s=s.replace(' while True:\n',' names += '+repr(names)+'\n while True:\n')
needle="  state['pending_cached_highest_S']=max([.4514130257498636,*score_values(science)])";assert s.count(needle)==1;s=s.replace(needle,"""  for tag,folder in [('actual_complete_fraction100','StockRank120Rank60_after183_consensusFraction8_screen100_v1_20261011'),('final_weight108','StockRank120Rank60_after183_consensusFractionWeight8_screen108_v1_20261011')]:
   d=Path('E:/赛题五_本机临时')/folder;rs=[read(p) for p in d.glob('case*_official.json')];science[tag]={'completed':len(rs),'expected':8,'best_S':max((r['connected_final_score'] for r in rs),default=None),'actual_full_scoring_complete':(d/'verification.json').exists(),'candidate_qualification_separate':True}
  chooser=A/'actual_final_fraction100_vs_weight108_S_only_best_pipeline110_decision_v1_20261011.json';state['final_only_highest_candidate_dispatch']=read(chooser) if chooser.exists() else {'status':'waiting_completed_final8_and_current_weight85_full_delivery'}
"""+needle)
for old,new in [('progress_v151','progress_v152'),('handoff_v312','handoff_v313'),("+'.151.tmp'","+'.152.tmp'")]:s=s.replace(old,new)
s=s.replace("lines.append(f'当前实际失败：{n}；{row[\"terminal\"][\"failure\"]}')","lines.append(f'保留的实际失败记录：{n}；{row[\"terminal\"][\"failure\"]}。当前最终派发以最高分候选决策为准。')")
p=A/'monitor_verified_current_optimization_v152_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8');name='actual_fast_optimization_progress_reboot_v152_20261011';r=start_service(name,p.name,[],{str(p):sha(p)});create(A/(name+'_activation.json'),r)
for _ in range(30):
 if (A/'optimization_live_progress_v152_20261011.json').exists():break
 time.sleep(.2)
assert (A/'optimization_live_progress_v152_20261011.json').exists();identity=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v151_20261011/native_launch.json')
if owned(identity):
 import handoff_joint_goss_round97_full_execution_20261006 as h
 parent,worker=h.pair(identity);before=h.stack(worker.pid);assert '(idle)' in before and 'main (monitor_verified_current_optimization_v151_20261011.py:' in before and not worker.children(),before
 worker.suspend();parent.suspend();after=h.stack(worker.pid)
 if not ('(idle)' in after and 'main (monitor_verified_current_optimization_v151_20261011.py:' in after and not worker.children()):parent.resume();worker.resume();raise AssertionError(after)
 create(A/'actual_observer151_idle_retired_after152_final_best_only_snapshot_v1_20261011.json',{'status':'actual_idle_observer_only_replaced_scientific_workers_preserved','identity':identity,'before':before,'after':after,'snapshot_sha256':sha(A/'optimization_live_progress_v152_20261011.json')});worker.terminate();parent.terminate()
