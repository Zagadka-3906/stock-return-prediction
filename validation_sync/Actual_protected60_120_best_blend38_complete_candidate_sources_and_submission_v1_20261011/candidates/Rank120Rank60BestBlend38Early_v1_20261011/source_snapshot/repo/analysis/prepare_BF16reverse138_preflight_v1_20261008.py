"""Adapt the proven prospective test to four full parent graphs and all36 reverse configurations."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_BF16reverse138_complete_receivers_v1_20261008 import adapt


def main():
    source=A/'verify_BF16wide40_prospective_routes_v5_20261008.py';text=adapt(source.read_text(encoding='utf8'))
    text=text.replace('BF16reverse40_prospective_routes_v5_20261008','BF16reverse40_prospective_routes_v1_20261008')
    text=text.replace('prepare_BF16reverse138_receivers_v1_20261008.py','prepare_BF16reverse138_complete_receivers_v1_20261008.py')
    text=text.replace('verify_BF16reverse138_actual_output_contract_v4_20261008.py','verify_BF16reverse138_D_scoring_scope_v1_20261008.py')
    text=text.replace('assert plan[\'qualified_anchor_rounds\']==[112,133,134]',"assert plan['qualified_anchor_rounds']==[135,136,137]")
    text=text.replace("        assert read(A/f'optimization_20261003_r{parent}/full_registration_execution.json')['status']=='passed'", "        # Future parents are prospective only; their actual qualification is required by admission.")
    needle="        actual_parent_graph=read(ROOT/'candidates/optimization_20261003_r134/verification.json')['whole_scheme_graph']"
    assert text.count(needle)==1
    extra="""        graph_kinds={'actual134':deepcopy(actual_parent_graph)}
        augmented=deepcopy(actual_parent_graph)
        for key in ('BF16_complete_parent_rank_CDF','nonflag_CPU_CrossFamily_complete_parent_CDF','nonflag_CPU_HuberIRLS64_complete_parent_CDF'):
            augmented=deepcopy(augmented);augmented[key]={'nested_marker':[{'all_fields_must_survive':True}], 'prospective_only':True}
            graph_kinds[key]=deepcopy(augmented)
"""
    text=text.replace(needle,needle+'\n'+extra.rstrip())
    start=text.index("        for role,w in [('all_valid',0.)");end=text.index('        body=next(',start)
    segment=text[start:end]
    segment=segment.replace("for role,w in [('all_valid',0.),*[(role,w) for role in plan['roles'] for w in (.0025,1.)]]:","for role,w in [('all_valid',0.),*[(role,w) for role in plan['roles'] for w in plan['weights']]]:")
    segment=segment.replace('deepcopy(actual_parent_graph)','deepcopy(prospective_graph)').replace('assert graph==actual_parent_graph','assert graph==prospective_graph')
    segment=segment.replace("and new['position']=='after_complete_qualified_parent'","and new['position']=='after_complete_qualified_parent' and new['signal_sign_on_valid_rows']==-1. and new['invalid_signal_bits_preserved']")
    segment=segment.replace("'all_actual134_parent_graph_values_preserved':True","'complete_parent_graph_kind':graph_kind,'all_nested_parent_values_preserved':True,'actual_future_parent_qualification_not_claimed':True")
    text=text[:start]+"        for graph_kind,prospective_graph in graph_kinds.items():\n"+''.join('    '+line+'\n' for line in segment.splitlines())+text[end:]
    needle="selection_path=A/f'optimization_20261003_r{parent}/selection.json';metrics=read(selection_path)['winner']['metrics']";assert text.count(needle)==1
    text=text.replace(needle,"selection_path=A/f'optimization_20261003_r{parent}/selection.json'\n        actual_path=selection_path if selection_path.is_file() else A/'optimization_20261003_r134/selection.json'\n        names.append(actual_path);metrics=read(actual_path)['winner']['metrics']")
    text=text.replace("'selection_source':selection_path","'selection_source':actual_path")
    text=text.replace("'actual_gain':ns['selection']['score_gain']","'actual_gain':ns['selection']['score_gain'],'prospective_baseline_only':actual_path!=selection_path")
    # The positive prototype's old recovery contract belongs to135; retain its source without re-labeling its proof.
    start=text.index("    contract_path=A/");end=text.index("    create(proof_path,",start)
    text=text[:start]+"    names += [A/'BF16reverse138_D_scoring_scope_v1_20261008.json',A/'prepare_BF16reverse138_preflight_v1_20261008.py']\n"+text[end:]
    text=text.replace('BF16reverse138_transfer_probe_v4','BF16reverse138_transfer_probe_v1').replace('/transfer_probe_v4.bin','/transfer_probe_v1.bin')
    # Execute both pilot and registration tie rules, including same-S unique model reuse.
    marker='    # Exercise the scoped cross-volume';assert text.count(marker)==1
    tie="""    ties=[]
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
"""
    text=text.replace(marker,tie+marker)
    text=text.replace("'baseline_gain_regressions':baselines,","'baseline_gain_regressions':baselines,'model_count_sort_controls':ties,")
    text=text.replace('Actual24 prospective135 sources','Actual24 prospective138 sources and444 complete-parent graphs')
    target=A/'verify_BF16reverse40_prospective_routes_v1_20261008.py';assert not target.exists()
    compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    from prepare_BF16reverse40_round138_sources_v1_20261008 import source_paths
    sources=[Path(__file__),source,target,*[p for p in source_paths() if p.is_file()]]
    create(A/'BF16reverse138_receiver_preparation_v1_20261008.json',{
        'status':'prepared_complete40_reverse_neural_scientific_registry_and_QA49_receivers_before_quality',
        'input_sha256':{str(p):sha(p) for p in sources},'new_quality_scores':0,'actual_future_X_calls':0,
        'actual24_prospective_and444_graph_controls_still_required':True,'test_labels_read':False})
    print('Complete138 receiver set prepared; execute24 prospective,444 graphs and9 baseline/6 tie controls next.',flush=True)


if __name__=='__main__':main()
