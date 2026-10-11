from pathlib import Path
from datetime import datetime
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
base=Path('E:/赛题五_本机临时');canonical=A/'optimization_20261003_r95/scoring_validation_only'
families=[('StockRank120Rank60_after183_disagreement_CDF8_screen75_v1_20261011','actual_rank120_rank60_after183_disagreement_CDF8_screen75_v1_20261011','Rank120Rank60DisagreementCDF_after183_actual8_76_sources_main_receipt_v1_20261011.json','rank120_rank60_disagreement_CDF8_gain_decision76_v1_20261011.json',False),('StockRank120Rank60_after183_disagreement_CDFfine8_screen77_v1_20261011','actual_rank120_rank60_after183_disagreement_CDFfine8_screen77_v1_20261011','Rank120Rank60DisagreementCDFFine_after183_actual8_78_sources_main_receipt_v1_20261011.json','rank120_rank60_disagreement_CDFfine8_gain_decision78_v1_20261011.json',True),('StockRank120Rank60_after183_consensus8_screen80_v1_20261011','actual_rank120_rank60_after183_consensus8_screen80_v1_20261011','Rank120Rank60Consensus_after183_actual8_81_sources_main_receipt_v1_20261011.json','rank120_rank60_consensus8_gain_decision81_v1_20261011.json',True)]
records=[];pins={};preserved=[]
for name,service,receiptname,decisionname,removeXY in families:
 folder=base/name;assert folder.resolve().parent==base.resolve();work=A/'service_owned_workflows_20261006'/service
 assert not owned(read(work/'native_launch.json')) and read(work/'service_execution.json')['status']=='passed'
 receipt=A/receiptname;decision=A/decisionname
 assert read(receipt)['status']=='pushed_and_remote_head_verified' and read(receipt)['branch']=='main' and read(decision)['adopt'] is False
 proof=read(folder/'verification.json');assert len(proof['records'])==8 and proof['test_labels_read'] is False
 for filename in (['测试集_X.csv','测试集_Y.csv'] if removeXY else [])+['submission.csv']:
  p=folder/'scoring_validation_only'/filename;assert p.is_file() and not p.is_symlink() and p.resolve().parent==(folder/'scoring_validation_only').resolve()
  assert str(p) not in proof['input_sha256'];digest=sha(p)
  if filename!='submission.csv':source=canonical/filename;assert digest==sha(source);binding={'reconstructable_exact_source':str(source)}
  else:
   last=proof['records'][-1];cap=Path(last['official_score_cache']['official_metrics_source']);assert sha(cap)==last['official_metric_capsule_sha256'] and read(cap)['scope']['submission_csv_sha256']==digest
   binding={'last_case':last['case'],'actual_official_capsule':str(cap),'last_case_S':last['connected_final_score']};pins[str(cap)]=sha(cap)
  records.append({'path':str(p),'sha256':digest,'bytes':p.stat().st_size,**binding})
 for p in [receipt,decision,folder/'verification.json',*folder.glob('case*_official.json'),*folder.glob('case*_controls.json')]:preserved.append({'path':str(p),'sha256':sha(p)})
plan=A/'actual_completed_no_gain_scoring_copies82_cleanup_plan_v1_20261011.json';create(plan,{'status':'predeclared_user_authorized_completed_published_no_gain_scoring_cache_cleanup_only_all_scores_controls_models_preserved','at_local':datetime.now().isoformat(),'files':records,'preserved_records':preserved,'input_sha256':pins,'actual_test_dataset_not_touched':True})
for row in records:
 assert allowed();p=Path(row['path']);assert sha(p)==row['sha256'];p.unlink();assert not p.exists()
for row in preserved:assert sha(row['path'])==row['sha256']
result={'status':'passed_seven_completed_no_gain_scoring_copies_removed_all_official_records_and_models_preserved','at_local':datetime.now().isoformat(),'plan_sha256':sha(plan),'deleted_files':len(records),'released_bytes':sum(r['bytes'] for r in records),'actual_test_dataset_not_touched':True}
create(A/'actual_completed_no_gain_scoring_copies82_cleanup_verification_v1_20261011.json',result);print(result,flush=True)
