"""Check feature-only adoption adapter on existing real TRAIN fixture; no model replay claim."""
from pathlib import Path
from types import SimpleNamespace
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    import numpy as np
    import cross120_after_complete169_native_stage_v2_20261010 as stage
    folder=Path('E:/赛题五_本机临时/daily_feature_encoder120_actual_TRAIN_controls_v1_20261010')
    info=read(folder/'verification.json');raw=np.load(folder/'raw63.npy');expected=np.load(folder/'encoded120.npy')
    dates=np.repeat(info['days'],4650);names=info['raw_names']
    meta={'raw_features':names,'features':info['encoded_names']}
    context=SimpleNamespace(dates=dates,_BF16_feature_names=names,_BF16_raw_features=raw,
                            valid=np.ones(len(raw),dtype=bool),flags=np.zeros(len(raw),dtype=bool))
    actual=stage.feature_matrix(context,meta)
    assert np.array_equal(actual.view('u4'),expected.view('u4'))
    assert context._BF16_feature_names is names and context._BF16_raw_features is raw
    context.valid[:]=False;context.flags[:]=True
    assert np.array_equal(stage.feature_matrix(context,meta).view('u4'),actual.view('u4'))
    cold=SimpleNamespace(dates=dates[:4650],_BF16_feature_names=names,_BF16_raw_features=raw[:4650])
    assert np.array_equal(stage.feature_matrix(cold,meta).view('u4'),actual[:4650].view('u4'))
    perm=np.random.default_rng(20261010).permutation(len(raw))
    shuffled=SimpleNamespace(dates=dates[perm],_BF16_feature_names=names,_BF16_raw_features=raw[perm])
    assert np.array_equal(stage.feature_matrix(shuffled,meta).view('u4'),actual[perm].view('u4'))
    incomplete=SimpleNamespace(dates=dates[:4649],_BF16_feature_names=names,_BF16_raw_features=raw[:4649])
    try:stage.feature_matrix(incomplete,meta)
    except AssertionError:pass
    else:raise AssertionError('Incomplete daily cohort accepted')
    paths=[Path(__file__),Path(stage.__file__),folder/'verification.json',folder/'raw63.npy',folder/'encoded120.npy']
    create(A/'cross120_after_complete169_context_encoder_actual_CPU_controls_v2_20261010.json',
           {'status':'passed_real13950_TRAIN_context_adapter_exact_independent_peer_ranks_without_parent_context_mutation',
            'rows':13950,'raw_feature_count':63,'encoded_feature_count':120,
            'price_and_flag_filter_invariance':True,'full_day_prefix_and_permutation_exact':True,
            'incomplete_daily_cohort_refused':True,'original_context_feature_arrays_unchanged':True,
            'input_sha256':{str(p):sha(p) for p in paths},'new_native_fits':0,'new_quality_scores':0,
            'actual_future_X_read':False,'test_labels_read':False,
            'actual_saved_GPU_model_and_complete169_callback_replays_still_required':True})
    print('PASS real13950 TRAIN context feature encoder; model and full parent replay pending',flush=True)

if __name__=='__main__':main()
