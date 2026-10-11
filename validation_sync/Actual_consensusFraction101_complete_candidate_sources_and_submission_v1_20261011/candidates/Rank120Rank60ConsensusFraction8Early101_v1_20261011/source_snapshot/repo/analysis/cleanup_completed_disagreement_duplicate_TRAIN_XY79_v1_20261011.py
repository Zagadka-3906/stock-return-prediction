"""Delete only re-creatable identical TRAIN scoring copies after actual main publication."""
from pathlib import Path
from datetime import datetime
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
base=Path('E:/赛题五_本机临时');canonical=A/'optimization_20261003_r95/scoring_validation_only'
items=[('StockRank120Rank60_after183_disagreement10_screen_v1_20261011','actual_rank120_rank60_after183_disagreement10_screen_v1_20261011','Rank120Rank60Disagreement_after183_actual10_sources_main_receipt_v1_20261011.json'),('StockRank120Rank60_after183_disagreement_CDF8_screen75_v1_20261011','actual_rank120_rank60_after183_disagreement_CDF8_screen75_v1_20261011','Rank120Rank60DisagreementCDF_after183_actual8_76_sources_main_receipt_v1_20261011.json')]
records=[];preserved=[]
for name,service,receiptname in items:
 folder=base/name;assert folder.resolve().parent==base.resolve()
 work=A/'service_owned_workflows_20261006'/service;assert not owned(read(work/'native_launch.json'))
 receipt=A/receiptname;assert read(receipt)['status']=='pushed_and_remote_head_verified' and read(receipt)['branch']=='main'
 proof=read(folder/'verification.json');assert len(proof['records']) in (8,10) and proof['test_labels_read'] is False
 for filename in ('测试集_X.csv','测试集_Y.csv'):
  path=folder/'scoring_validation_only'/filename;source=canonical/filename
  assert path.resolve().parent==(folder/'scoring_validation_only').resolve() and path.is_file() and not path.is_symlink()
  assert str(path) not in proof['input_sha256']
  digest=sha(path);assert digest==sha(source)
  records.append({'path':str(path),'sha256':digest,'bytes':path.stat().st_size,'exact_reconstruction_source':str(source)})
 preserved += [{'path':str(p),'sha256':sha(p)} for p in [folder/'verification.json',receipt,*folder.glob('case*_official.json'),*folder.glob('case*_controls.json')]]
plan=A/'actual_completed_disagreement_duplicate_TRAIN_XY79_cleanup_plan_v1_20261011.json';create(plan,{'status':'predeclared_user_authorized_local_historical_duplicate_scoring_copies_cleanup_only_actual_scores_and_weight_files_preserved','at_local':datetime.now().isoformat(),'files':records,'preserved_records':preserved,'actual_test_dataset_not_touched':True})
for row in records:
 assert allowed();path=Path(row['path']);assert sha(path)==sha(row['exact_reconstruction_source'])==row['sha256'];path.unlink();assert not path.exists()
for row in preserved:assert sha(row['path'])==row['sha256']
result={'status':'passed_four_completed_published_TRAIN_scoring_XY_duplicates_removed_canonical_sources_all_scores_controls_and_models_preserved','at_local':datetime.now().isoformat(),'plan_sha256':sha(plan),'deleted_files':len(records),'released_bytes':sum(r['bytes'] for r in records),'actual_test_dataset_not_touched':True}
create(A/'actual_completed_disagreement_duplicate_TRAIN_XY79_cleanup_verification_v1_20261011.json',result);print(result,flush=True)
