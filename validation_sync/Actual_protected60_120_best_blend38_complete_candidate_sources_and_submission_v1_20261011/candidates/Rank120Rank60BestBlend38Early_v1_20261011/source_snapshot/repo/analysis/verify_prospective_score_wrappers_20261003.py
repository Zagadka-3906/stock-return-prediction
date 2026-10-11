"""Validate both future scoring entry points with a frozen complete real-data control."""
from pathlib import Path
import json
import os
import sys
import time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[name]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
import polars as pl
import evaluate
import optimize_training_round16 as original
import optimize_training_round20 as prospective
from score_calibrated_candidates_20261003 import score
from identical_official_score_cache_20261003 import digest


def main():
    output=ROOT/'analysis/prospective_score_wrappers_qa_20261003'
    output.mkdir(exist_ok=True);target=output/'verification.json'
    assert not target.exists(),'Preserve completed evidence.'
    source=original.OUT
    expected=json.loads((source/'calibrated_csv_official.json').read_text(encoding='utf-8'))['metrics']
    ctx=original.Context();prediction=np.load(source/'selected_validation.npy')
    pandas_module=evaluate.pd
    def scoring_folder(name):
        folder=output/name/'scoring_validation_only';folder.mkdir(parents=True,exist_ok=True)
        for filename in ('测试集_X.csv','测试集_Y.csv'):
            path=folder/filename
            if not path.exists():os.link(source/'scoring_validation_only'/filename,path)
        return folder
    ctx.scoring=scoring_folder('causal_return_mapping')
    metrics=score(ctx,prediction)
    assert metrics==expected and evaluate.pd is pandas_module
    frozen_csv_sha=digest(source/'calibrated_validation.csv')
    assert digest(ctx.scoring/'submission.csv')==frozen_csv_sha
    calibrated=pl.read_csv(ctx.scoring/'submission.csv')['pred'].to_numpy()
    mapping=ctx.last_candidate_return_mapping
    # Final-fold labels cannot contribute to any of the five past-only mappings.
    y=ctx.frame['y_ret_1d'].to_numpy().copy();y[ctx.dates//10000==2024]=123.0
    ctx.frame=ctx.frame.with_columns(pl.Series('y_ret_1d',y))
    assert score(ctx,prediction)==expected
    assert digest(ctx.scoring/'submission.csv')==frozen_csv_sha
    ctx.__class__=prospective.Context
    ctx.scoring=scoring_folder('round20_inherited_entry_point')
    assert ctx.score(calibrated)==expected and evaluate.pd is pandas_module
    assert digest(ctx.scoring/'submission.csv')==frozen_csv_sha
    assert not ctx.last_official_score_cache['cache_hit']
    parse_event=ctx.last_validation_csv_parse_cache
    assert len(parse_event['events'])==2 and all(x['parsed_frame_reused'] for x in parse_event['events'])
    payload={'status':'passed','same_frozen_actual_return_csv_bit_identical':True,
             'round20_scoring_entry_point_official_cache_miss_exercised':True,
             'return_mapped_scoring_entry_point_official_cache_miss_exercised':True,
             'all_eight_official_metrics_bit_identical':True,
             'future_final_fold_label_poisoning_csv_bit_identical':True,
             'official_evaluator_restored':True,'validation_rows':len(prediction),
             'validation_days':len(np.unique(ctx.dates)),'new_model_scores':0,
             'test_labels_read':False,'metrics':metrics,'causal_return_mapping':mapping,
             'parsed_validation_reuse':parse_event,
             'input_sha256':{str(path.resolve()):digest(path) for path in (
                 source/'selected_validation.npy',source/'calibrated_validation.csv',
                 ROOT/'analysis/score_calibrated_candidates_20261003.py',
                 ROOT/'analysis/optimize_training_round20.py',
                 ROOT/'analysis/official_validation_csv_parse_cache_20261003.py',Path(__file__))},
             'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')}
    with target.open('x',encoding='utf-8') as stream:
        json.dump(payload,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print(json.dumps({'status':'passed','path':str(target)},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
