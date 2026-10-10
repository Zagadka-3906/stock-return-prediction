"""Bind existing measured selected169 score to its exact E TRAIN guard, without rescoring."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
    assert allowed()
    closed('FastNeuralFrontier169_selected_candidate_sealing_v1_20261010')
    assert allowed()
    release=A/'FastNeuralFrontier169_selected_release_v1_20261010'
    selected=read(release/'calibrated_csv_official.json')
    native=Path(read(A/'actual_fast_neural_frontier228_selected_native14_location_v1_20261010.json')['output'])
    pilot=read(native/'pilot228.json');best=pilot['best']
    guardpath=release/'actual_E_TRAIN_cache_guard_binding_v2_20261010.json';guard=read(guardpath)
    expected=Path('E:/赛题五_本机临时/第169轮_20261010/selected_scoring/scoring_validation_only').resolve()
    assert Path(guard['approved_exact_folder']).resolve()==expected
    canonical=A/'optimization_20261003_r95/scoring_validation_only'
    for name in ('测试集_X.csv','测试集_Y.csv'):
        assert sha(expected/name)==sha(canonical/name)==guard['label_sha256'][name]
    cache=selected['actual_official_capsule'];capsulepath=Path(cache['official_metrics_source']);capsule=read(capsulepath)
    assert len(selected['metrics'])==8 and selected['metrics']==best['metrics']==capsule['metrics']
    assert selected['csv_sha256']==capsule['scope']['submission_csv_sha256']
    assert selected['actual_mature_return_mapping']['test_labels_read'] is False
    assert guard['official_evaluator_changed'] is False
    paths=[Path(__file__),release/'calibrated_csv_official.json',guardpath,native/'pilot228.json',capsulepath,
           release/'verification.json',A/'exact_E_TRAIN_validation_cache_guard_runtime_v2_20261010.py']
    create(A/'exact_E_TRAIN_validation_actual_anchor169_all8_compatibility_v1_20261010.json',
           {'status':'passed_existing_actual_selected169_all8_metric_equivalence_under_exact_E_TRAIN_guard',
            'round':169,'official_metrics':selected['metrics'],'actual_score_cache':cache,
            'exact_E_TRAIN_directory':str(expected),'label_sha256':guard['label_sha256'],
            'input_sha256':{str(p):sha(p) for p in paths},'new_quality_scores':0,'new_native_fits':0,
            'original_capsule_reused_without_rescoring':True,'test_labels_read':False,
            'qualification_scope':'Selected frozen169 TRAIN score only; downstream Cross120 screen separately requires full169 QA and verified main publication.'})
    print('PASS existing actual selected169 all8 official metrics and exact E TRAIN binding; no new scoring',flush=True)

if __name__=='__main__':main()
