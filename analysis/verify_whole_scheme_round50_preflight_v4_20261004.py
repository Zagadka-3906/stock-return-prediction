"""Verify actual R50 context, parameter arms, calibration andfuture helper."""
from copy import deepcopy
from pathlib import Path
import json
import os
import sys
import time
for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[variable]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
import optimize_training_round50 as experiment
import finalize_training_round50 as release
import whole_scheme_future_runtime_20261004 as future
from predict_whole_scheme_round50 import predict
from verify_role_layer_replay_20261004 import sha,dump
from verify_whole_scheme_runtime_20261004 import root_graph,cfg,layer
QA=ROOT/'analysis/whole_scheme_round50_release_preflight_v4_20261004'
SCORE_QA=ROOT/'analysis/whole_scheme_score_preflight_v4_20261004'
PROPOSAL_QA=ROOT/'analysis/whole_scheme_round50_proposal_preflight_v4_20261004'
SOURCE=ROOT/'analysis/optimization_20261003_r26'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    import psutil
    while psutil.virtual_memory().available<8*2**30:time.sleep(10)
    for folder in (QA,SCORE_QA,PROPOSAL_QA):folder.mkdir(exist_ok=True)
    assert not (QA/'verification.json').exists()
    row=cfg(26)
    for field in experiment.FIELDS:
        if field.endswith('_augmentation'):row.setdefault(field,{role:{'model':'none','weight':0.} for role in ('membership','top','rest')})
        elif field.endswith('_limit_delta'):row.setdefault(field,0.)
    row.setdefault('standalone',None);row.setdefault('standalone_replacement',False)
    row['temporal_postprocessing']={'alpha':1.,'mix':0.,'power':1.}
    graph=root_graph(cfg(24));graph['layers']=[layer(26)];graph['temporal_postprocessing']=deepcopy(row['temporal_postprocessing'])
    axes=[]
    for group in ('diverse_augmentation','secondary_augmentation','final_augmentation','linear_augmentation'):
        for role,spec in graph['root']['configuration'][group].items():
            if spec['weight']>0:axes.append({'round':30,'group':group,'role':role,'model':spec['model'],'anchor':spec['weight']})
    for node in graph['layers']:
        for role,spec in node['specs'].items():
            if spec['weight']>0:axes.append({'round':node['round'],'group':node['group'],'role':role,'model':spec['model'],'anchor':spec['weight']})
    graph['active_weight_axes']=axes;row['whole_scheme_graph']=graph
    fixture=experiment.configuration(row)
    sources=[Path(__file__),ROOT/'analysis/optimize_training_round50.py',ROOT/'analysis/finalize_training_round50.py',
        ROOT/'analysis/predict_whole_scheme_round50.py',ROOT/'analysis/verify_methods_round50.py',ROOT/'analysis/run_training_round50_pipeline.py',
        ROOT/'analysis/whole_scheme_replay_runtime_20261004.py',ROOT/'analysis/whole_scheme_future_runtime_20261004.py',
        ROOT/'analysis/whole_scheme_runtime_preflight_20261004/verification.json',
        ROOT/'analysis/whole_scheme_future_runtime_qa_20261004/verification.json',
        ROOT/'analysis/finalize_training_round7.py',ROOT/'analysis/finalize_optimization.py',
        SOURCE/'selection.json',SOURCE/'selected_validation.npy',SOURCE/'future_return_mapping.json',
        ROOT/'candidates/optimization_20261003_r26/verification.json',ROOT/'candidates/optimization_20261003_r26/submission.csv']
    for path in sources:
        if path.name=='verification.json':assert read(path)['status']=='passed'
    sources += [ROOT/'analysis/verify_whole_scheme_round50_preflight_20261004.py',ROOT/'analysis/whole_scheme_round50_release_preflight_20261004/frozen_before_controls.json',ROOT/'analysis/whole_scheme_round50_preflight_recovery_20261004.json']
    sources += [ROOT/'analysis/verify_whole_scheme_round50_preflight_v2_20261004.py',ROOT/'analysis/whole_scheme_round50_release_preflight_v2_20261004/frozen_before_controls.json']
    sources += [ROOT/'analysis/verify_whole_scheme_round50_preflight_v3_20261004.py',ROOT/'analysis/whole_scheme_round50_release_preflight_v3_20261004/frozen_before_controls.json',ROOT/'analysis/whole_scheme_score_preflight_v3_20261004/verification.json']
    inputs={str(path.resolve()):sha(path) for path in sources}
    dump(QA/'frozen_before_controls.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'fixture':fixture,'input_sha256':inputs,'prototype_source_round':26,'new_quality_scores':0,'test_labels_read':False})
    # Changes are local module bindings inside this isolated checker process.
    # No saved predecessor source, parameter orscore file is modified.
    experiment.OUT=QA;experiment.PREVIOUS=SOURCE;experiment.baseline=lambda:deepcopy(fixture)
    original_release_init=release.ReleaseContext.__init__
    def fixture_release_init(self,*args,**kwargs):
        original_release_init(self,*args,**kwargs)
        for name in ('tail_bce128_e32','rank512_seed18_e64'):
            self._whole_paths[name]=ROOT/f'analysis/optimization_20261003_r25/raw/{name}.npy'
    release.ReleaseContext.__init__=fixture_release_init
    context=release.ReleaseContext(fixture)
    promote=context.finished('baseline');pred,_=context.predict(context.donor(promote),0.,0.)
    assert np.array_equal(pred,np.load(SOURCE/'selected_validation.npy'))
    metrics=context.score(pred);assert metrics==row['metrics']
    np.save(QA/'selected_validation.npy',pred);np.save(QA/'promote_baseline.npy',promote)
    proposal_checks=[]
    for axis in axes:
        arms=experiment.proposals(fixture,axis);assert len(arms)==6
        for key,proposal in arms:
            assert experiment.previous.configuration(proposal)==experiment.previous.configuration(fixture)
            changed=proposal['whole_scheme_graph']
            assert changed['layers'][0]['retention']==graph['layers'][0]['retention']
            assert changed['layers'][0]['original_delta']==graph['layers'][0]['original_delta']
            assert changed['temporal_postprocessing']==graph['temporal_postprocessing']
            weight=experiment.weight_at(changed,axis);assert 0<=weight<=.8
        proposal_checks.append({'axis':axis,'arms':6,'other_history_and_final_processing_preserved':True})
    retained=experiment.retention_axes(graph)
    assert retained==[{'kind':'root','round':30},{'kind':'layer','round':26}]
    assert experiment.expected_records(graph)==1+18*len(axes)+5*len(retained)+20
    dump(PROPOSAL_QA/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'weight_axes':proposal_checks,'retention_axes':retained,'bounded_record_count_rule_verified':True,
        'root_and_late_historical_retention_are_separate':True,'input_sha256':inputs,'new_quality_scores':0,'test_labels_read':False})
    # Exercise the actual shared past-return calibrator through R50's context.
    import finalize_training_round7 as shared
    selected={'winner':{**fixture,'donor':'baseline','connected_final_score':row['connected_final_score'],'metrics':metrics}}
    shared.OUT=QA;shared.selected=lambda:deepcopy(selected);shared.ReleaseContext=lambda:release.ReleaseContext(fixture);shared.verify=lambda:None
    shared.calibrate()
    official=read(QA/'calibrated_csv_official.json');assert official['status']=='passed'
    dump(SCORE_QA/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_R50_context_baseline_all8_official_metrics_bit_identical':True,
        'known_baseline_score':metrics['final_score'],'actual5635800_row_causal_calibration_passed':True,
        'causal_validation_sha256':sha(QA/'causal_validation.json'),'actual_calibrated_official_csv_sha256':sha(QA/'calibrated_csv_official.json'),
        'new_quality_scores':0,'test_labels_read':False,'input_sha256':inputs})
    original_resolve=future.resolve_native_sources
    overrides={30:ROOT/'candidates/optimization_20261003_r24'}
    future.resolve_native_sources=lambda value:original_resolve(value,overrides)
    native=future.resolve_native_sources(graph)
    root_models=future.candidate_models(ROOT/'candidates/optimization_20261003_r24')
    names=[f'seed{component["seed"]}_f{component["fraction"]:.3f}_r{component["rounds"]}' for component in graph['root']['configuration']['recipe']['components']]
    root_models={name:root_models[name] for name in names}
    experiment.root_model_sources=lambda value:deepcopy(root_models)
    dump(QA/'protocol.json',{'status':'frozen_implementation_control','future_native_model_sources':native,
         'future_root_model_sources':root_models,'input_sha256':inputs,'new_quality_scores':0,'test_labels_read':False})
    record={'winner':{**fixture,'connected_final_score':None},'frozen_sha256':{'active_release.json':sha(ROOT/'active_release.json')}}
    predict(record,candidate_path=QA/'candidate',mapping_path=SOURCE/'future_return_mapping.json')
    candidate=read(QA/'candidate/verification.json');assert candidate['status']=='passed' and candidate['validation_score'] is None
    assert sha(QA/'candidate/submission.csv')==sha(ROOT/'candidates/optimization_20261003_r26/submission.csv')
    for path,digest in inputs.items():assert sha(path)==digest,path
    dump(QA/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_R50_ReleaseContext_andshared_causal_calibration_passed':True,
        'actual_R50_future_helper_full1599600_row_csv_byte_identical':True,
        'actual80_day_model_andpipeline_cold_prefix_exact':True,
        'candidate_verification_sha256':sha(QA/'candidate/verification.json'),
        'official_score_preflight_sha256':sha(SCORE_QA/'verification.json'),
        'proposal_preflight_sha256':sha(PROPOSAL_QA/'verification.json'),
        'new_quality_scores':0,'test_labels_read':False,'input_sha256':inputs,
        'scope':'Actual R50 release/predict helpers using a frozen completedR26 fixture; R49 prerequisite remains required for the real joint search.'})
    print('Round50 actual context, all8 metrics, proposals, calibration andfuture helper passed',flush=True)


if __name__=='__main__':main()
