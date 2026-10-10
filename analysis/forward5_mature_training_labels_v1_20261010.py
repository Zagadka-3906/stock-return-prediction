"""Past-only5-day mean-return targets with complete stock/calendar spans and mature ends."""
import polars as pl
TARGET='y_ret_5mean'
HORIZON=5

def training_frame(lazy,cutoff,cfg):
    assert cfg['target']==TARGET and cfg['label_horizon_trading_days']==HORIZON
    # Never collect later labels. Last5 observations cannot form a mature target.
    past=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)).sort('ts_code','trade_date')
    calendar=past.select('trade_date').unique().sort('trade_date').with_row_index('_calendar5_index')
    aligned=past.join(calendar,on='trade_date',how='left')
    derived=aligned.with_columns([
        pl.col('y_ret_1d').cast(pl.Float64).rolling_mean(window_size=HORIZON,min_samples=HORIZON).shift(-(HORIZON-1)).over('ts_code').alias(TARGET),
        pl.col('trade_date').shift(-HORIZON).over('ts_code').alias('label_end_5d'),
        pl.col('_calendar5_index').shift(-HORIZON).over('ts_code').alias('_label_end_calendar5_index')])
    return derived.filter(pl.col('price_valid')&pl.col(TARGET).is_finite()&(pl.col('label_end_5d')<cutoff)&((pl.col('_label_end_calendar5_index')-pl.col('_calendar5_index'))==HORIZON)).drop('_calendar5_index','_label_end_calendar5_index').sort('trade_date','ts_code')
