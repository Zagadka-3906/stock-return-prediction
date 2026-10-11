"""Remove only twelve unused completed-fit resume caches; preserve all weights and score records."""
from pathlib import Path
from datetime import datetime
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
 assert allowed()
 control=[A/f'current_user_runtime_control_202610{d}.json' for d in ('09','10')]
 for p in control:assert read(p)['stop_at_local']=='2026-10-11T13:00:00+08:00'
 receipt=A/'Actual_completed224_recovery65_observer145_sources_retry3_main_receipt_v1_20261011.json'
 assert read(receipt)['status']=='pushed_and_remote_head_verified' and read(receipt)['branch']=='main'
 roots=[Path(f'E:/赛题五_本机临时/stock_rank{h}medium_embedding_medium2048_BF16_bank6_v1_20261011') for h in (60,120)]
 records=[];kept=[];pins={str(p):sha(p) for p in [Path(__file__),receipt,*control]}
 for h,root in zip((60,120),roots):
  assert root.resolve().parent==Path('E:/赛题五_本机临时').resolve()
  decision=A/f'rank{h}medium2048_best33_gain_decision_v1_20261011.json'
  assert read(decision)['adopt'] is False;pins[str(decision)]=sha(decision)
  proof=root/'verification.json';assert read(proof)['actual_native_fits']==6;pins[str(proof)]=sha(proof)
  for year in range(2020,2026):
   model=root/str(year)/'model.joblib';info=root/str(year)/'info.json';checkpoint=root/str(year)/'checkpoint.joblib'
   assert read(info)['status']=='passed_actual_complete_mature_BF16_micro_annual_model' and sha(model)==read(info)['model_sha256']
   assert checkpoint.is_file() and not checkpoint.is_symlink() and checkpoint.resolve().parent==(root/str(year)).resolve()
   kept += [{'path':str(p),'sha256':sha(p)} for p in (model,info)]
   records.append({'path':str(checkpoint),'sha256':sha(checkpoint),'bytes':checkpoint.stat().st_size})
 plan=A/'actual_unused_medium_completed_checkpoints73_cleanup_plan_v1_20261011.json'
 create(plan,{'status':'predeclared_user_authorized_unused_resume_cache_cleanup_only','at_local':datetime.now().isoformat(),'input_sha256':pins,'delete_only':records,'preserve_weights_and_information':kept,'planned_bytes':sum(r['bytes'] for r in records)})
 for row in records:
  assert allowed();path=Path(row['path']);assert sha(path)==row['sha256'];path.unlink();assert not path.exists()
 for row in kept:assert sha(row['path'])==row['sha256']
 result={'status':'passed_actual_unused_completed_fit_checkpoints_removed_all_final_weights_info_scores_preserved','at_local':datetime.now().isoformat(),'plan_sha256':sha(plan),'deleted_files':len(records),'released_bytes':sum(r['bytes'] for r in records),'all_preserved_weights_and_info_rehashed':True}
 create(A/'actual_unused_medium_completed_checkpoints73_cleanup_verification_v1_20261011.json',result);print(result,flush=True)
if __name__=='__main__':main()
