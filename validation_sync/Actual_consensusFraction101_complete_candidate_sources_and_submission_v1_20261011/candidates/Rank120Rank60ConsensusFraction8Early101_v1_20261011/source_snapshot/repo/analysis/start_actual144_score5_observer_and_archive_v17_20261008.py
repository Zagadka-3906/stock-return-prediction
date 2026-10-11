"""Observe actual score5/candidate5/registration6 and archive only their completed scratch CSVs."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
def main():
    source=A/'monitor_actual_optimization135_to144_v16_20261008.py';text=source.read_text(encoding='utf8')
    text=text.replace('ConeRidgeAlpha144_complete_hidden_launches_v4_20261008.json','ConeRidgeAlpha144_fresh_scoring_paths_hidden_launches_v5_20261008.json')
    text=text.replace("folder=A/'ConeRidgeAlpha100_official_comparison_v1_20261008'", "folder=A/'ConeRidgeAlpha100_official_comparison_v5_20261008'")
    text=text.replace('observer_version=16','observer_version=17').replace('progress_v16_','progress_v17_')
    text=text.replace("'source_version':3,'registration_version':4", "'source_version':4,'scoring_version':5,'registration_version':6")
    text=text.replace('seven_actual_receivers_dispatched','five_corrected_actual_receivers_dispatched')
    text=text.replace('实际六个科学接收器来源3及独立登记4已启动。','实际评分5、评分同步5、冻结推理5、封装5和独立登记6已启动；完整图来源4。')
    target=A/'monitor_actual_optimization135_to144_v17_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    source=A/'archive_ConeRidgeAlpha144_completed_scoring_CSV_v1_20261008.py';text=source.read_text(encoding='utf8')
    for before,after in (
        ('ConeRidgeAlpha100_official_comparison_v1_20261008','ConeRidgeAlpha100_official_comparison_v5_20261008'),
        ('ConeRidgeAlpha100_selected_candidate_preparation_v1_20261008','ConeRidgeAlpha100_selected_candidate_preparation_v5_20261008'),
        ('ConeRidgeAlpha144_D_scoring_v1_20261008','ConeRidgeAlpha144_D_scoring_v5_20261008'),
        ('scoring_CSV_archive_v1_20261008','scoring_CSV_archive_v5_20261008'),
        ("archive=base/'completed_scoring_CSV'","archive=base/'completed_scoring_CSV_v5'")):
        text=text.replace(before,after)
    archive=A/'archive_ConeRidgeAlpha144_completed_scoring_CSV_v5_20261008.py';assert not archive.exists();compile(text,str(archive),'exec');archive.write_text(text,encoding='utf8',newline='\n')
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    launches={}
    for name,path in [('actual_optimization135_to144_live_progress_v17_20261008',target),
                      ('ConeRidgeAlpha144_completed_scoring_CSV_archivist_v5_20261008',archive)]:
        launches[name]=start(name,path.name,[],{str(path):sha(path)})
    create(A/'actual144_score5_observer_archive_hidden_launches_v17_20261008.json',{
        'status':'started_actual_score5_progress_and_closed_only_D5_to_E5_CSV_archive',
        'launches':launches,'new_quality_scores':0,'all_failed_paths_and_old_archivers_preserved':True})
    print('Actual score5 observer17 and closed-only D5 scratch archival on E started.',flush=True)
if __name__=='__main__':main()
