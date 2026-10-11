"""Resume frozen R15 verification with a documented prefix-cache adapter; preserve every scored recipe."""
from pathlib import Path
import sys
import time
import traceback
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import finalize_training_round15 as release
import run_training_round15_pipeline as pipeline
from optimize_training_round15 import OUT,PREVIOUS,NEW_MODELS,sha,read,dump
OriginalReleaseContext=release.ReleaseContext


class PrefixSafeReleaseContext(OriginalReleaseContext):
    def augment(self,base,role):
        import numpy as np
        from optimize_wave15 import daily_ranks
        spec=self.diverse_augmentation[role]
        if spec['weight']>0:
            name=spec['model'];n=len(self.dates)
            if name not in self._diverse_cache or len(self._diverse_cache[name][1])<n:
                path=(OUT if name in NEW_MODELS else PREVIOUS)/f'rankers/{name}.npy'
                values=np.load(path)[:n]
                self._diverse_cache[name]=(values,daily_ranks(values,self.valid,self.dates))
        return super().augment(base,role)


def main():
    import numpy as np
    record=release.selected();winner=record['winner']
    failed=pipeline.STATE
    evidence=OUT/'calibration_original_failure_state.json'
    if not evidence.exists():evidence.write_bytes(failed.read_bytes())
    ctx=PrefixSafeReleaseContext(winner);promote=ctx.promote('baseline')
    pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    assert np.array_equal(pred,np.load(OUT/'selected_validation.npy'))
    del ctx,pred,promote
    release.ReleaseContext=PrefixSafeReleaseContext
    for stage in (release.calibrate,release.predict):
        pipeline.state('cache_recovery.'+stage.__name__);stage()
    import verify_methods_round15 as checks
    pipeline.state('cache_recovery.method_verification');checks.main()
    release.selected()
    dump(OUT/'calibration_cache_recovery.json',{'status':'passed','recorded_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'cause':'Cold prefix contexts loaded full-period ranker values against shorter dates/valid arrays.',
         'adapter':'Slice values to current length before daily ranking; refresh an existing shorter cache when a longer prefix is checked. The frozen augmentation formula is unchanged.',
         'frozen_recipe_and_source_files_unchanged':True,'full_selected_output_bit_identical':True,
         'cold_date_prefixes_passed':read(OUT/'causal_validation.json')['future_append_prefix_invariance'],
         'new_scored_records':0,'test_labels_read':False,'adapter_sha256':sha(Path(__file__)),
         'original_selection_sha256':sha(OUT/'selection.json'),'selected_forecast_sha256':sha(OUT/'selected_validation.npy')},immutable=True)
    from publish_training_round import publish
    import build_all_model_rankings_20261003 as ranking
    import verify_all_model_rankings_20261003 as qa
    pipeline.state('cache_recovery.publication_and_ranking_qa')
    result=publish(15,'扩展MLP结构与训练轮数分用途集成','diverse_augmentation_causal_checks.json',
                   ('三个用途独立集成','用途最优设置组合','集成权重细搜','输出细调'))
    ranking.main();qa.main()
    pipeline.state('round_complete_next_round_pending','completed',{'score':result['winner']['connected_final_score'],
                   'gain':result['score_gain'],'cache_recovery_verified':True,'continuous_goal_complete':False})


if __name__=='__main__':
    try:main()
    except Exception:
        pipeline.state('cache_recovery.failed','failed',{'traceback':traceback.format_exc()});raise
