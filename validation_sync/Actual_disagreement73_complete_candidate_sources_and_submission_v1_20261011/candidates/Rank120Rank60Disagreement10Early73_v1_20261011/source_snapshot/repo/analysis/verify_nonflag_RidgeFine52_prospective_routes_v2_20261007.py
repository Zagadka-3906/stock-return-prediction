"""Actually compile24 prospective sources and execute12 complete Ridge graph controls."""
from pathlib import Path
from copy import deepcopy
import ast,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import prepare_nonflag_RidgeFine52_round128_sources_v1_20261007 as generator
    scorer=A/'run_nonflag_RidgeFine52_official_comparison_v1_20261007.py'
    tree=ast.parse(scorer.read_text(encoding='utf8'))
    item=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in n.targets) and isinstance(n.value,ast.Dict))
    schema={k.value for k in item.keys if isinstance(k,ast.Constant)}
    plan_path=A/'nonflag_RidgeFine52_plan_20261007.json';plan=read(plan_path)
    future={A/n for n in generator.NAMES.values()}|{
      A/'nonflag_RidgeFine52_round128_source_admission_v1_20261007.json',
      A/'nonflag_RidgeFine52_round128_source_preparation_v1_20261007.json',
      A/'nonflag_RidgeFine52_scores_github_v1_20261007/receipt.json',
      A/'nonflag_RidgeFine52_selected_release_v1_20261007/selected_candidate_ready_for_registration.json',
      A/'nonflag_residual_RidgeFine49_transform_preflight_20261007/verification.json',
      A/'github_validation_sync_main_20261005/round127_receipt.json'}
    graph_controls=[];generated_hashes={};path_controls=[];issues=[]
    for parent in (112,121,127):
        sources=generator.generate(parent);generated_hashes[str(parent)]={}
        for name,text in sources.items():
            compile(text,str(A/name),'exec');generated_hashes[str(parent)][name]=hashlib.sha256(text.encode()).hexdigest()
        name='register_nonflag_RidgeFine52_round128_artifacts_20261007.py';text=sources[name];tree=ast.parse(text)
        required={n.slice.value for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='measured' and isinstance(n.slice,ast.Constant)}
        assert required<=schema,required-schema
        body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
        assignment=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='sources' for t in n.targets))
        ns={'A':A,'ROOT':ROOT,'Path':Path,'__file__':str(A/name)}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[assignment],type_ignores=[])),name,'exec'),ns)
        for path in ns['sources']:
            if not path.is_file() and path not in future:issues.append({'parent':parent,'undeclared_missing_source':str(path)})
        path_controls.append({'parent':parent,'concrete_paths':len(ns['sources'])})
        start=text.index("        if measured['case'] == pilot['best']['case']:");end=text.index('        row = ',start)
        graph_code=compile('if True:\n'+text[start:end],name,'exec')
        fake={'core':{'native_SHA':'retained106'},'conditional_flag_CPU_HGB_residual_CDF':{'flag':'retained'},
          'nonflag_CPU_HGB_residual_CDF':{'old':'remove'},'nonflag_CPU_Ridge_residual_CDF':{'old':'replace'},
          'nonflag_CPU_RFFRidge_residual_CDF':{'old':'remove'},'nonflag_CPU_RFF128_residual_CDF':{'old':'remove'}}
        examples=[('remove_nonflag_Ridge',0.,[]),*[(n,.001,[n]) for n in plan['single_native_heads']],
                  *[(n,.001,names) for n,names in plan['ensembles'].items()]]
        for model,weight,names in examples:
            ns={'cfg':{'model':model,'weight':weight,'anchor_round':112,'universe':plan['universe']},
              'measured':{'case':7,'native_bank_source':'actual10','ordered_native_components':names},
              'pilot':{'best':{'case':8},'actual_scheme_base_round':112},'deepcopy':deepcopy,'ROOT':ROOT,
              'read':lambda p:{'whole_scheme_graph':fake}}
            exec(graph_code,ns);graph=ns['graph']
            assert graph['core']==fake['core'] and graph['conditional_flag_CPU_HGB_residual_CDF']==fake['conditional_flag_CPU_HGB_residual_CDF']
            assert all(k not in graph for k in ('nonflag_CPU_HGB_residual_CDF','nonflag_CPU_RFFRidge_residual_CDF','nonflag_CPU_RFF128_residual_CDF'))
            if names:assert graph['nonflag_CPU_Ridge_residual_CDF']['ordered_equal_mean_components']==names
            else:assert 'nonflag_CPU_Ridge_residual_CDF' not in graph
            graph_controls.append({'parent':parent,'model':model,'complete_retained_graph_exact':True})
        assert 'collect(128, 39, 52)' in sources['publish_nonflag_RidgeFine52_round128_full_validation_20261007.py']
    assert len(graph_controls)==12
    create(A/'nonflag_RidgeFine52_prospective_routes_v2_20261007.json',{
      'status':'passed_actual24_prospective_sources_and12_graph_controls' if not issues else 'failed_undeclared_paths_preserved',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'issues':issues,'graph_controls':graph_controls,
      'source_path_controls':path_controls,'generated_source_sha256':generated_hashes,
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(generator.__file__),scorer,plan_path,A/'nonflag_RidgeFine52_round128_mapping_20261007.py']},
      'actual_quality_scores':0,'test_labels_read':False})
    print({'issues':issues,'actual_graph_controls':len(graph_controls)},flush=True)
    assert not issues

if __name__=='__main__':main()
