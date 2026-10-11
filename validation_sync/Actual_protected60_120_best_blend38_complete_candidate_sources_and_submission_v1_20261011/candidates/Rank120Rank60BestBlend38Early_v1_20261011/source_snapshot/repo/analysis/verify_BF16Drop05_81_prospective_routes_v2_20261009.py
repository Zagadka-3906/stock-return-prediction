"""Execute40 prospective route contracts, signed graph preservation, baselines and physical-model ties."""
from pathlib import Path
from copy import deepcopy
import sys,ast,hashlib,time,os
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import prepare_BF16Drop05_81_round156_sources_v1_20261009 as g
    from prepare_BF16Drop05_156_core_drafts_v1_20261009 import best_key
    from BF16Drop05_156_storage_v1_20261009 import OUTPUTS,empty,installed_transfer
    proofpath=A/'BF16Drop05_81_prospective_routes_v1_20261009.json';assert not proofpath.exists()
    scorer=A/'run_BF16Drop05_81_official_comparison_v1_20261009.py';tree=ast.parse(scorer.read_text(encoding='utf8'))
    item=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in n.targets) and isinstance(n.value,ast.Dict))
    schema={k.value for k in item.keys if isinstance(k,ast.Constant)}
    planpath=A/'BF16Drop05_81_round156_plan_v1_20261009.json';plan=read(planpath)
    assert plan['qualified_anchor_rounds']==[148,149,150,151,152,153,154,155] and len(plan['new_cases'])==73 and plan['expected_scored_records']==81
    sources=[Path(__file__),Path(g.__file__),scorer,planpath,A/'prepare_BF16Drop05_156_core_drafts_v1_20261009.py',
      A/'prepare_BF16Drop05_81_selected_candidate_v1_20261009.py',A/'seal_BF16Drop05_81_selected_candidate_v1_20261009.py',
      A/'run_BF16Drop05_81_round156_full_registration_v1_20261009.py',A/'publish_BF16Drop05_81_evidence_v1_20261009.py',
      A/'BF16Drop05_156_actual_receiver_bindings_v1_20261009.json',A/'BF16Drop05_156_storage_v1_20261009.py',
      A/'BF16Drop05_156_D_scoring_scope_v1_20261009.json',A/'BF16Drop05_156_complete_native_predictor_preparation_v1_20261009.json']
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    for p in OUTPUTS:empty(p)
    allowed={*(A/n for n in g.NAMES.values()),proofpath,
      A/'verify_BF16Drop05_81_round156_sources_v1_20261009.py',A/'BF16Drop05_81_round156_source_admission_v1_20261009.json',
      A/'BF16Drop05_81_actual_controls_index_v1_20261009.json',A/'BF16Drop05_81_round156_source_preparation_v1_20261009.json',
      A/'BF16Drop05_81_selected_release_v1_20261009/selected_candidate_ready_for_registration.json',
      A/'BF16Drop05_81_scores_github_v1_20261009/receipt.json',A/'actual_BF16Drop05_156_prior_complete_forecast_duplicate_audit_v1_20261009.json',
      A/'actual_BF16Drop05_156_full73_training_location_v1_20261009.json'}
    allowed.update({A/'actual_BF16Drop05_156_full73_training_location_v1_20261009.json'})
    allowed.update({A/'actual_BF16Drop05_156_native42_calendar_location_v1_20261009.json',A/'actual_BF16Drop05_156_full5_independent_location_v1_20261009.json',A/'actual_BF16_medium2048_drop05_seed09_e64_bank6_location_v1_20261009.json'})
    missing={p for p in g.source_paths() if not p.is_file()};assert missing<=allowed,missing-allowed
    sources.extend(p for p in g.source_paths() if p.is_file())
    baseproof=ROOT/'candidates/optimization_20261003_r148/verification.json';base=read(baseproof)['whole_scheme_graph'];sources.append(baseproof)
    assert 'nonflag_CPU_joint_Cross_Huber_adaptive_complete_parent_CDF' in base and plan['graph_key'] not in base
    variants={'actual_entire148':deepcopy(base)}
    for i,key in enumerate(('nested_sparse_after148_probe','nested_neural_probe','nested_postprocessor_probe')):
        augmented=deepcopy(base);augmented[key]={'all_original_fields_must_survive':[{'probe':i,'signed_values':[-.2,0.,.3]}]};variants[key]=augmented
    outputs={};graphs=[];baselines=[];sorts=[];collectors=[]
    registry_name='register_BF16Drop05_81_round156_artifacts_20261009.py'
    for parent in plan['qualified_anchor_rounds']:
        generated=g.generate(parent);outputs[str(parent)]={}
        for name,s in generated.items():
            assert not (A/name).exists();compile(s,str(A/name),'exec');outputs[str(parent)][name]=hashlib.sha256(s.encode()).hexdigest()
        text=generated[registry_name];registry=ast.parse(text)
        guard=next(n for n in ast.walk(registry) if isinstance(n,ast.Compare) and ast.unparse(n.left)=="pilot['status']")
        assert guard.comparators[0].value=='passed_actual81_BF16_medium2048_drop05_seed09_complete_parent_rank_CDF_full_official_comparisons'
        required={n.slice.value for n in ast.walk(registry) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='measured' and isinstance(n.slice,ast.Constant)}
        assert required<=schema,required-schema
        assert "'round156_full_scope' / (source.relative_to(ROOT) if source.is_relative_to(ROOT)" in text
        start=text.index("        if measured['case'] == pilot['best']['case']:");end=text.index('        row = ',start)
        code=compile('if True:\n'+text[start:end],registry_name,'exec')
        for variant,parentgraph in variants.items():
            for case,c in enumerate(plan['new_cases']):
                cfg={'anchor_round':148,'model':plan['model_name'] if c['weight'] else 'zero_BF16_rank_identity','role':c['role'],'weight':c['weight'],'sign':c['sign'],'universe':plan['rank_universe']}
                measured={'case':7,'native_bank_source':'six actual own2048 mature annual models','ordered_native_components':[plan['model_name']] if c['weight'] else [],'first2020_active':bool(c['weight'])}
                ns={'cfg':cfg,'measured':measured,'pilot':{'best':{'case':8},'actual_scheme_base_round':148},'ROOT':ROOT,'deepcopy':deepcopy,
                    'read':lambda p:{'whole_scheme_graph':deepcopy(parentgraph)}}
                exec(code,ns);graph=ns['graph'];new=graph.pop(plan['graph_key'],None);assert graph==parentgraph
                if c['weight']:
                    assert new['sign']==c['sign'] and new['role']==c['role'] and new['weight']==c['weight']
                    assert new['first2020_active'] and new['original_complete_parent_round']==148 and new['invalid_signal_bits_preserved']
                else:assert new is None
                graphs.append({'comparison_parent':parent,'parent_graph':variant,'case':case,'kind':'new_or_zero','all_nested_parent_fields_preserved':True,'sign':c['sign']})
            for selected in (False,True):
                cfg={'anchor_round':parent,'model':None,'weight':0.}
                ns={'cfg':cfg,'measured':{'case':8 if selected else 7},'pilot':{'best':{'case':8},'actual_scheme_base_round':148},
                  'ROOT':ROOT,'deepcopy':deepcopy,'actual':{'whole_scheme_graph':parentgraph},'read':lambda p:{'whole_scheme_graph':deepcopy(parentgraph)}}
                exec(code,ns);assert ns['graph']==parentgraph
                graphs.append({'comparison_parent':parent,'parent_graph':variant,'kind':'selected' if selected else 'anchor','all_nested_parent_fields_preserved':True})
        body=next(n for n in registry.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
        baseline=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='comparison_baseline' for t in n.targets))
        update=next(n for n in body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='selection.update')
        selection_path=A/f'optimization_20261003_r{parent}/selection.json';actual_path=selection_path if selection_path.is_file() else A/'optimization_20261003_r148/selection.json'
        sources.append(actual_path);metrics=read(actual_path)['winner']['metrics']
        for amplitude in (0.,1e-8,-4e-5):
            winner={'metrics':deepcopy(metrics),'connected_final_score':metrics['final_score']+amplitude};requested=[]
            def actual_read(path):
                assert Path(path)==selection_path;requested.append(path);return {'winner':{'metrics':metrics}}
            ns={'A':A,'ROOT':ROOT,'read':actual_read,'sha':sha,'selection':{},'winner':winner,'records':[],
              'pilot':{'actual_scheme_base_round':148},'selection_source':actual_path,'GRAPH_FIELD':'conditional_flag_residual_scheme_graph','time':time}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[baseline,update],type_ignores=[])),registry_name,'exec'),ns)
            assert len(requested)==1 and ns['selection']['baseline_score']==metrics['final_score']
            assert ns['selection']['score_gain']==winner['connected_final_score']-metrics['final_score'] and ns['selection']['explicit_comparison_parent_round']==parent
            baselines.append({'parent':parent,'amplitude':amplitude,'comparison_baseline_and_gain_exact':True,'actual_parent_qualification_not_claimed':True})
        sort=next(n for n in ast.walk(registry) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and ast.unparse(n.value.func)=='records.sort')
        for advantage in (0.,1e-8):
            samples=[{'case':case,'configuration':{'weight':weight},'connected_final_score':.451+(advantage if case==4 else 0.),'expected_unique_native_models':models}
              for case,weight,models in ((0,.1,24),(1,-.002,25),(2,0.,24),(3,.004,24),(4,.1,26))]
            records=[{'connected_final_score':r['connected_final_score'],'direct_rank_comparison_configuration':r['configuration'],'original_comparison_case':r['case'],'actual_full_conditional_residual_control':r} for r in samples]
            exec(compile(ast.fix_missing_locations(ast.Module(body=[sort],type_ignores=[])),registry_name,'exec'),{'records':records})
            assert records[0]['original_comparison_case']==min(samples,key=best_key)['case']
            assert records[0]['original_comparison_case']==(4 if advantage else 2)
            sorts.append({'parent':parent,'advantage':advantage,'identical_complete_S_physical_model_count_absolute_weight_case_order':True})
        pub=generated['publish_BF16Drop05_81_round156_full_validation_20261009.py']
        assert 'collect(155, 66, 80)' in pub and "actual_full_QA_version': 66" in pub and "namespace['snapshot'](155)" in pub
        for filename in ('lossless_ranking_runtime_adapter_round156_v2_20261008.py','build_lossless_ranking_display_round156_v2_20261008.py','verify_lossless_ranking_display_round156_v2_20261008.py'):
            routes='\n'.join(generated.values())+(A/'run_BF16Drop05_81_round156_full_registration_v1_20261009.py').read_text(encoding='utf8')
            assert filename.removesuffix('.py') in routes,filename
        collectors.append({'parent':parent,'target':156,'QA_version':67,'official_cases':81,'original_six_view_contract_retained':True})
    assert len(outputs)==8 and sum(map(len,outputs.values()))==64 and len(graphs)==2400 and len(baselines)==24 and len(sorts)==16
    source=A/'BF16Drop05_156_transfer_probe_v1_20261009.bin';target=Path('E:/赛题五_本机临时/第156轮_20261009/transfer_probe_v1.bin')
    assert not source.exists() and not target.exists();source.write_bytes(bytes(range(256))*31)
    with installed_transfer():os.link(source,target)
    assert sha(source)==sha(target);sources.extend((source,target))
    scope=read(A/'BF16Drop05_156_D_scoring_scope_v1_20261009.json')
    assert len(scope['controls'])==9
    for p,d in scope['input_sha256'].items():assert sha(p)==d,p
    create(proofpath,{'status':'passed_actual64_drop05_156_prospective_sources2400_graphs24_baselines16_physical_model_sort_checks',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in dict.fromkeys(sources)},
      'generated_source_sha256':outputs,'actual_scoring_item_fields':sorted(schema),'graph_controls':graphs,'baseline_controls':baselines,
      'physical_model_count_absolute_weight_sort_controls':sorts,'collector_contracts':collectors,'prospective_sources':64,
      'actual_future_parent_qualification_not_claimed':True,'actual_future_X_read':False,'new_quality_scores':0,'test_labels_read':False})
    print({'prospective_sources':64,'graph_controls':2400,'baselines':24,'physical_model_ties':16,'quality_admitted':False},flush=True)

if __name__=='__main__':main()
