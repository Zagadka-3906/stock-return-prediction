"""Copy only fully fingerprint-matched official capsules before the frozen cache lookup."""
from pathlib import Path
import hashlib
import math
import json
import identical_official_score_cache_20261003 as original
ROOT=Path(__file__).resolve().parents[1]
_DIRECTORIES=None
METRICS={'ic_mean','ic_std','icir','ic_positive_ratio','annual_excess','top1_annual_ret','mean_turnover','final_score'}


def score(ctx,pred):
    global _DIRECTORIES
    folder=Path(ctx.scoring).resolve()
    assert folder.name=='scoring_validation_only' and folder.is_relative_to(ROOT/'analysis')
    if _DIRECTORIES is None:
        _DIRECTORIES=tuple(sorted((ROOT/'analysis').rglob('identical_official_scores')))
    cache=folder.parent/'identical_official_scores'
    paths=[folder/'submission.csv',folder/'测试集_X.csv',folder/'测试集_Y.csv',
           ROOT/'evaluate.py',ROOT/'src/scoring.py',Path(original.__file__).resolve()]
    watched={path.resolve() for path in paths};fingerprints={};event={'cross_round_cache_hit':False}
    original_digest=original.digest
    def capture(path):
        result=original_digest(path);resolved=Path(path).resolve()
        if resolved not in watched:return result
        fingerprints[resolved]=result
        if len(fingerprints)!=len(watched):return result
        scope={'submission_csv_sha256':fingerprints[paths[0]],
               'inputs_sha256':{path.name:fingerprints[path.resolve()] for path in paths[1:]},
               'versions':{name:original.importlib.metadata.version(name) for name in ('numpy','pandas','polars','scipy')}}
        key=hashlib.sha256(original.canonical(scope)).hexdigest();target=cache/f'{key}.json'
        if target.exists():return result
        for directory in _DIRECTORIES:
            donor=directory/f'{key}.json'
            if directory.resolve()==cache or not donor.exists():continue
            assert donor.resolve().is_relative_to(ROOT/'analysis')
            payload=donor.read_bytes();entry=json.loads(payload.decode('utf-8'))
            assert entry['scope']==scope
            metrics=entry['metrics'];assert set(metrics)==METRICS
            assert all(math.isfinite(value) for value in metrics.values())
            assert hashlib.sha256(original.canonical(metrics)).hexdigest()==entry['metrics_sha256']
            assert math.isclose(.4*metrics['ic_mean']+.3*metrics['annual_excess']+.3*(1-metrics['mean_turnover']),metrics['final_score'],abs_tol=1e-12)
            cache.mkdir(exist_ok=True)
            with target.open('xb') as stream:stream.write(payload)
            event.update(cross_round_cache_hit=True,cache_key=key,source=str(donor),
                         source_sha256=hashlib.sha256(payload).hexdigest(),copied_capsule=str(target),
                         capsule_byte_identical=True,original_official_evaluation_timestamp_preserved=True)
            break
        return result
    original.digest=capture
    try:
        metrics=original.score(ctx,pred)
        if event['cross_round_cache_hit']:
            assert ctx.last_official_score_cache['cache_hit'] and ctx.last_official_score_cache['cache_key']==event['cache_key']
        return metrics
    finally:
        original.digest=original_digest
        ctx.last_cross_round_official_reuse=event
