"""Synchronize the actual nested GOSS launch controls with main-only raw-blob verification."""
from pathlib import Path
import hashlib
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from hidden_windows_child_creation_20261006 import install
import publish_classifier_consensus_workflows_20261006 as helpers

OUT=A/'actual_R85_rank_cache_effectiveness_github_20261006'
PREFIX=Path('validation_sync/actual_R85_rank_cache_effectiveness_20261006')


def main():
    source=A/'actual_R85_rank_cache_effectiveness_20261006';proof=read(source/'verification.json')
    assert proof['status']=='passed_all100_actual_R85_scoring_worker_cache_events_audited'
    assert proof['actual_scored_records']==100
    assert proof['new_quality_scores']==proof['new_model_fits']==0
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    assert not OUT.exists();OUT.mkdir()
    sources=[Path(__file__),A/'audit_actual_R85_rank_cache_effectiveness_20261006.py',*source.rglob('*.json')]
    sync=helpers.sync;targets={(PREFIX/'.gitattributes').as_posix():b'* -text\n'};files={}
    for path in sources:
        data=path.read_bytes();assert len(data)<5*1024**2 and not sync.SECRET.search(data)
        target=path.relative_to(ROOT) if path.parent==A else PREFIX/path.relative_to(ROOT)
        targets[target.as_posix()]=data;files[path.relative_to(ROOT).as_posix()]={'published_path':target.as_posix(),'raw_sha256':hashlib.sha256(data).hexdigest()}
    row=read(A/'service_owned_workflows_20261006/main_publisher_v6/native_launch.json');assert owned(row)
    root,worker=helpers.owned_pair(row['pid'],Path(row['script']),row['script_args']);suspended=[];restore=install()
    try:
        for _ in range(300):
            for p in (worker,root):p.suspend();suspended.append(p)
            busy=[p for p in root.children(recursive=True) if p.pid!=worker.pid and p.name().lower()!='conhost.exe']
            if not busy:break
            for p in reversed(suspended):p.resume()
            suspended.clear();time.sleep(1)
        else:raise RuntimeError('Main6 owns an active publication command')
        previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous);assert not sync.git('status','--porcelain')
        targets[(PREFIX/'manifest.json').as_posix()]=sync.encoded({'status':proof['status'],'previous_main':previous,'at_local':sync.now(),'files':files,'full_scientific_grid_pending_actual_execution':True,'new_quality_scores':0,'new_native_fits':0,'test_labels_read':False,'only_publication_branch':'main'})
        targets[(PREFIX/'README.md').as_posix()]=('# 第85轮实际排序缓存效果审计\n\n核对已完成并上传main的100项评分工作进程记录，现有1GiB缓存累计命中1623次、未命中28次、淘汰5次。全部记录的实际缓存容量守界，预测算法和官方评分器保持原样。原100项验证来源在第85轮完整main记录中保存；本次审计保留逐项计数、来源SHA与原验证commit。\n\n依据这些记录继续保留评分工作进程的1GiB容量。此审计不测量前置一致性检查耗时，不从函数命中次数推断整个流程提速，也不据此宣称计算资源或优化方向耗尽。若今后在前置检查使用缓存，需要另行完成全量结果及因果对照。没有新增训练或候选评分，不修改当前冻结方案。\n').encode('utf-8')
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        selected=sorted(targets)
        for offset in range(0,len(selected),50):sync.git('add','-f','--',*selected[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged and staged<=set(selected)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','审计85轮全部100项实际缓存效果，保留容量并明确资源结论范围',timeout=180)
        commit=sync.git('rev-parse','HEAD');expected={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()};assert helpers.blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
        receipt={'status':'pushed_actual_R85_rank_cache_effectiveness_main_only','at_local':sync.now(),'commit':commit,'raw_git_blobs_verified':len(expected),'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+PREFIX.as_posix()}
        create(OUT/'receipt.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
    except BaseException as error:
        create(OUT/'failure.json',{'status':'failed_preserved_R85_cache_audit_publication','error':f'{type(error).__name__}: {error}'});raise
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
        create(OUT/'actual_hidden_publication_children.json',{'events':restore()})


if __name__=='__main__':main()
