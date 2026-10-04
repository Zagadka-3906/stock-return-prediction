"""Fixed already-scored configurations for execution QA, not model selection."""
from pathlib import Path
import json
import time
import optimize_training_round21 as original

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'analysis/parallel_candidate_scoring_four_qa_20261004'


class Context(original.Context):
    def __init__(self):
        super().__init__()
        import os
        source=self.scoring;self.scoring=OUT/'serial'/'scoring_validation_only'
        self.scoring.mkdir(parents=True,exist_ok=True)
        for name in ('测试集_X.csv','测试集_Y.csv'):
            if not (self.scoring/name).exists():os.link(source/name,self.scoring/name)

    def score(self,pred):
        from score_calibrated_candidates_20261003 import score
        from evaluate import evaluate
        # Re-evaluate the actual mapped CSV without metric reuse for timing QA.
        cached=score(self,pred);start=time.perf_counter()
        actual={key:float(value) for key,value in evaluate(str(self.scoring/'submission.csv'),str(self.scoring)).items()}
        assert actual==cached
        self.direct_official_seconds=time.perf_counter()-start
        return actual


def evaluate(ctx,cfg):
    row=original.evaluate(ctx,cfg)
    capsule=json.loads(Path(row['official_score_cache']['official_metrics_source']).read_text(encoding='utf-8'))
    row['actual_mapped_csv_sha256']=capsule['scope']['submission_csv_sha256']
    row['direct_official_scorer_rechecked']=True
    row['direct_official_seconds']=ctx.direct_official_seconds
    return row
