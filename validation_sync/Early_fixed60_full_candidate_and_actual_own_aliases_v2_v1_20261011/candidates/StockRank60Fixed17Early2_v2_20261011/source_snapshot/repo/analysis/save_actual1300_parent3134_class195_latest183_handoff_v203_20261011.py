from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed();c=read(A/'current_user_runtime_control_20261010.json');read(A/'current_user_runtime_control_20261009.json');snapshot=read(A/'actual_optimization_fast_runtime_handoff_v200_20261011.json')
 names=['actual184_registered_QA_main_resume29_v1_20261011','actual184_registered_QA_main_complete_parent_bridge30_v1_20261011','actual_fast_optimization_progress_reboot_v112_20261011','actual_parent3134_frozen_publication_runtime_sources_main_v1_20261011','actual_stock_rank20class10_complete195_factory_v1_20261011','actual_stock_rank20class10_objective_stages_main_v1_20261011','actual_stock_rank20class10_objective_stages_main_v2_20261011','actual_stock_rank20class10_embedding_after183_exact_latest_anchor17_v1_20261011','actual_class10_after183_completed17_main_v1_20261011']
 for filename,key in [('completed_score_parent_chain_recovery31_routes_v1_20261011.json','remaining_tasks'),('new_objectives_exact_source_recovery34_routes_v1_20261011.json','remaining_tasks')]:
  d=read(A/filename);names.extend(d['service_aliases'].get(n,n) for n,_ in d[key])
 services={}
 for n in names:
  f=A/'service_owned_workflows_20261006'/n;t=read(f/'service_execution.json') if (f/'service_execution.json').exists() else None;r=read(f/'native_launch.json') if (f/'native_launch.json').exists() else None
  services[n]={'status':t['status'] if t else 'running_exact_owned' if r and owned(r) else 'not_started_or_not_owned','terminal':t,'identity':r}
 bank=Path('E:/赛题五_本机临时/stock_rank20class10_embedding_small512_BF16_bank6_v1_20261011');years=[y for y in range(2020,2026) if (p:=bank/str(y)/'info.json').exists() and read(p)['status']=='passed_actual_complete_mature_BF16_micro_annual_model']
 notes=['User explicit deadline13:00 today; goal remains active until actual cutoff, then pause per request. Do not restart old11 guardian.',
 'Current recovery chain31 uses actual184 resume29 and bridge30. New objectives use34; old24/25 failed,32/33 idle waiters retired only with exact stack and PID creation verification.',
 '34 full-registration imports actual watcher12 hold helper2 and strict frozen external publisher3. 34 sealers use actual34 preparation identity instead of failed canonical process.',
 'Current observer112 writes current Markdown and handoff200 (filename still200). Historical observer110/111 were retired; preserve frozen originals.',
 'Class10 BCE own6 is genuinely fresh training, pos_weight9, mature20 top10. Full195 factory passed source generation, future and full48/native14/QA106/main remain pending.',
 'Class10 publication actual phases v1; v2 is explicit metadata-only bridge verifying all3 actual v1 receipts. The195 receipt alias waits v2.',
 'Queued new17 against latest qualified183 after actual class46, independent Pandas16 and48 prefixes, publication queued. If it improves, build complete qualification/registry196 with correct19 records/anchors183195/Q10717967/W479; do not count score-only as delivery.',
 '184 full ranking actually observed active write_text and JSON decoding; do not restart it while live. Cached149 highest S .4514130257498636 pending189 qualification; fully qualified delivery183 S .4514109137146971.',
 'Automatic browser deletion review previously rejected; do not bypass via another tool. Models/data/tmp E; D sources. Root Git index must remain original SHA.']
 index=sha(ROOT/'.git/index');assert index=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
 create(A/'actual_user1300_parent3134_class195_latest183_handoff_v203_20261011.json',{'at_local':datetime.now(timezone(timedelta(hours=8))).isoformat(),'stop_at_local':c['stop_at_local'],'notes':notes,'actual_services':services,'actual_class10_completed_annual_years':years,'snapshot_observer':snapshot,'root_git_index_sha256':index,'D_free_bytes':psutil.disk_usage('D:/').free,'E_free_bytes':psutil.disk_usage('E:/').free,'goal_exhaustion_proven':False,'full_objective_complete':False})
 print({'actual_current_handoff203_saved':True,'class_completed_years':years,'actual_services':{n:r['status'] for n,r in services.items()}},flush=True)
if __name__=='__main__':main()
