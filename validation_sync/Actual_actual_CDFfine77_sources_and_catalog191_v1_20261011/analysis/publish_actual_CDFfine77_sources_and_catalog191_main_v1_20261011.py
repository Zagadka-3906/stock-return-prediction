"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    paths=[Path(__file__),*[Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_actual_CDFfine77_sources_and_catalog191_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_actual_disagreement10_score_priority72_observer148_sources_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_disagreement_CDF_fine8_priority77_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_rank120_rank60_after183_disagreement_CDFfine8_screen77_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement_CDFfine8_predeclared_sources77_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_actual191_disagreement10_CDF8_and_fine8_priority77_then_original48_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_idle_priority75_retirement_for_fine8_priority77_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_disagreement_CDFfine8_full_conditional78_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_disagreement_CDFfine8_results_selection_main_and_conditional78_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement_CDFfine8_early78_sources_admission_v2_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_disagreement_CDFfine8_actual_CPU_controls78_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_disagreement_CDFfine8_six_cases_CPU_controls78_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_disagreement_CDF76_actual_callback_and_storage_CPU_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_disagreement_CDF76_callback12_storage_and_recipe_CPU_controls_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_complete191_and_disagreement_completed_catalog_v3_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\build_complete191_plus_completed_raw_TRAIN_score_catalog_v3_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_actual_complete191_and_raw_TRAIN_score_catalog_v3_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_complete191_and_disagreement_completed_catalog_v3_sources_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement_CDF8_gain_decision76_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\github_validation_sync_main_20261005\\round191_receipt.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\normalize_rank120_rank60_disagreement10_early73_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\qualify_rank120_rank60_disagreement10_early73_selected_native14_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_Rank120Rank60Disagreement10Early73_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_Rank120Rank60Disagreement10Early73_selected_candidate_feature_cache_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\seal_Rank120Rank60Disagreement10Early73_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement10_early73_storage_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement_after_qualified183_native_stage73_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\predict_rank120_rank60_disagreement_complete_qualified183_scheme73_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\normalize_rank120_rank60_disagreement_CDFfine8_early78_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\qualify_rank120_rank60_disagreement_CDFfine8_early78_selected_native14_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_Rank120Rank60DisagreementCdfFine8Early78_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_Rank120Rank60DisagreementCdfFine8Early78_selected_candidate_feature_cache_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\seal_Rank120Rank60DisagreementCdfFine8Early78_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement_CDFfine8_early78_storage_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement_CDFfine_after_qualified183_native_stage78_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\predict_rank120_rank60_disagreement_CDFfine_complete_qualified183_scheme78_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_actual_disagreement73_complete_candidate_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_verified_disagreement73_alternate_submission_delivery_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_actual_disagreement_CDFfine78_complete_candidate_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_verified_disagreement_CDFfine78_alternate_submission_delivery_v1_20261011.py']]]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/Actual_actual_CDFfine77_sources_and_catalog191_v1_20261011');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**{'status': 'actual_large_CDF8_no_gain_and_original191_QA102_main_complete_frozen_fine_CDF8_hypotheses_CPU6_18_6_and_future37_model_pipeline78_sources_new_candidate_pending', 'actual_disagreement10_scores_pending': False, 'actual_CDF_large8_scores_complete_no_gain': True, 'actual_CDFfine8_scores_pending': True, 'new_fits': 0, 'new_scores_by_publication': 0, 'native_candidate_qualification_pending_if_gain': True, 'test_labels_read': False},'files':bindings})
    out=Path('E:/赛题五_本机临时/Actual_actual_CDFfine77_sources_and_catalog191_main_v1_20261011');out.mkdir(exist_ok=False)
    create(out/'frozen_before_publication.json',{'files':bindings})
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    from owned_idle_publication_wait_reboot_dynamic_boundary_v3_20261011 import hold
    with serial(out/'serial_mutex.json') as mutex,safe(out/'safe'),git_io(out/'file_backed_git'):
        mutex.acquire();assert allowed()
        parent,worker,idle=hold(read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json'),'    main (watch_validations_main_v7_20261006.py:71)')
        try:
            sync=h.sync;h.verify_main(sync.git('rev-parse','HEAD'));assert not sync.git('status','--porcelain')
            for name,data in payload.items():sync.atomic(sync.WORKTREE/name,data)
            names=sorted(payload)
            for i in range(0,len(names),50):sync.git('add','-f','--',*names[i:i+50])
            assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(names)
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','记录实际CDF大权重6方案不提分、冻结小权重6方案与完整原生条件候选78、实际小权重CPU6全量18前缀6扰动检查、完整191与新增评分明细榜排队；保留原48任务和运行中提分候选73',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'Actual_actual_CDFfine77_sources_and_catalog191_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
