"""Admit actual nonflag controls and complete120 routes with real qualified baselines."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(15)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    for name in ('nonflag_residual_EmpiricalBayes64_native_bank10','nonflag_residual_EmpiricalBayes37_transform_preflight_v3',
      'CPU_HGB44_round112_full_registration_v2','nonflag_RidgeFine52_round128_full_registration_v1',
      'nonflag_RFF128StreamMid76_round129_full_registration_v1','all_forecast_percentiles_full_scoring_benchmark','cached_official_spearman_full12_benchmark'):
        closed(name)
    closed('exact_native_JSON_archive_runtime_full_preflight')
    import prepare_nonflag_EmpiricalBayes40_round130_sources_v1_20261007 as generator
    proof_path=A/'nonflag_EmpiricalBayes40_round130_source_admission_v1_20261007.json';assert not proof_path.exists()
    plan_path=A/'nonflag_EmpiricalBayes40_plan_20261007.json';plan=read(plan_path)
    controls_path=A/'nonflag_residual_EmpiricalBayes37_transform_preflight_20261007/verification.json';controls=read(controls_path)
    assert controls['status']=='passed_actual37_full5635800_nonflag_residual_Ridge_independent_CDF_and111_cold_controls' and len(controls['controls'])==37
    native_path=A/'nonflag_residual_EmpiricalBayes64_native_hook3_preflight_20261007/verification.json';native=read(native_path)
    assert len(native['records'])==3
    assert read(A/'nonflag_residual_EmpiricalBayes64_bank10_20261007/verification.json')['actual_native_fits']==10
    assert native['status']=='passed_actual3_historical603_nonflag_EmpiricalBayes64_native_reload_decoder_CDF_and_whole_day_prefix_controls'
    assert len(plan['single_native_heads'])==2 and len(plan['ensembles'])==1 and len(plan['weights'])==12 and plan['expected_scored_records']==40
    scorer=A/'run_nonflag_EmpiricalBayes40_official_comparison_v1_20261007.py';tree=ast.parse(scorer.read_text(encoding='utf8'))
    item=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in n.targets) and isinstance(n.value,ast.Dict))
    schema={k.value for k in item.keys if isinstance(k,ast.Constant)}
    sources=[Path(__file__),Path(generator.__file__),scorer,plan_path,controls_path,native_path,
      A/'publish_nonflag_EmpiricalBayes40_evidence_v1_20261007.py',A/'run_nonflag_EmpiricalBayes40_round130_full_registration_v1_20261007.py',
      A/'prepare_nonflag_EmpiricalBayes40_selected_candidate_v1_20261007.py',A/'seal_nonflag_EmpiricalBayes40_selected_candidate_v1_20261007.py',
      A/'predict_nonflag_residual_EmpiricalBayes_complete_scheme_20261007.py',A/'nonflag_residual_EmpiricalBayes64_native_stage_20261007.py',
      A/'nonflag_residual_HGB_CDF_transform_20261007.py',A/'nonflag_residual_HGB_preprocessing_20261007.py',
      A/'resolve_sealed_scientific_protocol_v2_20261007.py',A/'nonflag_residual_EmpiricalBayes64_bank10_20261007/verification.json',
      A/'nonflag_HGB40_complete_routes_source_preparation_v2_20261007.json',
      A/'all_forecast_percentile_runtime_20261007.py',A/'cached_official_spearman_runtime_20261007.py',
      *[A/f'github_validation_sync_main_20261005/round{n}_receipt.json' for n in (112,128,129)]]
    sources += [A/'exact_native_JSON_archive_runtime_20261007.py',A/'exact_native_pretty_JSON_archive_20261007.py',A/'exact_native_JSON_archive_runtime_full_preflight_20261007/runtime_verification.json',A/'handoff_nonflag_HGB40_archive_routes_v3_20261007.py',A/'nonflag_HGB40_archive_routes_v3_actual_handoff_20261007/verification.json']
    sources += [A/'nonflag_EmpiricalBayes40_round130_mapping_20261007.py',
      A/'nonflag_EmpiricalBayes40_science_route_preparation_v1_20261007.json',
      A/'nonflag_EmpiricalBayes40_prospective_routes_v2_20261007.json',
      A/'actual4_official_scoring_8_5GiB_gate_preflight_20261007/verification.json']
    sources += [A/'nonflag_EmpiricalBayes40_control_gate_recovery_v2_20261007.json',A/'nonflag_EmpiricalBayes40_prospective_routes_v3_20261007.json',A/'run_nonflag_EmpiricalBayes40_official_comparison_v2_20261007.py',A/'prepare_nonflag_EmpiricalBayes40_selected_candidate_v2_20261007.py',A/'publish_nonflag_EmpiricalBayes40_evidence_v2_20261007.py']
    sources += [A/'nonflag_EmpiricalBayes40_full_control_recovery_v3_20261007.json',A/'run_nonflag_EmpiricalBayes40_official_comparison_v3_20261007.py',A/'prepare_nonflag_EmpiricalBayes40_selected_candidate_v3_20261007.py',A/'publish_nonflag_EmpiricalBayes40_evidence_v3_20261007.py']
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    wrapper=(A/'predict_nonflag_residual_EmpiricalBayes_complete_scheme_20261007.py').read_text(encoding='utf8')
    seal=(A/'seal_nonflag_EmpiricalBayes40_selected_candidate_v1_20261007.py').read_text(encoding='utf8')
    status='passed_actual_complete_parent_and_nonflag_EmpiricalBayes64_two_full_replays_independent_and_cold80'
    assert repr(status) in wrapper and repr(status) in seal
    assert "candidate/'nonflag_residual_EmpiricalBayes64_native_replay_verification.json'" in seal
    candidate=(A/'prepare_nonflag_EmpiricalBayes40_selected_candidate_v1_20261007.py').read_text(encoding='utf8')
    assert "CANDIDATE=ROOT/'candidates/nonflag_EmpiricalBayes40_v1_20261007'" in candidate and 'expected_scored_records=40' in candidate
    assert "if not key.startswith(('nonflag_cpu_hgb_','nonflag_cpu_ridge_','nonflag_cpu_empirical_bayes64_','nonflag_cpu_rffridge_','nonflag_cpu_rff128_','nonflag_cpu_rff128low_','nonflag_cpu_rff128hi_'))" in candidate
    future={A/n for n in generator.NAMES.values()}|{proof_path,A/'nonflag_EmpiricalBayes40_round130_source_preparation_v1_20261007.json',
      A/'nonflag_EmpiricalBayes40_scores_github_v1_20261007/receipt.json',A/'nonflag_EmpiricalBayes40_selected_release_v1_20261007/selected_candidate_ready_for_registration.json'}
    outputs={};graph_controls=[];baseline_controls=[];path_controls=[]
    for parent in (112,128,129):
        generated=generator.generate(parent);outputs[str(parent)]={}
        for name,text in generated.items():
            assert not (A/name).exists(),name
            compile(text,str(A/name),'exec');outputs[str(parent)][name]=hashlib.sha256(text.encode('utf8')).hexdigest()
        name='register_nonflag_EmpiricalBayes40_round130_artifacts_20261007.py';text=generated[name];registry=ast.parse(text)
        required={n.slice.value for n in ast.walk(registry) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='measured' and isinstance(n.slice,ast.Constant)}
        assert required<=schema,required-schema
        assert "'round130_full_scope' / source.relative_to(ROOT)" in text
        body=next(n for n in registry.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
        assignment=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='sources' for t in n.targets))
        ns={'A':A,'ROOT':ROOT,'Path':Path,'__file__':str(A/name)}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[assignment],type_ignores=[])),name,'exec'),ns)
        for p in ns['sources']:assert p.is_file() or p in future,p
        path_controls.append({'parent':parent,'source_count':len(ns['sources']),'all_concrete_paths_checked':True})
        start=text.index("        if measured['case'] == pilot['best']['case']:");end=text.index('        row = ',start)
        graph_code=compile('if True:\n'+text[start:end],name,'exec')
        fake={'core':{'native_SHA':'preserved106'},'conditional_flag_CPU_HGB_residual_CDF':{'complete_flag_parent':'preserved'},'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'},'nonflag_CPU_Ridge_residual_CDF':{'old_Ridge':'remove'},'nonflag_CPU_RFFRidge_residual_CDF':{'old_RFF32':'remove'},'nonflag_CPU_RFF128_residual_CDF':{'old_RFF128':'remove'}}
        examples=[('remove_nonflag_EmpiricalBayes64',0.,[]),*[(n,.0125,[n]) for n in plan['single_native_heads']],*[(n,.0125,names) for n,names in plan['ensembles'].items()]]
        for model,weight,names in examples:
            measured={'case':7,'native_bank_source':'actual10','ordered_native_components':names}
            ns={'cfg':{'model':model,'weight':weight,'anchor_round':112,'universe':plan['universe']},'measured':measured,
              'pilot':{'best':{'case':8},'actual_scheme_base_round':112},'deepcopy':deepcopy,'ROOT':ROOT,'read':lambda path:{'whole_scheme_graph':fake}}
            exec(graph_code,ns);graph=ns['graph']
            assert graph['core']==fake['core'] and graph['conditional_flag_CPU_HGB_residual_CDF']==fake['conditional_flag_CPU_HGB_residual_CDF']
            assert 'nonflag_CPU_HGB_residual_CDF' not in graph and 'nonflag_CPU_Ridge_residual_CDF' not in graph and 'nonflag_CPU_RFFRidge_residual_CDF' not in graph and 'nonflag_CPU_RFF128_residual_CDF' not in graph
            if names:assert graph['nonflag_CPU_EmpiricalBayes64_residual_CDF']['ordered_equal_mean_components']==names
            else:assert 'nonflag_CPU_EmpiricalBayes64_residual_CDF' not in graph
            graph_controls.append({'parent':parent,'model':model,'flag_graph_preserved':True})
        baseline=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='comparison_baseline' for t in n.targets))
        update=next(n for n in body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and isinstance(n.value.func.value,ast.Name) and n.value.func.value.id=='selection' and n.value.func.attr=='update')
        parent_selection=A/f'optimization_20261003_r{parent}/selection.json';base_metrics=read(parent_selection)['winner']['metrics']
        assert read(A/f'optimization_20261003_r{parent}/full_registration_execution.json')['status']=='passed'
        for amplitude in (0.,1e-8,-4e-5):
            winner={'metrics':deepcopy(base_metrics)};winner['metrics']['ic_mean']+=amplitude/.4
            winner['connected_final_score']=.4*winner['metrics']['ic_mean']+.3*winner['metrics']['annual_excess']+.3*(1.-winner['metrics']['mean_turnover'])
            selection={};requested=[]
            def actual_read(path):
                assert Path(path)==parent_selection;requested.append(str(path));return {'winner':{'metrics':base_metrics}}
            ns={'A':A,'ROOT':ROOT,'read':actual_read,'sha':sha,'selection':selection,'winner':winner,'records':[],
              'pilot':{'actual_scheme_base_round':112},'selection_source':A/'optimization_20261003_r112/selection.json','GRAPH_FIELD':'conditional_flag_residual_scheme_graph','time':time}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[baseline,update],type_ignores=[])),name,'exec'),ns)
            gain=winner['connected_final_score']-base_metrics['final_score']
            assert requested==[str(parent_selection)] and selection['baseline_score']==base_metrics['final_score'] and selection['score_gain']==gain and selection['explicit_comparison_parent_round']==parent
            baseline_controls.append({'parent':parent,'synthetic_IC_amplitude':amplitude,'actual_gain':gain})
        pub=generated['publish_nonflag_EmpiricalBayes40_round130_full_validation_20261007.py']
        assert "actual_full_QA_version': 41" in pub and 'collect(130, 41, 40)' in pub and "namespace['snapshot'](130)" in pub
    assert len(graph_controls)==12 and len(baseline_controls)==9
    create(proof_path,{'status':'passed_actual37_controls_and24_prospective130_complete_source_schema_paths_and_graph_routes',
      'input_sha256':{str(p):sha(p) for p in sources},'generated_source_sha256':outputs,
      'graph_metadata_controls':graph_controls,'baseline_gain_regressions':baseline_controls,'source_path_controls':path_controls,
      'actual_full_transform_controls':37,'actual_cold_prefix_controls':111,'actual_historical_native_hook_cases':3,
      'actual_scoring_item_fields':sorted(schema),'declared_prospective_sources':24,
      'new_native_fits':0,'new_quality_scores':0,'full130_future_inference_and_QA41_not_yet_claimed':True,'test_labels_read':False})

if __name__=='__main__':main()
