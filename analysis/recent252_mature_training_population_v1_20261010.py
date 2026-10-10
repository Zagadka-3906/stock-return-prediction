"""Select at most252 prior TRAIN calendar sessions; future rows cannot alter the window."""
def training_frame(lazy,cutoff,cfg):
    import polars as pl
    assert cfg['training_calendar_window']==252 and cfg['target']=='y_ret_1d'
    past=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff))
    dates=past.select('trade_date').unique().sort('trade_date').tail(252)
    return past.join(dates,on='trade_date',how='semi').filter(pl.col('price_valid')&pl.col(cfg['target']).is_finite()).sort('trade_date','ts_code')
