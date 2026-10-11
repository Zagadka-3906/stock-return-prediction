"""Mean20 mature labels, restricted to the last252 pre-cutoff TRAIN calendar dates."""
def training_frame(lazy,cutoff,cfg):
    import polars as pl
    import forward5_mature_training_labels_v1_20261010 as labels
    assert cfg['training_calendar_window']==252 and cfg['target']==labels.TARGET and cfg['label_horizon_trading_days']==5
    past=lazy.filter(pl.col('is_train')&(pl.col('trade_date')<cutoff))
    dates=past.select('trade_date').unique().sort('trade_date').tail(252)
    # Derive targets on the original full past panel before restricting the origin dates.
    # Otherwise removing price-invalid future observations changes the provided TRAIN target.
    return labels.training_frame(lazy,cutoff,cfg).join(dates,on='trade_date',how='semi').sort('trade_date','ts_code')
