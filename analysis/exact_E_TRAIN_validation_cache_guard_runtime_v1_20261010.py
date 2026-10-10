"""Allow exactly a verified E-backed TRAIN scoring folder; keep evaluator and cache math unchanged."""
from pathlib import Path
from contextlib import contextmanager
import sys,types
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

NAMES=('测试集_X.csv','测试集_Y.csv')
CANONICAL=A/'optimization_20261003_r95/scoring_validation_only'

def validate(folder,approved,digests,fingerprint=sha):
    folder=Path(folder).resolve();approved=Path(approved).resolve()
    assert approved.drive.upper()=='E:' and approved.is_relative_to(Path('E:/赛题五_本机临时'))
    assert folder==approved and folder.name=='scoring_validation_only'
    for name in NAMES:assert fingerprint(folder/name)==digests[name],name
    return True

@contextmanager
def installed(approved,log):
    import official_validation_csv_parse_cache_20261003 as cache
    proof=read(A/'exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v1_20261010.json')
    assert len(proof['records'])==6 and proof['status']=='passed6_exact_E_TRAIN_guard_admission_and_refusal_CPU_cases'
    assert sha(Path(__file__))==proof['input_sha256'][str(Path(__file__))]
    assert sha(Path(cache.__file__))==proof['input_sha256'][str(Path(cache.__file__))]
    approved=Path(approved).resolve()
    digests={name:sha(CANONICAL/name) for name in NAMES}
    validate(approved,approved,digests)
    original=cache.run
    source=Path(cache.__file__).read_text(encoding='utf8')
    old="assert folder.name=='scoring_validation_only' and folder.is_relative_to(ROOT/'analysis')"
    assert source.count(old)==1
    source=source.replace(old,"assert folder.name=='scoring_validation_only' and (folder.is_relative_to(ROOT/'analysis') or _exact_E_TRAIN_guard(folder))")
    namespace=dict(vars(cache));namespace['_exact_E_TRAIN_guard']=lambda folder:validate(folder,approved,digests)
    exec(compile(source,str(cache.__file__),'exec'),namespace)
    modified=namespace['run'];namespace['_CACHE']=cache._CACHE
    def run(ctx,pred,operation):
        value=modified(ctx,pred,operation)
        ctx.last_validation_csv_parse_cache.update(exact_E_TRAIN_folder_admitted=str(approved),TRAIN_label_sha256=digests,scoped_guard_runtime_sha256=sha(Path(__file__)),original_evaluator_and_all_numeric_cache_code_unchanged=True)
        return value
    create(log,{'status':'frozen_before_first_E_TRAIN_score_with_single_directory_guard_extension','approved_exact_folder':str(approved),'canonical_TRAIN_labels':str(CANONICAL),'label_sha256':digests,'input_sha256':{str(p):sha(p) for p in [Path(__file__),A/'exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v1_20261010.json',Path(cache.__file__),ROOT/'evaluate.py']},'official_evaluator_or_metric_math_changed':False})
    cache.run=run
    try:yield
    finally:
        assert cache.run is run;cache.run=original

def controls():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    actual=Path('E:/赛题五_本机临时/RecentReturn252_after167_protected_fine31_screen_v1_20261010/scoring_validation_only').resolve()
    digests={n:sha(CANONICAL/n) for n in NAMES};rows=[]
    assert validate(actual,actual,digests)
    rows.append({'case':'exact_E_folder_canonical_TRAIN_bytes','expected':'admitted','passed':True})
    for name,path in [('different_E_folder',actual.parent.parent/'unregistered/scoring_validation_only'),('actual_raw_TEST_folder',ROOT/'data/raw'),('wrong_leaf_name',actual.parent/'not_scoring_validation_only')]:
        try:validate(path,actual,digests)
        except AssertionError:rows.append({'case':name,'expected':'refused','passed':True})
        else:raise AssertionError(name)
    for name in NAMES:
        def mismatch(path,name=name):return '0'*64 if Path(path).name==name else digests[Path(path).name]
        try:validate(actual,actual,digests,mismatch)
        except AssertionError:rows.append({'case':'changed_'+name,'expected':'refused','passed':True})
        else:raise AssertionError(name)
    import official_validation_csv_parse_cache_20261003 as cache
    create(A/'exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v1_20261010.json',{'status':'passed6_exact_E_TRAIN_guard_admission_and_refusal_CPU_cases','records':rows,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(cache.__file__),ROOT/'evaluate.py']},'canonical_TRAIN_label_sha256':digests,'actual_full_official_anchor_score_equivalence_pending':True,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False})
    print('PASS6 exact E-folder TRAIN byte admission/refusal cases; full official anchor equivalence pending',flush=True)
if __name__=='__main__':controls()
