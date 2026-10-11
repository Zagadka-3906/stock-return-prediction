"""Keep absolute source pins while placing external evidence under collision-free metadata paths."""
from pathlib import Path
from contextlib import contextmanager
import builtins,sys,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
MODULES={'register_RFFSparse59_round151_artifacts_20261009','register_SparseAfter14829_round152_artifacts_20261009','register_BF16Medium78_round153_artifacts_20261009'}
def corrected(source):
    needle='source.relative_to(ROOT)'
    assert source.count(needle)==1
    s=source.replace(needle,"(source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(sha(source)+'_'+source.name))")
    compile(s,'external_registry_source_path_adapter','exec');return s
@contextmanager
def installed():
    original=builtins.__import__;seen=set();saved=[]
    def checked(name,*args,**kwargs):
        module=original(name,*args,**kwargs)
        if name in MODULES and name not in seen:
            seen.add(name);saved.append((module,module.main))
            ns={**module.__dict__,'__name__':'actual_external_registry_sources_preserved_v1'}
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
    generators=['prepare_RFFSparse59_round151_sources_v1_20261009','prepare_SparseAfter14829_round152_sources_v1_20261009','prepare_BF16Medium78_round153_sources_v1_20261009']
    records=[];inputs=[Path(__file__)]
    for number,parents,label in [(151,(147,148,149,150),generators[0]),(152,(148,149,150,151),generators[1]),(153,(148,149,150,151,152),generators[2])]:
        g=importlib.import_module(label);inputs.append(Path(g.__file__))
        for parent in parents:
            generated=g.generate(parent);name=next(x for x in generated if x.startswith('register_'));s=generated[name]
            adapted=corrected(s);compile(adapted,name,'exec')
            assert s.replace('source.relative_to(ROOT)','EXTERNAL_PATH')==adapted.replace("(source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(sha(source)+'_'+source.name))",'EXTERNAL_PATH')
            records.append({'round':number,'parent':parent,'compiled_registry':name,'only_external_copy_destination_changed':True})
    create(A/'external_registry_source_paths_runtime_v1_20261009.json',{'status':'passed13_actual_generated_registry_paths_preserving_all_scientific_and_absolute_provenance_bytes',
        'input_sha256':{str(p):sha(p) for p in inputs},'records':records,'quality_scores':0,'native_fits':0,'test_labels_read':False})
    print({'registry_routes_checked':len(records)})
if __name__=='__main__':main()
