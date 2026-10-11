"""Admit actual25 controls and prospective complete118 routes before official28 work."""
from pathlib import Path
from copy import deepcopy
import ast
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def closed(name):
    service=A/'service_owned_workflows_20261006'/name
    while not (service/'native_launch.json').exists() or owned(read(service/'native_launch.json')):time.sleep(15)
    assert read(service/'service_execution.json')['status']=='passed',name

def main():
    closed('quantile_HGB_full85_transform_preflight')
    closed('quantile_HGB_native_hook7_preflight')
    closed('all_forecast_percentiles_full_scoring_benchmark')
    closed('cached_official_spearman_full12_benchmark')
    closed('HGB_quarter_numeric28_round118_full_registration_v5')
    import prepare_quantile_HGB88_round119_sources_v6_20261007 as generator
    import prepare_HGB_quarter_numeric28_round118_sources_v2_20261007 as source_base
    proof_path=A/'quantile_HGB88_round119_source_admission_v6_20261007.json';assert not proof_path.exists()
    preflight=A/'quantile_HGB88_transform_preflight_20261007/verification.json';controls=read(preflight)
    assert controls['status']=='passed_actual85_full5635800_quantile_HGB_independent_oracle_and_cold80_260_975_controls' and len(controls['controls'])==85
    native=A/'quantile_HGB_native_hook7_preflight_20261007/verification.json'
    assert len(read(native)['records'])==7
    benchmark=A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json'
    assert read(benchmark)['status']=='passed_actual12_uncached_full_official_calls_all_mapped_bits_CSV_bytes_eight_metrics_and_two_orders'
    scorer=A/'run_quantile_HGB88_official_comparison_v6_20261007.py'
    tree=ast.parse(scorer.read_text(encoding='utf8'))
    item=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in n.targets) and isinstance(n.value,ast.Dict))
    schema={key.value for key in item.keys if isinstance(key,ast.Constant)}
    plan=read(A/'quantile_HGB88_plan_20261007.json')
    assert len(plan['single_native_heads'])==4 and len(plan['ensembles'])==3 and len(plan['weights'])==12 and plan['expected_scored_records']==88
    sources=[Path(__file__),Path(generator.__file__),scorer,preflight,native,benchmark,
      A/'publish_quantile_HGB88_evidence_v6_20261007.py',A/'run_quantile_HGB88_round119_full_registration_v6_20261007.py',
      A/'prepare_quantile_HGB88_selected_candidate_v6_20261007.py',
      A/'seal_quantile_HGB88_selected_candidate_v6_20261007.py',
      A/'predict_refined_quantile_HGB_scheme_v2_20261007.py',
      A/'predict_quantile_HGB_residual_CDF_scheme_v2_20261007.py',
      A/'predict_lower_pool_after_quantile_HGB_scheme_v2_20261007.py',
      A/'quantile_HGB88_plan_20261007.json',
      A/'all_forecast_percentile_runtime_20261007.py',A/'exact_numpy_all_forecast_percentiles_20261007.py',
      *[A/n for n in generator.NAMES],*[A/f'github_validation_sync_main_20261005/round{n}_receipt.json' for n in (112,117,118)]]
    sources += [Path(source_base.__file__),*[A/n for n in source_base.NAMES],
        A/'verify_quantile_HGB88_transform_20261007.py',A/'quantile_HGB88_complete_pipeline_source_preparation_20261007.json']
    sources += [Path(source_base.base.__file__),*[A/n for n in source_base.base.NAMES],
      A/'cached_official_spearman_runtime_20261007.py',A/'exact_cached_official_spearman_v2_20261007.py',
      A/'cached_official_spearman_full_scoring_benchmark_20261007/verification.json']
    sources += [A/'prepare_quantile_HGB88_complete_routes_v2_20261007.py',A/'quantile_HGB88_complete_routes_source_preparation_v2_20261007.json']
    sources += [A/'prepare_quantile_HGB88_routes_v3_before_scoring_20261007.py',A/'quantile_HGB88_routes_source_preparation_v3_20261007.json']
    sources += [A/'prepare_local_118_119_protocol_recovery_v4_20261007.py',A/'local_118_119_protocol_recovery_source_preparation_v4_20261007.json',A/'resolve_sealed_scientific_protocol_20261007.py']
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    future={A/n for n in generator.NAMES.values()}|{proof_path,A/'quantile_HGB88_round119_source_preparation_v6_20261007.json',
      A/'quantile_HGB88_scores_github_v6_20261007/receipt.json',
      A/'quantile_HGB88_selected_release_v6_20261007/selected_candidate_ready_for_registration.json'}
    outputs={};baseline_controls=[];path_controls=[];graph_controls=[]
    for parent in (112,117,118):
        generated=generator.generate(parent);assert len(generated)==8
        outputs[str(parent)]={}
        for name,text in generated.items():
            assert not (A/name).exists(),name
            compile(text,str(A/name),'exec');outputs[str(parent)][name]=hashlib.sha256(text.encode('utf8')).hexdigest()
        name='register_quantile_HGB88_round119_artifacts_20261007.py';text=generated[name];registry=ast.parse(text)
        assert "'original_registry_alias_round119.json'" in text and "'round119_full_scope' / source.relative_to(ROOT)" in text
        required={n.slice.value for n in ast.walk(registry) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='measured' and isinstance(n.slice,ast.Constant)}
        assert required<=schema,required-schema
        body=next(n for n in registry.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
        source_assign=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='sources' for t in n.targets))
        ns={'A':A,'ROOT':ROOT,'Path':Path,'__file__':str(A/name)}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[source_assign],type_ignores=[])),name,'exec'),ns)
        for p in ns['sources']:assert p.is_file() or p in future,p
        path_controls.append({'parent':parent,'concrete_source_count':len(ns['sources']),
          'future_source_paths':sorted(str(p) for p in ns['sources'] if not p.is_file()),'all_existing_paths_checked':True})
        start=text.index("        if measured['case'] == pilot['best']['case']:");end=text.index('        row = ',start)
        code=compile('if True:\n'+text[start:end],name,'exec')
        fake={'core':{'native_SHA':'preserved106'},'conditional_flag_CPU_HGB_residual_CDF':{'old':True},'protected_upper_pool_CPU_HGB_CDF':{'keep':True}}
        examples=[('remove_flagged_HGB',0.,[]),*[(n,.0125,[n]) for n in plan['single_native_heads']],*[(n,.0125,names) for n,names in plan['ensembles'].items()]]
        for model,weight,names in examples:
            cfg={'model':model,'weight':weight,'anchor_round':112,'universe':plan['universe']}
            measured={'case':7,'native_bank_source':'existing20','ordered_native_components':names}
            ns={'cfg':cfg,'measured':measured,'pilot':{'best':{'case':8},'actual_scheme_base_round':112},
              'deepcopy':deepcopy,'read':lambda path:{'whole_scheme_graph':fake},'ROOT':ROOT}
            exec(code,ns);graph=ns['graph'];assert graph['core']==fake['core'] and graph['protected_upper_pool_CPU_HGB_CDF']==fake['protected_upper_pool_CPU_HGB_CDF']
            if model=='remove_flagged_HGB':assert 'conditional_flag_CPU_HGB_residual_CDF' not in graph
            else:
                component=graph['conditional_flag_CPU_HGB_residual_CDF'];assert component['training_teacher_round']==106
                assert component['ordered_equal_mean_components']==names and component['ordered_mean_component_count']==len(names)
                assert len(names) in (1,2,4) and len(set(names))==len(names) and component['native_components_unique'] is True
            graph_controls.append({'parent':parent,'model':model,'ordered_slots':len(names),'unique_components':len(set(names))})
        baseline=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='comparison_baseline' for t in n.targets))
        update=next(n for n in body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and isinstance(n.value.func.value,ast.Name) and n.value.func.value.id=='selection' and n.value.func.attr=='update')
        actual_parent=A/f'optimization_20261003_r{parent}/selection.json';base=read(actual_parent)['winner']['metrics']
        for amplitude in (0.,1e-8,-4e-5):
            winner={'metrics':deepcopy(base)};winner['metrics']['ic_mean']+=amplitude/.4
            winner['connected_final_score']=.4*winner['metrics']['ic_mean']+.3*winner['metrics']['annual_excess']+.3*(1.-winner['metrics']['mean_turnover'])
            winner['metrics']['final_score']=winner['connected_final_score'];selection={};requested=[]
            def mock_read(path):
                requested.append(str(path));assert Path(path)==actual_parent
                return {'winner':{'metrics':base}}
            ns={'pilot':{'actual_scheme_base_round':112},'A':A,'ROOT':ROOT,'read':mock_read,'sha':sha,'selection':selection,
              'winner':winner,'records':[],'selection_source':A/'optimization_20261003_r112/selection.json','GRAPH_FIELD':'conditional_flag_residual_scheme_graph','time':time}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[baseline,update],type_ignores=[])),name,'exec'),ns)
            gain=winner['connected_final_score']-base['final_score']
            assert selection['explicit_comparison_parent_round']==parent and requested==[str(actual_parent)]
            assert selection['baseline_score']==base['final_score'] and selection['score_gain']==gain
            contribution=.4*(winner['metrics']['ic_mean']-base['ic_mean'])+.3*(winner['metrics']['annual_excess']-base['annual_excess'])-.3*(winner['metrics']['mean_turnover']-base['mean_turnover'])
            assert abs(gain-contribution)<1e-12
            baseline_controls.append({'parent':parent,'synthetic_IC_amplitude':amplitude,'gain':gain,'contribution_difference':gain-contribution})
        pub=generated['publish_quantile_HGB88_round119_full_validation_20261007.py']
        assert "prefix = Path('validation_sync/round119')" in pub and "namespace['snapshot'](119)" in pub
        assert "actual_full_QA_version': 30" in pub and 'collect(119, 30, 88)' in pub
        assert 'validation_sync/round117' not in pub
    candidate=(A/'prepare_quantile_HGB88_selected_candidate_v6_20261007.py').read_text(encoding='utf8')
    assert 'expected_scored_records=88' in candidate and 'expected_scored_records=28' not in candidate
    assert len(baseline_controls)==9 and len(graph_controls)==24
    create(proof_path,{'status':'passed_actual85_controls_and24_prospective119_complete_source_schema_paths_and_graph_routes',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
      'generated_source_sha256':outputs,'baseline_gain_regressions':baseline_controls,'source_path_controls':path_controls,'graph_metadata_controls':graph_controls,
      'actual_scoring_item_fields':sorted(schema),'declared_prospective_sources':24,'actual_full_transform_controls':85,
      'actual_native_hook_cases':7,'actual_uncached_official_equivalence_calls':12,'new_native_fits':0,'new_quality_scores':0,
      'canonical119_sources_written':0,'full119_future_inference_and_QA30_not_yet_claimed':True,'test_labels_read':False})
    print({'status':'passed','prospective_sources':24,'baseline_regressions':9,'graph_metadata_controls':24},flush=True)

if __name__=='__main__':main()
