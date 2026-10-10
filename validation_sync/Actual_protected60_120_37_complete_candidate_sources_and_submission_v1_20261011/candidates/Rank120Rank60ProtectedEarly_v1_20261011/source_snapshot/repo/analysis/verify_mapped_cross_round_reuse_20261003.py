"""Verify current causal mapping plus exact-byte cross-round metrics on the frozen full OOF."""
from pathlib import Path
import os
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
import polars as pl
import identical_official_score_cache_20261003 as original
from optimize_training_round16 import Context,OUT as source,read,dump,sha
from score_calibrated_candidates_20261003 import score


def main():
    qa=ROOT/'analysis/mapped_cross_round_reuse_qa_20261003';qa.mkdir(exist_ok=True)
    assert not (qa/'verification.json').exists()
    folder=qa/'scoring_validation_only';folder.mkdir(exist_ok=True)
    for filename in ('测试集_X.csv','测试集_Y.csv'):
        if not (folder/filename).exists():os.link(source/'scoring_validation_only'/filename,folder/filename)
    ctx=Context();ctx.scoring=folder;pred=np.load(source/'selected_validation.npy')
    expected=read(source/'calibrated_csv_official.json')['metrics'];saved_digest=original.digest
    assert score(ctx,pred)==expected and original.digest is saved_digest
    assert ctx.last_official_score_cache['cache_hit'] and ctx.last_cross_round_official_reuse['cross_round_cache_hit']
    assert sha(folder/'submission.csv')==sha(source/'calibrated_validation.csv')
    first_reuse=ctx.last_cross_round_official_reuse;mapping=ctx.last_candidate_return_mapping
    y=ctx.frame['y_ret_1d'].to_numpy().copy();y[ctx.dates//10000==2024]=456.
    ctx.frame=ctx.frame.with_columns(pl.Series('y_ret_1d',y))
    assert score(ctx,pred)==expected and original.digest is saved_digest
    assert sha(folder/'submission.csv')==sha(source/'calibrated_validation.csv')
    dump(qa/'verification.json',{'status':'passed','actual_calibrated_csv_byte_identical':True,
         'all_eight_official_metrics_bit_identical':True,'full_validation_rows':len(pred),
         'cross_round_capsule_reused':first_reuse,'future_final_fold_label_poisoning_csv_bit_identical':True,
         'original_digest_restored':True,'causal_return_mapping':mapping,
         'new_model_scores':0,'test_labels_read':False,
         'input_sha256':{str(path.resolve()):sha(path) for path in (Path(__file__),
             ROOT/'analysis/score_calibrated_candidates_20261003.py',ROOT/'analysis/cross_round_official_score_reuse_20261003.py',
             ROOT/'analysis/cross_round_official_reuse_qa_20261003/verification.json')},
         'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')},immutable=True)
    print('Causal return mapping and cross-round exact-byte official reuse passed.',flush=True)


if __name__=='__main__':main()
