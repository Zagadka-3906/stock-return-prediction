"""Execute24 prospective receiver routes, preserving signed-Bayes and optional BF16 branches before quality."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def strings(text):
    return [node.value for node in ast.walk(ast.parse(text)) if isinstance(node,ast.Constant) and isinstance(node.value,str)]


def main():
    import prepare_CrossFamily94_round136_sources_v3_20261008 as generator
    from CrossFamily136_storage_v1_20261008 import OUTPUTS,empty,installed_transfer
    from CrossFamily_complete_parent_CDF_v1_20261008 import GROUPS
    from run_CrossFamily94_official_comparison_v3_20261008 import best_key
    from predict_CrossFamily_complete_parent_scheme_v2_20261008 import prepared_parent_source
    proof_path=A/'CrossFamily94_prospective_routes_v3_20261008.json';assert not proof_path.exists()
    scorer=A/'run_CrossFamily94_official_comparison_v3_20261008.py';tree=ast.parse(scorer.read_text(encoding='utf8'))
    item=next(node.value for node in ast.walk(tree) if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='item' for target in node.targets) and isinstance(node.value,ast.Dict))
    schema={key.value for key in item.keys if isinstance(key,ast.Constant)}
    names=[Path(__file__),scorer,Path(generator.__file__),A/'prepare_CrossFamily136_receiver_drafts_v1_20261008.py',
        A/'prepare_CrossFamily94_selected_candidate_v3_20261008.py',A/'seal_CrossFamily94_selected_candidate_v3_20261008.py',
        A/'run_CrossFamily94_round136_full_registration_v3_20261008.py',A/'publish_CrossFamily94_evidence_v3_20261008.py',
        A/'verify_CrossFamily94_round136_sources_v3_20261008.py',A/'queue_CrossFamily136_complete_pipeline_v3_20261008.py',
        A/'CrossFamily136_storage_v1_20261008.py',A/'CrossFamily94_round136_plan_v1_20261008.json',
        A/'CrossFamily136_receiver_preparation_v3_20261008.json',A/'predict_CrossFamily_complete_parent_scheme_v2_20261008.py',
        A/'CrossFamily_complete_parent_native_stage_v2_20261008.py',A/'CrossFamily_complete_parent_CDF_v1_20261008.py',
        A/'verify_CrossFamily91_current_parent_v1_20261008.py',A/'CrossFamily136_D_scoring_scope_v1_20261008.json',
        A/'verify_CrossFamily136_D_scoring_scope_v1_20261008.py',ROOT/'evaluate.py',A/'build_all_model_rankings_20261003.py',
        ROOT/'candidates/optimization_20261003_r134/verification.json',A/'optimization_20261003_r134/selection.json']
    for path in names:
        assert path.is_file(),path
        if path.suffix=='.py':compile(path.read_text(encoding='utf8'),str(path),'exec')
    for path in OUTPUTS:empty(path)
    future=set(generator.source_paths())-set(path for path in generator.source_paths() if path.is_file())
    allowed=set(A/name for name in generator.NAMES.values())|{proof_path,A/'CrossFamily94_actual_controls_index_v2_20261008.json',
        A/'CrossFamily94_round136_source_admission_v3_20261008.json',A/'CrossFamily94_round136_source_preparation_v3_20261008.json',
        A/'CrossFamily94_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',A/'CrossFamily94_scores_github_v1_20261008/receipt.json'}
    assert future<=allowed,future-allowed
    outputs={};graphs=[];baselines=[];statuses=[];sort_controls=[];path_controls=[]
    original_graph=read(ROOT/'candidates/optimization_20261003_r134/verification.json')['whole_scheme_graph']
    assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in original_graph
    augmented=deepcopy(original_graph)
    augmented['BF16_complete_parent_rank_CDF']={'role':'all_valid','weight':.01,'first2020_active':True,'position':'after_complete_qualified_parent',
        'native_component':{'prospective_only':True,'nested_marker':[{'all_fields_must_survive':True}],'actual_future_model_not_claimed':True}}
    source_metrics=read(A/'optimization_20261003_r134/selection.json')['winner']['metrics']
    for parent in (112,134,135):
        generated=generator.generate(parent);outputs[str(parent)]={name:hashlib.sha256(text.encode()).hexdigest() for name,text in generated.items()}
        assert len(generated)==8
        for name,text in generated.items():assert not (A/name).exists();compile(text,str(A/name),'exec')
        name='register_CrossFamily94_round136_artifacts_20261008.py';text=generated[name];registry=ast.parse(text)
        required={node.slice.value for node in ast.walk(registry) if isinstance(node,ast.Subscript) and isinstance(node.value,ast.Name) and node.value.id=='measured' and isinstance(node.slice,ast.Constant)}
        assert required<=schema,required-schema
        guard=next(node for node in ast.walk(registry) if isinstance(node,ast.Compare) and ast.unparse(node.left)=="pilot['status']")
        assert guard.comparators[0].value=='passed_actual94_CrossFamily_complete_parent_full_official_comparisons'
        statuses.append({'parent':parent,'pilot_status':guard.comparators[0].value})
        assert "'round136_full_scope' / source.relative_to(ROOT)" in text
        start=text.index("        if measured['case'] == pilot['best']['case']:");end=text.index('        row = ',start)
        code=compile('if True:\n'+text[start:end],name,'exec')
        for label,parent_graph in (('actual_complete134',original_graph),('prospective134_plus_BF16',augmented)):
            configs=[{'group':None,'share':None,'weight':0.,'model':'zero_CrossFamily_residual_identity'}]
            configs += [{'group':group,'share':share,'weight':weight,'model':f'crossfamily_group{group}_share{share}'} for group in range(5) for share in (.25,.5,.75) for weight in (.0025,.1)]
            for config in configs:
                cfg={**config,'anchor_round':134,'role':'nonflag_valid_2021_onward','universe':'all_current_raw_forecasts'}
                components=[] if cfg['weight']==0. else list(dict.fromkeys(h for members,sign in GROUPS[cfg['group']] for h in members))
                measured={'case':7,'native_bank_source':'actual30 existing native head audit','ordered_native_components':components,'first2020_identity':True}
                namespace={'cfg':cfg,'measured':measured,'pilot':{'best':{'case':8},'actual_scheme_base_round':134},'deepcopy':deepcopy,'ROOT':ROOT,
                    'read':lambda path:{'whole_scheme_graph':deepcopy(parent_graph)}}
                exec(code,namespace);graph=namespace['graph'];stage=graph.pop('nonflag_CPU_CrossFamily_complete_parent_CDF',None)
                assert graph==parent_graph
                if cfg['weight']==0.:assert stage is None
                else:
                    assert stage['group']==cfg['group'] and stage['share']==cfg['share'] and stage['amplitude']==cfg['weight']
                    assert stage['first2020_identity'] and stage['position']=='after_complete_qualified_parent' and stage['ordered_native_component_heads']==components
                graphs.append({'comparison_parent':parent,'graph_kind':label,**config,'all_original_parent_values_preserved':True,'actual135_NN_quality_or_inference_not_claimed':True})
        body=next(node for node in registry.body if isinstance(node,ast.FunctionDef) and node.name=='main').body
        baseline=next(node for node in body if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='comparison_baseline' for target in node.targets))
        update=next(node for node in body if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and isinstance(node.value.func.value,ast.Name) and node.value.func.value.id=='selection' and node.value.func.attr=='update')
        selection_path=A/f'optimization_20261003_r{parent}/selection.json'
        actual_path=selection_path if selection_path.is_file() else A/'optimization_20261003_r134/selection.json'
        metrics=read(actual_path)['winner']['metrics'];names.append(actual_path)
        for delta in (0.,1e-8,-4e-5):
            winner={'metrics':deepcopy(metrics)};winner['metrics']['ic_mean']+=delta/.4
            winner['connected_final_score']=.4*winner['metrics']['ic_mean']+.3*winner['metrics']['annual_excess']+.3*(1-winner['metrics']['mean_turnover'])
            requested=[]
            def requested_read(path):
                assert Path(path)==selection_path;requested.append(path);return {'winner':{'metrics':metrics}}
            namespace={'A':A,'ROOT':ROOT,'read':requested_read,'sha':sha,'selection':{},'winner':winner,'records':[],
                'pilot':{'actual_scheme_base_round':134},'selection_source':actual_path,'GRAPH_FIELD':'conditional_flag_residual_scheme_graph','time':time}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[baseline,update],type_ignores=[])),name,'exec'),namespace)
            assert len(requested)==1 and namespace['selection']['baseline_score']==metrics['final_score']
            assert namespace['selection']['score_gain']==winner['connected_final_score']-metrics['final_score'] and namespace['selection']['explicit_comparison_parent_round']==parent
            baselines.append({'parent':parent,'delta':delta,'source_metrics':str(actual_path),'prospective135_only':parent==135 and actual_path!=selection_path})
        sort_node=next(node for node in body if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and ast.unparse(node.value.func)=='records.sort')
        for advantage in (0.,1e-8):
            samples=[{'case':case,'configuration':{'weight':weight},'connected_final_score':source_metrics['final_score']+(advantage if case==3 else 0.),'expected_unique_native_models':models} for case,weight,models in ((0,.1,18),(1,.0025,20),(2,0.,19),(3,.05,22))]
            records=[{'connected_final_score':sample['connected_final_score'],'direct_rank_comparison_configuration':sample['configuration'],
                'original_comparison_case':sample['case'],'actual_full_conditional_residual_control':sample} for sample in samples]
            exec(compile(ast.fix_missing_locations(ast.Module(body=[sort_node],type_ignores=[])),name,'exec'),{'records':records})
            assert records[0]['original_comparison_case']==min(samples,key=best_key)['case']
            sort_controls.append({'parent':parent,'score_advantage':advantage,'official_score_first_then_unique_models_then_amplitude':True})
        pub=generated['publish_CrossFamily94_round136_full_validation_20261008.py']
        assert 'collect(136, 47, 94)' in pub and "namespace['snapshot'](136)" in pub and "'scored_records': 94" in pub
        assert "== full['scored_records'] == 94" in pub and "'original_official_pilot_records_registered': 94" in pub
        path_controls.append({'comparison_parent':parent,'source_paths':len(generator.source_paths()),'truthful94_record_and_QA47_counts':True})
    # Execute actual producer path expressions, including phase-dependent publication folders.
    producer=(A/'publish_CrossFamily94_evidence_v3_20261008.py').read_text(encoding='utf8')
    expression=next(node.value for node in ast.walk(ast.parse(producer)) if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='out' for target in node.targets))
    for phase,consumer in (('controls',scorer),('scores',A/'prepare_CrossFamily94_selected_candidate_v3_20261008.py')):
        output=eval(compile(ast.Expression(body=expression),'<actual136_path>','eval'),{'__builtins__':{},'A':A,'phase':phase})
        assert output==A/f'CrossFamily94_{phase}_github_v1_20261008'
        assert output.name+'/receipt.json' in strings(consumer.read_text(encoding='utf8'))
    manifest=next(node for node in ast.walk(ast.parse(producer)) if isinstance(node,ast.Dict) and any(isinstance(key,ast.Constant) and key.value=='actual_existing_native_head_audits' for key in node.keys))
    actual_fields={key.value:value for key,value in zip(manifest.keys,manifest.values) if isinstance(key,ast.Constant)}
    assert actual_fields['round'].value==136
    selected_text=(A/'prepare_CrossFamily94_selected_candidate_v3_20261008.py').read_text(encoding='utf8')
    assert 'selected_by_all94_actual_official_scores' in strings(selected_text) and 'selected_by_all40_actual_official_scores' not in selected_text
    scope=read(A/'CrossFamily136_D_scoring_scope_v1_20261008.json')
    assert scope['status']=='passed_actual3_original_scope_guards_reject_E_and_accept_both_D_scoring_directories'
    for path,digest in scope['input_sha256'].items():assert sha(path)==digest,path
    # Original full-parent source has a single explicit teacher exposure point for optional BF16 routing.
    parent_source=A/'predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py';signed=parent_source.read_text(encoding='utf8')
    exposed=prepared_parent_source(signed);assert exposed.count('context._CrossFamily_teacher106=teacher')==1
    compile(exposed,str(parent_source),'exec');names += [parent_source,A/'predict_BF16_complete_parent_rank_scheme_v1_20261008.py']
    source=A/'CrossFamily136_transfer_probe_v3_20261008.bin';target=Path('E:/赛题五_本机临时/第136轮_20261008/transfer_probe_v3.bin')
    assert not source.exists() and not target.exists();source.write_bytes(bytes(range(256))*31)
    with installed_transfer():__import__('os').link(source,target)
    assert sha(source)==sha(target);names += [source,target]
    create(proof_path,{'status':'passed_actual24_prospective136_sources_schema_graphs_baselines_status_paths_model_counts_and_cross_volume_bytes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(path):sha(path) for path in dict.fromkeys(names)},
        'generated_source_sha256':outputs,'actual_scoring_item_fields':sorted(schema),'graph_controls':graphs,'baseline_gain_regressions':baselines,
        'model_count_sort_controls':sort_controls,'source_path_controls':path_controls,'truthful_status_guards':statuses,'prospective_sources':24,
        'cross_volume_transfer_bytes':source.stat().st_size,'actual135_future_or_new136_quality_not_yet_claimed':True,
        'final_current_parent_and_selected_future_native_replays_and_QA47_still_required':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print('Actual24 prospective136 receivers,186 graph preservation controls,9 baselines,6 model-count ties and true D/E paths passed.',flush=True)


if __name__=='__main__':main()
