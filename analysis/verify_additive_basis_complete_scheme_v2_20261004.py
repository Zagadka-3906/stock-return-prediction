"""Actual new scheme contexts, complete causal calibration andfuture CSV controls."""
from pathlib import Path
from copy import deepcopy
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'analysis'),str(ROOT),str(ROOT/'analysis/connected_validation_20261002')]
OUT=ROOT/'analysis/additive_basis_complete_scheme_preflight_v2_20261004'
SOURCE=ROOT/'analysis/optimization_20261003_r29'


def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    gates=[ROOT/'analysis/additive_basis_bank_20261004/oof_audit.json',
        ROOT/'analysis/additive_basis_future_models_qa_20261004/verification.json']
    while not all(path.exists() for path in gates):time.sleep(10)
    for path in gates:assert read(path)['status']=='passed'
    import gc
    import psutil
    while psutil.virtual_memory().available<8*2**30:time.sleep(10)
    import numpy as np
    import polars as pl
    import optimize_training_round50 as parent
    import optimize_training_round51 as roles
    import optimize_training_round52 as pure
    import finalize_training_round51 as release
    from additive_basis_scheme_runtime_20261004 import (
        append_role_layer,standalone_graph,prepare_raw,native_sources,cumulative_delta)
    from predict_additive_basis_scheme_20261004 import predict
    from verify_whole_scheme_runtime_20261004 import root_graph
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    old=read(SOURCE/'selection.json')['winner'];origin=root_graph(old)
    origin['root']['configuration']=deepcopy(old)
    origin['temporal_postprocessing']={'alpha':1.,'mix':0.,'power':1.}
    base=deepcopy(old)
    for key in parent.FIELDS:
        if key.endswith('_augmentation'):base.setdefault(key,{role:{'model':'none','weight':0.} for role in roles.ROLES})
        elif key.endswith('_limit_delta'):base.setdefault(key,0.)
    base.setdefault('temporal_postprocessing',deepcopy(origin['temporal_postprocessing']));base['whole_scheme_graph']=origin
    fixture={**parent.configuration(base),'basis_role_scheme_graph':append_role_layer(origin)}
    fixture52={**deepcopy(fixture),'basis_standalone_scheme_graph':deepcopy(fixture['basis_role_scheme_graph'])}
    scripts=('additive_basis_scheme_runtime_20261004.py','additive_basis_search_engine_20261004.py',
        'additive_basis_release_engine_20261004.py','predict_additive_basis_scheme_20261004.py',
        'check_additive_basis_scheme_20261004.py','run_additive_basis_round_pipeline_20261004.py',
        'optimize_training_round51.py','optimize_training_round52.py','finalize_training_round51.py',
        'finalize_training_round52.py','run_training_round51_pipeline.py','run_training_round52_pipeline.py')
    sources=[Path(__file__),*[ROOT/'analysis'/name for name in scripts],*gates,
        ROOT/'analysis/additive_basis_bank_20261004/protocol.json',
        ROOT/'analysis/whole_scheme_runtime_preflight_20261004/verification.json',
        ROOT/'analysis/whole_scheme_future_runtime_qa_20261004/verification.json',
        SOURCE/'selection.json',SOURCE/'selected_validation.npy',SOURCE/'future_return_mapping.json',
        ROOT/'candidates/optimization_20261003_r29/verification.json',
        ROOT/'candidates/optimization_20261003_r29/submission.csv']
    sources += [ROOT/'analysis/verify_additive_basis_complete_scheme_20261004.py',ROOT/'analysis/additive_basis_complete_scheme_preflight_20261004/frozen_before_controls.json',ROOT/'analysis/additive_basis_search_generator_preflight_20261004/verification.json',ROOT/'analysis/additive_basis_search_execution_20261004.json']
    inputs={str(path.resolve()):roles.sha(path) for path in sources}
    roles.dump(OUT/'frozen_before_controls.json',{'status':'frozen_implementation_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':inputs,'prototype_source_round':29,
        'new_quality_scores':0,'test_labels_read':False},immutable=True)
    for module,cfg in ((roles,fixture),(pure,fixture52)):
        module.OUT=OUT/f'prototype_r{module.NUMBER}';module.OUT.mkdir(exist_ok=True)
        module.PREVIOUS=SOURCE;module.baseline=lambda value=deepcopy(cfg):deepcopy(value)
    # All source arrays use actual mature fold model outputs, never labels.
    paths=prepare_raw(roles.OUT);pure_paths=prepare_raw(pure.OUT)
    ctx=roles.Context();pred,_=ctx.predict(ctx.donor(ctx.finished('baseline')),0.,0.)
    assert np.array_equal(pred,np.load(SOURCE/'selected_validation.npy'))
    assert ctx.score(pred)==old['metrics']
    controls=[roles.prefix_controls(ctx,fixture)];scopes=[]
    for target in ('y_rank','y_ret_1d'):
        for layout in ('narrow','wide5'):
            name=next(name for name,cfg in roles.trainer.CONFIGS.items() if cfg['target']==target and cfg['basis_layout']==layout)
            for role in roles.ROLES:
                candidate=deepcopy(fixture);roles.node(candidate)['specs'][role]={'model':name,'weight':.025}
                assert parent.configuration(candidate)==parent.configuration(fixture)
                assert candidate['basis_role_scheme_graph']['root']==origin['root']
                assert candidate['basis_role_scheme_graph']['layers'][:-1]==origin['layers']
                assert candidate['basis_role_scheme_graph']['temporal_postprocessing']==origin['temporal_postprocessing']
                controls.append(roles.prefix_controls(ctx,candidate,counts=(80,260)))
            scopes.append({'target':target,'layout':layout,'all_three_roles_checked':True})
    assert cumulative_delta(origin)==old['limit_up_delta']+old['final_limit_delta']+old['linear_limit_delta']
    ctx=None;gc.collect()
    c=pure.Context();pred,_=c.predict(c.donor(c.finished('baseline')),0.,0.);assert np.array_equal(pred,np.load(SOURCE/'selected_validation.npy'))
    standalone_controls=[]
    for target in ('y_rank','y_ret_1d'):
        for layout in ('narrow','wide5'):
            name=next(name for name,cfg in roles.trainer.CONFIGS.items() if cfg['target']==target and cfg['basis_layout']==layout)
            cfg=pure.standalone_cfg(name);graph=pure.graph(cfg)
            assert roles.configuration(cfg)==roles.configuration(fixture52)
            assert graph['root']['round']==52 and graph['root']['kind']=='standalone' and graph['layers']==[]
            assert all(not any(spec['weight']>0 for spec in value.values()) for key,value in graph['root']['configuration'].items() if key.endswith('_augmentation'))
            assert graph['temporal_postprocessing']==origin['temporal_postprocessing']
            standalone_controls.append(pure.prefix_controls(c,cfg))
            # Independent composition using the actual native fold source.
            from src.scoring import Panel
            from optimize_wave6 import make_prediction_param
            from optimize_wave13 import build_ab
            c.configure(cfg);raw=np.load(pure_paths[name],mmap_mode='r')
            post=graph['root']['configuration']['standalone']['postprocessing']
            p=make_prediction_param(Panel.from_frame(c.label_free.with_columns(pl.Series('pred_raw',raw))),c.label_free['aux_raw'].to_numpy(),**post)
            ordered=np.where(p>-9,p+1e-9*c.tie_key,p);reference,_=build_ab(ordered,ordered,ordered,c.dates,c.flags,c.codes,c.n_codes,.98)
            reference[c.flags==1]+=.075
            actual,_=c.predict(c.donor(c.finished('baseline')),0.,0.);assert np.array_equal(actual,reference)
    # Switching back must restore the actual whole predecessor, with no stale donor.
    c.configure(fixture52);assert np.array_equal(c.predict(c.donor(c.finished('baseline')),0.,0.)[0],np.load(SOURCE/'selected_validation.npy'))
    assert c.score(c.predict(c.donor(c.finished('baseline')),0.,0.)[0])==old['metrics']
    c=None;gc.collect()
    roles.dump(OUT/'parameter_andreplay_checks.json',{'status':'passed','new_role_cases':scopes,
        'role_controls':controls,'standalone_controls':standalone_controls,
        'actual_prior5635800_row_vector_andall8_metrics_exact':True,
        'four_independent_actual_native_standalone_compositions_exact':True,
        'switching_back_to_complete_predecessor_bit_identical':True,
        'bounded_arm_counts':{'51':[145,8,18,25],'52':[73,168,17]},
        'new_quality_scores':0,'test_labels_read':False},immutable=True)
    # Exercise the actual release class andshared causal return calibrator.
    import finalize_training_round7 as shared
    selected={'winner':{**fixture,'donor':'baseline','connected_final_score':old['connected_final_score'],'metrics':old['metrics']}}
    shared.OUT=roles.OUT;shared.selected=lambda:deepcopy(selected)
    shared.ReleaseContext=lambda:release.ReleaseContext(deepcopy(selected['winner']));shared.verify=lambda:None
    np.save(roles.OUT/'selected_validation.npy',np.load(SOURCE/'selected_validation.npy'))
    shared.calibrate();assert read(roles.OUT/'calibrated_csv_official.json')['status']=='passed'
    # Freeze actual model sources before reading future X in the new helper.
    from whole_scheme_future_runtime_20261004 import candidate_models
    root_models=candidate_models(ROOT/'candidates/optimization_20261003_r29')
    names=[f'seed{item["seed"]}_f{item["fraction"]:.3f}_r{item["rounds"]}' for item in origin['root']['configuration']['recipe']['components']]
    root_models={name:root_models[name] for name in names}
    for module in (roles,pure):
        module.future_native_sources=lambda g:native_sources(g,{30:ROOT/'candidates/optimization_20261003_r29'})
        module.root_model_sources=lambda g:{} if g['root']['kind']=='standalone' else deepcopy(root_models)
    cases=[('role_baseline',roles,fixture),('standalone_baseline',pure,fixture52)]
    for module,cfg,label in ((roles,fixture,'role_changed'),(pure,fixture52,'pure_changed')):
        changed=deepcopy(cfg)
        if module.NUMBER==51:roles.node(changed)['specs']['rest']={'model':roles.MODELS[0],'weight':.025}
        else:changed=module.standalone_cfg(next(name for name in pure.MODELS if 'wide5' in name))
        cases.append((label,module,changed))
    for label,module,cfg in cases:
        destination=OUT/label;destination.mkdir(exist_ok=True);module.OUT=destination
        graph=module.graph(cfg);native=module.future_native_sources(graph);roots=module.root_model_sources(graph)
        module.dump(destination/'protocol.json',{'status':'frozen_implementation_control','input_sha256':inputs,
            'future_native_model_sources':native,'future_root_model_sources':roots,'new_quality_scores':0,'test_labels_read':False},immutable=True)
        record={'winner':{**cfg,'connected_final_score':None},'frozen_sha256':{'active_release.json':module.sha(ROOT/'active_release.json')}}
        predict(module,record,candidate_path=destination/'candidate',mapping_path=SOURCE/'future_return_mapping.json')
        verification=read(destination/'candidate/verification.json');assert verification['status']=='passed' and verification['validation_score'] is None
        if label.endswith('baseline'):assert module.sha(destination/'candidate/submission.csv')==module.sha(ROOT/'candidates/optimization_20261003_r29/submission.csv')
    for path,digest in inputs.items():assert roles.sha(path)==digest,path
    roles.dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_new_contexts_complete5635800_row_prior_output_andall8_metrics_exact':True,
        'new_role_each_target_layout_androle_cold_prefix_controls_passed':True,
        'actual_standalone_branch_replacement_andindependent_composition_checks_passed':True,
        'actual_release_context_shared_causal_calibration_passed':True,
        'actual_new_future_helper_full1599600_row_baseline_CSV_byte_identical':True,
        'actual_changed_role_andnative_standalone_copied_model_future_CSV_andcold80_day_checks_passed':True,
        'candidate_verification_sha256':{label:roles.sha(OUT/label/'candidate/verification.json') for label,_,_ in cases},
        'parameter_replay_sha256':roles.sha(OUT/'parameter_andreplay_checks.json'),'input_sha256':inputs,
        'new_quality_scores':0,'test_labels_read':False,
        'scope':'Actual new helpers using completedR29 andall12 native basis models; realR50/R51 predecessors still required for actual official searches.'},immutable=True)
    print('Complete additive role/standalone scheme controls passed',flush=True)


if __name__=='__main__':main()
