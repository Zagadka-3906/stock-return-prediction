"""Execute32 actual generated routes before scores: signed ties, fixed-stage graph retention and original official/cache paths."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    from run_dependency_queue_v3_20261006 import owned
    calendar_service=A/'service_owned_workflows_20261006/HuberCrossFamilyFine30_multiyear_calendar_controls_v1_20261008'
    while not (calendar_service/'service_execution.json').exists():time.sleep(5)
    assert read(calendar_service/'service_execution.json')['status']=='passed'
    while owned(read(calendar_service/'native_launch.json')):time.sleep(1)
    import prepare_HuberCrossFamilyFine125_round146_sources_v3_20261008 as generator
    from HuberCrossFamilyFine146_storage_v1_20261008 import OUTPUTS,empty,installed_transfer,EBASE
    from HuberCrossFamilyFine_complete_parent_CDF_v1_20261008 import GROUPS
    from run_HuberCrossFamilyFine125_official_comparison_v2_20261008 import best_key
    proof_path=A/'HuberCrossFamilyFine125_prospective_routes_v3_20261008.json';assert not proof_path.exists()
    plan_path=A/'HuberCrossFamilyFine125_round146_plan_v2_20261008.json';plan=read(plan_path)
    assert plan['anchor_rounds']==[136,139,141,145] and plan['fixed_scientific_stage_base_round']==136 and len(plan['new_cases'])==120
    assert plan['final_selection_rule']=='official_S_desc_unique_physical_model_SHA_count_asc_absolute_amplitude_asc_case_asc'
    for path in OUTPUTS:empty(path)
    paths=generator.source_paths();future={p for p in paths if not p.is_file()}
    allowed={A/n for n in generator.NAMES.values()}|{proof_path,A/'HuberCrossFamilyFine125_actual_controls_index_v1_20261008.json',A/'HuberCrossFamilyFine125_round146_source_admission_v2_20261008.json',
        A/'HuberCrossFamilyFine125_round146_source_preparation_v1_20261008.json',A/'HuberCrossFamilyFine125_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',A/'HuberCrossFamilyFine125_scores_github_v1_20261008/receipt.json'}
    assert future<=allowed,future-allowed
    inputs=[Path(__file__),plan_path,*(p for p in paths if p.is_file()),ROOT/'evaluate.py',ROOT/'后续选模标准.md',A/'optimization_20261003_r136/selection.json',ROOT/'candidates/optimization_20261003_r136/verification.json']
    for p in inputs:
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    assert sha(ROOT/'evaluate.py')=='72dc59987e92ba8ae6b506e114dfe8591b5608c9beccd0769d5d1f778f9189c2'
    scorer=A/'run_HuberCrossFamilyFine125_official_comparison_v2_20261008.py';scorer_ast=ast.parse(scorer.read_text(encoding='utf8'))
    item=next(n.value for n in ast.walk(scorer_ast) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in n.targets))
    schema={k.value for k in item.keys if isinstance(k,ast.Constant)}
    count_node=next(n for n in ast.walk(scorer_ast) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='expected_models' for t in n.targets) and 'model_sha' in ast.unparse(n.value))
    model_counts=[]
    for base,heads in (({'a'},[]),({'a'},['h0']),({'a','b'},['h0']),({'a'},['h0','h1']),({'a','b'},['h0','h1']),({'a','b','c'},['h0','h1','h2']),({'a'},['h0','h1','h2']),({'a','b','c'},['h0','h0','h2'])):
        infos={f'h{i}':{'native_model_sha256':v} for i,v in enumerate(('a','b','c'))};ns={'model_sha':base,'components':heads,'final_infos':infos}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[count_node],type_ignores=[])),str(scorer),'exec'),ns)
        assert ns['expected_models']==len(base|{infos[h]['native_model_sha256'] for h in heads});model_counts.append({'base_SHA':sorted(base),'components':heads,'actual_models':ns['expected_models']})
    metrics=read(A/'optimization_20261003_r136/selection.json')['winner']['metrics'];graph136=read(ROOT/'candidates/optimization_20261003_r136/verification.json')['whole_scheme_graph']
    assert plan['graph_key'] not in graph136
    augmented=deepcopy(graph136);augmented['BF16_complete_parent_rank_CDF']={'prospective_only':True,'nested_marker':[{'complete_parent_branch_must_survive':True}]}
    graphs_by_kind={'actual136':graph136,'augmented_complete_parent':augmented}
    outputs={};graph_controls=[];baselines=[];ties=[];collectors=[];path_controls=[]
    for parent in plan['anchor_rounds']:
        generated=generator.generate(parent);assert len(generated)==8
        outputs[str(parent)]={n:hashlib.sha256(s.encode()).hexdigest() for n,s in generated.items()}
        for n,s in generated.items():assert not (A/n).exists();compile(s,str(A/n),'exec')
        name='register_HuberCrossFamilyFine125_round146_artifacts_20261008.py';text=generated[name];tree=ast.parse(text)
        required={n.slice.value for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='measured' and isinstance(n.slice,ast.Constant)}
        assert required<=schema,required-schema
        guard=next(n for n in ast.walk(tree) if isinstance(n,ast.Compare) and ast.unparse(n.left)=="pilot['status']");assert guard.comparators[0].value=='passed_actual125_HuberCrossFamily_complete_parent_full_official_comparisons'
        first=text.index("        if measured['case'] == pilot['best']['case']:");last=text.index('        row = ',first);code=compile('if True:\n'+text[first:last],name,'exec')
        for kind,parent_graph in graphs_by_kind.items():
            for cfg0 in [*plan['new_cases'],{'group':None,'share':None,'amplitude':0.}]:
                cfg={'anchor_round':136,'model':f'crossfamily_group4_share{cfg0["share"]}' if cfg0['amplitude'] else 'zero_HuberCrossFamily_residual_identity',
                    'group':cfg0['group'],'share':cfg0['share'],'weight':cfg0['amplitude'],'role':'nonflag_valid_2021_onward','universe':'all_current_raw_forecasts'}
                heads=list(dict.fromkeys(h for members,sign in GROUPS[4] for h in members)) if cfg0['amplitude'] else []
                measured={'case':7,'ordered_native_components':heads,'native_bank_source':'prospective_actual15_saved_states','first2020_identity':True};requested=[]
                def base_read(p):
                    assert Path(p)==ROOT/'candidates/optimization_20261003_r136/verification.json';requested.append(str(p));return {'whole_scheme_graph':deepcopy(parent_graph)}
                ns={'cfg':cfg,'measured':measured,'pilot':{'best':{'case':8},'actual_scheme_base_round':136,'actual_comparison_parent_round':parent},'deepcopy':deepcopy,'ROOT':ROOT,'read':base_read}
                exec(code,ns);graph=ns['graph'];stage=graph.pop(plan['graph_key'],None);assert graph==parent_graph and len(requested)==1
                if cfg0['amplitude']:
                    assert stage['group']==4 and stage['share']==cfg0['share'] and stage['amplitude']==cfg0['amplitude'] and stage['ordered_native_component_heads']==heads
                    assert stage['position']=='after_complete_qualified_parent' and stage['original_complete_parent_round']==136 and stage['first2020_identity']
                else:assert stage is None
                graph_controls.append({'comparison_parent':parent,'stage_base':136,'graph_kind':kind,**cfg0,'all_complete_parent_graph_values_preserved_once':True})
        for anchor in plan['anchor_rounds']:
            existing=deepcopy(augmented);existing[plan['graph_key']]={'existing_qualified_anchor_stage':True}
            cfg={'anchor_round':anchor,'model':None,'weight':0.};requested=[]
            def anchor_read(p):
                assert Path(p)==ROOT/f'candidates/optimization_20261003_r{anchor}/verification.json';requested.append(str(p));return {'whole_scheme_graph':deepcopy(existing)}
            ns={'cfg':cfg,'measured':{'case':7},'pilot':{'best':{'case':8},'actual_scheme_base_round':136},'deepcopy':deepcopy,'ROOT':ROOT,'read':anchor_read}
            exec(code,ns);assert ns['graph']==existing and len(requested)==1
        body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
        baseline=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='comparison_baseline' for t in n.targets))
        update=next(n for n in body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='selection.update')
        sort_node=next(n for n in body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='records.sort')
        for delta in (0.,1e-8,-4e-5):
            winner={'connected_final_score':metrics['final_score']+delta};expected=A/f'optimization_20261003_r{parent}/selection.json';requested=[]
            def expected_read(p):
                assert Path(p)==expected;requested.append(str(p));return {'winner':{'metrics':metrics}}
            ns={'A':A,'ROOT':ROOT,'read':expected_read,'sha':sha,'selection':{},'winner':winner,'records':[],'pilot':{'actual_scheme_base_round':136},'selection_source':A/'optimization_20261003_r136/selection.json','GRAPH_FIELD':'conditional_flag_residual_scheme_graph','time':time}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[baseline,update],type_ignores=[])),name,'exec'),ns)
            assert len(requested)==1 and ns['selection']['baseline_score']==metrics['final_score'] and ns['selection']['score_gain']==winner['connected_final_score']-metrics['final_score']
            assert ns['selection']['explicit_comparison_parent_round']==parent and ns['selection']['actual_scheme_base_round']==136
            baselines.append({'comparison_parent':parent,'stage_base':136,'delta':delta,'comparison_baseline_reads_exact_actual_parent':True})
        for advantage in (0.,1e-8):
            samples=[{'connected_final_score':metrics['final_score']+(advantage if case==4 else 0.),'direct_rank_comparison_configuration':{'weight':w},'original_comparison_case':case,
                'actual_full_conditional_residual_control':{'expected_unique_native_models':m}} for case,w,m in ((0,-.00325,18),(1,.00025,20),(2,-.00025,18),(3,0.,18),(4,.00325,22))]
            ns={'records':samples};exec(compile(ast.fix_missing_locations(ast.Module(body=[sort_node],type_ignores=[])),name,'exec'),ns)
            assert samples[0]['original_comparison_case']==(4 if advantage else 3)
            scores=[{'connected_final_score':r['connected_final_score'],'expected_unique_native_models':r['actual_full_conditional_residual_control']['expected_unique_native_models'],'configuration':r['direct_rank_comparison_configuration'],'case':r['original_comparison_case']} for r in samples]
            assert min(scores,key=best_key)['case']==samples[0]['original_comparison_case'];ties.append({'parent':parent,'score_advantage':advantage,'SHA_count_before_absolute_amplitude':True})
        collector=next(s for n,s in generated.items() if n.startswith('collect_full_'));t=ast.parse(collector);fn=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='collect');forwarded=[]
        ns={'namespace':{'collect':lambda *args:forwarded.append(args)}};exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'<145_collector>','exec'),ns);ns['collect'](146,57,125);assert forwarded==[(146,57,125)]
        collectors.append({'parent':parent,'contract':[146,57,125]})
        pub=generated['publish_HuberCrossFamilyFine125_round146_full_validation_20261008.py'];assert 'collect(146, 57, 125)' in pub and "namespace['snapshot'](146)" in pub and "== full['scored_records'] == 125" in pub
        path_controls.append({'parent':parent,'all125_scored_records_QA57_and_main_paths':True})
    producer=A/'publish_HuberCrossFamilyFine125_evidence_v3_20261008.py';t=ast.parse(producer.read_text(encoding='utf8'));expression=next(n.value for n in ast.walk(t) if isinstance(n,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='out' for k in n.targets))
    for phase,consumer in (('controls',scorer),('scores',A/'prepare_HuberCrossFamilyFine125_selected_candidate_v2_20261008.py')):
        out=eval(compile(ast.Expression(body=expression),'<145_phase>','eval'),{'__builtins__':{},'A':A,'phase':phase})
        assert out==A/f'HuberCrossFamilyFine125_{phase}_github_v1_20261008' and out.name+'/receipt.json' in consumer.read_text(encoding='utf8')
    scope=read(A/'HuberCrossFamilyFine146_D_scoring_scope_v1_20261008.json');assert scope['original_cache_functions_and_official_script_unmodified']
    # Cross-volume transfer is exercised without writing large artifacts or invoking inference.
    source=A/'HuberCrossFamilyFine146_cross_volume_byte_probe_v3.bin';target=EBASE/'cross_volume_byte_probe_v3.bin';assert not source.exists() and not target.exists();source.write_bytes(bytes(range(256))*7)
    import os
    with installed_transfer():os.link(source,target)
    assert source.read_bytes()==target.read_bytes() and sha(source)==sha(target);inputs.append(source)
    inputs=list(dict.fromkeys(inputs));pins={str(p):sha(p) for p in inputs}
    create(proof_path,{'status':'passed_actual32_prospective146_sources_fixed_stage_graphs_baselines_status_paths_model_counts_signed_ties_and_cross_volume_bytes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'generated_source_sha256':outputs,'actual_prospective_sources':32,'actual_graph_controls':len(graph_controls),
        'graph_controls':graph_controls,'baseline_controls':baselines,'same_score_sort_controls':ties,'path_controls':path_controls,'collector_controls':collectors,'physical_SHA_count_controls':model_counts,
        'actual_future_anchor_quality_or_inference_not_claimed':True,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print('32 source routes, '+str(len(graph_controls))+' fixed-stage graphs,12 baselines,8 signed ties and4 collector contracts passed before any official125 score.',flush=True)
if __name__=='__main__':main()
