"""Validate all24 prospective receivers using real qualified parent graphs and truthful score schemas."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create


def main():
    import prepare_BF16wide40_round135_sources_v2_20261008 as generator
    from BF16wide135_storage_v1_20261008 import OUTPUTS,empty,installed_transfer
    proof_path=A/'BF16wide40_prospective_routes_v2_20261008.json';assert not proof_path.exists()
    scorer=A/'run_BF16wide40_official_comparison_v2_20261008.py';tree=ast.parse(scorer.read_text(encoding='utf8'))
    item=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in n.targets) and isinstance(n.value,ast.Dict))
    schema={k.value for k in item.keys if isinstance(k,ast.Constant)}
    names=[scorer,Path(__file__),Path(generator.__file__),A/'prepare_BF16wide135_receivers_v1_20261008.py',
        A/'prepare_BF16wide40_selected_candidate_v2_20261008.py',A/'seal_BF16wide40_selected_candidate_v2_20261008.py',
        A/'run_BF16wide40_round135_full_registration_v2_20261008.py',A/'publish_BF16wide40_evidence_v2_20261008.py',
        A/'verify_BF16wide40_round135_sources_v2_20261008.py',A/'queue_BF16wide135_complete_pipeline_v2_20261008.py',
        A/'BF16wide135_storage_v1_20261008.py',A/'BF16wide40_round135_plan_v1_20261008.json',
        A/'BF16wide135_receiver_preparation_v2_20261008.json',A/'predict_BF16_complete_parent_rank_scheme_v1_20261008.py',
        A/'BF16_complete_parent_native_stage_v1_20261008.py',A/'BF16_complete_parent_rank_CDF_v1_20261008.py']
    for p in names:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    for path in OUTPUTS:empty(path)
    future=set(generator.source_paths())-set(p for p in generator.source_paths() if p.is_file())
    allowed=set(A/n for n in generator.NAMES.values())|{proof_path,A/'BF16wide40_actual_controls_index_v1_20261008.json',
        A/'BF16wide40_round135_source_admission_v2_20261008.json',A/'BF16wide40_round135_source_preparation_v2_20261008.json',
        A/'BF16wide40_selected_release_v1_20261008/selected_candidate_ready_for_registration.json',A/'BF16wide40_scores_github_v2_20261008/receipt.json'}
    assert future<=allowed,future-allowed
    graphs=[];baselines=[];outputs={};paths=[];guards=[]
    plan=read(A/'BF16wide40_round135_plan_v1_20261008.json')
    assert plan['qualified_anchor_rounds']==[112,133,134]
    for parent in (112,133,134):
        assert read(A/f'optimization_20261003_r{parent}/full_registration_execution.json')['status']=='passed'
        generated=generator.generate(parent);outputs[str(parent)]={}
        for name,text in generated.items():
            assert not (A/name).exists();compile(text,str(A/name),'exec');outputs[str(parent)][name]=hashlib.sha256(text.encode()).hexdigest()
        name='register_BF16wide40_round135_artifacts_20261008.py';text=generated[name];registry=ast.parse(text)
        status=[n for n in ast.walk(registry) if isinstance(n,ast.Compare) and ast.unparse(n.left)=="pilot['status']"]
        assert len(status)==1 and status[0].comparators[0].value=='passed_actual40_BF16_complete_parent_rank_CDF_full_official_comparisons'
        guards.append({'parent':parent,'actual_pilot_status_guard':status[0].comparators[0].value})
        required={n.slice.value for n in ast.walk(registry) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='measured' and isinstance(n.slice,ast.Constant)}
        assert required<=schema,required-schema
        assert "'round135_full_scope' / source.relative_to(ROOT)" in text
        for p in generator.source_paths():assert p.is_file() or p in allowed,p
        paths.append({'parent':parent,'concrete_source_count':len(generator.source_paths()),'all_paths_existing_or_explicit_future':True})
        start=text.index("        if measured['case'] == pilot['best']['case']:");end=text.index('        row = ',start)
        code=compile('if True:\n'+text[start:end],name,'exec')
        actual_parent_graph=read(ROOT/'candidates/optimization_20261003_r134/verification.json')['whole_scheme_graph']
        assert 'nonflag_CPU_ReverseBayes64_residual_CDF' in actual_parent_graph
        for role,w in [('all_valid',0.),*[(role,w) for role in plan['roles'] for w in (.0025,1.)]]:
            cfg={'model':'zero_BF16_rank_identity' if w==0. else plan['model_name'],'role':role,'weight':w,'anchor_round':134,'universe':plan['rank_universe']}
            measured={'case':7,'native_bank_source':'actual six own mature wide models','ordered_native_components':[] if w==0. else [plan['model_name']],'first2020_active':w>0.}
            ns={'cfg':cfg,'measured':measured,'pilot':{'best':{'case':8},'actual_scheme_base_round':134},'deepcopy':deepcopy,'ROOT':ROOT,
                'read':lambda path: {'whole_scheme_graph':deepcopy(actual_parent_graph)}}
            exec(code,ns);graph=ns['graph'];new=graph.pop('BF16_complete_parent_rank_CDF',None)
            assert graph==actual_parent_graph,'All original graph keys and nested branches must survive.'
            if w==0.:assert new is None
            else:assert new['role']==role and new['weight']==w and new['first2020_active'] and new['position']=='after_complete_qualified_parent'
            graphs.append({'comparison_parent':parent,'role':role,'weight':w,'all_actual134_parent_graph_values_preserved':True})
        body=next(n for n in registry.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
        baseline=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='comparison_baseline' for t in n.targets))
        update=next(n for n in body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and isinstance(n.value.func.value,ast.Name) and n.value.func.value.id=='selection' and n.value.func.attr=='update')
        selection_path=A/f'optimization_20261003_r{parent}/selection.json';metrics=read(selection_path)['winner']['metrics']
        for amplitude in (0.,1e-8,-4e-5):
            winner={'metrics':deepcopy(metrics)};winner['metrics']['ic_mean']+=amplitude/.4
            winner['connected_final_score']=.4*winner['metrics']['ic_mean']+.3*winner['metrics']['annual_excess']+.3*(1-winner['metrics']['mean_turnover'])
            requested=[]
            def actual_read(path):
                assert Path(path)==selection_path;requested.append(path);return {'winner':{'metrics':metrics}}
            ns={'A':A,'ROOT':ROOT,'read':actual_read,'sha':sha,'selection':{},'winner':winner,'records':[],
                'pilot':{'actual_scheme_base_round':134},'selection_source':selection_path,'GRAPH_FIELD':'conditional_flag_residual_scheme_graph','time':time}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[baseline,update],type_ignores=[])),name,'exec'),ns)
            assert len(requested)==1 and ns['selection']['baseline_score']==metrics['final_score']
            assert ns['selection']['score_gain']==winner['connected_final_score']-metrics['final_score']
            assert ns['selection']['explicit_comparison_parent_round']==parent
            baselines.append({'parent':parent,'amplitude':amplitude,'actual_gain':ns['selection']['score_gain']})
        pub=generated['publish_BF16wide40_round135_full_validation_20261008.py']
        assert 'collect(135, 46, 40)' in pub and "actual_full_QA_version': 46" in pub and "namespace['snapshot'](135)" in pub
    # Exercise the scoped cross-volume byte-preserving transfer used by future native/alias/source flows.
    source=A/'BF16wide135_transfer_probe_v2_20261008.bin';target=Path('E:/赛题五_本机临时/第135轮_20261008/transfer_probe_v2.bin')
    assert not source.exists() and not target.exists();source.write_bytes(bytes(range(256))*31)
    with installed_transfer():__import__('os').link(source,target)
    assert sha(source)==sha(target)
    names += [source,target]
    from verify_BF16wide135_D_scoring_scope_v2_20261008 import main as scope_checks
    scope_checks()
    names += [A/'verify_BF16wide135_D_scoring_scope_v2_20261008.py',A/'BF16wide135_D_scoring_scope_v2_20261008.json',A/'actual_BF16wide135_D_scoring_receiver_recovery_v4_20261008.json']
    create(proof_path,{'status':'passed_actual24_prospective135_sources_schema_graphs_baselines_status_paths_and_cross_volume_bytes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in names},
        'generated_source_sha256':outputs,'actual_scoring_item_fields':sorted(schema),'graph_controls':graphs,
        'baseline_gain_regressions':baselines,'source_path_controls':paths,'truthful_status_guards':guards,
        'prospective_sources':24,'cross_volume_transfer_bytes':source.stat().st_size,
        'actual_full_GPU_CDF_hooks_not_yet_claimed':True,'future_candidate_and_QA46_not_yet_executed':True,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print('All24 prospective135 receivers admitted structurally; actual GPU full controls remain prerequisites.',flush=True)


if __name__=='__main__':main()
