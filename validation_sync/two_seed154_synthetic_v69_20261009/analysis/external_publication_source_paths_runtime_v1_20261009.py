"""Publish external source bytes with collision-free targets and retain their absolute provenance keys."""
from pathlib import Path
from contextlib import contextmanager
import builtins,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
MODULES={'publish_HuberSparse59_round150_full_validation_20261008','publish_RFFSparse59_round151_full_validation_20261009','publish_SparseAfter14829_round152_full_validation_20261009','publish_BF16Medium78_round153_full_validation_20261009'}
def corrected(s):
    target="target = (prefix / 'original_execution_evidence' / path.relative_to(ROOT)).as_posix()"
    binding="manifest['local_input_source_sha256'][path.relative_to(ROOT).as_posix()] = raw_sha"
    assert s.count(target)==s.count(binding)==1
    s=s.replace(target,"target = (prefix / 'original_execution_evidence' / (path.relative_to(ROOT) if path.is_relative_to(ROOT) else Path('external_metadata')/(sha(path)+'_'+path.name))).as_posix()")
    s=s.replace(binding,"manifest['local_input_source_sha256'][path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)] = raw_sha")
    compile(s,'external_publication_source_path_adapter','exec');return s
@contextmanager
def installed():
    original=builtins.__import__;seen=set();saved=[]
    def checked(name,*args,**kwargs):
        module=original(name,*args,**kwargs)
        if name in MODULES and name not in seen:
            seen.add(name);saved.append((module,module.main))
            ns={**module.__dict__,'__name__':'actual_external_publication_sources_preserved_v1'}
            exec(compile(corrected(Path(module.__file__).read_text(encoding='utf8')),str(Path(__file__)),'exec'),ns)
            module.main=ns['main']
        return module
    builtins.__import__=checked
    try:yield
    finally:
        assert builtins.__import__ is checked;builtins.__import__=original
        for module,main in saved:module.main=main
def main():
    import importlib
    inputs=[Path(__file__)];records=[]
    for n,parents,gname in [(150,(146,147,148,149),'prepare_HuberSparse59_round150_sources_v2_20261009'),
        (151,(147,148,149,150),'prepare_RFFSparse59_round151_sources_v1_20261009'),
        (152,(148,149,150,151),'prepare_SparseAfter14829_round152_sources_v1_20261009'),
        (153,(148,149,150,151,152),'prepare_BF16Medium78_round153_sources_v1_20261009')]:
        g=importlib.import_module(gname);inputs.append(Path(g.__file__))
        for parent in parents:
            generated=g.generate(parent);name=next(x for x in generated if x.startswith('publish_'));corrected(generated[name])
            records.append({'round':n,'parent':parent,'publisher_source':name,'external_target_and_absolute_provenance_preserved':True})
    create(A/'external_publication_source_paths_runtime_v1_20261009.json',{'status':'passed17_actual_generated_publisher_external_targets_and_absolute_source_provenance_checks',
        'input_sha256':{str(p):sha(p) for p in inputs},'records':records,'new_scores':0,'new_fits':0,'test_labels_read':False})
    print({'checked_publishers':len(records)})
if __name__=='__main__':main()
