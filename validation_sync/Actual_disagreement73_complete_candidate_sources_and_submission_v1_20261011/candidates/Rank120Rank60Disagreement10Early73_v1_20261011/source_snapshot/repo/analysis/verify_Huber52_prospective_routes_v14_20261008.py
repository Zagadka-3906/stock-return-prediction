"""Execute24 prospective137 routes and all complete-parent combinations; no new quality or future inputs."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def strings(text):return [node.value for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Constant) and isinstance(node.value,str)]


def main():
    import prepare_Huber52_round137_sources_v14_20261008 as generator
    from Huber137_storage_v1_20261008 import OUTPUTS,empty,installed_transfer
    from Huber52_complete_parent_receiver_codec_v1_20261008 import GROUPS
    from run_Huber52_official_comparison_v14_20261008 import best_key
    from predict_HuberIRLS64_complete_parent_scheme_v3_20261008 import prepared_backend
    proof_path=A/'Huber52_prospective_routes_v14_20261008.json';assert not proof_path.exists()
    scorer=A/'run_Huber52_official_comparison_v14_20261008.py';scorer_text=scorer.read_text(encoding='utf8');tree=ast.parse(scorer_text)
    item=next(node.value for node in ast.walk(tree) if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='item' for target in node.targets) and isinstance(node.value,ast.Dict))
    schema={key.value for key in item.keys if isinstance(key,ast.Constant)}
    actual_status=next(node.value.value for node in tree.body if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='STATUS' for target in node.targets))
    paths=[Path(__file__),scorer,Path(generator.__file__),A/'prepare_Huber137_complete_receivers_v1_20261008.py',
        A/'prepare_Huber52_selected_candidate_v14_20261008.py',A/'seal_Huber52_selected_candidate_v14_20261008.py',
        A/'run_Huber52_round137_full_registration_v14_20261008.py',A/'publish_Huber52_evidence_v14_20261008.py',
        A/'verify_Huber52_round137_sources_v14_20261008.py',A/'queue_Huber137_complete_pipeline_v3_20261008.py',
        A/'Huber137_storage_v1_20261008.py',A/'Huber52_round137_receiver_contract_v1_20261008.json',
        A/'Huber137_receiver_preparation_v14_20261008.json',A/'predict_HuberIRLS64_complete_parent_scheme_v3_20261008.py',
        A/'HuberIRLS64_complete_parent_native_stage_v3_20261008.py',A/'Huber52_complete_parent_receiver_codec_v1_20261008.py',
        A/'verify_HuberIRLS64_49_current_parent_v6_20261008.py',A/'Huber137_D_scoring_scope_v1_20261008.json',
        A/'verify_Huber137_D_scoring_scope_v1_20261008.py',ROOT/'evaluate.py',A/'build_all_model_rankings_20261003.py',
        ROOT/'candidates/optimization_20261003_r134/verification.json',A/'optimization_20261003_r134/selection.json']
    for path in paths:
        assert path.is_file(),path
        if path.suffix=='.py':compile(path.read_text(encoding='utf8'),str(path),'exec')
    for path in OUTPUTS:empty(path)
    future=set(generator.source_paths())-set(path for path in generator.source_paths() if path.is_file())
    allowed=set(A/name for name in generator.NAMES.values())|{proof_path,A/'Huber52_actual_controls_index_v14_20261008.json',
        A/'Huber52_round137_source_admission_v14_20261008.json',A/'Huber52_round137_source_preparation_v14_20261008.json',
        A/'Huber52_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',A/'Huber52_scores_github_v1_20261008/receipt.json'}
    assert future<=allowed,future-allowed
    original_graph=read(ROOT/'candidates/optimization_20261003_r134/verification.json')['whole_scheme_graph']
    assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in original_graph
    parent_graphs={}
    for has_bf in (False,True):
        for has_cross in (False,True):
            graph=deepcopy(original_graph)
            if has_bf:graph['BF16_complete_parent_rank_CDF']={'native_component':{'prospective_only':True,'nested_marker':[{'all_fields_must_survive':True}]}}
            if has_cross:graph['nonflag_CPU_CrossFamily_complete_parent_CDF']={'group':4,'ordered_native_components':[{'head':'ridge_l001','nested_marker':[{'preserve_every_field':True}]}]}
            parent_graphs[f'BF16{int(has_bf)}_CrossFamily{int(has_cross)}']=graph
    source_metrics=read(A/'optimization_20261003_r134/selection.json')['winner']['metrics']
    plan=read(A/'Huber52_round137_receiver_contract_v1_20261008.json');outputs={};graphs=[];baselines=[];statuses=[];sort_controls=[];path_controls=[]
    for parent in (134,135,136):
        generated=generator.generate(parent);assert len(generated)==8
        outputs[str(parent)]={name:hashlib.sha256(text.encode()).hexdigest() for name,text in generated.items()}
        for name,text in generated.items():assert not (A/name).exists();compile(text,str(A/name),'exec')
        name='register_Huber52_round137_artifacts_20261008.py';text=generated[name];registry=ast.parse(text)
        required={node.slice.value for node in ast.walk(registry) if isinstance(node,ast.Subscript) and isinstance(node.value,ast.Name) and node.value.id=='measured' and isinstance(node.slice,ast.Constant)}
        assert required<=schema,required-schema
        guard=next(node for node in ast.walk(registry) if isinstance(node,ast.Compare) and ast.unparse(node.left)=="pilot['status']")
        assert guard.comparators[0].value==actual_status;statuses.append({'parent':parent,'pilot_status':actual_status})
        assert "'round137_full_scope' / source.relative_to(ROOT)" in text
        start=text.index("        if measured['case'] == pilot['best']['case']:");end=text.index('        row = ',start)
        code=compile('if True:\n'+text[start:end],name,'exec')
        configs=[{'group':None,'share':None,'weight':0.,'model':'zero_HuberIRLS64_residual_identity'}]
        configs += [{'group':case['group'],'share':.5,'weight':case['amplitude'],'model':f'HuberIRLS64_group{case["group"]}_share0.5'} for case in plan['new_cases']]
        for label,parent_graph in parent_graphs.items():
            for config in configs:
                cfg={**config,'anchor_round':parent,'role':'nonflag_valid_2021_onward','universe':'all_current_raw_forecasts'}
                components=[] if cfg['weight']==0. else list(dict.fromkeys(head for members,sign in GROUPS[cfg['group']] for head in members))
                measured={'case':7,'native_bank_source':'actual10 Huber native head audit','ordered_native_components':components,'first2020_identity':True}
                namespace={'cfg':cfg,'measured':measured,'pilot':{'best':{'case':8},'actual_scheme_base_round':parent},'deepcopy':deepcopy,'ROOT':ROOT,
                    'read':lambda path:{'whole_scheme_graph':deepcopy(parent_graph)}}
                exec(code,namespace);graph=namespace['graph'];stage=graph.pop('nonflag_CPU_HuberIRLS64_complete_parent_CDF',None)
                assert graph==parent_graph
                if cfg['weight']==0.:assert stage is None
                else:
                    assert stage['group']==cfg['group'] and stage['share']==.5 and stage['amplitude']==cfg['weight']
                    assert stage['first2020_identity'] and stage['position']=='after_complete_qualified_parent' and stage['ordered_native_component_heads']==components
                graphs.append({'comparison_parent':parent,'prospective_graph':label,**config,'every_original_graph_field_preserved':True,
                    'actual135136_quality_or_future_model_not_claimed':True})
        body=next(node for node in registry.body if isinstance(node,ast.FunctionDef) and node.name=='main').body
        baseline=next(node for node in body if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='comparison_baseline' for target in node.targets))
        update=next(node for node in body if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and isinstance(node.value.func.value,ast.Name) and node.value.func.value.id=='selection' and node.value.func.attr=='update')
        selection_path=A/f'optimization_20261003_r{parent}/selection.json';actual_path=selection_path if selection_path.is_file() else A/'optimization_20261003_r134/selection.json'
        metrics=read(actual_path)['winner']['metrics'];paths.append(actual_path)
        for delta in (0.,1e-8,-4e-5):
            winner={'metrics':deepcopy(metrics)};winner['metrics']['ic_mean']+=delta/.4
            winner['connected_final_score']=.4*winner['metrics']['ic_mean']+.3*winner['metrics']['annual_excess']+.3*(1-winner['metrics']['mean_turnover']);requested=[]
            def requested_read(path):assert Path(path)==selection_path;requested.append(path);return {'winner':{'metrics':metrics}}
            namespace={'A':A,'ROOT':ROOT,'read':requested_read,'sha':sha,'selection':{},'winner':winner,'records':[],
                'pilot':{'actual_scheme_base_round':parent},'selection_source':actual_path,'GRAPH_FIELD':'conditional_flag_residual_scheme_graph','time':time}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[baseline,update],type_ignores=[])),name,'exec'),namespace)
            assert len(requested)==1 and namespace['selection']['baseline_score']==metrics['final_score']
            assert namespace['selection']['score_gain']==winner['connected_final_score']-metrics['final_score'] and namespace['selection']['explicit_comparison_parent_round']==parent
            baselines.append({'parent':parent,'delta':delta,'source_metrics':str(actual_path),'prospective_metrics_not_actual135136':actual_path!=selection_path})
        sort_node=next(node for node in body if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and ast.unparse(node.value.func)=='records.sort')
        for advantage in (0.,1e-8):
            samples=[{'case':case,'configuration':{'weight':weight},'connected_final_score':source_metrics['final_score']+(advantage if case==3 else 0.),'expected_unique_native_models':models} for case,weight,models in ((0,.1,18),(1,.0025,20),(2,0.,19),(3,.05,22))]
            records=[{'connected_final_score':sample['connected_final_score'],'direct_rank_comparison_configuration':sample['configuration'],
                'original_comparison_case':sample['case'],'actual_full_conditional_residual_control':sample} for sample in samples]
            exec(compile(ast.fix_missing_locations(ast.Module(body=[sort_node],type_ignores=[])),name,'exec'),{'records':records})
            assert records[0]['original_comparison_case']==min(samples,key=best_key)['case'];sort_controls.append({'parent':parent,'score_advantage':advantage,'sort_order_exact':True})
        pub=generated['publish_Huber52_round137_full_validation_20261008.py']
        assert 'collect(137, 48, 52)' in pub and "namespace['snapshot'](137)" in pub and "'scored_records': 52" in pub
        assert "== full['scored_records'] == 52" in pub and "'original_official_pilot_records_registered': 52" in pub
        path_controls.append({'parent':parent,'truthful52_cases_QA48_and_source_contract':True})
    producer=(A/'publish_Huber52_evidence_v14_20261008.py').read_text(encoding='utf8')
    expression=next(node.value for node in ast.walk(ast.parse(producer)) if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='out' for target in node.targets))
    for phase,consumer in (('controls',scorer),('scores',A/'prepare_Huber52_selected_candidate_v14_20261008.py')):
        output=eval(compile(ast.Expression(body=expression),'<actual137_path>','eval'),{'__builtins__':{},'A':A,'phase':phase})
        assert output==A/f'Huber52_{phase}_github_v1_20261008'
        assert output.name+'/receipt.json' in strings(consumer.read_text(encoding='utf8'))
    manifest=next(node for node in ast.walk(ast.parse(producer)) if isinstance(node,ast.Dict) and any(isinstance(key,ast.Constant) and key.value=='actual_existing_native_head_audits' for key in node.keys))
    fields={key.value:value for key,value in zip(manifest.keys,manifest.values) if isinstance(key,ast.Constant)}
    assert (fields['round'].value,fields['actual_existing_native_head_audits'].value,fields['actual_full_native_OOF_heads'].value,
        fields['actual_full_CDF_controls'].value,fields['actual_cold_CDF_controls'].value,fields['actual_historical_native_hooks'].value)==(137,10,2,49,147,18)
    selected_text=(A/'prepare_Huber52_selected_candidate_v14_20261008.py').read_text(encoding='utf8')
    assert 'selected_by_all52_actual_official_scores' in strings(selected_text)
    assert "'state_kind':'HuberIRLS64_linear'" in selected_text
    predecessor='CrossFamily94_round136_full_registration_v6_20261008'
    assert predecessor in strings(producer) and predecessor in strings((A/'run_Huber52_round137_full_registration_v14_20261008.py').read_text(encoding='utf8'))
    scope=read(A/'Huber137_D_scoring_scope_v1_20261008.json');assert scope['status']=='passed_actual3_original_scope_guards_reject_E_and_accept_both_D_scoring_directories'
    for path,digest in scope['input_sha256'].items():assert sha(path)==digest,path
    backends=[]
    for backend,filename in (('ReverseBayes','predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py'),
        ('BF16','predict_BF16_complete_parent_rank_scheme_v1_20261008.py'),('CrossFamily','predict_CrossFamily_complete_parent_scheme_v2_20261008.py')):
        path=A/filename;prepared=prepared_backend(path.read_text(encoding='utf8'),backend);compile(prepared,str(path),'exec');paths.append(path)
        backends.append({'backend':backend,'compiled_source_sha256':hashlib.sha256(prepared.encode()).hexdigest(),'actual_future_replay_not_claimed':True})
    source=A/'Huber137_transfer_probe_v14_20261008.bin';target=Path('E:/赛题五_本机临时/第137轮_20261008/transfer_probe_v14.bin')
    assert not source.exists() and not target.exists();source.write_bytes(bytes(range(256))*31)
    with installed_transfer():__import__('os').link(source,target)
    assert sha(source)==sha(target);paths += [source,target]
    create(proof_path,{'status':'passed_actual24_prospective137_sources_schema_complete_graphs_baselines_status_paths_model_counts_and_cross_volume_bytes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(path):sha(path) for path in dict.fromkeys(paths)},
        'generated_source_sha256':outputs,'actual_scoring_item_fields':sorted(schema),'graph_controls':graphs,'baseline_gain_regressions':baselines,
        'model_count_sort_controls':sort_controls,'source_path_controls':path_controls,'truthful_status_guards':statuses,'prospective_sources':24,
        'backend_compilation_controls':backends,'cross_volume_transfer_bytes':source.stat().st_size,'actual_quality_scores':0,
        'actual135136_quality_and_Huber_future_candidate_not_claimed':True,'actual_current_parent_and_selected_replays_QA48_still_required':True,'test_labels_read':False})
    print(f'Actual24 prospective137 sources, {len(graphs)} complete-graph controls,9 baselines,6 ties and D/E paths passed.',flush=True)


if __name__=='__main__':main()
