"""Main-only publication of actual candidate reconstruction and the queued36/173/QA84 flow."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,hashlib,gzip
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    paths=[Path(__file__),*[Path(p) for p in ['D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_actual_disagreement_gain10_CDF8_native76_sources_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_actual_disagreement10_score_priority72_observer148_sources_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_disagreement_CDF8_science_priority75_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_rank120_rank60_after183_disagreement_CDF8_screen75_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement_CDF8_predeclared_sources75_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_actual191_then_disagreement10_and_CDF8_science_priority75_then_original48_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_disagreement_CDF8_priority75_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_idle_administrative_priority72_retirement_for_new_science75_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_disagreement_CDF8_full_conditional76_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_disagreement_CDF8_results_selection_main_and_conditional76_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement_CDF8_early76_sources_admission_v2_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\verify_disagreement_CDF8_actual_CPU_controls76_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_disagreement_CDF8_six_cases_CPU_controls76_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\refresh_actual_observer149_disagreement_gain_and_CDF75_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\monitor_verified_current_optimization_v149_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_observer149_disagreement10_gain_and_CDF8_snapshot_admission_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement10_gain_decision_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\actual_StockRank120Rank60_after183_disagreement10_screen_location_v1_20261011.json', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\normalize_rank120_rank60_disagreement10_early73_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\qualify_rank120_rank60_disagreement10_early73_selected_native14_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_Rank120Rank60Disagreement10Early73_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_Rank120Rank60Disagreement10Early73_selected_candidate_feature_cache_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\seal_Rank120Rank60Disagreement10Early73_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement10_early73_storage_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement_after_qualified183_native_stage73_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\predict_rank120_rank60_disagreement_complete_qualified183_scheme73_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\normalize_rank120_rank60_disagreement_CDF8_early76_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\qualify_rank120_rank60_disagreement_CDF8_early76_selected_native14_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_Rank120Rank60DisagreementCdf8Early76_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\run_Rank120Rank60DisagreementCdf8Early76_selected_candidate_feature_cache_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\seal_Rank120Rank60DisagreementCdf8Early76_selected_candidate_v2_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement_CDF8_early76_storage_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\rank120_rank60_disagreement_CDF_after_qualified183_native_stage76_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\predict_rank120_rank60_disagreement_CDF_complete_qualified183_scheme76_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_actual_disagreement73_complete_candidate_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_verified_disagreement73_alternate_submission_delivery_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\publish_actual_disagreement_CDF76_complete_candidate_main_v1_20261011.py', 'D:\\3.Study\\数据分析\\赛题五\\analysis\\prepare_verified_disagreement_CDF76_alternate_submission_delivery_v1_20261011.py']]]
    import publish_classifier_consensus_workflows_20261006 as h
    prefix=Path('validation_sync/Actual_actual_disagreement_gain10_CDF8_native76_sources_v1_20261011');payload={};bindings={}
    for p in dict.fromkeys(paths):
        raw=p.read_bytes();assert not h.sync.SECRET.search(raw),p
        digest=hashlib.sha256(raw).hexdigest();rel=p.relative_to(ROOT) if p.is_relative_to(ROOT) else Path('external_metadata')/(digest+'_'+p.name)
        name=(prefix/rel).as_posix();data=raw
        if len(data)>=5*1024**2:data=gzip.compress(data,mtime=0);name+='.gz';assert gzip.decompress(data)==raw
        assert len(data)<95*1024**2;payload[name]=data;bindings[str(p)]={'path':name,'raw_sha256':digest}
    payload[(prefix/'.gitattributes').as_posix()]=b'* -text\n'
    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**{'status': 'actual_all10_OFFICIAL_TRAIN_S_gain_selected_full_native_pending_new8_CDF_hypotheses_frozen_CPU_controls_actual_conditional37_native76_sources_only_no_candidate_completion_claim', 'actual_disagreement10_scores_pending': False, 'actual_disagreement_CDF8_scores_pending': True, 'new_fits': 0, 'new_scores_by_publication': 0, 'native_candidate_qualification_pending_if_gain': True, 'test_labels_read': False},'files':bindings})
    out=Path('E:/赛题五_本机临时/Actual_actual_disagreement_gain10_CDF8_native76_sources_main_v1_20261011');out.mkdir(exist_ok=False)
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
            sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','记录实际10项跨时长分歧官方S提分0.451455137、冻结6项可改变官方Top持仓的CDF验证、实际6全量CPU与18前缀6未来扰动控制、完整原生候选76条件流程及实际监控149；候选资格仍待完成',timeout=180)
            commit=sync.git('rev-parse','HEAD');hashes={n:hashlib.sha256(d).hexdigest() for n,d in payload.items()};assert h.blob_hashes(commit,hashes)==hashes
            sync.git('push','origin','HEAD:refs/heads/main',timeout=180);h.verify_main(commit);h.watcher.advance_source_index(commit)
            receipt={'status':'pushed_and_remote_head_verified','branch':'main','commit':commit,'raw_git_blobs_verified':len(hashes),'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+prefix.as_posix()}
            create(out/'receipt.json',receipt);create(A/'Actual_actual_disagreement_gain10_CDF8_native76_sources_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)
        finally:
            for p in (parent,worker):
                if p.is_running():p.resume()
if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
