"""One-day centered rank labels; preserve the same actual mature calendar and return availability."""
def training_frame(lazy,cutoff,cfg):
    import polars as pl
    from recent252_mature_training_population_v1_20261010 import training_frame as mature_returns
    assert cfg['target']=='y_rank' and cfg['training_calendar_window']==252
    return mature_returns(lazy,cutoff,{**cfg,'target':'y_ret_1d'}).filter(pl.col('y_rank').is_finite())
