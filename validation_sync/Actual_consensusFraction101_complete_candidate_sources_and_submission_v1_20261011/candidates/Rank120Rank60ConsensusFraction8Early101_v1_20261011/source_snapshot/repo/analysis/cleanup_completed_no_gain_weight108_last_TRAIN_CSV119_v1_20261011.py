from pathlib import Path
import sys,shutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
assert allowed();closed('actual_rank120_rank60_after183_consensusFractionWeight8_screen108_v1_20261011');closed('actual_completed_consensusFractionWeight8_actual8_early114_main_v1_20261011')
base=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_consensusFractionWeight8_screen108_v1_20261011');report=base/'verification.json';proof=read(report);incumbent=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_consensusFraction8_screen100_v1_20261011/verification.json');older=read(incumbent)
assert len(proof['records'])==8 and proof['best']['connected_final_score']<older['best']['connected_final_score']
last=proof['records'][-1];p=base/'scoring_validation_only/submission.csv';cap=Path(last['official_score_cache']['official_metrics_source']);assert sha(cap)==last['official_metric_capsule_sha256'];digest=sha(p);assert digest==read(cap)['scope']['submission_csv_sha256'] and str(p) not in proof['input_sha256'] and not p.is_symlink()
retained=[report,incumbent,*base.glob('case*_official.json'),*base.glob('case*_controls.json')];pins={str(x):sha(x) for x in retained};size=p.stat().st_size
create(A/'actual_completed_no_gain_weight108_last_TRAIN_CSV119_cleanup_plan_v1_20261011.json',{'file':str(p),'sha256':digest,'bytes':size,'actual_no_gain_S_only_comparison':{'best108':proof['best']['connected_final_score'],'best100':older['best']['connected_final_score']},'retained_sha256':pins})
p.unlink()
for file,d in pins.items():assert sha(file)==d,file
create(A/'actual_completed_no_gain_weight108_last_TRAIN_CSV119_cleanup_verification_v1_20261011.json',{'status':'passed_completed_main_published_no_gain_family_last_TRAIN_csv_only_removed_all_score_control_and_model_records_preserved','released_bytes':size,'free_E_bytes':shutil.disk_usage('E:/').free,'retained_sha256':pins})
