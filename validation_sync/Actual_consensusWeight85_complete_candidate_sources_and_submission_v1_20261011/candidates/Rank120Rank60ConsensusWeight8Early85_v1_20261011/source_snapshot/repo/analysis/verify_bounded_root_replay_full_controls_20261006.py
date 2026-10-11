"""Full matched replay benchmark; guard admission before loading real contexts."""
from pathlib import Path
from copy import deepcopy
import argparse
import gc
import json
import os
import sys
import time

import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=A/'bounded_root_replay_full_controls_20261006'

def admission():
    return {'available_host_bytes':psutil.virtual_memory().available,'required_admission_bytes':14*2**30,
        'minimum_D_free_bytes':2*2**30,'D_free_bytes':psutil.disk_usage('D:/').free,
        'guard_is_scheduling_policy_not_physical_exhaustion':True}

def main(execute=False):
    current=admission()
    if not execute:
        print(json.dumps({'status':'full_control_not_started_readonly_admission_probe',**current,
            'admitted':current['available_host_bytes']>=current['required_admission_bytes'] and current['D_free_bytes']>=current['minimum_D_free_bytes'],
            'new_quality_scores':0},ensure_ascii=False),flush=True)
        return
    assert current['available_host_bytes']>=current['required_admission_bytes'],current
    assert current['D_free_bytes']>=current['minimum_D_free_bytes'],current
    assert not OUT.exists();OUT.mkdir()
    scratch=ROOT/'tmp/bounded_root_replay_full_controls_20261006';scratch.mkdir(exist_ok=True)
    for variable in ('TMP','TEMP','TMPDIR'):os.environ[variable]=str(scratch)
    import numpy as np
    import polars as pl
    import optimize_training_round95_v3 as ns
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    from bounded_root_replay_memoization_20261006 import enable,statistics,MAXIMUM_BYTES
    from whole_scheme_replay_runtime_20261004 import slice_context
    import standalone_root_source_adapter_20261005 as root_adapter
    import optimize_training_round50 as root_sources
    restore=root_adapter.install(root_sources)
    ns.root_model_sources=root_sources.root_model_sources
    protocol=read(ns.OUT/'protocol.json');audit=read(ns.OUT/'component_audit.json')
    assert audit['status']=='passed'
    first=read(ns.OUT/'wave371_results.json');second=read(ns.OUT/'wave372_results.json')
    assert first['status']==second['status']=='complete'
    base=ns.configuration(first['results']['baseline'])
    cases=[('baseline',first['results']['baseline'])]
    for role in ns.ROLES:
        choices=[(key,row) for key,row in first['results'].items() if ns.node(row)['specs'][role]['weight']>0]
        key,row=max(choices,key=lambda item:item[1]['connected_final_score'])
        cases.append((role+'_'+key,row))
    compound=[(key,row) for key,row in second['results'].items() if sum(s['weight']>0 for s in ns.node(row)['specs'].values())==3]
    assert len(compound)==1;cases.append(('compound_'+compound[0][0],compound[0][1]))
    sources=[Path(__file__),A/'bounded_root_replay_memoization_20261006.py',
        A/'bounded_root_replay_memoization_semantic_controls_20261006/verification.json',
        ns.OUT/'protocol.json',ns.OUT/'component_audit.json',ns.OUT/'wave371_results.json',ns.OUT/'wave372_results.json',
        A/'standalone_root_source_adapter_20261005.py',A/'locked_read_hash_cache_20261004.py']
    pins={**protocol['input_sha256'],**audit['output_sha256'],**{str(p):sha(p) for p in sources}}
    pins.update({row['official_score_cache']['official_metrics_source']:sha(row['official_score_cache']['official_metrics_source']) for key,row in cases})
    create(OUT/'frozen_before_full_controls.json',{'status':'frozen_before_actual5635800_row_root_cache_controls',
        'input_sha256':pins,'admission':current,'cases':[{'key':key,'configuration':ns.configuration(row),'reference_metrics':row['metrics']} for key,row in cases],
        'expected_shape':[5635800,1212,4650],'maximum_retained_payload_bytes':MAXIMUM_BYTES,
        'warm_same_cases_timed_after_one_cold_baseline':True,'new_model_fits':0,'new_quality_records':0,'test_labels_read':False})
    measurements=[]
    try:
        with LockedReadHashCache(pins):
            ctx=ns.Context(fixture=base,scoring=OUT/'scoring_validation_only')
            assert (len(ctx.dates),len(np.unique(ctx.dates)),ctx.n_codes)==(5635800,1212,4650)
            original_class=type(ctx)
            for index,(key,row) in enumerate(cases):
                cfg=ns.configuration(row);ctx.configure(cfg)
                ctx._whole_signal_cache.clear();ctx._whole_regime_cache.clear()
                started=time.perf_counter();prediction,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.)
                elapsed=time.perf_counter()-started
                assert ctx.score(prediction)==row['metrics']
                target=OUT/f'reference_prediction_{index}.npy';np.save(target,prediction)
                measurements.append({'key':key,'uncached_prediction_seconds':elapsed,
                    'reference_prediction_sha256':sha(target),'reference_stats':stats,
                    'reference_metric_capsule':row['official_score_cache']['official_metrics_source']})
                del prediction;gc.collect()
            enable(ctx,pins)
            for index,(key,row) in enumerate(cases):
                ctx.configure(ns.configuration(row));ctx._whole_signal_cache.clear();ctx._whole_regime_cache.clear()
                before=statistics(ctx);started=time.perf_counter()
                prediction,stats=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.)
                elapsed=time.perf_counter()-started
                assert np.array_equal(prediction,np.load(OUT/f'reference_prediction_{index}.npy',mmap_mode='r'))
                assert stats==measurements[index]['reference_stats']
                assert ctx.score(prediction)==row['metrics']
                measurements[index].update(cached_prediction_seconds=elapsed,before_cache=before,after_cache=statistics(ctx),
                    all5635800_prediction_values_bit_identical=True,all8_original_official_metrics_exact=True)
                del prediction;gc.collect()
            cfg=ns.configuration(cases[-1][1]);ctx.configure(cfg)
            full,_=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.)
            dates=np.unique(ctx.dates);prefixes=[]
            for days in (80,260):
                n=int(np.searchsorted(ctx.dates,dates[days-1],side='right'))
                prefix=slice_context(ctx,n,cold=True)
                assert statistics(prefix)=={'cold_owner':True}
                predicted,_=prefix.predict(prefix.donor(prefix.finished('baseline')),0.,0.)
                assert np.array_equal(predicted,full[:n])
                prefixes.append({'days':days,'rows':n,'cold_cache_and_full_prefix_bit_identical':True,'actual_cache':statistics(prefix)})
                del prefix,predicted
            from copy import copy
            poisoned=copy(ctx);poisoned.frame=ctx.frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
            poisoned._whole_base=copy(ctx._whole_base)
            poisoned._whole_base.frame=ctx._whole_base.frame.with_columns(pl.lit(float('nan')).alias('y_ret_1d'))
            assert statistics(poisoned)=={'cold_owner':True}
            assert np.array_equal(full,poisoned.predict(poisoned.donor(poisoned.finished('baseline')),0.,0.)[0])
            mutation=deepcopy(cfg);ns.graph(mutation)['root']['configuration']['retention']=.95
            ctx.configure(mutation);memoized_class=type(ctx);ctx.__class__=original_class
            changed,_=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.)
            ctx.__class__=memoized_class;before=statistics(ctx).get('misses',0)
            actual,_=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.)
            assert np.array_equal(changed,actual) and statistics(ctx)['misses']>before
            del full,poisoned,changed,actual;gc.collect()
            assert statistics(ctx)['retained_payload_bytes']<=MAXIMUM_BYTES
            warm_old=float(np.median([r['uncached_prediction_seconds'] for r in measurements[1:]]))
            warm_new=float(np.median([r['cached_prediction_seconds'] for r in measurements[1:]]))
            proof={'status':'passed_actual_full_root_cache_bits8_metrics_cold_prefix_poisoning_and_root_mutation_controls',
                'input_sha256':pins,'actual_rows':5635800,'actual_days':1212,'actual_codes':4650,
                'all5_reference_configurations':measurements,'actual_cold_prefix_controls':prefixes,
                'full_poisoned_labels_bit_identical_with_separate_cold_owner':True,
                'changed_root_forces_recomputation_and_matches_original_full_output':True,
                'warm_prediction_median_original_seconds':warm_old,'warm_prediction_median_cached_seconds':warm_new,
                'warm_prediction_median_improved':warm_new<warm_old,'actual_final_cache':statistics(ctx),
                'runtime_adopted':False,'separate_actual_unstarted_workflow_adoption_required':True,
                'actual_candidate_inference_implementation_not_patched_by_this_instance_cache':True,
                'new_model_fits':0,'new_quality_records':0,'new_quality_scores':0,'test_labels_read':False,
                'original124_record_R95_grid_and_all_frozen_sources_unchanged':True,
                'global_resource_exhaustion_established':False}
            create(OUT/'verification.json',proof)
            print(json.dumps({k:proof[k] for k in ('status','warm_prediction_median_original_seconds','warm_prediction_median_cached_seconds','warm_prediction_median_improved')},ensure_ascii=False),flush=True)
    finally:restore()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');args=parser.parse_args()
    try:main(args.execute)
    except BaseException as exc:
        if OUT.exists() and not (OUT/'failure.json').exists():create(OUT/'failure.json',{'status':'failed_preserved_actual_root_cache_full_control','error':f'{type(exc).__name__}: {exc}'})
        raise
