"""Publish confirmed selection-history correction to main; do not resume optimization."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import sys,os,json,hashlib,subprocess,posixpath,re
from urllib.parse import unquote
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
import publish_classifier_consensus_workflows_20261006 as h
OUT=Path('E:/赛题五_本机临时/选模标准审计142_20261011')
PREFIX=ROOT/'validation_sync/Actual_selection_compliance142_correction_v1_20261011'

def tree(commit):
    raw=subprocess.check_output(['git','ls-tree','-r','-z',commit],cwd=h.sync.WORKTREE);result={}
    for entry in raw.split(b'\0'):
        if entry:header,name=entry.split(b'\t',1);result[name.decode('utf8')]=header.split()[2].decode()
    return result

def main():
    controls=[read(A/f'current_user_runtime_control_202610{d}.json') for d in ('10','09')]
    now=datetime.now(timezone(timedelta(hours=8))).isoformat()
    assert all(c['status']=='project_workers_stopped_until_actual_user_manual_continue' and not c['automatic_restart_enabled'] for c in controls)
    state=read(ROOT/'selection_compliance.json');assert state['confirmed_test_feedback'] and state['current_recommended_submission'] is None
    proof=read(PREFIX/'evidence_manifest.json')
    for row in proof['evidence']:assert sha(row['original_path'])==sha(ROOT/row['archive_path'])==row['sha256']
    for p,d in proof['protected_artifact_SHA256'].items():assert sha(p)==d,p
    assert read(ROOT/'active_release.json')['status']=='selection_compliance_suspended'
    latest=read(ROOT/'docs/latest_results.json');assert all(not latest[k]['recommended_under_selection_standard'] for k in ['latest_packaged_candidate','fully_registered_delivery'])
    selected=read(A/'alternate_verified_consensusFraction101_submission_delivery_v1_20261011.json')
    for folder in [Path(selected['output']),Path(latest['fully_registered_delivery']['local_delivery_path'])]:assert (folder/'选模来源合规更正_20261011.md').read_bytes()==(ROOT/'docs/SELECTION_COMPLIANCE.md').read_bytes()
    src=PREFIX/'audit'/Path(__file__).name;src.write_bytes(Path(__file__).read_bytes())
    names=['README.md','ABOUT.md','active_release.json','selection_compliance.json','docs/README.md','docs/METHODS.md','docs/RESULTS.md','docs/GETTING_STARTED.md','docs/REPOSITORY_GUIDE.md','docs/SELECTION_COMPLIANCE.md','docs/latest_results.json','analysis/README.md','experiments/README.md','results/README.md','validation_sync/README.md']
    payload={name:(ROOT/name).read_bytes() for name in names}
    payload.update({p.relative_to(ROOT).as_posix():p.read_bytes() for p in PREFIX.rglob('*') if p.is_file()})
    for name,raw in payload.items():assert not h.sync.SECRET.search(raw),name
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    from verified_TLS_Git_retry_runtime_v3_20261010 import installed as git_io
    with serial(OUT/'publication_mutex.json') as mutex,safe(OUT/'publication_safe'),git_io(OUT/'publication_git_io'):
        mutex.acquire();sync=h.sync
        assert not owned(read(A/'service_owned_workflows_20261006/main_publisher_reboot_v12_20261011/native_launch.json'))
        previous=read(A/'Actual_repository_cleanup140_main_receipt_v1_20261011.json')['commit']
        assert sync.git('rev-parse','HEAD')==previous;h.verify_main(previous);assert not sync.git('status','--porcelain')
        original=tree(previous);newpaths=set(original)|set(payload)
        missing=[];checked=0
        for name,raw in payload.items():
            if not name.endswith('.md') or name.startswith(PREFIX.relative_to(ROOT).as_posix()+'/historical_evidence/') or name.endswith('previous_local_package_usage.md'):continue
            for link in re.findall(r'\]\(([^)]+)\)',raw.decode('utf8')):
                target=unquote(link.split('#',1)[0].strip('<>'))
                if not target or ':' in target or target.startswith('/'):continue
                p=posixpath.normpath(posixpath.join(posixpath.dirname(name),target));checked+=1
                if p not in newpaths and not any(n.startswith(p.rstrip('/')+'/') for n in newpaths):missing.append((name,link))
        assert not missing,missing
        summary={'status':'confirmed_historical_test_feedback_corrected_current_recommendation_preserved_original_scores_and_models','at_local':now,'previous_main':previous,'actual_user_evidence':'2026-09-28 reconstructed343 TEST outcomes fed back into candidate recommendations and research directions; latest lineage inherited these routes','current_recommendation_suspended':True,'quantitative_score_unchanged':.4514612196682616,'uncached_unmodified_official_calls':2,'real_or_reconstructed_TEST_labels_not_read_during_audit':True,'all37_models_CSV_ZIP_protected_SHA256':proof['protected_artifact_SHA256'],'relative_markdown_links_verified':checked,'optimization_remains_paused':True,'old_scores_manifests_and_receipts_not_overwritten':True,'no_new_training':True,'no_new_model_inference':True,'payload_SHA256':{n:hashlib.sha256(b).hexdigest() for n,b in payload.items()}}
        create(OUT/'frozen_before_correction_publication.json',summary)
        summary_path=PREFIX/'publication_verification.json';summary_path.write_bytes(sync.encoded(summary));payload[summary_path.relative_to(ROOT).as_posix()]=summary_path.read_bytes()
        for name,raw in payload.items():assert not sync.SECRET.search(raw),name;sync.atomic(sync.WORKTREE/name,raw)
        sync.git('add','-f','--',*sorted(payload))
        assert set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())==set(payload)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','更正历史测试反馈：撤回严格训练内选模结论并暂停合规推荐，保留评分与模型证据',timeout=180)
        commit=sync.git('rev-parse','HEAD');after=tree(commit)
        assert set(after)==newpaths|{summary_path.relative_to(ROOT).as_posix()}
        for name,oid in original.items():
            if name not in payload:assert after[name]==oid,name
        expected={n:hashlib.sha256(b).hexdigest() for n,b in payload.items()};assert h.blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=600);h.verify_main(commit);h.watcher.advance_source_index(commit)
        for p,d in proof['protected_artifact_SHA256'].items():assert sha(p)==d,p
        assert not sync.git('status','--porcelain')
        receipt={'status':'pushed_and_remote_head_verified_selection_history_correction','branch':'main','commit':commit,'previous_main':previous,'raw_blobs_verified':len(payload),'relative_links_verified':checked,'all_other_Git_tree_blobs_unchanged':True,'models37_CSV_ZIP_unchanged':True,'current_compliance_recommendation_suspended':True,'clean_replacement_not_claimed':True,'optimization_remains_paused':True}
        create(OUT/'main_receipt.json',receipt);create(A/'Actual_selection_compliance142_main_receipt_v1_20261011.json',receipt);print(receipt,flush=True)

if __name__=='__main__':
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2);main()
