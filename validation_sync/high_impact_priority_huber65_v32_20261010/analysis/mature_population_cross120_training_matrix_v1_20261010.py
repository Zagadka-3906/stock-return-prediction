"""Encode the entire supplied same-date cohort first, then select mature labelled TRAIN rows."""
def matrix(lazy,mature,raw_features):
    import numpy as np,polars as pl
    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder
    from run import to_matrix
    keys=['ts_code','trade_date'];assert len(mature)>0 and len(raw_features)==63
    assert not mature.select(keys).is_duplicated().any()
    dates=mature['trade_date'].unique().to_list()
    cohort=lazy.filter(pl.col('is_train')&pl.col('trade_date').is_in(dates)).select(keys+raw_features).sort('trade_date','ts_code').collect()
    assert not cohort.select(keys).is_duplicated().any()
    assert all(n==4650 for n in cohort.group_by('trade_date').len()['len'].to_list())
    raw=to_matrix(cohort,raw_features);encoded=encoder.encode(raw,cohort['trade_date'].to_numpy(),raw_features)
    assert np.array_equal(raw.view('u4'),encoded[:,:63].view('u4'))
    lookup=mature.select(keys).with_row_index('_training_order').join(cohort.select(keys).with_row_index('_encoded_row'),on=keys,how='left',validate='1:1').sort('_training_order')
    assert lookup.select(keys).equals(mature.select(keys)) and lookup['_encoded_row'].null_count()==0
    indices=lookup['_encoded_row'].to_numpy()
    result=np.ascontiguousarray(encoded[indices],dtype=np.float32)
    assert result.shape==(len(mature),120)
    return result,{'all_supplied_same_date_cohort_rows':len(cohort),'mature_label_rows':len(mature),'dates':len(dates),
        'encoder_before_label_and_price_valid_filter':True,'stock_date_join_exact_and_unique':True,'raw63_bits_unchanged':True,'feature_names':encoder.names(raw_features)[0]}
