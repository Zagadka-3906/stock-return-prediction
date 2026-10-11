from pathlib import Path
import sys,os,shutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
assert allowed();closed('actual_completed_weight84_actual8_early96_main_v1_20261011')
base=Path('E:/赛题五_本机临时');old=base/'StockRank120Rank60_after183_consensusFraction8_screen88_v1_20261011';service=A/'service_owned_workflows_20261006/actual_rank120_rank60_after183_consensusFraction8_screen88_v1_20261011';assert read(service/'service_execution.json')['status']=='failed' and not owned(read(service/'native_launch.json'))
p=old/'scoring_validation_only/submission.csv';canonical=base/'StockRank120Rank60_after183_disagreement10_screen_v1_20261011/scoring_validation_only/submission.csv';digest=sha(p);assert digest==sha(canonical) and not p.is_symlink()
weight=base/'StockRank120Rank60_after183_consensusWeight8_screen84_v1_20261011';report=read(weight/'verification.json');last=report['records'][-1];assert last!=report['best'] and last['connected_final_score']<report['best']['connected_final_score'];q=weight/'scoring_validation_only/submission.csv';cap=Path(last['official_score_cache']['official_metrics_source']);assert sha(cap)==last['official_metric_capsule_sha256'];qd=sha(q);assert qd==read(cap)['scope']['submission_csv_sha256'] and str(q) not in report['input_sha256']
retained=[service/'service_execution.json',weight/'verification.json',old/'case001_official.json',*weight.glob('case*_official.json'),*weight.glob('case*_controls.json')];pins={str(x):sha(x) for x in retained};size=p.stat().st_size+q.stat().st_size
create(A/'actual_partial88_and_unused_weight84_TRAIN_CSV105_cleanup_plan_v1_20261011.json',{'same_bytes_link':{'path':str(p),'preserved_source':str(canonical),'sha256':digest},'unused_last_case_CSV_remove':{'path':str(q),'sha256':qd,'last_case':last['case'],'selected_case':report['best']['case']},'retained_sha256':pins})
link=p.with_name(p.name+'.same_bytes105_link');assert not link.exists();os.symlink(canonical.resolve(),link);assert sha(link)==digest;os.replace(link,p);assert sha(p)==sha(canonical)==digest;q.unlink()
for path,d in pins.items():assert sha(path)==d,path
create(A/'actual_partial88_and_unused_weight84_TRAIN_CSV105_cleanup_verification_v1_20261011.json',{'status':'passed_same_bytes_duplicate_partial_reference_CSV_linked_and_completed_published_nonselected_last_case_CSV_only_removed_all_actual_scores_preserved','released_bytes':size,'remaining_E_free_bytes':shutil.disk_usage('E:/').free,'retained_sha256':pins,'actual_TEST_candidate_files_untouched':True})
