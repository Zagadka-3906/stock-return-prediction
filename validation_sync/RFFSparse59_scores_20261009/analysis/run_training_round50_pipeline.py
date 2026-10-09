"""Run whole-scheme joint optimization after all predecessors andpreflights."""
from pathlib import Path
import json
import sys
import time
import traceback
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
STATE=ROOT/'analysis/ongoing_optimization_r50_state.json'


def state(stage,status='running',extra=None):
    payload={'round':50,'stage':stage,'status':status,'updated_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'continuous_optimization_authorized':True,'test_labels_read':False,**(extra or {})}
    STATE.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(payload,ensure_ascii=False),flush=True)
def main():
    gates=[ROOT/'results/optimization_20261003_r49.json']+[
        ROOT/f'analysis/{folder}/verification.json' for folder in ('whole_scheme_runtime_preflight_20261004',
        'whole_scheme_future_runtime_qa_20261004','whole_scheme_score_preflight_20261004',
        'whole_scheme_round50_proposal_preflight_20261004','whole_scheme_round50_release_preflight_20261004')]
    state('waiting_for_previous_round_and_whole_scheme_checks');last=time.monotonic()
    while not all(path.exists() for path in gates):
        time.sleep(10)
        if time.monotonic()-last>=50:
            state('waiting_for_previous_round_and_whole_scheme_checks',extra={'pending':[str(path) for path in gates if not path.exists()]});last=time.monotonic()
    import optimize_training_round50 as experiment
    for stage in (experiment.freeze,experiment.build,experiment.independent,experiment.forward,experiment.reverse,experiment.retention_refinement,experiment.temporal_refinement):state(stage.__name__);stage()
    from parallel_candidate_scoring_four_20261004 import shutdown
    shutdown('optimize_training_round50')
    import finalize_training_round50 as release
    import verify_methods_round50 as checks
    for stage in (release.select,release.calibrate,release.predict,checks.main):state(stage.__module__+'.'+stage.__name__);stage()
    from publish_training_round import publish
    import build_all_model_rankings_20261003 as ranking
    import verify_all_model_rankings_20261003 as qa
    state('publication_and_ranking_qa');result=publish(50,'全部选中模型层的联合权重与逐层留存重调','whole_scheme_joint_causal_checks.json',
        ('全部活跃层独立权重对照','正向逐层权重重调','逆向逐层权重重调','各历史层留存参数重调','最终平滑与融合强度重调'))
    ranking.main();qa.main();state('round_complete_next_round_pending','completed',{'score':result['winner']['connected_final_score'],'gain':result['score_gain'],'continuous_goal_complete':False})


if __name__=='__main__':
    try:main()
    except Exception:state('failed','failed',{'traceback':traceback.format_exc()});raise
