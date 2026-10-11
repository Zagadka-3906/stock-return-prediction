"""Publish only the new fixed baseline's source, native models and audit records."""
from pathlib import Path
import os,sys,json,hashlib,gzip,subprocess
from datetime import datetime,timezone,timedelta
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
import publish_classifier_consensus_workflows_20261006 as h
from train_only_baseline143_v1_20261011 import sha,read,put,RUN_ID
W=Path('E:/赛题五_本机临时/固定训练内基线143_20261011')
PREFIX=ROOT/'validation_sync/TRAIN_only_baseline143_v1_20261011'


def tree(commit):
    raw=subprocess.check_output(['git','ls-tree','-r','-z',commit],cwd=h.sync.WORKTREE,
                                creationflags=subprocess.CREATE_NO_WINDOW)
    d={}
    for row in raw.split(b'\0'):
        if row:
            header,name=row.split(b'\t',1);d[name.decode('utf-8')]=header.split()[2].decode('ascii')
    return d


def main():
    for day in ['10','09']:
        c=read(A/f'current_user_runtime_control_202610{day}.json')
        assert c['status']=='user_authorized_bounded_TRAIN_only_baseline_training' and c['bounded_training_run_id']==RUN_ID
        assert not c['automatic_restart_enabled']
    now=datetime.now(timezone(timedelta(hours=8))).isoformat()
    v=read(W/'verification.json');delivery=read(W/'delivery.json');p=read(W/'protocol.json')
    assert v['status'].startswith('passed_') and not v['current_run_TEST_outcomes_read_or_reconstructed']
    assert sha(W/'protocol.json')==v['protocol_sha256'] and p['candidate_count']==1
    assert delivery['submission_sha256']==v['submission_sha256']
    receipt=W/'main_receipt.json'
    if receipt.is_file():h.verify_main(read(receipt)['commit']);print(read(receipt),flush=True);return
    PREFIX.mkdir(parents=True,exist_ok=False)
    (PREFIX/'.gitattributes').write_bytes(b'* -text\n')
    files=['protocol.json','protocol.sha256','synthetic_causality.json','train_features_manifest.json',
           'official_TRAIN_metrics.json','frozen_before_TEST_inference.json','verification.json','delivery.json',
           'evaluate.py','model_final.txt','model_final.json',
           'train_only_baseline143_v1_20261011.py','train_only_features143_v1_20261011.py',
           'train_only_baseline143_inference_v2_20261011.py',
           'inference_adapter_frozen_before_TEST_inference.json','first_inference_failure.json',
           'train_only_baseline143_inference_v3_20261011.py',
           'inference_prefix_audit_alignment_v3.json','second_inference_audit_failure.json']
    for y in range(2020,2025):files += [f'model_{y}.txt',f'model_{y}.json',f'oof_{y}.parquet']
    for n in files:(PREFIX/n).write_bytes((W/n).read_bytes())
    # Preserve actual submission bytes compactly, without pushing the raw data.
    with (W/'submission.csv').open('rb') as src,(PREFIX/'submission.csv.gz').open('wb') as out:
        with gzip.GzipFile(filename='',fileobj=out,mode='wb',compresslevel=6,mtime=0) as z:
            while b:=src.read(4*1024**2):z.write(b)
    digest=hashlib.sha256()
    with gzip.open(PREFIX/'submission.csv.gz','rb') as z:
        while b:=z.read(4*1024**2):digest.update(b)
    assert digest.hexdigest()==v['submission_sha256']
    (PREFIX/'training_authorization.json').write_bytes((A/'user_authorized_train_only_baseline143_v1_20261011.json').read_bytes())
    (PREFIX/'publish_train_only_baseline143_main_v1_20261011.py').write_bytes(Path(__file__).read_bytes())
    doc=Path(delivery['path'])/'README.md'
    (PREFIX/'README.md').write_bytes(doc.read_bytes())
    (ROOT/'docs/TRAIN_ONLY_BASELINE143.md').write_bytes(doc.read_bytes())
    summary={'status':'completed_fixed_TRAIN_only_direct_return_baseline',
             'candidate':p['candidate'],'run_id':RUN_ID,'at_local':now,
             'official_TRAIN_metrics':read(W/'official_TRAIN_metrics.json')['metrics'],
             'official_TEST_score':None,'comparison_with_historically_contaminated_winners_not_used_for_selection':True,
             'single_candidate_predeclared':True,'pre_revelation_architecture_anchor':p['pre_revelation_architecture_anchor'],
             'fresh_TRAIN_only_feature_computation':True,'new_native_fits':6,
             'annual_validation_years':[2020,2021,2022,2023,2024],
             'predicted_TEST_input_rows':v['rows'],'predicted_TEST_days':v['days'],
             'current_run_TEST_outcomes_read_or_reconstructed':False,
             'data_and_causal_execution_checks_passed':True,
             'historical_TEST_exposure_not_erased_or_claimed_unviewed':True,
             'new_complete_design_not_claimed_frozen_before_historical_reveal':True,
             'organizer_submission_eligibility_not_certified':True,
             'old37_model_selection_compliance_correction_remains_valid':True,
             'no_old_release_recommendation_overwritten':True,
             'submission_sha256':v['submission_sha256'],'final_model_sha256':v['final_model_sha256'],
             'protocol_sha256':v['protocol_sha256'],'local_delivery':delivery['path'],
             'archive':'validation_sync/TRAIN_only_baseline143_v1_20261011',
             'record':'docs/TRAIN_ONLY_BASELINE143.md'}
    put(ROOT/'results/train_only_baseline143_v1_20261011.json',summary)
    manifest={x.relative_to(PREFIX).as_posix():{'sha256':sha(x),'bytes':x.stat().st_size}
              for x in PREFIX.iterdir() if x.is_file()}
    put(PREFIX/'archive_manifest.json',{'files':manifest,'submission_gzip_decompressed_SHA256':v['submission_sha256'],
                                       'raw_TRAIN_or_TEST_data_exported':False})
    payload={x.relative_to(ROOT).as_posix():x.read_bytes() for x in PREFIX.iterdir() if x.is_file()}
    for n in ['docs/TRAIN_ONLY_BASELINE143.md','results/train_only_baseline143_v1_20261011.json',
              'analysis/train_only_baseline143_v1_20261011.py','analysis/train_only_features143_v1_20261011.py',
              'analysis/publish_train_only_baseline143_main_v1_20261011.py',
              'analysis/train_only_baseline143_inference_v2_20261011.py',
              'analysis/train_only_baseline143_inference_v3_20261011.py']:
        payload[n]=(ROOT/n).read_bytes()
    for n,b in payload.items():
        if n.endswith(('.md','.json','.py')):assert not h.sync.SECRET.search(b),n
        assert len(b)<95*1024**2,n
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    with serial(W/'publication_mutex.json') as mutex,safe(W/'publication_safe'),git_io(W/'publication_git_io'):
        mutex.acquire();s=h.sync
        previous=s.git('rev-parse','HEAD');h.verify_main(previous);assert not s.git('status','--porcelain')
        before=tree(previous);assert all(n not in before for n in payload), 'New baseline must not overwrite previous records.'
        for n,b in payload.items():s.atomic(s.WORKTREE/n,b)
        s.git('add','-f','--',*sorted(payload))
        assert set(s.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(payload)
        s.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m',
              '新增固定训练内收益基线：预揭示架构锚定、六次成熟标签训练、连续官方评分与完整推理核验',timeout=180)
        commit=s.git('rev-parse','HEAD');after=tree(commit)
        assert set(after)==set(before)|set(payload)
        assert all(after[n]==oid for n,oid in before.items())
        hashes={n:hashlib.sha256(b).hexdigest() for n,b in payload.items()}
        assert h.blob_hashes(commit,hashes)==hashes
        s.git('push','origin','HEAD:refs/heads/main',timeout=600);h.verify_main(commit)
        h.watcher.advance_source_index(commit)
        assert not s.git('status','--porcelain')
        result={'status':'pushed_and_remote_main_verified_fixed_TRAIN_only_baseline143',
                'branch':'main','commit':commit,'previous_main':previous,'files_verified':len(payload),
                'all_previous_Git_blobs_unchanged':True,'old_selection_compliance_record_preserved':True,
                'official_TRAIN_score':v['official_TRAIN_score'],'raw_dataset_exported':False,
                'submission_decompressed_sha256':v['submission_sha256']}
        put(receipt,result);put(A/'Actual_train_only_baseline143_main_receipt_v1_20261011.json',result)
        print(result,flush=True)


if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate([('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1')]):
        os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    main()
