"""Independently align real49153 mature labels to Pandas ranks of all supplied peer rows."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    import numpy as np,polars as pl
    import daily_cross_sectional_feature_encoder120_v1_20261010 as encoder
    import mature_population_cross120_training_matrix_v1_20261010 as population
    import recent252_forward5_mature_training_population_v1_20261010 as labels
    import neural_BF16_medium2048_cross120recent252forward5huber050_seed09_e64_native_v1_20261009 as native
    from run import FEATURE_FILE,feature_names,to_matrix
    raw_names=feature_names();keys=['ts_code','trade_date'];lazy=pl.scan_parquet(FEATURE_FILE)
    mature=labels.training_frame(lazy,20191231,native.CONFIG).select(keys+raw_names+['y_ret_5mean','label_end_5d']).limit(49153).collect()
    dates=mature['trade_date'].unique().to_list()
    peers=lazy.filter(pl.col('is_train')&pl.col('trade_date').is_in(dates)).select(keys+raw_names).sort('trade_date','ts_code').collect()
    oracle=encoder.pandas_oracle(to_matrix(peers,raw_names),peers['trade_date'].to_numpy(),raw_names)
    # A Python tuple dictionary is independent of the production Polars row-index join.
    lookup={tuple(key):i for i,key in enumerate(peers.select(keys).rows())};assert len(lookup)==len(peers)
    expected=oracle[[lookup[tuple(key)] for key in mature.select(keys).rows()]]
    folder=Path(read(A/'actual_Cross120Recent252Forward5Huber050_past_fixture_location_v2_20261010.json')['output'])
    actual=np.load(folder/'past_features.npy');targets=np.load(folder/'past_return_targets.npy')
    assert np.array_equal(actual.view('u4'),expected.view('u4'))
    assert np.array_equal(targets.view('u8'),mature['y_ret_5mean'].to_numpy().view('u8'))
    reversed_frame=mature.head(127)[np.arange(126,-1,-1)];replayed,meta=population.matrix(lazy,reversed_frame,raw_names)
    assert np.array_equal(replayed.view('u4'),expected[:127][::-1].view('u4'))
    bad=pl.concat([mature.head(2),mature.head(1)])
    try:population.matrix(lazy,bad,raw_names)
    except AssertionError:pass
    else:raise AssertionError('Duplicate training keys accepted')
    missing=mature.head(1).with_columns(pl.lit('not_a_supplied_stock').alias('ts_code'))
    try:population.matrix(lazy,missing,raw_names)
    except AssertionError:pass
    else:raise AssertionError('Absent forecast key accepted')
    create(A/'cross120_real49153_mature_fixture_alignment_actual_CPU_controls_v1_20261010.json',{
        'status':'passed_actual49153_stock_date_dictionary_and_independent_Pandas_peer_ranks_targets_exact_reversed127_duplicate_and_missing_key_refusals',
        'rows':49153,'all_supplied_cohort_rows':len(peers),'actual_same_date_cohort_dates':len(dates),'input_feature_count':120,
        'encoded_before_target_and_price_valid_filter':True,'independent_tuple_lookup_Pandas_feature_bits_exact':True,
        'provided_mature_label_bits_exact':True,'reversed127_rows_exact':True,'duplicate_and_absent_stock_date_keys_rejected':True,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(encoder.__file__),Path(population.__file__),Path(labels.__file__),Path(native.__file__),folder/'verification.json',folder/'past_features.npy',folder/'past_return_targets.npy']},
        'GPU_used':False,'new_native_fits':0,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False})
    print({'actual_mature_rows':49153,'full_peer_rows':len(peers),'encoded_feature_count':120,'Pandas_and_stock_date_dictionary_exact':True},flush=True)
if __name__=='__main__':main()
