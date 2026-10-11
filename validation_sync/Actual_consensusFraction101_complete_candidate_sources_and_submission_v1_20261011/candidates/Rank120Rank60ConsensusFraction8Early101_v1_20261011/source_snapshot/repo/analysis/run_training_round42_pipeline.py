"""Complete standalone model comparison after the preceding round is published."""
from pathlib import Path
import json
import sys
import time
import traceback
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
STATE=ROOT/'analysis/ongoing_optimization_r42_state.json'


def state(stage,status='running',extra=None):
    payload={'round':42,'stage':stage,'status':status,'updated_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
             'continuous_optimization_authorized':True,'test_labels_read':False,**(extra or {})}
    STATE.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload,ensure_ascii=False),flush=True)


def main():
    state('waiting_for_previous_round')
    gates=[ROOT/'analysis/additive_ridge_bank_20261004/oof_audit.json',ROOT/'results/optimization_20261003_r41.json',ROOT/'analysis/optimization_20261003_r41/additive_ridge_role_causal_checks.json']
    gates += [ROOT/'analysis/standalone_round42_preflight_v2/verification.json',ROOT/'analysis/additive_ridge_round_baselines_qa_20261004/verification.json']
    last_notice=time.monotonic()
    while not all(p.exists() for p in gates):
        time.sleep(10)
        if time.monotonic()-last_notice>=50:
            state('waiting_for_previous_round',extra={'pending':[str(p) for p in gates if not p.exists()]});last_notice=time.monotonic()
    import optimize_training_round42 as experiment
    for stage in (experiment.freeze,experiment.build,experiment.independent,experiment.model_refinement,experiment.refinement):
        state(stage.__name__);stage()
    from parallel_candidate_scoring_four_20261004 import shutdown
    shutdown('optimize_training_round42')
    import finalize_training_round42 as release
    import verify_methods_round42 as checks
    for stage in (release.select,release.calibrate,release.predict,checks.main):
        state(stage.__module__+'.'+stage.__name__);stage()
    from publish_training_round import publish
    import build_all_model_rankings_20261003 as ranking
    import verify_all_model_rankings_20261003 as qa
    state('publication_and_ranking_qa')
    result=publish(42,'固定分段基函数加性Ridge的独立完整主模型比较','standalone_causal_checks.json',
                   ('6个加性Ridge主方案独立平滑与辅助信号比较','每个模型独立平滑和持仓持续性细搜','完整输出细调'))
    ranking.main();qa.main()
    state('round_complete_next_round_pending','completed',{'score':result['winner']['connected_final_score'],
          'gain':result['score_gain'],'continuous_goal_complete':False})


if __name__=='__main__':
    try:main()
    except Exception:
        state('failed','failed',{'traceback':traceback.format_exc()});raise
