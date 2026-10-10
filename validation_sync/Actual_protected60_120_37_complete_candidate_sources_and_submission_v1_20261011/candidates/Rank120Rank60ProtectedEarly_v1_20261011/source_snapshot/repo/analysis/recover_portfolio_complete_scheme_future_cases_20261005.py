"""Complete the two declared portfolio future cases after retained fixture failure.

Reuse SHA-bound successful controls; do not change production sources or fits.
"""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import hashlib
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'analysis'),str(ROOT),str(ROOT/'analysis/connected_validation_20261002')]
OUT=ROOT/'analysis/portfolio_surrogate_complete_scheme_preflight_20261004'
RECOVERY=ROOT/'analysis/portfolio_surrogate_complete_scheme_recovery_20261005'
RUN=ROOT/'analysis/portfolio_surrogate_scheme_recovery_run_20261005.json'
SOURCE=ROOT/'analysis/optimization_20261003_r29'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def create(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2);stream.write('\n')


def main():
    while not RUN.exists():time.sleep(1)
    job=read(RUN);assert job['source_sha256']==sha(__file__)
    assert not (OUT/'verification.json').exists()
    assert not any((ROOT/f'analysis/optimization_20261003_r{n}/protocol.json').exists() for n in (59,60))
    original=read(OUT/'frozen_before_controls.json');inputs=deepcopy(original['input_sha256'])
    for path,digest in inputs.items():assert sha(path)==digest,path
    parameters=OUT/'parameter_andreplay_checks.json';values=read(parameters)
    assert values['status']=='passed' and values['new_quality_scores']==0
    assert len(values['new_role_cases'])==4 and len(values['role_controls'])==13 and len(values['standalone_controls'])==4
    old_job=read(ROOT/'analysis/portfolio_surrogate_scheme_qa_run_20261004.json')
    error_path=Path(old_job['stderr']);errors=error_path.read_text(encoding='utf-8',errors='replace')
    assert 'FileNotFoundError' in errors and 'optimization_20261003_r59' in errors
    import psutil
    if psutil.pid_exists(old_job['pid']):
        assert old_job['script'] not in psutil.Process(old_job['pid']).cmdline(),'original failed helper still running'
    expected_names=tuple(read(ROOT/'analysis/portfolio_surrogate_complete_output_search_plan_20261004.json')['model_configurations'])
    assert len(expected_names)==4
    corrected={'role_changed':expected_names[0],'pure_changed':expected_names[2]}
    original_helper=ROOT/'analysis/verify_portfolio_surrogate_complete_scheme_20261004.py'
    text=original_helper.read_text(encoding='utf-8')
    assert "'model':'rank1024_drop000_seed07_e32'" in text and "standalone_cfg('rank4096_drop000_seed07_e32')" in text
    baselines={}
    for label in ('role_baseline','standalone_baseline'):
        path=OUT/label/'candidate/verification.json';value=read(path)
        assert value['status']=='passed' and value['validation_score'] is None
        assert (value['rows'],value['days'],value['codes'])==(1599600,344,4650)
        assert value['csv_replay_byte_identical'] and value['cold80_day_prefix_bit_identical'] and not value['test_labels_read']
        assert sha(path.parent/'submission.csv')==value['csv_sha256']==sha(ROOT/'candidates/optimization_20261003_r29/submission.csv')
        baselines[label]=sha(path)
    calibration=OUT/'prototype_r59/calibrated_csv_official.json'
    assert read(calibration)['status']=='passed' and read(calibration)['metrics']==read(SOURCE/'selection.json')['winner']['metrics']
    additions=[Path(__file__),RUN,parameters,error_path,calibration,*[OUT/label/'candidate/verification.json' for label in baselines]]
    inputs.update({str(path.resolve()):sha(path) for path in additions})
    audit={'status':'frozen_before_remaining_actual_future_controls','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':inputs,'original_helper_retained':str(original_helper),
        'original_failure':'Two copied width-model fixture names were outside the declared portfolio bank; role_changed tried an uncreatedR59 candidate.',
        'corrected_declared_portfolio_models':corrected,'successful_parameter_andreplay_controls_reused':True,
        'successful_actual_written_CSV_calibration_reused':True,'successful_future_baseline_controls_reused':baselines,
        'production_algorithms_andtraining_andscoring_sources_unchanged':True,
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False}
    create(RECOVERY/'frozen_before_future_controls.json',audit)
    print('Frozen recovery: four-model parameter controls andtwo actual baselines retained; correcting only remaining declared-model fixture references.',flush=True)
    while psutil.virtual_memory().available<8*2**30:time.sleep(10)
    import optimize_training_round58 as parent
    import optimize_training_round59 as roles
    import optimize_training_round60 as pure
    from portfolio_surrogate_scheme_runtime_20261004 import append_role_layer,native_sources
    from predict_portfolio_surrogate_scheme_20261004 import predict
    from whole_scheme_future_runtime_20261004 import candidate_models
    from verify_whole_scheme_runtime_20261004 import root_graph
    from additive_basis_scheme_runtime_20261004 import append_role_layer as earlier
    from no_dropout_seed_scheme_runtime_20261004 import append_role_layer as prior
    from neural_interaction_scheme_runtime_20261004 import append_role_layer as interaction
    from neural_width_scheme_runtime_20261004 import append_role_layer as width
    assert tuple(roles.MODELS)==expected_names and tuple(pure.MODELS)==expected_names
    old=read(SOURCE/'selection.json')['winner'];origin=root_graph(old)
    origin['root']['configuration']=deepcopy(old);origin['temporal_postprocessing']={'alpha':1.,'mix':0.,'power':1.}
    base=deepcopy(old)
    for key in parent.FIELDS:
        if key.endswith('_augmentation'):base.setdefault(key,{role:{'model':'none','weight':0.} for role in roles.ROLES})
        elif key.endswith('_limit_delta'):base.setdefault(key,0.)
    base.setdefault('temporal_postprocessing',deepcopy(origin['temporal_postprocessing']));base['whole_scheme_graph']=origin
    base['basis_role_scheme_graph']=earlier(origin);base['basis_standalone_scheme_graph']=deepcopy(base['basis_role_scheme_graph'])
    base['no_dropout_role_scheme_graph']=prior(base['basis_standalone_scheme_graph']);base['no_dropout_standalone_scheme_graph']=deepcopy(base['no_dropout_role_scheme_graph'])
    base['neural_interaction_role_scheme_graph']=interaction(base['no_dropout_standalone_scheme_graph']);base['neural_interaction_standalone_scheme_graph']=deepcopy(base['neural_interaction_role_scheme_graph'])
    base['neural_width_role_scheme_graph']=width(base['neural_interaction_standalone_scheme_graph']);base['neural_width_standalone_scheme_graph']=deepcopy(base['neural_width_role_scheme_graph'])
    fixture={**parent.configuration(base),'portfolio_surrogate_role_scheme_graph':append_role_layer(base['neural_width_standalone_scheme_graph'])}
    fixture60={**deepcopy(fixture),'portfolio_surrogate_standalone_scheme_graph':deepcopy(fixture['portfolio_surrogate_role_scheme_graph'])}
    roots=candidate_models(ROOT/'candidates/optimization_20261003_r29')
    names=[f'seed{item["seed"]}_f{item["fraction"]:.3f}_r{item["rounds"]}' for item in origin['root']['configuration']['recipe']['components']]
    roots={name:roots[name] for name in names}
    for module,cfg in ((roles,fixture),(pure,fixture60)):
        module.OUT=OUT/f'prototype_r{module.NUMBER}';module.PREVIOUS=SOURCE
        module.baseline=lambda value=deepcopy(cfg):deepcopy(value)
        module.future_native_sources=lambda graph:native_sources(graph,{30:ROOT/'candidates/optimization_20261003_r29'})
        module.root_model_sources=lambda graph:{} if graph['root']['kind']=='standalone' else deepcopy(roots)
    assert roles.graph(fixture)==read(OUT/'role_baseline/candidate/verification.json')['whole_scheme_graph']
    assert pure.graph(fixture60)==read(OUT/'standalone_baseline/candidate/verification.json')['whole_scheme_graph']
    role_cfg=deepcopy(fixture);roles.node(role_cfg)['specs']['rest']={'model':corrected['role_changed'],'weight':.025}
    pure_cfg=pure.standalone_cfg(corrected['pure_changed'])
    completed={**baselines}
    for label,module,cfg in (('role_changed',roles,role_cfg),('pure_changed',pure,pure_cfg)):
        destination=OUT/label;destination.mkdir(exist_ok=True);module.OUT=destination
        graph=module.graph(cfg);native=module.future_native_sources(graph);root_sources=module.root_model_sources(graph)
        assert corrected[label] in native
        module.dump(destination/'protocol.json',{'status':'frozen_implementation_control','input_sha256':inputs,
            'future_native_model_sources':native,'future_root_model_sources':root_sources,
            'fixture_reference_recovery':str((RECOVERY/'frozen_before_future_controls.json').resolve()),
            'new_quality_scores':0,'test_labels_read':False},immutable=True)
        record={'winner':{**cfg,'connected_final_score':None},'frozen_sha256':{'active_release.json':sha(ROOT/'active_release.json')}}
        predict(module,record,candidate_path=destination/'candidate',mapping_path=SOURCE/'future_return_mapping.json')
        path=destination/'candidate/verification.json';value=read(path)
        assert value['status']=='passed' and value['validation_score'] is None
        assert (value['rows'],value['days'],value['codes'])==(1599600,344,4650)
        assert value['model_reload_bit_identical'] and value['csv_replay_byte_identical'] and value['cold80_day_prefix_bit_identical'] and not value['test_labels_read']
        assert sha(path.parent/'submission.csv')==value['csv_sha256']
        completed[label]=sha(path);print('Actual corrected future case passed: '+label+' / '+corrected[label],flush=True)
    for path,digest in inputs.items():assert sha(path)==digest,path
    create(RECOVERY/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'corrected_declared_models':corrected,'actual_corrected_future_cases':2,
        'all_four_actual_future_case_sha256':completed,'input_sha256':inputs,
        'original_failed_sources_logs_andpassed_partial_proofs_retained':True,
        'production_algorithms_andtraining_andscoring_sources_unchanged':True,
        'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_new_contexts_complete5635800_row_prior_output_andall8_metrics_exact':True,
        'all4_new_native_models_each_role_cold_prefix_controls_passed':True,
        'actual_standalone_branch_replacement_andindependent_composition_checks_passed':True,
        'actual_release_context_shared_causal_calibration_passed':True,
        'actual_new_future_helper_full1599600_row_baseline_CSV_byte_identical':True,
        'actual_changed_role_andnative_standalone_copied_model_future_CSV_andcold80_day_checks_passed':True,
        'candidate_verification_sha256':completed,'parameter_replay_sha256':sha(parameters),'input_sha256':inputs,
        'versioned_fixture_recovery_evidence':str((RECOVERY/'verification.json').resolve()),
        'versioned_fixture_recovery_evidence_sha256':sha(RECOVERY/'verification.json'),
        'new_quality_scores':0,'test_labels_read':False,
        'scope':'Aggregate completedR29 controls: retained passed four-model past/parameter/calibration/baseline stages andtwo recovered declared-portfolio future cases. ActualR58/R59 predecessor quality searches remain required.'})
    print('Aggregate portfolio complete-scheme controls passed after retained fixture-reference recovery.',flush=True)


if __name__=='__main__':main()
