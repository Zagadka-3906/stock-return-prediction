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

OUT=A/'ready_goss_observer31_github_20261006'
PREFIX=Path('validation_sync/ready_goss_observer31_20261006')


def main():
    source=A/'ready_goss_observer31_actual_handoff_20261006';proof=read(source/'verification.json')
    assert proof['status']=='passed_actual_observer31_full_generation_and_preserved_scientific_execution'
    assert proof['scientific_processes_stopped_or_restarted']==0
    assert proof['old_source_and_R95_frozen_protocol_unchanged'] is True
    assert owned(proof['actual_observer'])
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    assert not OUT.exists();OUT.mkdir()
    sources=[Path(__file__),A/'monitor_actual_optimization_progress_v31_20261006.py',A/'monitor_actual_optimization_progress_v30_20261006.py',A/'check_ready_goss_observer31_ownership_20261006.py',A/'handoff_ready_goss_observer31_20261006.py',*source.rglob('*.json'),*(A/'ready_goss_observer31_ownership_preflight_20261006').glob('*.json'),*(A/'service_owned_workflows_20261006/progress_monitor_v31').glob('*.json'),A/'service_owned_workflows_20261006/progress_monitor_v30/administrative_supersession_for_ready_GOSS_20261006.json']
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
        targets[(PREFIX/'README.md').as_posix()]=('# 第95/96轮实际进程归属监控修正\n\n旧监控在新增95/96轮运行时遗漏已确认进程归属标志。新版本保留原完整收集器、科学资格检查、年度训练次数和三个公开快照的完整事务，只补充实际队列进程及其创建时间和命令校验。真实第95轮识别成功；私有创建时间不匹配控制被拒绝，未写入真实队列。\n\n实际隐藏启动新监控31，三个公开快照同一完整generation确认第95轮在运行；旧监控30仅在原休眠边界退役。科学进程、队列7及main发布6未停止或重启；旧源码及第95轮冻结协议SHA不变，原67至94轮和新增262项GOSS方案保留。此修正不新增训练或评分，实际GOSS训练仍为30次年度及6次最终训练。\n').encode('utf-8')
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        selected=sorted(targets)
        for offset in range(0,len(selected),50):sync.git('add','-f','--',*selected[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged and staged<=set(selected)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','修正GOSS95及96实际进程归属监控，保留原完整验证与冻结来源',timeout=180)
        commit=sync.git('rev-parse','HEAD');expected={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()};assert helpers.blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
        receipt={'status':'pushed_verified_actual_observer31_handoff_main_only','at_local':sync.now(),'commit':commit,'raw_git_blobs_verified':len(expected),'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+PREFIX.as_posix()}
        create(OUT/'receipt.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
    except BaseException as error:
        create(OUT/'failure.json',{'status':'failed_preserved_observer31_publication','error':f'{type(error).__name__}: {error}'});raise
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
        create(OUT/'actual_hidden_publication_children.json',{'events':restore()})


if __name__=='__main__':main()
