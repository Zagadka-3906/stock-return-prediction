from pathlib import Path
import sys,shutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
assert allowed();closed('actual_rank120_rank60_after183_consensusFraction8_screen100_v1_20261011');closed('actual_completed_consensusFraction8_actual8_early114_main_v1_20261011')
base=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_consensusFraction8_screen100_v1_20261011');report=base/'verification.json';proof=read(report);assert len(proof['records'])==8;last=proof['records'][-1];assert last!=proof['best'] and last['connected_final_score']<proof['best']['connected_final_score']
p=base/'scoring_validation_only/submission.csv';cap=Path(last['official_score_cache']['official_metrics_source']);assert sha(cap)==last['official_metric_capsule_sha256'];digest=sha(p);assert digest==read(cap)['scope']['submission_csv_sha256'] and str(p) not in proof['input_sha256'] and not p.is_symlink()
preserved=[report,*base.glob('case*_official.json'),*base.glob('case*_controls.json')];pins={str(x):sha(x) for x in preserved};size=p.stat().st_size
create(A/'actual_completed_nonselected_fraction100_last_TRAIN_CSV118_cleanup_plan_v1_20261011.json',{'file':str(p),'sha256':digest,'bytes':size,'last_case':last['case'],'selected_case':proof['best']['case'],'retained_sha256':pins,'candidate101_inputs_and_model_weights_preserved':True})
p.unlink()
for file,d in pins.items():assert sha(file)==d,file
create(A/'actual_completed_nonselected_fraction100_last_TRAIN_CSV118_cleanup_verification_v1_20261011.json',{'status':'passed_only_completed_main_published_nonselected_last_case_TRAIN_submission_copy_removed_all_scores_controls_models_and_future_candidate_inputs_preserved','released_bytes':size,'free_E_bytes':shutil.disk_usage('E:/').free,'retained_sha256':pins})
