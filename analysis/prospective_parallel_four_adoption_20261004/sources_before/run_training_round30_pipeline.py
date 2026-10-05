"""Run the complete-output augmentation search after all parents are published."""
from pathlib import Path
import json
import sys
import time
import traceback
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
STATE=ROOT/'analysis/ongoing_optimization_r30_state.json'


def state(stage,status='running',extra=None):
    payload={'round':30,'stage':stage,'status':status,'updated_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
             'continuous_optimization_authorized':True,'test_labels_read':False,**(extra or {})}
    STATE.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(payload,ensure_ascii=False),flush=True)


def main():
    state('waiting_for_previous_round_and_linear_bank')
    gates=[ROOT/'results/optimization_20261003_r29.json',ROOT/'analysis/optimization_20261003_r29/linear_role_causal_checks.json',ROOT/'analysis/complete_scheme_replay_20261003/oof_audit.json']
    last_notice=time.monotonic()
    while not all(p.exists() for p in gates):
        time.sleep(10)
        if time.monotonic()-last_notice>=50:
            state('waiting_for_previous_round_and_linear_bank',extra={'pending':[str(p) for p in gates if not p.exists()]});last_notice=time.monotonic()
    import optimize_training_round30 as experiment
    for stage in (experiment.freeze,experiment.build,experiment.independent,experiment.coordinate,experiment.refinement):
        state(stage.__name__);stage()
    from parallel_candidate_scoring_20261004 import shutdown
    shutdown('optimize_training_round30')
    import finalize_training_round30 as release
    import verify_methods_round30 as checks
    for stage in (release.select,release.calibrate,release.predict,checks.main):state(stage.__module__+'.'+stage.__name__);stage()
    from publish_training_round import publish
    import build_all_model_rankings_20261003 as ranking
    import verify_all_model_rankings_20261003 as qa
    state('publication_and_ranking_qa')
    result=publish(30,'完整方案各层模型权重与后处理联合复搜','complete_scheme_causal_checks.json',
                   ('各层有效权重独立比较','完整重新计算的坐标细搜','完整输出参数细调'))
    ranking.main();qa.main()
    state('round_complete_next_round_pending','completed',{'score':result['winner']['connected_final_score'],
          'gain':result['score_gain'],'continuous_goal_complete':False})


if __name__=='__main__':
    try:main()
    except Exception:state('failed','failed',{'traceback':traceback.format_exc()});raise
