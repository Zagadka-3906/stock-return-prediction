"""The original 63 causal price/volume features, with no label dependency.

Prediction is after the close of t, for t+1. Current-day fields are allowed.
Rolling operators are trailing within a stock; ranks are within the same day.
"""
import polars as pl

PRICE = ('open', 'high', 'low', 'close')
RAW = ['ts_code', 'trade_date', *PRICE, 'vol', 'amount', 'flag_limit_up', 'flag_limit_down']
WINDOWS = (5, 10, 20, 60)


def div(a, b):
    return pl.when(b.abs() > 1e-12).then(a / b).otherwise(None)


def source(path, train=False):
    schema = {c: pl.Float32 for c in (*PRICE, 'vol', 'amount')}
    schema.update(ts_code=pl.String, trade_date=pl.Int32,
                  flag_limit_up=pl.Int8, flag_limit_down=pl.Int8,
                  y_ret_1d=pl.Float64)
    cols = RAW + (['y_ret_1d'] if train else [])
    return (pl.scan_csv(path, schema_overrides=schema,
                        null_values=['NaN', 'nan', ''], low_memory=True)
            .select(cols).with_row_index('row_id'))


def features(lf):
    # Drop any label column before constructing even the first feature.
    lf = lf.select(RAW + ['row_id']).sort('ts_code', 'trade_date')
    lf = lf.with_columns(pl.col(c).fill_nan(None) for c in (*PRICE, 'vol', 'amount'))
    lf = lf.with_columns(pl.when(pl.col(c) > 0).then(pl.col(c)).otherwise(None).alias(c)
                         for c in PRICE)
    o, h, l, c, v, a = (pl.col(x) for x in (*PRICE, 'vol', 'amount'))
    spread, top, bottom = h-l, pl.max_horizontal(o, c), pl.min_horizontal(o, c)
    q = dict(KMID=div(c-o, o), KLEN=div(spread, o),
             KMID2=div(c-o, spread+1e-12), KUP=div(h-top, o),
             KUP2=div(h-top, spread+1e-12), KLOW=div(bottom-l, o),
             KLOW2=div(bottom-l, spread+1e-12), KSFT=div(2*c-h-l, o),
             KSFT2=div(2*c-h-l, spread+1e-12), OPEN0=div(o, c),
             HIGH0=div(h, c), LOW0=div(l, c))
    for w in WINDOWS:
        q[f'ROC{w}'] = div(c.shift(w).over('ts_code'), c)
        q[f'MA{w}'] = div(c.rolling_mean(w, min_samples=w).over('ts_code'), c)
        q[f'STD{w}'] = div(c.rolling_std(w, min_samples=w).over('ts_code'), c)
        q[f'VMA{w}'] = div(v.rolling_mean(w, min_samples=w).over('ts_code'), v)
        q[f'VSTD{w}'] = div(v.rolling_std(w, min_samples=w).over('ts_code'), v)
    lf = lf.with_columns(e.alias(n) for n, e in q.items())
    custom = {}
    for w in (1, 2, 3, 5, 10, 20, 60):
        custom[f'RET{w}'] = div(c, c.shift(w).over('ts_code'))-1
    for w in (5, 20, 60):
        custom[f'AMT_RATIO{w}'] = div(a, a.rolling_mean(w, min_samples=w).over('ts_code'))
        custom[f'VOL_RATIO{w}'] = div(v, v.rolling_mean(w, min_samples=w).over('ts_code'))
    custom['LOG_AMOUNT'] = a.clip(lower_bound=0).log1p()
    custom['LOG_VOL'] = v.clip(lower_bound=0).log1p()
    custom['PRICE_TO_20D_HIGH'] = div(c, h.rolling_max(20, min_samples=20).over('ts_code'))
    custom['PRICE_TO_60D_HIGH'] = div(c, h.rolling_max(60, min_samples=60).over('ts_code'))
    custom['ILLIQ'] = div((div(c, c.shift(1).over('ts_code'))-1).abs(), a)
    for w in (5, 10, 20):
        custom[f'UP_COUNT{w}'] = pl.col('flag_limit_up').rolling_sum(w, min_samples=w).over('ts_code')
    lf = lf.with_columns(e.alias(n) for n, e in custom.items())
    lf = lf.with_columns(div(pl.col('RET1').rolling_std(w, min_samples=w).over('ts_code'),
                            pl.lit(1.)).alias(f'RVOL{w}') for w in (5, 20))
    names = list(q)+list(custom)+['RVOL5', 'RVOL20', 'flag_limit_up', 'flag_limit_down']
    ranks = ['RET1', 'RET5', 'RET20', 'KLEN', 'LOG_AMOUNT', 'RVOL20']
    lf = lf.with_columns((pl.col(n).rank(method='average').over('trade_date') /
                          pl.col(n).count().over('trade_date')).alias(f'CS_{n}') for n in ranks)
    names += [f'CS_{n}' for n in ranks]
    lf = lf.with_columns(c.is_not_null().alias('price_valid'))
    lf = lf.with_columns(pl.when(pl.col(n).is_finite()).then(pl.col(n)).otherwise(None)
                         .cast(pl.Float32).alias(n) for n in names)
    return lf.select(['ts_code', 'trade_date', 'row_id', 'price_valid']+names), names
