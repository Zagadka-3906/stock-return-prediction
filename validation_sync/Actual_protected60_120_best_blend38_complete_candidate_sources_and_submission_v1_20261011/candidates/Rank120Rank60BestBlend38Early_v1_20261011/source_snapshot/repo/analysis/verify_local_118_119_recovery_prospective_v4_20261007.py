"""Check generated concrete paths without claiming future parents are qualified."""
from pathlib import Path
import ast,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    import prepare_HGB_quarter_numeric28_round118_sources_v4_20261007 as g118
    import prepare_quantile_HGB88_round119_sources_v4_20261007 as g119
    records=[]
    paths=[Path(__file__),A/'local_118_119_protocol_recovery_source_preparation_v4_20261007.json']
    for number,generator,parents in [(118,g118,(112,116,117)),(119,g119,(112,117,118))]:
        declared={A/n for n in generator.NAMES.values()}
        declared |= {A/f'github_validation_sync_main_20261005/round{parent}_receipt.json' for parent in parents}
        stem='HGB_quarter_numeric28' if number==118 else 'quantile_HGB88'
        declared |= {A/f'{stem}_round{number}_source_admission_v4_20261007.json',
                     A/f'{stem}_round{number}_source_preparation_v4_20261007.json',
                     A/f'{stem}_scores_github_v4_20261007/receipt.json',
                     A/f'{stem}_selected_release_v4_20261007/selected_candidate_ready_for_registration.json'}
        paths.append(Path(generator.__file__))
        for parent in parents:
            generated=generator.generate(parent);assert len(generated)==8
            for name,text in generated.items():compile(text,str(A/name),'exec')
            name=next(n for n in generated if n.startswith('register_'))
            tree=ast.parse(generated[name]);body=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main').body
            assignment=next(n for n in body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='sources' for t in n.targets))
            ns={'A':A,'ROOT':ROOT,'Path':Path,'__file__':str(A/name)}
            exec(compile(ast.fix_missing_locations(ast.Module(body=[assignment],type_ignores=[])),name,'exec'),ns)
            for p in ns['sources']:assert p.is_file() or p in declared,(number,parent,p)
            records.append({'round':number,'parent':parent,'compiled_sources':8,
              'concrete_registry_paths':len(ns['sources']),
              'declared_future_paths':[str(p) for p in ns['sources'] if not p.is_file()]})
    create(A/'local_118_119_recovery_prospective_v4_20261007.json',{
      'status':'passed_actual48_compiled_prospective_sources_and_concrete_paths',
      'input_sha256':{str(p):sha(p) for p in paths},'controls':records,
      'actual_parent_qualification_and_scientific_admission_not_claimed':True,
      'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print({'status':'passed','prospective_sources':48,'routes':len(records)})

if __name__=='__main__':main()
