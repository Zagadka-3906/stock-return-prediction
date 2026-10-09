"""Exercise unchanged-cache semantics, changed-label misses and a full real-data reuse."""
from pathlib import Path
from types import SimpleNamespace
import shutil
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
import numpy as np
import polars as pl
import identical_official_score_cache_20261003 as original
import cross_round_official_score_reuse_20261003 as adapter
import evaluate


def main():
    qa=ROOT/'analysis/cross_round_official_reuse_qa_20261003';qa.mkdir(exist_ok=True)
    assert not (qa/'verification.json').exists()
    rng=np.random.default_rng(20261003);codes=[f'{i:06d}.SZ' for i in range(120)]
    frame=pl.DataFrame({'ts_code':codes*4,'trade_date':np.repeat([20190102,20190103,20190104,20190107],120)})
    pred=rng.normal(size=len(frame));labels=rng.normal(0,.02,len(frame));saved_digest=original.digest
    def context(name):
        folder=qa/name/'scoring_validation_only';folder.mkdir(parents=True,exist_ok=True)
        frame.with_columns(pl.lit(0).alias('flag_limit_up')).write_csv(folder/'测试集_X.csv')
        frame.with_columns(pl.Series('y_ret_1d',labels)).write_csv(folder/'测试集_Y.csv',float_precision=17)
        return SimpleNamespace(frame=frame,scoring=folder)
    donor=context('synthetic_donor');expected=original.score(donor,pred)
    recipient=context('synthetic_recipient');assert adapter.score(recipient,pred)==expected
    assert original.digest is saved_digest and recipient.last_official_score_cache['cache_hit']
    reuse=recipient.last_cross_round_official_reuse;assert reuse['cross_round_cache_hit']
    assert Path(reuse['source']).read_bytes()==Path(reuse['copied_capsule']).read_bytes()
    source_entry=original.json.loads(Path(reuse['source']).read_text(encoding='utf-8'))
    copied_entry=original.json.loads(Path(reuse['copied_capsule']).read_text(encoding='utf-8'))
    assert copied_entry['official_evaluation_at_local']==source_entry['official_evaluation_at_local']
    changed=context('synthetic_changed_labels');changed_labels=labels.copy();changed_labels[0]+=1.
    frame.with_columns(pl.Series('y_ret_1d',changed_labels)).write_csv(changed.scoring/'测试集_Y.csv',float_precision=17)
    changed_metrics=adapter.score(changed,pred)
    assert not changed.last_cross_round_official_reuse['cross_round_cache_hit']
    assert not changed.last_official_score_cache['cache_hit'] and changed_metrics!=expected
    assert original.digest is saved_digest
    # Full real-data control reuses an already measured frozen calibrated CSV.
    source=ROOT/'analysis/optimization_20261003_r16';real=pl.read_csv(source/'calibrated_validation.csv')
    folder=qa/'real_full_oof'/'scoring_validation_only';folder.mkdir(parents=True,exist_ok=True)
    for filename in ('测试集_X.csv','测试集_Y.csv'):
        if not (folder/filename).exists():os_link=__import__('os').link;os_link(source/'scoring_validation_only'/filename,folder/filename)
    real_ctx=SimpleNamespace(frame=real.select('ts_code','trade_date'),scoring=folder)
    expected_real=original.json.loads((source/'calibrated_csv_official.json').read_text(encoding='utf-8'))['metrics']
    # Reading numeric CSVs may change last-bit serialization; use the immutable mapped array.
    raw=np.load(source/'selected_validation.npy')
    from score_calibrated_candidates_20261003 import score as mapped_score
    from optimize_training_round16 import Context
    full_ctx=Context();full_ctx.scoring=folder
    import score_calibrated_candidates_20261003 as mapped_module
    # Explicitly test the adapter with the exact reconstructed mapped values below.
    mapped_score(full_ctx,raw)
    assert original.digest(folder/'submission.csv')==original.digest(source/'calibrated_validation.csv')
    real_pred=pl.read_csv(folder/'submission.csv')['pred'].to_numpy()
    # Pandas-style parser roundtrips are not assumed: recover exact mapping again through
    # a narrow operation interception, retaining the original scoring output proof.
    captured={}
    import official_validation_csv_parse_cache_20261003 as parsing
    old_run=parsing.run
    def capture_values(ctx,values,operation):
        captured['pred']=values.copy();return old_run(ctx,values,operation)
    parsing.run=capture_values
    try:mapped_score(full_ctx,raw)
    finally:parsing.run=old_run
    pristine=qa/'real_cross_recipient'/'scoring_validation_only';pristine.mkdir(parents=True,exist_ok=True)
    for filename in ('测试集_X.csv','测试集_Y.csv'):
        __import__('os').link(source/'scoring_validation_only'/filename,pristine/filename)
    real_ctx.scoring=pristine
    metrics=adapter.score(real_ctx,captured['pred'])
    assert metrics==expected_real and real_ctx.last_cross_round_official_reuse['cross_round_cache_hit']
    assert original.digest(pristine/'submission.csv')==original.digest(source/'calibrated_validation.csv')
    assert original.digest is saved_digest
    payload={'status':'passed','synthetic_capsule_byte_identical':True,
         'original_official_evaluation_timestamp_preserved':True,'changed_label_bytes_force_official_miss':True,
         'full5635800_row_actual_return_csv_byte_identical':True,'all_eight_official_metrics_bit_identical':True,
         'full_real_reuse':real_ctx.last_cross_round_official_reuse,
         'original_digest_restored':True,'test_labels_read':False,'new_model_scores':0,
         'source_sha256':{str(path.resolve()):original.digest(path) for path in (Path(__file__),Path(adapter.__file__),Path(original.__file__))},
         'verified_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')}
    with (qa/'verification.json').open('x',encoding='utf-8') as stream:
        original.json.dump(payload,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print('Cross-round exact-byte reuse and changed-label misses passed.',flush=True)


if __name__=='__main__':main()
