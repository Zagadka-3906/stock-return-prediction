"""Past-only10-day mean-return targets with complete stock/calendar spans and mature ends."""
import polars as pl
TARGET='y_ret_120mean'
HORIZON=120

def training_frame(lazy,cutoff,cfg):
    assert cfg['target']==TARGET and cfg['label_horizon_trading_days']==HORIZON
    # Never collect later labels. Last10 observations cannot form a mature target.
    past=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)).sort('ts_code','trade_date')
    calendar=past.select('trade_date').unique().sort('trade_date').with_row_index('_calendar120_index')
    aligned=past.join(calendar,on='trade_date',how='left')
    derived=aligned.with_columns([
        pl.col('y_ret_1d').cast(pl.Float64).rolling_mean(window_size=HORIZON,min_samples=HORIZON).shift(-(HORIZON-1)).over('ts_code').alias(TARGET),
        pl.col('trade_date').shift(-HORIZON).over('ts_code').alias('label_end_120d'),
        pl.col('_calendar120_index').shift(-HORIZON).over('ts_code').alias('_label_end_calendar120_index')])
    return derived.filter(pl.col('price_valid')&pl.col(TARGET).is_finite()&(pl.col('label_end_120d')<cutoff)&((pl.col('_label_end_calendar120_index')-pl.col('_calendar120_index'))==HORIZON)).drop('_calendar120_index','_label_end_calendar120_index').sort('trade_date','ts_code')
