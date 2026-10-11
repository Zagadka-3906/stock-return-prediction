"""Record confirmed historical test feedback without changing frozen models or scores."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
OUT=Path('E:/赛题五_本机临时/选模标准审计142_20261011')
ARCHIVE=ROOT.parent/'赛题五_历史归档_20261001'/'analysis'
PREFIX=ROOT/'validation_sync/Actual_selection_compliance142_correction_v1_20261011'

def read(p):return json.loads(Path(p).read_text(encoding='utf8'))
def sha(p):
    d=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(4*1024**2),b''):d.update(b)
    return d.hexdigest()
def raw_json(o):return (json.dumps(o,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf8')
def save(p,o,exclusive=True):
    with Path(p).open('xb' if exclusive else 'wb') as f:f.write(raw_json(o))

def main():
    controls=[read(A/f'current_user_runtime_control_202610{d}.json') for d in ('10','09')]
    assert all(not c['automatic_restart_enabled'] for c in controls)
    now=datetime.now(timezone(timedelta(hours=8))).isoformat()
    scores=read(OUT/'verification.json');assert scores['status'].startswith('completed_two_uncached_unchanged_official_calls')
    assert all(v==0 for v in scores['cached_metrics_minus_published'].values())
    assert scores['original_text_metrics_minus_cached']['final_score']==0.
    delivery=read(A/'alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json')
    candidate=Path(delivery['source_candidate']);native=read(candidate/'verification.json')
    assert native['validation_score']==delivery['official_TRAIN_internal_score']==.4514612196682616
    bundle=read(A/'actual_fraction101_delivery_bundle137_verification_v1_20261011.json')
    protected={str(candidate/'manifest.json'):delivery['source_candidate_manifest_sha256'],str(Path(delivery['output'])/'submission.csv'):delivery['csv_sha256'],str(Path(bundle['archive'])):bundle['archive_sha256']}
    protected.update({m['path']:m['sha256'] for m in native['models'].values()})
    assert len(native['models'])==37
    for p,d in protected.items():assert sha(p)==d,p
    historical=['HOLDOUT_STATUS_20260928.md','frozen_holdout_20260928/runner.py','frozen_holdout_20260928/label_reconstruction.json','frozen_holdout_20260928/冻结留出检验报告.md','all_models_test_20260929/重点配置对比.md','freeze_mlp_training_validation.py','top2_training_validation_20260929/audit/协议独立审计.md']
    assert read(ARCHIVE/'frozen_holdout_20260928/label_reconstruction.json')['days']==343
    assert 'shift(-1)' in (ARCHIVE/'frozen_holdout_20260928/runner.py').read_text(encoding='utf8')
    assert 'reconstructed test slice' in (ARCHIVE/'freeze_mlp_training_validation.py').read_text(encoding='utf8')
    PREFIX.mkdir(exist_ok=False)
    (PREFIX/'.gitattributes').write_bytes(b'* -text\n')
    bindings=[]
    for relative in historical:
        p=ARCHIVE/relative;target=PREFIX/'historical_evidence'/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
        bindings.append({'original_path':str(p),'archive_path':target.relative_to(ROOT).as_posix(),'sha256':sha(p)})
    for p in [Path(__file__),A/'audit_selection142_official_inputs_and_scores_v1_20261011.py',OUT/'verification.json',OUT/'frozen_audit_before_uncached_official_calls.json',OUT/'raw_TRAIN_scoring_input_comparison.json',OUT/'cached_TRAIN_input_uncached_official.json',OUT/'original_TRAIN_decimal_text_uncached_official.json']:
        target=PREFIX/'audit'/p.name;target.parent.mkdir(exist_ok=True);target.write_bytes(p.read_bytes());bindings.append({'original_path':str(p),'archive_path':target.relative_to(ROOT).as_posix(),'sha256':sha(p)})
    graph=native['whole_scheme_graph']
    save(PREFIX/'current_lineage.json',{'source_candidate':str(candidate),'candidate_manifest_sha256':delivery['source_candidate_manifest_sha256'],'whole_scheme_graph_keys':list(graph),'models':37,'original_parent_round':183,'selected_configuration':native['construction'],'original_parent_selection_source':str(A/'optimization_20261003_r183/selection.json'),'membership_ordering_research_source':str(A/'connected_validation_20261002/optimize_wave15.py'),'source_SHA256':{str(p):sha(p) for p in [candidate/'selection.json',candidate/'verification.json',A/'optimization_20261003_r183/selection.json',A/'connected_validation_20261002/optimize_wave15.py']},'direction_initial_decision':{'user_reports_test_feedback':True,'first_membership_ordering_decision_text_not_independently_located':True}})
    state={'status':'historical_test_feedback_confirmed_selection_compliance_not_established','as_of_local':now,'standard':'后续选模标准.md §2: 禁止从测试X后续价格重建答案并反馈选模；训练内确定模型、参数、集成与后处理','confirmed_test_feedback':True,'reconstructed_test_days':343,'reconstructed_test_rows':1594950,'first_reveal_utc':'2026-09-28T14:53:02.315174+00:00','feedback_types_confirmed':['test_score_based_candidate_recommendation','test_outcome_motivated_MLP_training_validation','test_outcome_motivated_Top2_training_validation'],'current_lineage_inherits_post_revelation_research':True,'current_recommended_submission':None,'strict_training_only_selection_claim_withdrawn':True,'fully_documented_test_independent_replacement_selected':False,'current_research_candidate_score':delivery['official_TRAIN_internal_score'],'official_TRAIN_S_reproduced_without_adapters_or_score_cache':True,'uncached_official_evaluation_calls':2,'actual_or_reconstructed_TEST_Y_read_in_this_audit':False,'frozen_scores_models_CSV_ZIP_unchanged':True,'former_registration_is_not_selection_provenance_certificate':True,'latest_candidate_and_C189_not_automatically_qualified_by_old_registration':True,'known_restriction_filtered_catalog_does_not_filter_historical_test_feedback':True,'evidence_directory':PREFIX.relative_to(ROOT).as_posix(),'report':'docs/SELECTION_COMPLIANCE.md','optimization_queue_remains_paused':True,'new_training':0,'new_model_inference':0}
    save(ROOT/'selection_compliance.json',state);save(PREFIX/'selection_compliance.json',state)
    # Preserve the old pointer as evidence; change only current recommendation semantics.
    pointer=ROOT/'active_release.json';(PREFIX/'previous_active_release.json').write_bytes(pointer.read_bytes());previous=read(pointer)
    previous['artifact_status_before_selection_review']=previous['status'];previous['status']='selection_compliance_suspended'
    previous['historical_selected_by']=previous['selected_by'];previous['selected_by']=None
    previous['selection_compliance_status']=state['status'];previous['recommended_under_selection_standard']=False;previous['selection_compliance_record']='selection_compliance.json'
    previous['artifact_files_preserved']=True;save(pointer,previous,exclusive=False)
    latest=ROOT/'docs/latest_results.json';(PREFIX/'previous_latest_results.json').write_bytes(latest.read_bytes());data=read(latest)
    data['selection_compliance']={k:state[k] for k in ['status','as_of_local','confirmed_test_feedback','reconstructed_test_days','strict_training_only_selection_claim_withdrawn','fully_documented_test_independent_replacement_selected','report']}
    for key in ['latest_packaged_candidate','fully_registered_delivery']:
        data[key]['recommended_under_selection_standard']=False;data[key]['selection_provenance_status']=state['status']
    data['score_catalog']['historical_test_feedback_not_removed_by_existing_numeric_restriction_filter']=True
    save(latest,data,exclusive=False)
    warning=(ROOT/'docs/SELECTION_COMPLIANCE.md').read_bytes()
    warning_name='选模来源合规更正_20261011.md'
    for folder in [Path(delivery['output']),Path(data['fully_registered_delivery']['local_delivery_path'])]:
        assert folder.resolve().drive.upper()=='E:' and folder.resolve().is_relative_to(Path('E:/赛题五_最终提交'))
        p=folder/warning_name
        with p.open('xb') as f:f.write(warning)
    save(PREFIX/'evidence_manifest.json',{'status':'confirmed_historical_test_feedback_and_current_claims_corrected','at_local':now,'evidence':bindings,'protected_artifact_SHA256':protected,'source_standard_SHA256':sha(ROOT/'后续选模标准.md'),'model_and_frozen_candidate_modifications':0,'competition_upload_performed':False,'optimization_automatic_restart_enabled':False})
    (PREFIX/'README.md').write_bytes(b'# Selection provenance correction\n\nSee [the report](../../docs/SELECTION_COMPLIANCE.md) and [current status](../../selection_compliance.json). Historical scores and artifacts remain unchanged. The archived source files document reconstructed test outcomes and their feedback into research. Numerical reproduction is not proof of independent selection.\n')
    for p,d in protected.items():assert sha(p)==d,p
    save(OUT/'correction_record.json',{'status':'current_recommendation_suspended_historical_test_feedback_confirmed','archive':str(PREFIX),'protected_artifacts_unchanged':True,'model_native_count':37,'corrected_current_pointer_status':previous['status'],'source_evidence_files':len(bindings),'real_TEST_labels_not_read':True,'GitHub_main_publication_pending':True})
    print({'recorded':state['status'],'evidence_files':len(bindings),'models_CSV_ZIP_unchanged':True},flush=True)

if __name__=='__main__':main()
