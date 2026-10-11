"""Extend actual monitor with the live150 queue and remove obsolete unprepared status."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def main():
    s=(A/'monitor_actual_chronological_optimization_progress_v46_20261009.py').read_text(encoding='utf8')
    s=s.replace("149:('PureRFFHuber128',128,1)}","149:('PureRFFHuber128',128,1),150:('HuberSparse59',59,1)}")
    s=s.replace('optimization_live_progress_v46_20261009','optimization_live_progress_v47_20261009')
    s=s.replace("'actual_official_scores':0,'actual_future_inference':0,\n        'complete_quality_receivers_not_yet_prepared':True,'duplicate_audit_still_required':True,", "'actual_official_scores':pipeline['150']['completed_cases'],'actual_future_inference':0,\n        'complete_quality_receivers_not_yet_prepared':False,'duplicate_audit_still_required':status('HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009')['status']!='passed',\n        'complete_prospective_controls':status('HuberSparse150_complete_prospective_controls_v1_20261009'),\n        'duplicate_audit':status('HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009'),\n        'chronological_dispatch':status('HuberSparse150_complete_chronological_dispatch_v1_20261009'),\n        'prospective_main_publication':status('HuberSparse150_prospective_main_publication_v1_20261009'),")
    before='59项正式评分接收流程与历史预测去重仍需准备。尚无该轮质量分或测试推理。'
    after="59项正式评分接收流程32代码/440图检查已通过；历史预测去重{state['huber_sparse150_frontier']['duplicate_audit']['status']}，连续派发{state['huber_sparse150_frontier']['chronological_dispatch']['status']}，实际质量评分见上表。"
    assert before in s;s=s.replace(before,after)
    save('monitor_actual_chronological_optimization_progress_v47_20261009.py',s)
if __name__=='__main__':main()
