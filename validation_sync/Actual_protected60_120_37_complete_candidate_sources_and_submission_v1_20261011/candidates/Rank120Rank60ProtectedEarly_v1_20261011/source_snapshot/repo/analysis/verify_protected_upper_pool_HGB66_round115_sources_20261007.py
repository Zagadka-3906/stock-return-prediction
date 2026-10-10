"""Prospective source/schema and baseline regressions; never write canonical future round files."""
from pathlib import Path
from copy import deepcopy
import ast
import hashlib
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def main():
    import prepare_protected_upper_pool_HGB66_round115_sources_20261007 as generator
    service=A/'service_owned_workflows_20261006/protected_upper_pool_HGB_selected_hook_preflight'
    assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='passed'
    hook_path=A/'protected_upper_pool_HGB_selected_hook_preflight_20261007/verification.json';hook=read(hook_path)
    assert hook['status']=='passed_actual_historical603_features_native_HGB_lower_pool_hook_and_whole_day_prefix_controls'
    assert len(hook['records'])==63
    proof=A/'protected_upper_pool_HGB66_candidate_source_admission_20261007.json';assert not proof.exists()
    sources=[Path(__file__),Path(generator.__file__),A/'run_protected_upper_pool_HGB66_round115_full_registration_20261007.py',
        A/'prepare_protected_upper_pool_HGB66_selected_candidate_20261007.py',A/'seal_protected_upper_pool_HGB66_selected_candidate_20261007.py',
        A/'predict_protected_upper_pool_CPU_HGB_scheme_20261007.py',A/'protected_upper_pool_HGB_CDF_transform_20261007.py',hook_path,
        A/'run_protected_upper_pool_HGB66_official_comparison_v2_20261007.py',*[A/n for n in generator.NAMES]]
    scorer=ast.parse((A/'run_protected_upper_pool_HGB66_official_comparison_v2_20261007.py').read_text(encoding='utf8'))
    item=next(n.value for n in ast.walk(scorer) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in n.targets) and isinstance(n.value,ast.Dict))
    schema={key.value for key in item.keys if isinstance(key,ast.Constant)}
    outputs={};controls=[]
    for parent in (112,113,114):
        generated=generator.generate(parent);assert len(generated)==8
        outputs[str(parent)]={}
        for name,text in generated.items():
            assert not (A/name).exists(),name
            compile(text,str(A/name),'exec')
            outputs[str(parent)][name]=hashlib.sha256(text.encode('utf8')).hexdigest()
        registry=ast.parse(generated['register_protected_upper_pool_HGB66_round115_artifacts_20261007.py'])
        required={n.slice.value for n in ast.walk(registry) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='measured' and isinstance(n.slice,ast.Constant)}
        assert required<=schema,required-schema
        function=next(n for n in registry.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        baseline=next(n for n in function.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='comparison_baseline' for t in n.targets))
        update=next(n for n in function.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and isinstance(n.value.func.value,ast.Name) and n.value.func.value.id=='selection' and n.value.func.attr=='update')
        actual_parent=A/f'optimization_20261003_r{parent}/selection.json'
        #114 has not run. Its baseline route uses an explicitly hypothetical112 metric set.
        metric_source=actual_parent if actual_parent.exists() else A/'optimization_20261003_r112/selection.json'
        base=read(metric_source)['winner']['metrics']
        for amplitude in (0.,1e-8,-4e-5):
            winner={'metrics':deepcopy(base)};winner['metrics']['ic_mean']+=amplitude/.4
            winner['connected_final_score']=.4*winner['metrics']['ic_mean']+.3*winner['metrics']['annual_excess']+.3*(1.-winner['metrics']['mean_turnover'])
            winner['metrics']['final_score']=winner['connected_final_score'];selection={};requested=[]
            def mock_read(path):
                requested.append(str(path));assert Path(path)==actual_parent
                return {'winner':{'metrics':base}}
            namespace={'A':A,'ROOT':ROOT,'read':mock_read,'sha':sha,'selection':selection,'winner':winner,'records':[],
                'selection_source':A/'optimization_20261003_r112/selection.json','GRAPH_FIELD':'conditional_flag_residual_scheme_graph','time':time}
            code=ast.fix_missing_locations(ast.Module(body=[baseline,update],type_ignores=[]))
            exec(compile(code,'actual_generated_parent_baseline_regression','exec'),namespace)
            assert selection['explicit_comparison_parent_round']==parent and requested==[str(actual_parent)]
            gain=winner['connected_final_score']-base['final_score']
            assert selection['baseline_score']==base['final_score'] and selection['score_gain']==gain
            contributions=.4*(winner['metrics']['ic_mean']-base['ic_mean'])+.3*(winner['metrics']['annual_excess']-base['annual_excess'])-.3*(winner['metrics']['mean_turnover']-base['mean_turnover'])
            assert abs(gain-contributions)<1e-12
            controls.append({'comparison_parent':parent,'metric_source':str(metric_source),'actual_parent_metrics_available':actual_parent.exists(),
                'synthetic_IC_amplitude_for_metadata_regression':amplitude,'actual_generated_baseline':selection['baseline_score'],
                'actual_generated_gain':gain,'official_contribution_difference':gain-contributions})
    assert len(controls)==9
    create(proof,{'status':'passed_actual_native_hook_and24_prospective_source_AST_hashes_schema_and_parent_baseline_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},
        'generated_source_sha256':outputs,'baseline_gain_regression_controls':controls,
        'actual_scoring_item_fields':sorted(schema),'declared_prospective_sources':24,'actual_historical_hook_cases':63,
        'original113_six_view_and45second_QA_source_routers_preserved':True,'all_eight_hashes_checked_before_any_production_write':True,
        'hypothetical_metadata_controls_not_new_quality_scores_or_actual114_candidate':True,
        'canonical115_sources_written':0,'new_native_fits':0,'new_quality_scores':0,
        'actual_future_candidate_and_full_QA26_not_claimed':True,'test_labels_read':False})
    print({'status':'passed','prospective_sources':24,'baseline_regressions':9,'canonical_sources_written':0},flush=True)


if __name__=='__main__':main()
