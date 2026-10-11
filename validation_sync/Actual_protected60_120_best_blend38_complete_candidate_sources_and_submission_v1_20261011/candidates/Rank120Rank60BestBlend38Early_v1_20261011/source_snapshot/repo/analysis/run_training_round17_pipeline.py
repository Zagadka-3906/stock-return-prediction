"""Wait for training memory to clear, then finish all authorized R17 stages."""
from pathlib import Path
import json
import sys
import time
import traceback
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
STATE=ROOT/'analysis/ongoing_optimization_r17_state.json'


def state(stage,status='running',extra=None):
    payload={'round':17,'stage':stage,'status':status,'updated_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
             'continuous_optimization_authorized':True,'test_labels_read':False,**(extra or {})}
    STATE.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(payload,ensure_ascii=False),flush=True)


def main():
    state('waiting_for_previous_round_and_objective_bank')
    gates=[ROOT/'results/optimization_20261003_r16.json',ROOT/'analysis/optimization_20261003_r16/diverse_augmentation_causal_checks.json',ROOT/'analysis/objective_bank_20261003/oof_audit.json']
    last_notice=time.monotonic()
    while not all(path.exists() for path in gates):
        time.sleep(10)
        if time.monotonic()-last_notice>=50:
            state('waiting_for_previous_round_and_objective_bank',extra={'pending':[str(p) for p in gates if not p.exists()]});last_notice=time.monotonic()
    import optimize_training_round17 as experiment
    for stage in (experiment.freeze,experiment.build,experiment.independent,experiment.combinations,experiment.refine_weights,experiment.refinement):
        state(stage.__name__);stage()
    import finalize_training_round17 as release
    import verify_methods_round17 as checks
    for stage in (release.select,release.calibrate,release.predict,checks.main):
        state(stage.__module__+'.'+stage.__name__);stage()
    from publish_training_round import publish
    import build_all_model_rankings_20261003 as ranking
    import verify_all_model_rankings_20261003 as qa
    state('publication_and_ranking_qa')
    result=publish(17,'头部识别与同日成对排序神经网络集成','diverse_augmentation_causal_checks.json',
                   ('三个用途独立集成','用途最优设置组合','集成权重细搜','输出细调'))
    ranking.main();qa.main()
    state('round_complete_next_round_pending','completed',{'score':result['winner']['connected_final_score'],
                                                        'gain':result['score_gain'],'continuous_goal_complete':False})


if __name__=='__main__':
    try:main()
    except Exception:
        state('failed','failed',{'traceback':traceback.format_exc()});raise
