"""Officially score each prospective candidate's causal return-mapped CSV."""
def score(ctx,pred):
    import numpy as np
    import polars as pl
    from pathlib import Path
    from run import fold_cutoff
    from return_mapping import daily_percentile,fit_mapping,apply_mapping
    from cross_round_official_score_reuse_20261003 import score as official_score
    root=Path(__file__).resolve().parents[1]
    pct=daily_percentile(ctx.frame.select('trade_date').to_pandas(),pred)
    y=ctx.frame['y_ret_1d'].to_numpy().astype(np.float64);mapped=np.empty_like(pct);boundaries=[]
    for year in np.unique(ctx.dates//10000):
        cutoff=fold_cutoff(int(year));mask=ctx.dates//10000==year;history=(ctx.dates<cutoff)&np.isfinite(y)
        if history.any():
            mapped[mask]=apply_mapping(fit_mapping(pct[history],y[history]),pct[mask]);last=int(ctx.dates[history].max())
            method='past mature OOF isotonic'
        else:
            if not hasattr(ctx,'_first_fold_return_moments'):
                labels=pl.scan_csv(root/'data/raw/训练集.csv',schema_overrides={'trade_date':pl.Int32,'y_ret_1d':pl.Float64},null_values=['NaN','nan','']).filter((pl.col('trade_date')<cutoff)&pl.col('y_ret_1d').is_finite()).select('trade_date','y_ret_1d').collect()
                ctx._first_fold_return_moments=(float(labels['y_ret_1d'].mean()),float(labels['y_ret_1d'].std()),int(labels['trade_date'].max()))
            mean,scale,last=ctx._first_fold_return_moments;assert np.isfinite(mean) and np.isfinite(scale) and scale>0
            mapped[mask]=mean+.1*scale*(pct[mask]-.5);method='prevalidation training moments affine fallback'
        assert last<cutoff<int(ctx.dates[mask].min())
        boundaries.append({'year':int(year),'mapping_last_label_date':last,'exclusive_cutoff':cutoff,'method':method})
    assert np.array_equal(pct,daily_percentile(ctx.frame.select('trade_date').to_pandas(),mapped))
    from official_validation_csv_parse_cache_20261003 import run
    metrics=run(ctx,mapped,official_score)
    ctx.last_candidate_return_mapping={'actual_return_mapped_csv_scored':True,'within_day_ranks_bit_identical':True,
                                       'boundaries':boundaries,'test_labels_read':False,
                                       'cross_round_identical_official_reuse':ctx.last_cross_round_official_reuse}
    return metrics
