from pathlib import Path
import sys,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
assert allowed()
closed("actual_rank120_rank60_after183_consensusFraction8_screen100_v1_20261011");closed("actual_rank120_rank60_after183_consensusFractionWeight8_screen108_v1_20261011");closed("actual_completed_weight85_full_pipeline90_v1_20261011")
base=Path("E:/赛题五_本机临时");folders=[base/"StockRank120Rank60_after183_consensusFraction8_screen100_v1_20261011",base/"StockRank120Rank60_after183_consensusFractionWeight8_screen108_v1_20261011"];reports=[read(f/"verification.json") for f in folders]
for f,p in zip(folders,reports):
 assert len(p["records"])==p["new_quality_score_records"]==8 and (p["actual_nonidentity_full_controls"],p["actual_nonidentity_prefix_controls"])==(7,21)
 for file,d in p["input_sha256"].items():assert sha(file)==d,file
 for r in p["records"]:
  cap=Path(r["official_score_cache"]["official_metrics_source"]);assert sha(cap)==r["official_metric_capsule_sha256"] and read(cap)["metrics"]==r["metrics"]
  assert sha(f/f"case{r['case']:03d}_controls.json")==r["control_sha256"]
choice=1 if reports[1]["best"]["connected_final_score"]>reports[0]["best"]["connected_final_score"] else 0
create(A/"actual_final_fraction100_vs_weight108_S_only_best_pipeline110_decision_v1_20261011.json",{"status":"actual_S_only_highest_of_completed_16_records_one_full_candidate_pipeline_only","choice":choice,"scores":[p["best"]["connected_final_score"] for p in reports],"input_sha256":{str(f/"verification.json"):sha(f/"verification.json") for f in folders},"test_labels_read":False})
runpy.run_path(str(A/(["run_fraction101_storage_safe_controller103_v1_20261011.py","run_fraction109_storage_safe_controller111_v1_20261011.py"][choice])),run_name="__main__")
