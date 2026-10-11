"""Actual failed constructor, native four workers andlater ancestry control."""
from pathlib import Path
from copy import deepcopy
import importlib
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
from late_context_initialization_recovery_20261004 import install,normalize,TARGETS
from verify_role_layer_replay_20261004 import sha,dump
OUT=ROOT/'analysis/late_context_initialization_recovery_20261004'
PREVIOUS=ROOT/'analysis/optimization_20261003_r28'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    sources=[Path(__file__),ROOT/'analysis/late_context_initialization_recovery_20261004.py',
        ROOT/'analysis/run_late_context_recovered_pipeline_20261004.py',
        ROOT/'analysis/late_context_recovery_sources_20261004.json',OUT/'round29_failed_state.json',
        ROOT/'analysis/parallel_candidate_scoring_four_20261004.py',PREVIOUS/'selection.json',PREVIOUS/'selected_validation.npy']
    sources += [ROOT/f'analysis/optimize_training_round{number}{suffix}.py'
        for number in TARGETS for suffix in ('','_context_recovery_20261004')]
    inputs={str(path.resolve()):sha(path) for path in sources}
    dump(OUT/'frozen_before_controls.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'input_sha256':inputs,'new_quality_scores':0,'test_labels_read':False})
    old=read(ROOT/'analysis/optimization_20261003_r23/selection.json')['winner']
    schemas=[]
    for number in TARGETS:
        module=importlib.import_module(f'optimize_training_round{number}')
        normalized=normalize(old,module.FIELDS)
        assert old=={key:normalized[key] for key in old}
        assert set(module.FIELDS).issubset(normalized)
        assert normalize(normalized,module.FIELDS) is normalized
        schemas.append({'round':number,'only_absent_typed_layer_fields_added':True,
                        'already_complete_configuration_passes_through_without_copy_or_change':True})
    module=install(29);ctx=module.Context();cfg=module.baseline()
    assert ctx._late_normalized_field_events and not ctx._late_constructor_warming
    ctx.configure(cfg);assert ctx._foundation_configuration==module.previous.configuration(cfg)
    pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),cfg['slow16_weight'],cfg['retention'],cfg['limit_up_delta'])
    assert np.array_equal(pred,np.load(PREVIOUS/'selected_validation.npy'))
    metrics=ctx.score(pred);assert metrics==read(PREVIOUS/'selection.json')['winner']['metrics']
    from parallel_candidate_scoring_four_20261004 import evaluate_many,shutdown
    jobs=[(f'constructor_control_{index}',deepcopy(cfg)) for index in range(4)]
    records=list(evaluate_many('optimize_training_round29',jobs,OUT))
    for key,row in records:assert row['metrics']==metrics
    shutdown('optimize_training_round29')
    worker_pids=sorted({row['parallel_execution']['worker_pid'] for key,row in records});assert len(worker_pids)==4
    print('ActualR29 constructor andfour official worker controls passed',flush=True)
    # This controlled later ancestry has no actual R30–32 winner yet.  It tests
    # inherited initialization only, with the already completed R28 fixture.
    fixture=read(PREVIOUS/'selection.json')['winner']
    for number in (30,31,32,33):
        current=importlib.import_module(f'optimize_training_round{number}')
        complete=normalize(fixture,current.FIELDS)
        current.OUT=OUT/f'prototype_round{number}';current.OUT.mkdir(exist_ok=True)
        current.PREVIOUS=PREVIOUS
        if hasattr(current,'FOUNDATION'):current.FOUNDATION=PREVIOUS
        current.baseline=lambda payload=deepcopy(complete),target=current:target.configuration(payload)
    later=install(33);future_context=later.Context()
    assert future_context._late_normalized_field_events and not future_context._late_constructor_warming
    future_cfg=later.baseline();future_context.configure(future_cfg)
    future_pred,_=future_context.predict(future_context.donor(future_context.finished('baseline')),
        future_cfg['slow16_weight'],future_cfg['retention'],future_cfg['limit_up_delta'])
    assert np.array_equal(future_pred,np.load(PREVIOUS/'selected_validation.npy'))
    for path,digest in inputs.items():assert sha(path)==digest,path
    dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_failed_R29_constructor_now_initializes':True,'actual5635800_row_previous_output_bit_identical':True,
        'all8_previous_official_metrics_exact':True,'native_four_worker_factory_metrics_exact':True,
        'worker_pids':worker_pids,'later_R33_inherited_constructor_fixture_passed':True,
        'later_R33_fixture_output_bit_identical':True,'schema_controls':schemas,
        'scope':'ActualR29 startup/scoring recovery andlater inheritance fixture; other pending rounds still require their real baseline/causal checks.',
        'new_quality_scores':0,'test_labels_read':False,'input_sha256':inputs})
    print('Constructor recovery controls passed',flush=True)


if __name__=='__main__':main()
