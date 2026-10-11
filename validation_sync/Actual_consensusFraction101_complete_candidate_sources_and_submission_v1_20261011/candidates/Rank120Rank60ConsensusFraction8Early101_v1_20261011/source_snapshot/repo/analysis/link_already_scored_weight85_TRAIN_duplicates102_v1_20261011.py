from pathlib import Path
from datetime import datetime
import os,sys,shutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
assert allowed()
release=A/'Rank120Rank60ConsensusWeight8Early85_selected_release_v1_20261011';official=release/'calibrated_csv_official.json';proof=read(official);decision=read(A/'rank120_rank60_consensusWeight8_gain_decision85_v1_20261011.json');assert proof['status']=='passed' and proof['metrics']==decision['best']['metrics']
base=Path('E:/赛题五_本机临时/60与120日一致性权重8项完整候选85_20261011/selected_scoring/scoring_validation_only');rows=[]
for name in ('测试集_X.csv','测试集_Y.csv'):
 p=base/name;source=A/'optimization_20261003_r95/scoring_validation_only'/name
 assert p.resolve().is_relative_to(base.resolve()) and p.is_file() and not p.is_symlink() and source.is_file()
 digest=sha(p);assert digest==sha(source);rows.append({'path':str(p),'preserved_canonical':str(source.resolve()),'sha256':digest,'bytes':p.stat().st_size})
create(A/'actual_scored_weight85_TRAIN_duplicate_links102_plan_v1_20261011.json',{'status':'frozen_after_actual_official_score_before_replacing_only_same_bytes_duplicate_XY_with_exact_canonical_links','files':rows,'official_sha256':sha(official),'candidate_source_and_inference_unchanged':True})
for r in rows:
 assert sha(r['path'])==sha(r['preserved_canonical'])==r['sha256'];p=Path(r['path']);link=p.with_name(p.name+'.same_bytes102_link');assert not link.exists();os.symlink(r['preserved_canonical'],link);assert sha(link)==r['sha256'];os.replace(link,p);assert p.is_symlink() and sha(p)==r['sha256']
assert sha(official)==read(A/'actual_scored_weight85_TRAIN_duplicate_links102_plan_v1_20261011.json')['official_sha256']
create(A/'actual_scored_weight85_TRAIN_duplicate_links102_verification_v1_20261011.json',{'status':'passed_only_already_scored_duplicate_TRAIN_XY_physical_copies_replaced_by_same_bytes_canonical_links_original_paths_preserved','at_local':datetime.now().isoformat(),'released_bytes':sum(r['bytes'] for r in rows),'free_E_bytes':shutil.disk_usage('E:/').free,'input_files_same_sha256':rows,'candidate_inference_not_interrupted':True})
