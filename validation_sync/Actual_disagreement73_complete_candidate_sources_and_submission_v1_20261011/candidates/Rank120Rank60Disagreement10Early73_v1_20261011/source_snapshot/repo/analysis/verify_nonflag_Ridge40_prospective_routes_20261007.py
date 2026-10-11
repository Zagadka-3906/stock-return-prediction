"""Execute prospective schema and graph controls; future baselines remain explicitly pending."""
from pathlib import Path
from copy import deepcopy
import ast,sys,time,hashlib
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import prepare_nonflag_Ridge40_round121_sources_v1_20261007 as generator
    plan=read(A/'nonflag_Ridge40_plan_20261007.json'); out=A/'nonflag_Ridge40_prospective_routes_20261007.json'; assert not out.exists()
    tree=ast.parse((A/'run_nonflag_Ridge40_official_comparison_v1_20261007.py').read_text(encoding='utf8'))
    item=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in n.targets) and isinstance(n.value,ast.Dict))
    schema={k.value for k in item.keys if isinstance(k,ast.Constant)}
    prospective={A/n for n in generator.NAMES.values()}|{A/'nonflag_Ridge40_round121_source_admission_v1_20261007.json',
        A/'nonflag_Ridge40_round121_source_preparation_v1_20261007.json',A/'nonflag_Ridge40_scores_github_v1_20261007/receipt.json',
        A/'nonflag_Ridge40_selected_release_v1_20261007/selected_candidate_ready_for_registration.json',
        *[A/f'github_validation_sync_main_20261005/round{n}_receipt.json' for n in (119,120)]}
    issues=[]; outputs={}; graph_controls=[]; path_controls=[]
    for parent in (112,119,120):
        generated=generator.generate(parent); outputs[str(parent)]={n:hashlib.sha256(t.encode('utf8')).hexdigest() for n,t in generated.items()}
        for n,t in generated.items():compile(t,str(A/n),'exec')
        name='register_nonflag_Ridge40_round121_artifacts_20261007.py'; text=generated[name]; registry=ast.parse(text)
        required={n.slice.value for n in ast.walk(registry) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='measured' and isinstance(n.slice,ast.Constant)}
        assert required<=schema
        body=next(n for n in registry.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
        assignment=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='sources' for t in n.targets))
        ns={'A':A,'ROOT':ROOT,'Path':Path,'__file__':str(A/name)}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[assignment],type_ignores=[])),name,'exec'),ns)
        for p in ns['sources']:
            if not (p.is_file() or p in prospective):issues.append({'parent':parent,'missing_unclassified_source':str(p)})
        path_controls.append({'parent':parent,'source_count':len(ns['sources'])})
        start=text.index("        if measured['case'] == pilot['best']['case']:"); end=text.index('        row = ',start)
        code=compile('if True:\n'+text[start:end],name,'exec')
        fake={'core':{'native_SHA':'preserved106'},'conditional_flag_CPU_HGB_residual_CDF':{'complete_flag_parent':'preserved'},'nonflag_CPU_HGB_residual_CDF':{'old_branch':'must_be_removed'}}
        examples=[('remove_nonflag_Ridge',0.,[]),*[(n,.0125,[n]) for n in plan['single_native_heads']],*[(n,.0125,c) for n,c in plan['ensembles'].items()]]
        for model,weight,components in examples:
            env={'cfg':{'model':model,'weight':weight,'anchor_round':112,'universe':plan['universe']},'measured':{'case':7,'native_bank_source':'actual10','ordered_native_components':components},
                'pilot':{'best':{'case':8},'actual_scheme_base_round':112},'deepcopy':deepcopy,'ROOT':ROOT,'read':lambda path:{'whole_scheme_graph':fake}}
            exec(code,env); graph=env['graph']
            assert graph['core']==fake['core'] and graph['conditional_flag_CPU_HGB_residual_CDF']==fake['conditional_flag_CPU_HGB_residual_CDF']
            assert 'nonflag_CPU_HGB_residual_CDF' not in graph
            if components: assert graph['nonflag_CPU_Ridge_residual_CDF']['ordered_equal_mean_components']==components
            else:assert 'nonflag_CPU_Ridge_residual_CDF' not in graph
            graph_controls.append({'parent':parent,'model':model,'flag_graph_preserved':True,'old_nonflag_HGB_removed':True})
        assert 'nonflag_residual_Ridge_native_replay_verification.json' in text
    runtime=A/'run_nonflag_Ridge40_round121_full_registration_v1_20261007.py'; rtext=runtime.read_text(encoding='utf8')
    for n in ast.walk(ast.parse(rtext)):
        if isinstance(n,ast.ImportFrom) and n.module and any(n.module.startswith(p) for p in ('register_','lossless_ranking_runtime_adapter_round121','publish_nonflag_')):
            if n.module+'.py' not in generator.NAMES.values():issues.append({'missing_generated_runtime_import':n.module})
    for n in ast.walk(ast.parse(rtext)):
        if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.endswith('.py') and 'round121' in n.value:
            if Path(n.value).name not in generator.NAMES.values():issues.append({'missing_generated_runtime_literal':n.value})
    create(out,{'status':'passed_actual24_prospective_sources_and12_graph_controls' if not issues else 'failed_actual_prospective_route_audit',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'issues':issues,'generated_source_sha256':outputs,'actual_graph_controls':graph_controls,'actual_source_path_controls':path_controls,
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(generator.__file__),runtime,A/'nonflag_Ridge40_plan_20261007.json']},
        'qualified119_120_real_baseline_admission_not_claimed':True,'actual_quality_scores':0,'test_labels_read':False})
    print({'status':'passed' if not issues else 'failed','issues':issues,'actual_graph_controls':len(graph_controls)},flush=True)
if __name__=='__main__':main()
