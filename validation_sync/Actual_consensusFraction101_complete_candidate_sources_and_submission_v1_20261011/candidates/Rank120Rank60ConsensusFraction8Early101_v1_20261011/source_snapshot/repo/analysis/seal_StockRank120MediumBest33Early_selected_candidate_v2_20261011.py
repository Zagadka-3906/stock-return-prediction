"""Seal the executed lower-pool candidate; retain honest zero-inference anchor reuse."""
from pathlib import Path
import os
import sys
import time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def main():
    service=A/'service_owned_workflows_20261006/actual_StockRank120MediumBest33Early_selected_candidate_preparation_v2_20261011'
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed
    closed(service.name)
    assert read(service/'service_execution.json')['status']=='passed'
    release=A/'StockRank120MediumBest33Early_selected_release_v2_20261011'
    ready=read(release/'inference_ready.json');candidate=Path(ready['source_candidate'])
    if not ready['new_inference_claimed']:
        assert ready['status']=='passed_exact_selected_anchor35_candidate_reuse'
        assert sha(candidate/'manifest.json')==ready['manifest_sha256']
        for relative,info in read(candidate/'manifest.json')['files'].items():assert sha(candidate/relative)==info['sha256']
        original_release=Path(ready['source_release'])
        for name in ('protocol.json','selected_validation.npy','causal_validation.json','calibrated_csv_official.json'):os.link(original_release/name,release/name)
        create(release/'source_package_verification.json',{'status':'passed_sealed_actual_conditional_residual_candidate',
            'candidate':str(candidate),'manifest_sha256':sha(candidate/'manifest.json'),
            'all_parent_sealed_bytes_graph_metrics_and_original_freeze_confirmed':True,'new_inference_claimed':False,'test_labels_read':False})
        create(release/'selected_candidate_ready_for_registration.json',{**ready,'original_source_release':str(original_release),
            'source_release':str(release),'status':'passed_selected_best33_candidate_full_graph_and_metrics_and_source_bytes',
            'source_manifest_sha256':sha(candidate/'manifest.json'),'sealed_candidate_complete':True})
        return
    assert ready['status']=='passed_actual_selected_new_StockRank120MediumBest33Early_candidate_inference'
    assert not (candidate/'manifest.json').exists()
    selection=read(candidate/'selection.json');assert selection==read(release/'selection.json')
    before=read(release/'frozen_before_actual_candidate_inference.json')
    assert sha(release/'selection.json')==before['selection_sha256']
    prediction=read(candidate/'verification.json')
    assert prediction['status']=='passed' and prediction['test_labels_read'] is False
    for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical','pipeline_replay_bit_identical'):assert prediction[key]
    assert sha(candidate/'submission.csv')==prediction['csv_sha256']
    assert len(prediction['models'])==len(prediction['actual_model_reload_controls'])==len(prediction['actual80_day_prefix_model_controls'])==ready['actual_saved_native_models']
    assert read(candidate/'stock_rank120medium_embedding_complete_parent_native_replay_verification.json')['status']=='passed_actual_complete_qualified_parent_stock_rank120medium_embedding_two_full_native_independent_replays_and_cold80'
    freeze=Path(ready['pre_inference_source_snapshot']);sources=read(freeze/'manifest.json')
    assert sources['at_local']<=selection['frozen_at_local']
    for relative,info in sources['files'].items():
        source=freeze/'repo'/relative;assert sha(ROOT/relative)==sha(source)==info['sha256']
        target=candidate/'source_snapshot/repo'/relative;target.parent.mkdir(parents=True,exist_ok=True);os.link(source,target);assert sha(target)==info['sha256']
    for name,info in prediction['models'].items():
        assert Path(info['path']).resolve().is_relative_to(candidate.resolve())
        assert sha(info['path'])==info['sha256'],name
    evidence=[freeze/'manifest.json',*[release/n for n in ('selected_case_before_future_features.json','frozen_before_actual_candidate_inference.json','verification.json','causal_validation.json','calibrated_csv_official.json')],
        service/'native_launch.json',service/'service_execution.json',
        Path('E:/赛题五_本机临时/stock_rank120medium_best33_native14_v2_20261011/selected_best33.json'),
        Path('E:/赛题五_本机临时/stock_rank120medium_best33_native14_v2_20261011/verification.json')]
    for source in evidence:
        relative=source.relative_to(A) if source.is_relative_to(A) else Path('external_frozen_metadata')/(sha(source)+'_'+source.name)
        target=candidate/'evidence'/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists():assert sha(target)==sha(source)
        else:os.link(source,target)
        assert sha(target)==sha(source)
    repair=A/'early_fixed17_actual_replay_filename_sealing_recovery_v3_20261011.json'
    for extra in [Path(__file__),repair]:
        target=candidate/'evidence/post_inference_sealing_repair'/extra.name
        target.parent.mkdir(parents=True,exist_ok=True);os.link(extra,target);assert sha(extra)==sha(target)
    create(candidate/'source_package_verification.json',{'status':'passed_actual_pre_inference_source_snapshot_and_StockRank120MediumBest33Early_native_candidate',
        'actual_source_files':len(sources['files']),'csv_sha256':prediction['csv_sha256'],'new_native_fits':0,'test_labels_read':False})
    create(candidate/'manifest.json',{'status':'passed','files':{p.relative_to(candidate).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size}
        for p in sorted(candidate.rglob('*')) if p.is_file() and p!=candidate/'manifest.json'}})
    for relative,info in read(candidate/'manifest.json')['files'].items():assert sha(candidate/relative)==info['sha256'],relative
    create(release/'source_package_verification.json',{'status':'passed_sealed_actual_conditional_residual_candidate',
        'candidate':str(candidate),'manifest_sha256':sha(candidate/'manifest.json'),'test_labels_read':False})
    create(release/'selected_candidate_ready_for_registration.json',{**ready,
        'status':'passed_selected_best33_candidate_full_graph_and_metrics_and_source_bytes',
        'source_manifest_sha256':sha(candidate/'manifest.json'),'sealed_candidate_complete':True})


if __name__=='__main__':
    from stock_rank120medium_best33_early_storage_v2_20261011 import installed_transfer
    with installed_transfer():main()
