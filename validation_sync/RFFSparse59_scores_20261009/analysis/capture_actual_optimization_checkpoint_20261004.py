"""Save an immutable, point-in-time checkpoint from actual completed proofs."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    result=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(8*1024*1024),b''):
            result.update(block)
    return result.hexdigest()


def main():
    completed=[]
    for path in (ROOT/'results').glob('optimization_20261003_r*.json'):
        number=int(path.stem.rsplit('_r',1)[1])
        evidence=complete_round_evidence(number)
        if evidence is not None:completed.append((number,path,evidence))
    latest,result_path,evidence=max(completed,key=lambda item:item[0])
    result=read(result_path)
    previous_paths=list((ROOT/'analysis').glob('optimization_progress_checkpoint_*.json'))
    previous=read(max(previous_paths,key=lambda path:read(path)['at_local'])) if previous_paths else {}
    previous_round=previous.get('latest_completed_round',0)
    progress_path=ROOT/'analysis/ongoing_optimization_state.json'
    boundary_path=ROOT/'analysis/optimization_boundary_evidence_20261004.json'
    qa_path=ROOT/'analysis/all_model_ranking_qa/interaction_result.json'
    progress,boundary,qa=map(read,(progress_path,boundary_path,qa_path))
    assert qa['status']=='passed'
    assert progress['last_completed_round']==latest
    assert boundary['latest_completed_round']==latest
    assert not progress['test_labels_read'] and not boundary['test_labels_read']
    inspection=ROOT/'analysis/neural_width_complete_model_inspection_execution_20261004/verification.json'
    wide=read(inspection) if inspection.exists() else {}
    paths=[Path(__file__),result_path,qa_path,progress_path,boundary_path,
        ROOT/'results/all_model_rankings_20261003.html',ROOT/'results/all_model_rankings_20261003.json']
    paths.extend(ROOT/path for path in evidence['source_sha256'])
    for relative in ('analysis/neural_width_bank_20261004/oof_audit.json',
            'analysis/neural_width_bank_20261004/training_execution_scope.json',
            'analysis/neural_width_resource_scope_audit_20261004.json',
            'analysis/neural_width_measured_prefix20_20261004/verification.json',
            'analysis/neural_width_future_models_qa_20261004/verification.json',
            'analysis/neural_width_future_resource_scope_audit_20261004.json',
            'analysis/neural_width_complete_scheme_preflight_20261004/verification.json',
            'analysis/portfolio_surrogate_bank_20261004/oof_audit.json',
            'analysis/portfolio_surrogate_bank_20261004/training_execution_scope.json',
            'analysis/portfolio_surrogate_resource_scope_audit_20261004.json',
            'analysis/portfolio_surrogate_future_models_qa_20261004/verification.json',
            'analysis/portfolio_surrogate_future_resource_scope_audit_20261004.json',
            'analysis/portfolio_surrogate_complete_scheme_preflight_20261004/verification.json',
            'analysis/portfolio_surrogate_complete_scheme_recovery_20261005/verification.json'):
        path=ROOT/relative
        if path.exists():assert read(path)['status']=='passed';paths.append(path)
    if inspection.exists():assert wide['status']=='passed';paths.append(inspection)
    for family in ('neural_width','portfolio_surrogate','nystrom_ridge'):
        count_audit=ROOT/f'analysis/{family}_scheme_count_metadata_audit_20261004/verification.json'
        if count_audit.exists():
            value=read(count_audit)
            assert value['status']=='passed_with_copied_display_label_clarified'
            assert value['actual_native_models']==4
            paths.append(count_audit)
    active=progress['round']
    active_folder=ROOT/f'analysis/optimization_20261003_r{active}'
    active_proofs=[active_folder/'protocol.json',active_folder/'component_audit.json',
        active_folder/'baseline_future_control/verification.json',
        active_folder/'selection.json',active_folder/'calibrated_csv_official.json',
        ROOT/f'candidates/optimization_20261003_r{active}/verification.json']
    active_proofs.extend(active_folder.glob('*causal_checks.json'))
    pending_evidence={}
    for path in active_proofs:
        if path.exists():
            value=read(path);paths.append(path)
            pending_evidence[str(path.relative_to(ROOT))]={'status':value.get('status'),
                'metrics':value.get('metrics'),'csv_sha256':value.get('csv_sha256')}
        else:pending_evidence[str(path.relative_to(ROOT))]={'status':'pending'}
    now=datetime.now()
    output={'status':'progress','at_local':now.isoformat(timespec='seconds'),
        'goal_complete':False,'latest_completed_round':latest,
        'new_completed_official_records':sum(item[2]['scored_records'] for item in completed if item[0]>previous_round),
        'latest_round_distinct_output_configurations':result['distinct_output_configurations'],
        'latest_round_repeat_records':result['repeat_records'],'latest_round_score_gain':result['score_gain'],
        'completed_validation_best':evidence['score'],'completed_board_records':qa['connected_records'],
        'completed_board_sources':qa['source_hashes'],'actual_candidate_csv_sha256':evidence['candidate_csv_sha256'],
        'actual_new_annual_fits_completed':progress['actual_new_annual_fits_completed'],
        'actual_wide_saved_models_inspected':wide.get('actual_saved_models_inspected',0),
        'actual_wide_fulltraining_artifacts_completed':progress.get('neural_width_fulltraining_artifacts_completed',0),
        'actual_wide_native_fullfuture_controls_recorded':progress.get('neural_width_native_fullfuture_controls_recorded',0),
        'actual_portfolio_annual_fits_completed':progress.get('portfolio_surrogate_annual_artifacts_completed',0),
        'portfolio_training_status':progress.get('portfolio_training_status'),
        'wide_future_qa_status':progress.get('neural_width_future_qa_status','pending_actual_controls'),
        'wide_future_last_complete_resource_observation':progress.get('neural_width_future_last_sample'),
        'active_partial_score':progress.get('active_partial_score'),
        'partial_score_not_promoted_to_completed_best':True,
        'wide_fulltraining_future_andofficial_quality_still_required':progress.get('neural_width_future_qa_status')!='passed' or complete_round_evidence(58) is None,
        'active_round':progress['round'],'active_stage':progress['stage'],
        'active_round_partial_evidence_not_completed_publication':pending_evidence,
        'remaining_feasible_directions':len(boundary['open_feasible_directions']),
        'global_resource_exhaustion_established':False,'test_labels_read':False,
        'mutable_report_hashes_describe_this_snapshot_only':True,
        'input_sha256':{str(path.resolve()):sha(path) for path in dict.fromkeys(paths)}}
    target=ROOT/f'analysis/optimization_progress_checkpoint_{now:%Y%m%d_%H%M%S}.json'
    with target.open('x',encoding='utf-8') as stream:
        json.dump(output,stream,ensure_ascii=False,indent=2)
        stream.write('\n')
    print(json.dumps({'status':'progress','checkpoint':str(target),'latest_completed_round':latest,
        'new_completed_official_records':output['new_completed_official_records'],
        'actual_wide_saved_models_inspected':output['actual_wide_saved_models_inspected']}))


if __name__=='__main__':main()
