"""Execute registration branches for every declared mixture and every full parent graph."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    import prepare_ConeRidgeAlpha100_round144_sources_v4_20261008 as generator
    from ConeRidgeAlpha8_64_complete_parent_CDF_v1_20261008 import GROUPS
    from ConeRidgeAlpha144_storage_v3_20261008 import OUTPUTS,empty
    proof_path=A/'ConeRidgeAlpha100_prospective_routes_v4_20261008.json';assert not proof_path.exists()
    scorer=A/'run_ConeRidgeAlpha100_official_comparison_v5_20261008.py';scorer_ast=ast.parse(scorer.read_text(encoding='utf8'))
    item=next(node.value for node in ast.walk(scorer_ast) if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in node.targets))
    schema={key.value for key in item.keys if isinstance(key,ast.Constant)}
    status=next(node.value.value for node in scorer_ast.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='STATUS' for t in node.targets))
    inputs=[Path(__file__),Path(generator.__file__),scorer,A/'ConeRidgeAlpha100_round144_plan_v1_20261008.json',
        A/'ConeRidgeAlpha144_receiver_drafts_v1_20261008.json',A/'ConeRidgeAlpha144_D_scoring_scope_v1_20261008.json',
        A/'ConeRidgeAlpha144_native_receiver_preflight_v1_20261008.json',A/'prepare_ConeRidgeAlpha144_complete_receivers_v1_20261008.py',
        ROOT/'evaluate.py',A/'optimization_20261003_r134/selection.json',ROOT/'candidates/optimization_20261003_r134/verification.json']
    inputs += [path for path in generator.source_paths() if path.is_file()]
    for path in inputs:
        if path.suffix=='.py':compile(path.read_text(encoding='utf8'),str(path),'exec')
    for path in OUTPUTS:
        if 'official_comparison' in path.name and path!=A/'ConeRidgeAlpha100_official_comparison_v5_20261008':continue
        empty(path)
    original_graph=read(ROOT/'candidates/optimization_20261003_r143/verification.json')['whole_scheme_graph']
    graphs_by_kind={'actual143':deepcopy(original_graph)};augmented=deepcopy(original_graph)
    for key in ('BF16_complete_parent_rank_CDF','nonflag_CPU_CrossFamily_complete_parent_CDF',
        'nonflag_CPU_HuberIRLS64_complete_parent_CDF','BF16_reverse_complete_parent_rank_CDF','nonflag_CPU_HuberCrossFamily_complete_parent_CDF','nonflag_CPU_SpectralGram64_complete_parent_CDF','nonflag_CPU_KrylovGram64_complete_parent_CDF','nonflag_CPU_ConeRidge64_complete_parent_CDF'):
        augmented=deepcopy(augmented);augmented[key]={'prospective_only':True,'nested_marker':[{'unchanged_complete_branch':True}]}
        graphs_by_kind[key]=deepcopy(augmented)
    plan=read(A/'ConeRidgeAlpha100_round144_plan_v1_20261008.json');assert len(plan['new_cases'])==96
    outputs={};graphs=[];baselines=[];sorts=[];paths=[];model_counts=[]
    source_metrics=read(A/'optimization_20261003_r134/selection.json')['winner']['metrics']
    count_node=next(node for node in ast.walk(scorer_ast) if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='expected_models' for t in node.targets) and 'model_sha' in ast.unparse(node.value))
    for base_shas,heads in (({'a'},[]),({'a'},['h0']),({'a','b'},['h0']),({'a'},['h0','h1']),
        ({'a','b'},['h0','h1']),({'a','b','c'},['h0','h1','h2']),({'a'},['h0','h1','h2']),({'a','b','c'},['h0','h0','h2'])):
        final_infos={f'h{i}':{'native_model_sha256':key} for i,key in enumerate(('a','b','c'))}
        namespace={'model_sha':base_shas,'components':heads,'final_infos':final_infos}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[count_node],type_ignores=[])),str(scorer),'exec'),namespace)
        assert namespace['expected_models']==len(base_shas|{final_infos[h]['native_model_sha256'] for h in heads})
        model_counts.append({'base_SHA':sorted(base_shas),'head_aliases':heads,'actual_unique_physical_models':namespace['expected_models']})
    for parent in (132,134,143):
        generated=generator.generate(parent);outputs[str(parent)]={name:hashlib.sha256(text.encode()).hexdigest() for name,text in generated.items()}
        assert len(generated)==8
        for name,text in generated.items():assert not (A/name).exists();compile(text,str(A/name),'exec')
        name='register_ConeRidgeAlpha100_round144_artifacts_20261008.py';text=generated[name];tree=ast.parse(text)
        required={node.slice.value for node in ast.walk(tree) if isinstance(node,ast.Subscript) and isinstance(node.value,ast.Name) and node.value.id=='measured' and isinstance(node.slice,ast.Constant)}
        assert required<=schema,required-schema
        guard=next(node for node in ast.walk(tree) if isinstance(node,ast.Compare) and ast.unparse(node.left)=="pilot['status']")
        assert guard.comparators[0].value==status
        first=text.index("        if measured['case'] == pilot['best']['case']:");last=text.index('        row = ',first)
        code=compile('if True:\n'+text[first:last],name,'exec')
        configs=[{'group':None,'share':None,'amplitude':0.}]+plan['new_cases']
        for kind,parent_graph in graphs_by_kind.items():
            for config in configs:
                cfg={'anchor_round':parent,'model':'zero_ConeRidge_residual_identity' if not config['amplitude'] else f'ConeRidge_group{config["group"]}_share{config["share"]}',
                    'group':config['group'],'share':config['share'],'weight':config['amplitude'],'role':'nonflag_valid_2021_onward','universe':'all_current_raw_forecasts'}
                heads=[] if not cfg['weight'] else list(dict.fromkeys(h for members,sign in GROUPS[cfg['group']] for h in members))
                measured={'case':7,'native_bank_source':'actual40 existing native heads','ordered_native_components':heads,'first2020_identity':True}
                namespace={'cfg':cfg,'measured':measured,'pilot':{'best':{'case':8},'actual_scheme_base_round':parent},'deepcopy':deepcopy,'ROOT':ROOT,
                    'read':lambda path:{'whole_scheme_graph':deepcopy(parent_graph)}}
                exec(code,namespace);graph=namespace['graph'];stage=graph.pop(plan['graph_key'],None);assert graph==parent_graph
                if not cfg['weight']:assert stage is None
                else:
                    assert stage['group']==cfg['group'] and stage['share']==cfg['share'] and stage['amplitude']==cfg['weight']
                    assert stage['first2020_identity'] and stage['position']=='after_complete_qualified_parent' and stage['ordered_native_component_heads']==heads
                graphs.append({'parent':parent,'graph_kind':kind,**config,'all_parent_graph_values_preserved':True})
        body=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='main').body
        baseline=next(node for node in body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='comparison_baseline' for t in node.targets))
        update=next(node for node in body if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and ast.unparse(node.value.func)=='selection.update')
        actual_path=A/'optimization_20261003_r134/selection.json';expected_path=A/f'optimization_20261003_r{parent}/selection.json'
        for delta in (0.,1e-8,-4e-5):
            winner={'metrics':deepcopy(source_metrics)};winner['metrics']['ic_mean']+=delta/.4
            winner['connected_final_score']=.4*winner['metrics']['ic_mean']+.3*winner['metrics']['annual_excess']+.3*(1-winner['metrics']['mean_turnover'])
            requested=[]
            def requested_read(path):
                assert Path(path)==expected_path;requested.append(path);return {'winner':{'metrics':source_metrics}}
            namespace={'A':A,'ROOT':ROOT,'read':requested_read,'sha':sha,'selection':{},'winner':winner,'records':[],
                'pilot':{'actual_scheme_base_round':parent},'selection_source':actual_path,'GRAPH_FIELD':'conditional_flag_residual_scheme_graph','time':time}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[baseline,update],type_ignores=[])),name,'exec'),namespace)
            assert len(requested)==1 and namespace['selection']['baseline_score']==source_metrics['final_score']
            assert namespace['selection']['score_gain']==winner['connected_final_score']-source_metrics['final_score']
            assert namespace['selection']['explicit_comparison_parent_round']==parent
            baselines.append({'parent':parent,'delta':delta,'actual134_metrics_only_for_prospective_test':True})
        sort_node=next(node for node in body if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and ast.unparse(node.value.func)=='records.sort')
        for advantage in (0.,1e-8):
            samples=[{'connected_final_score':source_metrics['final_score']+(advantage if case==3 else 0.),
                'direct_rank_comparison_configuration':{'weight':weight},'original_comparison_case':case,
                'actual_full_conditional_residual_control':{'expected_unique_native_models':models}} for case,weight,models in ((0,.1,18),(1,.0025,20),(2,0.,19),(3,.05,22))]
            namespace={'records':samples};exec(compile(ast.fix_missing_locations(ast.Module(body=[sort_node],type_ignores=[])),name,'exec'),namespace)
            assert samples[0]['original_comparison_case']==(3 if advantage else 0);sorts.append({'parent':parent,'S_advantage':advantage,'physical_SHA_count_before_amplitude':True})
        pub=generated['publish_ConeRidgeAlpha100_round144_full_validation_20261008.py']
        assert 'collect(144, 100, 55)' in pub and "namespace['snapshot'](144)" in pub and "== full['scored_records'] == 100" in pub
        collector_tree=ast.parse(generated['collect_full_lossless_round144_qa55_20261007.py'])
        function=next(node for node in collector_tree.body if isinstance(node,ast.FunctionDef) and node.name=='collect')
        forwarded=[]
        def actual_contract(n,q,c):
            forwarded.append((n,q,c));return {'contract_executed':True}
        scope={'namespace':{'collect':actual_contract}}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[])),'<actual144collector-contract>','exec'),scope)
        assert scope['collect'](144,100,55)=={'contract_executed':True}
        assert forwarded==[(144,55,100)]
        for invalid in ((143,100,55),(144,55,100),(144,99,55)):
            try:scope['collect'](*invalid)
            except AssertionError:pass
            else:raise AssertionError(('invalid collector call accepted',invalid))
        paths.append({'parent':parent,'actual100_records_QA55':True})
    producer=A/'publish_ConeRidgeAlpha100_evidence_v5_20261008.py';tree=ast.parse(producer.read_text(encoding='utf8'))
    expression=next(node.value for node in ast.walk(tree) if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='out' for t in node.targets))
    for phase,consumer in (('controls',scorer),('scores',A/'prepare_ConeRidgeAlpha100_selected_candidate_v5_20261008.py')):
        output=eval(compile(ast.Expression(body=expression),'<139_phase_path>','eval'),{'__builtins__':{},'A':A,'phase':phase})
        assert output==A/f'ConeRidgeAlpha100_{phase}_github_v1_20261008' and output.name+'/receipt.json' in consumer.read_text(encoding='utf8')
    assert read(A/'ConeRidgeAlpha144_D_scoring_scope_v1_20261008.json')['original_cache_functions_and_official_script_unmodified']
    # Execute the actual transfer helper across volumes with exclusive tiny files, preserving both byte hashes.
    from ConeRidgeAlpha144_storage_v3_20261008 import installed_transfer,EBASE
    source=A/'ConeRidgeAlpha144_cross_volume_byte_probe_v6.bin';target=EBASE/'cross_volume_byte_probe_v6.bin'
    assert not source.exists() and not target.exists();source.write_bytes(bytes(range(256))*7)
    import os
    with installed_transfer():os.link(source,target)
    assert source.read_bytes()==target.read_bytes() and sha(source)==sha(target);inputs.append(source)
    inputs=list(dict.fromkeys(inputs));pins={str(path):sha(path) for path in inputs}
    assert len(graphs)==2619 and len(baselines)==9 and len(sorts)==6 and len(model_counts)==8
    create(proof_path,{'status':'passed_actual24_prospective144_sources_schema_graphs_baselines_status_paths_model_counts_and_cross_volume_bytes',
        'input_sha256':pins,'generated_source_sha256':outputs,'actual_prospective_sources':24,'actual_graph_controls':len(graphs),
        'graph_controls':graphs,'baseline_controls':baselines,'same_score_sort_controls':sorts,'path_controls':paths,
        'actual_physical_model_count_controls':8,'physical_model_count_controls':model_counts,
        'prospective_future_parent_quality_or_inference_not_claimed':True,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(A/'ConeRidgeAlpha144_receiver_preparation_v4_20261008.json',{'status':'passed_complete141_receivers_before_quality',
        'input_sha256':{**pins,str(proof_path):sha(proof_path)},'prospective_sources':24,'full_parent_graph_controls':len(graphs),
        'source_freeze_and_large_candidate_outputs_on_E':True,'new_quality_scores':0,'test_labels_read':False})
    print('24 sources, '+str(len(graphs))+' complete graphs,9 baselines,6 ties,8 SHA-union counts and D/E bytes passed.',flush=True)


if __name__=='__main__':main()
