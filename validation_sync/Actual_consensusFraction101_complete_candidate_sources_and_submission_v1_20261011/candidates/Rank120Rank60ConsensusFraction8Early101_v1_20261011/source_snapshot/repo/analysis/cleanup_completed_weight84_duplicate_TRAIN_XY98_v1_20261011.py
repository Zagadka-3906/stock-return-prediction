from pathlib import Path
from datetime import datetime
import sys,shutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
assert allowed();closed('actual_completed_weight84_namespace_bridge90_v1_20261011');closed('actual_completed_weight84_actual8_early96_main_v1_20261011')
base=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_consensusWeight8_screen84_v1_20261011');report=base/'verification.json';proof=read(report)
assert len(proof['records'])==8 and proof['test_labels_read'] is False
receipt=A/'Rank120Rank60ConsensusWeight_after183_actual8_96_sources_main_receipt_v1_20261011.json';assert read(receipt)['status']=='pushed_and_remote_head_verified'
retained=[report,receipt,*base.glob('case*_official.json'),*base.glob('case*_controls.json')];retained_sha={str(p):sha(p) for p in retained};plan=[]
for name in ('测试集_X.csv','测试集_Y.csv'):
 p=base/'scoring_validation_only'/name;canonical=A/'optimization_20261003_r95/scoring_validation_only'/name
 assert p.resolve().is_relative_to(base.resolve()) and not p.is_symlink() and str(p) not in proof['input_sha256']
 digest=sha(p);assert digest==sha(canonical);plan.append({'path':str(p),'canonical_preserved':str(canonical),'sha256':digest,'bytes':p.stat().st_size,'TRAIN_scoring_alias_not_actual_test_labels':True})
create(A/'actual_completed_weight84_duplicate_TRAIN_XY98_cleanup_plan_v1_20261011.json',{'files':plan,'retained_sha256':retained_sha,'actual8_all_scores_main_receipt':read(receipt),'at_local':datetime.now().isoformat()})
for row in plan:
 assert sha(row['path'])==sha(row['canonical_preserved'])==row['sha256'];Path(row['path']).unlink()
for p,d in retained_sha.items():assert sha(p)==d,p
create(A/'actual_completed_weight84_duplicate_TRAIN_XY98_cleanup_verification_v1_20261011.json',{'status':'passed_only_two_completed_published_duplicate_TRAIN_scoring_copies_removed_all_score_records_models_and_candidate_files_preserved','released_bytes':sum(r['bytes'] for r in plan),'remaining_E_free_bytes':shutil.disk_usage('E:/').free,'retained_sha256':retained_sha,'at_local':datetime.now().isoformat()})
