"""Check prospective120 structure now; actual admission still requires qualified119."""
from pathlib import Path
from copy import deepcopy
import ast,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import prepare_nonflag_HGB40_round120_sources_v2_20261007 as generator
    plan=read(A/'nonflag_HGB40_plan_20261007.json');records=[]
    scorer=A/'run_nonflag_HGB40_official_comparison_v2_20261007.py';tree=ast.parse(scorer.read_text(encoding='utf8'))
    item=next(n.value for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='item' for t in n.targets) and isinstance(n.value,ast.Dict))
    schema={k.value for k in item.keys if isinstance(k,ast.Constant)}
    declared={A/n for n in generator.NAMES.values()}|{
      A/'nonflag_HGB40_round120_source_admission_v2_20261007.json',A/'nonflag_HGB40_round120_source_preparation_v2_20261007.json',
      A/'nonflag_HGB40_scores_github_20261007/receipt.json',A/'nonflag_HGB40_selected_release_v2_20261007/selected_candidate_ready_for_registration.json',
      *[A/f'github_validation_sync_main_20261005/round{n}_receipt.json' for n in (112,118,119)]}
    for parent in (112,118,119):
        generated=generator.generate(parent)
        for name,text in generated.items():compile(text,str(A/name),'exec')
        name='register_nonflag_HGB40_round120_artifacts_20261007.py';text=generated[name];tree=ast.parse(text)
        required={n.slice.value for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='measured' and isinstance(n.slice,ast.Constant)}
        assert required<=schema,required-schema
        body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
        s=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='sources' for t in n.targets))
        ns={'A':A,'ROOT':ROOT,'Path':Path,'__file__':str(A/name)}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[s],type_ignores=[])),name,'exec'),ns)
        for p in ns['sources']:assert p.is_file() or p in declared,p
        start=text.index("        if measured['case'] == pilot['best']['case']:");end=text.index('        row = ',start)
        code=compile('if True:\n'+text[start:end],name,'exec')
        fake={'core':{'native_SHA':'preserved106'},'conditional_flag_CPU_HGB_residual_CDF':{'complete_parent':'unchanged'}}
        examples=[('remove_nonflag_HGB',0.,[]),*[(n,.0125,[n]) for n in plan['single_native_heads']],*[(n,.0125,names) for n,names in plan['ensembles'].items()]]
        for model,weight,names in examples:
            ns={'cfg':{'model':model,'weight':weight,'anchor_round':112,'universe':plan['universe']},
              'measured':{'case':7,'native_bank_source':'actual10','ordered_native_components':names},
              'pilot':{'best':{'case':8},'actual_scheme_base_round':112},'deepcopy':deepcopy,'ROOT':ROOT,'read':lambda path:{'whole_scheme_graph':fake}}
            exec(code,ns);graph=ns['graph'];assert graph['core']==fake['core'] and graph['conditional_flag_CPU_HGB_residual_CDF']==fake['conditional_flag_CPU_HGB_residual_CDF']
            if names:assert graph['nonflag_CPU_HGB_residual_CDF']['ordered_equal_mean_components']==names
            else:assert 'nonflag_CPU_HGB_residual_CDF' not in graph
            records.append({'parent':parent,'model':model,'flag_branch_preserved':True})
        pub=generated['publish_nonflag_HGB40_round120_full_validation_20261007.py']
        assert "actual_full_QA_version': 31" in pub and 'collect(120, 31, 40)' in pub
    wrapper=(A/'predict_nonflag_residual_HGB_complete_scheme_20261007.py').read_text(encoding='utf8')
    seal=(A/'seal_nonflag_HGB40_selected_candidate_v2_20261007.py').read_text(encoding='utf8')
    expected='passed_actual_complete_parent_and_nonflag_HGB_two_full_replays_independent_and_cold80'
    assert repr(expected) in wrapper and repr(expected) in seal and "candidate/'nonflag_residual_HGB_native_replay_verification.json'" in seal
    publication=(A/'publish_nonflag_HGB40_evidence_v2_20261007.py').read_text(encoding='utf8')
    assert "==(37 if phase=='controls' else 40)" in publication and "target=A/'nonflag_HGB40_scores_github" not in publication
    create(A/'nonflag_HGB40_prospective24_source_and12_graph_preflight_v2_20261007.json',{
      'status':'passed_actual24_compiled_sources12_metadata_graphs_and_single_receipt_contract',
      'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(generator.__file__),scorer,
        A/'prepare_nonflag_HGB40_selected_candidate_v2_20261007.py',A/'seal_nonflag_HGB40_selected_candidate_v2_20261007.py',
        A/'publish_nonflag_HGB40_evidence_v2_20261007.py',A/'verify_nonflag_HGB40_round120_sources_v2_20261007.py']},
      'metadata_graph_controls':records,'actual_parent_qualification_and_official40_not_claimed':True,
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'passed','prospective_sources':24,'metadata_graph_controls':12})

if __name__=='__main__':main()
