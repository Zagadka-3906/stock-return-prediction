"""Scope all three cache directory guards to one canonical TRAIN-only E folder."""
from pathlib import Path
from contextlib import contextmanager
import ast,types,sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from exact_E_TRAIN_validation_cache_guard_runtime_v1_20261010 import validate,NAMES,CANONICAL
SPECS=[('official_validation_csv_parse_cache_20261003','run',"assert folder.name=='scoring_validation_only' and folder.is_relative_to(ROOT/'analysis')"),('cross_round_official_score_reuse_20261003','score',"assert folder.name=='scoring_validation_only' and folder.is_relative_to(ROOT/'analysis')"),('identical_official_score_cache_20261003','score',"assert folder.resolve().is_relative_to(ROOT/'analysis')")]

def compiled(module,old):
    source=Path(module.__file__).read_text(encoding='utf8');assert source.count(old)==1
    new="assert folder.name=='scoring_validation_only' and (folder.resolve().is_relative_to(ROOT/'analysis') or _exact_E_TRAIN_guard(folder))"
    changed=source.replace(old,new)
    assert changed.replace(new,old)==source
    assert ast.dump(ast.parse(changed.replace(new,old)))==ast.dump(ast.parse(source))
    namespace=dict(vars(module));exec(compile(changed,str(module.__file__),'exec'),namespace)
    return namespace

@contextmanager
def installed(approved,log):
    import importlib
    proof=read(A/'exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v2_20261010.json')
    assert proof['status']=='passed6_E_TRAIN_refusals_and_all3_cache_sources_single_guard_only_AST_admission'
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    approved=Path(approved).resolve();digests={name:sha(CANONICAL/name) for name in NAMES}
    validate(approved,approved,digests)
    replacements=[]
    for name,field,old in SPECS:
        module=importlib.import_module(name);namespace=compiled(module,old);original=getattr(module,field)
        assert '_exact_E_TRAIN_guard' not in vars(module)
        vars(module)['_exact_E_TRAIN_guard']=lambda folder:validate(folder,approved,digests)
        # Bind the exact original globals, so the existing cross-round digest interception
        # and original parsing cache keep their actual behavior.
        fn=types.FunctionType(namespace[field].__code__,vars(module),field,namespace[field].__defaults__,namespace[field].__closure__)
        setattr(module,field,fn);replacements.append((module,field,original,fn))
    create(log,{'status':'frozen_all3_exact_E_TRAIN_directory_guard_extensions_before_first_score','approved_exact_folder':str(approved),'label_sha256':digests,'input_sha256':{str(p):sha(p) for p in [Path(__file__),A/'exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v2_20261010.json',*[Path(x[0].__file__) for x in replacements],ROOT/'evaluate.py']},'numeric_code_AST_restored_exactly_except_directory_guard':True,'cross_round_digest_interception_and_parsing_cache_original_globals_preserved':True,'official_evaluator_changed':False})
    try:yield
    finally:
        for module,field,original,fn in reversed(replacements):
            assert getattr(module,field) is fn;setattr(module,field,original);vars(module).pop('_exact_E_TRAIN_guard')

def controls():
    import importlib
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    actual=Path('E:/赛题五_本机临时/RecentReturn252_after167_protected_fine31_screen_v1_20261010/scoring_validation_only').resolve()
    digests={n:sha(CANONICAL/n) for n in NAMES};rows=[]
    assert validate(actual,actual,digests);rows.append({'case':'canonical_TRAIN_E_bytes','passed':True})
    for name,path in [('different_E_folder',actual.parent.parent/'unregistered/scoring_validation_only'),('actual_raw_TEST_folder',ROOT/'data/raw'),('wrong_leaf_name',actual.parent/'wrong_name')]:
        try:validate(path,actual,digests)
        except AssertionError:rows.append({'case':name,'passed':True})
        else:raise AssertionError(name)
    for name in NAMES:
        try:validate(actual,actual,digests,lambda p,name=name:'0'*64 if Path(p).name==name else digests[Path(p).name])
        except AssertionError:rows.append({'case':'changed_'+name,'passed':True})
        else:raise AssertionError(name)
    modules=[importlib.import_module(name) for name,_,_ in SPECS]
    for module,(_,field,old) in zip(modules,SPECS):assert callable(compiled(module,old)[field])
    create(A/'exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v2_20261010.json',{'status':'passed6_E_TRAIN_refusals_and_all3_cache_sources_single_guard_only_AST_admission','records':rows,'admitted_cache_modules':[m.__name__ for m in modules],'input_sha256':{str(p):sha(p) for p in [Path(__file__),A/'exact_E_TRAIN_validation_cache_guard_runtime_v1_20261010.py',*[Path(m.__file__) for m in modules],ROOT/'evaluate.py']},'actual_full_anchor168_all8_official_metrics_pending':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print('PASS6 exact TRAIN guard cases and all3 original cache ASTs; real official anchor score pending',flush=True)
if __name__=='__main__':controls()
