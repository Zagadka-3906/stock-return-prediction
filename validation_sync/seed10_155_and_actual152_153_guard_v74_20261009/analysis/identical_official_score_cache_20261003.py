"""Reuse only official metrics with identical CSV bytes, validation data, scorer and runtime versions."""
from pathlib import Path
import hashlib
import importlib.metadata
import json
import math
import time
ROOT=Path(__file__).resolve().parents[1]


def digest(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda:stream.read(8*1024*1024),b''):value.update(chunk)
    return value.hexdigest()


def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')


def score(ctx,pred):
    import polars as pl
    from evaluate import evaluate
    folder=Path(ctx.scoring);assert folder.name=='scoring_validation_only'
    assert folder.resolve().is_relative_to(ROOT/'analysis')
    assert len(pred)==len(ctx.frame)
    csv=folder/'submission.csv'
    ctx.frame.select(['ts_code','trade_date']).with_columns(pl.Series('pred',pred)).write_csv(csv,float_precision=17)
    paths=[folder/'测试集_X.csv',folder/'测试集_Y.csv',ROOT/'evaluate.py',ROOT/'src/scoring.py',Path(__file__)]
    scope={'submission_csv_sha256':digest(csv),
           'inputs_sha256':{path.name:digest(path) for path in paths},
           'versions':{name:importlib.metadata.version(name) for name in ('numpy','pandas','polars','scipy')}}
    key=hashlib.sha256(canonical(scope)).hexdigest();cache=folder.parent/'identical_official_scores';cache.mkdir(exist_ok=True)
    path=cache/f'{key}.json'
    if path.exists():
        entry=json.loads(path.read_text(encoding='utf-8'));assert entry['scope']==scope
        metrics=entry['metrics'];assert hashlib.sha256(canonical(metrics)).hexdigest()==entry['metrics_sha256']
        calculated=.4*metrics['ic_mean']+.3*metrics['annual_excess']+.3*(1-metrics['mean_turnover'])
        assert math.isclose(calculated,metrics['final_score'],abs_tol=1e-12)
        event={'cache_hit':True,'cache_key':key,'official_metrics_source':str(path)}
    else:
        metrics={key:float(value) for key,value in evaluate(str(csv),str(folder)).items()}
        assert all(math.isfinite(metrics[name]) for name in ('ic_mean','annual_excess','mean_turnover','final_score'))
        entry={'scope':scope,'metrics':metrics,'metrics_sha256':hashlib.sha256(canonical(metrics)).hexdigest(),
               'official_evaluation_at_local':time.strftime('%Y-%m-%dT%H:%M:%S')}
        with path.open('x',encoding='utf-8') as stream:json.dump(entry,stream,ensure_ascii=False,indent=2);stream.write('\n')
        event={'cache_hit':False,'cache_key':key,'official_metrics_source':str(path)}
    ctx.last_official_score_cache=event
    with (cache/'events.jsonl').open('a',encoding='utf-8') as stream:
        stream.write(json.dumps({'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),**event},ensure_ascii=False)+'\n')
    return dict(metrics)
