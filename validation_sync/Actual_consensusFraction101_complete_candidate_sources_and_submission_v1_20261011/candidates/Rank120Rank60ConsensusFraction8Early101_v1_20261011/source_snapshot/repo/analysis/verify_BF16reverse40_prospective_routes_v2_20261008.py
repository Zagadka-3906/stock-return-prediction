"""Validate all24 prospective receivers using real qualified parent graphs and truthful score schemas."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    import prepare_BF16reverse40_round138_sources_v1_20261008 as generator
    from BF16reverse138_storage_v1_20261008 import OUTPUTS,empty,installed_transfer
    proof_path=A/'BF16reverse40_prospective_routes_v1_20261008.json';assert not proof_path.exists()
    scorer=A/'run_BF16reverse40_official_comparison_v1_20261008.py';tree=ast.parse(scorer.read_text(encoding='utf8'))
    item=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in n.targets) and isinstance(n.value,ast.Dict))
    schema={k.value for k in item.keys if isinstance(k,ast.Constant)}
    names=[scorer,Path(__file__),Path(generator.__file__),A/'prepare_BF16reverse138_complete_receivers_v1_20261008.py',
        A/'prepare_BF16reverse40_selected_candidate_v1_20261008.py',A/'seal_BF16reverse40_selected_candidate_v1_20261008.py',
        A/'run_BF16reverse40_round138_full_registration_v1_20261008.py',A/'publish_BF16reverse40_evidence_v1_20261008.py',
        A/'verify_BF16reverse40_round138_sources_v1_20261008.py',A/'queue_BF16reverse138_complete_pipeline_v1_20261008.py',
        A/'BF16reverse138_storage_v1_20261008.py',A/'BF16reverse40_round138_plan_v1_20261008.json',
        A/'BF16reverse138_receiver_preparation_v1_20261008.json',A/'predict_BF16_reverse_complete_parent_scheme_v1_20261008.py',
        A/'BF16_reverse_complete_parent_native_stage_v1_20261008.py',A/'BF16_reverse_complete_parent_rank_CDF_v1_20261008.py']
    for p in names:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    for path in OUTPUTS:empty(path)
    future=set(generator.source_paths())-set(p for p in generator.source_paths() if p.is_file())
    allowed=set(A/n for n in generator.NAMES.values())|{proof_path,A/'BF16reverse40_actual_controls_index_v1_20261008.json',
        A/'BF16reverse40_round138_source_admission_v1_20261008.json',A/'BF16reverse40_round138_source_preparation_v1_20261008.json',
        A/'BF16reverse40_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',A/'BF16reverse40_scores_github_v1_20261008/receipt.json'}
    assert future<=allowed,future-allowed
    graphs=[];baselines=[];outputs={};paths=[];guards=[]
    plan=read(A/'BF16reverse40_round138_plan_v1_20261008.json')
    assert plan['qualified_anchor_rounds']==[135,136,137]
    for parent in (135,136,137):
        # Future parents are prospective only; their actual qualification is required by admission.
        generated=generator.generate(parent);outputs[str(parent)]={}
        for name,text in generated.items():
            assert not (A/name).exists();compile(text,str(A/name),'exec');outputs[str(parent)][name]=hashlib.sha256(text.encode()).hexdigest()
        name='register_BF16reverse40_round138_artifacts_20261008.py';text=generated[name];registry=ast.parse(text)
        status=[n for n in ast.walk(registry) if isinstance(n,ast.Compare) and ast.unparse(n.left)=="pilot['status']"]
        assert len(status)==1 and status[0].comparators[0].value=='passed_actual40_BF16_reverse_complete_parent_rank_CDF_full_official_comparisons'
        guards.append({'parent':parent,'actual_pilot_status_guard':status[0].comparators[0].value})
        required={n.slice.value for n in ast.walk(registry) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='measured' and isinstance(n.slice,ast.Constant)}
        assert required<=schema,required-schema
        assert "'round138_full_scope' / source.relative_to(ROOT)" in text
        for p in generator.source_paths():assert p.is_file() or p in allowed,p
        paths.append({'parent':parent,'concrete_source_count':len(generator.source_paths()),'all_paths_existing_or_explicit_future':True})
        start=text.index("        if measured['case'] == pilot['best']['case']:");end=text.index('        row = ',start)
        code=compile('if True:\n'+text[start:end],name,'exec')
        actual_parent_graph=read(ROOT/'candidates/optimization_20261003_r134/verification.json')['whole_scheme_graph']
        graph_kinds={'actual134':deepcopy(actual_parent_graph)}
        augmented=deepcopy(actual_parent_graph)
        for key in ('BF16_complete_parent_rank_CDF','nonflag_CPU_CrossFamily_complete_parent_CDF','nonflag_CPU_HuberIRLS64_complete_parent_CDF'):
            augmented=deepcopy(augmented);augmented[key]={'nested_marker':[{'all_fields_must_survive':True}], 'prospective_only':True}
            graph_kinds[key]=deepcopy(augmented)
        assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in actual_parent_graph
        for graph_kind,prospective_graph in graph_kinds.items():
            for role,w in [('all_valid',0.),*[(role,w) for role in plan['roles'] for w in plan['weights']]]:
                cfg={'model':'zero_BF16_rank_identity' if w==0. else plan['model_name'],'role':role,'weight':w,'anchor_round':134,'universe':plan['rank_universe']}
                measured={'case':7,'native_bank_source':'actual six own mature wide models','ordered_native_components':[] if w==0. else [plan['model_name']],'first2020_active':w>0.}
                ns={'cfg':cfg,'measured':measured,'pilot':{'best':{'case':8},'actual_scheme_base_round':134},'deepcopy':deepcopy,'ROOT':ROOT,
                    'read':lambda path: {'whole_scheme_graph':deepcopy(prospective_graph)}}
                exec(code,ns);graph=ns['graph'];new=graph.pop('BF16_reverse_complete_parent_rank_CDF',None)
                assert graph==prospective_graph,'All original graph keys and nested branches must survive.'
                if w==0.:assert new is None
                else:assert new['role']==role and new['weight']==w and new['first2020_active'] and new['position']=='after_complete_qualified_parent' and new['signal_sign_on_valid_rows']==-1. and new['invalid_signal_bits_preserved']
                graphs.append({'comparison_parent':parent,'role':role,'weight':w,'complete_parent_graph_kind':graph_kind,'all_nested_parent_values_preserved':True,'actual_future_parent_qualification_not_claimed':True})
        body=next(n for n in registry.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
        baseline=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='comparison_baseline' for t in n.targets))
        update=next(n for n in body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and isinstance(n.value.func.value,ast.Name) and n.value.func.value.id=='selection' and n.value.func.attr=='update')
        selection_path=A/f'optimization_20261003_r{parent}/selection.json'
        actual_path=selection_path if selection_path.is_file() else A/'optimization_20261003_r134/selection.json'
        names.append(actual_path);metrics=read(actual_path)['winner']['metrics']
        for amplitude in (0.,1e-8,-4e-5):
            winner={'metrics':deepcopy(metrics)};winner['metrics']['ic_mean']+=amplitude/.4
            winner['connected_final_score']=.4*winner['metrics']['ic_mean']+.3*winner['metrics']['annual_excess']+.3*(1-winner['metrics']['mean_turnover'])
            requested=[]
            def actual_read(path):
                assert Path(path)==selection_path;requested.append(path);return {'winner':{'metrics':metrics}}
            ns={'A':A,'ROOT':ROOT,'read':actual_read,'sha':sha,'selection':{},'winner':winner,'records':[],
                'pilot':{'actual_scheme_base_round':134},'selection_source':actual_path,'GRAPH_FIELD':'conditional_flag_residual_scheme_graph','time':time}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[baseline,update],type_ignores=[])),name,'exec'),ns)
            assert len(requested)==1 and ns['selection']['baseline_score']==metrics['final_score']
            assert ns['selection']['score_gain']==winner['connected_final_score']-metrics['final_score']
            assert ns['selection']['explicit_comparison_parent_round']==parent
            baselines.append({'parent':parent,'amplitude':amplitude,'actual_gain':ns['selection']['score_gain'],'prospective_baseline_only':actual_path!=selection_path})
        pub=generated['publish_BF16reverse40_round138_full_validation_20261008.py']
        assert 'collect(138, 49, 40)' in pub and "actual_full_QA_version': 49" in pub and "namespace['snapshot'](138)" in pub
    ties=[]
    from prepare_BF16reverse138_complete_receivers_v1_20261008 import best_key
    sort_node=next(n for n in ast.walk(registry) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='records.sort')
    for parent in (135,136,137):
        for advantage in (0.,1e-8):
            samples=[{'case':case,'configuration':{'weight':weight},'connected_final_score':.451+(advantage if case==3 else 0.),'expected_unique_native_models':models} for case,weight,models in ((0,.1,18),(1,.0025,20),(2,0.,19),(3,.05,22))]
            records=[{'connected_final_score':sample['connected_final_score'],'direct_rank_comparison_configuration':sample['configuration'],'original_comparison_case':sample['case'],'actual_full_conditional_residual_control':sample} for sample in samples]
            exec(compile(ast.fix_missing_locations(ast.Module(body=[sort_node],type_ignores=[])),name,'exec'),{'records':records})
            assert records[0]['original_comparison_case']==min(samples,key=best_key)['case']
            ties.append({'parent':parent,'advantage':advantage,'same_pilot_and_registry_S_unique_SHA_models_weight_case_order':True})
    assert len(graphs)==444 and len(baselines)==9 and len(ties)==6
    # Exercise the scoped cross-volume byte-preserving transfer used by future native/alias/source flows.
    source=A/'BF16reverse138_transfer_probe_v2_20261008.bin';target=Path('E:/赛题五_本机临时/第138轮_20261008/transfer_probe_v2.bin')
    assert not source.exists() and not target.exists();source.write_bytes(bytes(range(256))*31)
    with installed_transfer():__import__('os').link(source,target)
    assert sha(source)==sha(target)
    names += [source,target,A/'BF16reverse138_prospective_scope_reference_recovery_v1_20261008.json',A/'verify_BF16reverse40_prospective_routes_v1_20261008.py']
    from verify_BF16reverse138_D_scoring_scope_v1_20261008 import main as scope_checks
    actual_scope=read(A/'BF16reverse138_D_scoring_scope_v1_20261008.json')
    assert actual_scope['status']=='passed_actual3_original_scope_guards_reject_E_and_accept_both_D_scoring_directories'
    for p,d in actual_scope['input_sha256'].items():assert sha(p)==d,p
    names += [A/'verify_BF16reverse138_D_scoring_scope_v1_20261008.py',A/'BF16reverse138_D_scoring_scope_v1_20261008.json']
    names += [A/'BF16reverse138_D_scoring_scope_v1_20261008.json',A/'prepare_BF16reverse138_preflight_v1_20261008.py']
    create(proof_path,{'status':'passed_actual24_prospective138_sources_schema_graphs_baselines_status_paths_and_cross_volume_bytes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in names},
        'generated_source_sha256':outputs,'actual_scoring_item_fields':sorted(schema),'graph_controls':graphs,
        'baseline_gain_regressions':baselines,'model_count_sort_controls':ties,'source_path_controls':paths,'truthful_status_guards':guards,
        'prospective_sources':24,'cross_volume_transfer_bytes':source.stat().st_size,
        'actual_full_GPU_CDF_hooks_not_yet_claimed':True,'future_candidate_and_QA49_not_yet_executed':True,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print('All24 prospective138 receivers admitted structurally; actual GPU full controls remain prerequisites.',flush=True)


if __name__=='__main__':main()
