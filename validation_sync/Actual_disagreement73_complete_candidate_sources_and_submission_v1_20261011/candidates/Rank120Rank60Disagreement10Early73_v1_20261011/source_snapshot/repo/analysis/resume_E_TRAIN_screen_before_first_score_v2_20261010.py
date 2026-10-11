"""Reuse verified pre-score freeze/label copies; never overwrite or repeat completed scores."""
from pathlib import Path
import sys,json
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main(kind):
    assert allowed()
    stem='RecentReturn252_after167_protected_fine31' if kind=='fine31' else 'Recent252Forward20_after168_high_impact65'
    count=31 if kind=='fine31' else 65
    original=A/('run_'+stem+'_screen_v1_20261010.py')
    failed=A/'service_owned_workflows_20261006'/('actual_'+stem+'_screen_E_guard_recovery_v2_20261010')
    assert not owned(read(failed/'native_launch.json'))
    assert read(failed/'service_execution.json')['status']=='failed'
    stderr=(failed/'stderr.log').read_text(encoding='utf8')
    assert 'cross_round_official_score_reuse_20261003.py' in stderr and 'folder.is_relative_to' in stderr
    out=Path('E:/赛题五_本机临时')/(stem+'_screen_v1_20261010')
    assert not list(out.glob('case*_official.json')) and not (out/'verification.json').exists()
    frozen_sha=sha(out/'frozen_before_any_new_controls_or_scores.json')
    freeze=read(out/'frozen_before_any_new_controls_or_scores.json');assert len(freeze['cases'])==count
    for p,d in freeze['input_sha256'].items():assert sha(p)==d,p
    scoring=out/'scoring_validation_only'
    assert {p.name for p in scoring.iterdir()}=={'测试集_X.csv','测试集_Y.csv'}
    for name in ('测试集_X.csv','测试集_Y.csv'):assert sha(scoring/name)==sha(A/'optimization_20261003_r95/scoring_validation_only'/name)
    control=read(out/'case000_controls.json');assert control['case']==0 and control['rows']==5635800
    supplemental=out/'frozen_E_guard_recovery_before_first_official_score_v2_20261010.json'
    create(supplemental,{'status':'verified_failed_before_first_score_only_reuse_original_case0_freeze_and_TRAIN_copies','failed_service':str(failed),'failed_execution_sha256':sha(failed/'service_execution.json'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),original,out/'frozen_before_any_new_controls_or_scores.json',out/'case000_controls.json',A/'exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010.py',A/'exact_E_TRAIN_validation_cache_guard_actual_CPU_controls_v2_20261010.json']},'completed_official_scores_before_recovery':0,'new_native_fits':0,'test_labels_read':False})
    text=original.read_text(encoding='utf8')
    substitutions={
        'OUT.mkdir(exist_ok=False)':'assert OUT.is_dir()',
        'scoring.mkdir(parents=True,exist_ok=False)':'assert scoring.is_dir()',
        'scratch.mkdir()':'assert scratch.is_dir()',
        'shutil.copyfile(label_source,scoring/name)':'assert sha(label_source)==sha(scoring/name)',
        'shutil.copyfile(source,scoring/name)':'assert sha(source)==sha(scoring/name)',
    }
    for before,after in substitutions.items():
        if before in text:assert text.count(before)==1; text=text.replace(before,after)
    namespace={'__file__':str(original),'__name__':'verified_original_E_screen_recovery'}
    exec(compile(text,str(original),'exec'),namespace)
    def reuse_create(path,value):
        path=Path(path)
        if path in (out/'frozen_before_any_new_controls_or_scores.json',out/'case000_controls.json'):
            previous=read(path)
            lhs={k:v for k,v in previous.items() if k!='at_local'};rhs={k:v for k,v in value.items() if k!='at_local'}
            assert lhs==rhs,path
            return
        return create(path,value)
    namespace['create']=reuse_create
    from exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010 import installed
    with installed(scoring,out/'actual_E_TRAIN_cache_guard_binding_v2_20261010.json'):
        namespace['main']()
    proof=read(out/'verification.json');assert len(proof['records'])==count
    assert proof['records'][0]['metrics']==read(A/'optimization_20261003_r168/calibrated_csv_official.json')['metrics']
    assert sha(out/'frozen_before_any_new_controls_or_scores.json')==frozen_sha
    create(out/'E_TRAIN_guard_recovery_completed_v2_20261010.json',{'status':'passed_exact_full_anchor168_all8_official_metrics_and_original31_or65_controls_completed','records':count,'original_freeze_sha256':frozen_sha,'original_freeze_unchanged':True,'new_native_fits':0,'test_labels_read':False})
if __name__=='__main__':main(sys.argv[1])
