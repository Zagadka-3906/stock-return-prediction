"""Lazy gated complete official search, freeze, calibration, inference andpublication."""
from pathlib import Path
import importlib
import json
import sys
import time
import traceback
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]


def main(number):
    assert number in (55,56)
    state_path=ROOT/f'analysis/ongoing_optimization_r{number}_state.json'
    def state(stage,status='running',extra=None):
        value={'round':number,'stage':stage,'status':status,'updated_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'continuous_optimization_authorized':True,'test_labels_read':False,**(extra or {})}
        state_path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(value,ensure_ascii=False),flush=True)
    gates=[ROOT/f'results/optimization_20261003_r{number-1}.json',
        ROOT/'analysis/neural_interaction_bank_20261004/oof_audit.json',
        ROOT/'analysis/neural_interaction_future_models_qa_20261004/verification.json',
        ROOT/'analysis/neural_interaction_search_generator_preflight_20261004/verification.json',
        ROOT/'analysis/neural_interaction_complete_scheme_preflight_20261004/verification.json']
    try:
        state('waiting_for_actual_previous_round_andcomplete_scheme_checks');last=time.monotonic()
        while not all(path.exists() for path in gates):
            time.sleep(10)
            if time.monotonic()-last>=50:
                state('waiting_for_actual_previous_round_andcomplete_scheme_checks',extra={'pending':[str(path) for path in gates if not path.exists()]});last=time.monotonic()
        module=importlib.import_module(f'optimize_training_round{number}')
        stages=(module.freeze,module.build,module.independent,module.combinations,module.refine_weights,module.refinement) if number==55 else (
            module.freeze,module.build,module.independent,module.model_refinement,module.refinement)
        for stage in stages:state(stage.__name__);stage()
        from parallel_candidate_scoring_four_20261004 import shutdown
        shutdown(f'optimize_training_round{number}')
        release=importlib.import_module(f'finalize_training_round{number}')
        for stage in (release.select,release.calibrate,release.predict):state('release.'+stage.__name__);stage()
        from check_neural_interaction_scheme_20261004 import main as checks
        state('complete_scheme_causal_checks');checks(number)
        from publish_training_round import publish
        import build_all_model_rankings_20261003 as ranking
        import verify_all_model_rankings_20261003 as qa
        state('publication_andranking_qa')
        label='无Dropout学习率、训练轮数与权重衰减组合的完整方案用途融合' if number==55 else '无Dropout学习率、训练轮数与权重衰减组合的独立完整主模型'
        stages=('全部模型分用途独立对照','最佳单用途模型组合','新用途权重顺序细搜','新成员留存与涨停偏移细搜') if number==55 else (
            '全部模型独立完整方案','每模型后处理与留存细搜','最高分方案最终参数细搜')
        result=publish(number,label,'neural_interaction_scheme_causal_checks.json',stages)
        ranking.main();qa.main();state('round_complete_next_round_pending','completed',
            {'score':result['winner']['connected_final_score'],'gain':result['score_gain'],'continuous_goal_complete':False})
    except Exception:state('failed','failed',{'traceback':traceback.format_exc()});raise
