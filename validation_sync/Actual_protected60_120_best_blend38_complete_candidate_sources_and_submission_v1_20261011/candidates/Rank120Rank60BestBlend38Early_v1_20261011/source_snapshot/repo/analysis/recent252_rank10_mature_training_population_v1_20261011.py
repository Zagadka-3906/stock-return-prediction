"""Mature five-day targets ranked within their own TRAIN date, then rolling252 origins."""
def training_frame(lazy,cutoff,cfg):
    import polars as pl
    import forward10_mature_training_labels_v1_20261011 as labels
    assert cfg['target']=='y_rank_5mean' and cfg['label_horizon_trading_days']==10 and cfg['training_calendar_window']==252
    raw=labels.training_frame(lazy,cutoff,{**cfg,'target':labels.TARGET})
    ranked=raw.with_columns((pl.col(labels.TARGET).rank(method='average').over('trade_date')/pl.len().over('trade_date')).alias('y_rank_5mean'))
    dates=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff)).select('trade_date').unique().sort('trade_date').tail(252)
    return ranked.join(dates,on='trade_date',how='semi').sort('trade_date','ts_code')
