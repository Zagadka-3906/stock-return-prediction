"""Publish the actual persistent waiter launch verification to main."""
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
OUT=A/'joint_goss_round97_idle_waiter_github_20261006'
PREFIX=Path('validation_sync/joint_goss_round97_idle_waiter_20261006')

def main():
    proofpath=A/'joint_goss_round97_idle_waiter_launch_control_20261006/verification.json'
    proof=read(proofpath)
    assert proof['status']=='passed_actual_owned_consoleless_persistent_waiter_and_preserved_live_R95_and_neural'
    for p,digest in proof['input_sha256'].items():assert sha(p)==digest,p
    assert owned(proof['actual_waiter']) and all(owned(r) for r in proof['preserved_live_scientific_workers'])
    assert not OUT.exists();OUT.mkdir()
    sources=[Path(__file__),proofpath,*map(Path,proof['input_sha256'])]
    sync=helpers.sync;targets={(PREFIX/'.gitattributes').as_posix():b'* -text\n'};files={}
    for path in dict.fromkeys(sources):
        data=path.read_bytes();assert len(data)<5*1024**2 and not sync.SECRET.search(data),path
        target=path.relative_to(ROOT) if path.parent==A and path.suffix=='.py' else PREFIX/path.relative_to(ROOT)
        targets[target.as_posix()]=data
        files[path.relative_to(ROOT).as_posix()]={'published_path':target.as_posix(),'raw_sha256':hashlib.sha256(data).hexdigest()}
    rows=[read(A/f'service_owned_workflows_20261006/{name}/native_launch.json') for name in ('main_publisher_v7','main_publisher_v6')
        if (A/f'service_owned_workflows_20261006/{name}/native_launch.json').exists()]
    row=next(r for r in rows if owned(r));root,worker=helpers.owned_pair(row['pid'],Path(row['script']),row['script_args'])
    suspended=[];restore=install()
    try:
        for _ in range(180):
            for p in (worker,root):p.suspend();suspended.append(p)
            busy=[p for p in root.children(recursive=True) if p.pid!=worker.pid and p.name().lower()!='conhost.exe']
            if not busy:break
            for p in reversed(suspended):p.resume()
            suspended=[];time.sleep(1)
        else:raise RuntimeError('Main publisher still owns an active publication command')
        previous=sync.git('rev-parse','HEAD');helpers.verify_main(previous)
        assert not sync.git('status','--porcelain')
        targets[(PREFIX/'manifest.json').as_posix()]=sync.encoded({'status':proof['status'],'previous_main':previous,
            'at_local':sync.now(),'files':files,'new_quality_scores':0,'new_native_fits':0,'only_publication_branch':'main'})
        targets[(PREFIX/'README.md').as_posix()]=('''# 第97轮实际后台等待程序

实际独立启动的等待程序通过PID、创建时间和命令核验；控制台句柄0，位于命令会话Job之外，临时目录D盘。现有第95轮仍是旧队列的子任务，因此先等待子进程自然完成；只有旧队列的子进程树为空、暂停前后两次均确认处于原有休眠位置后，才执行已验证的增量接入。保持原第67—96轮，新增第97轮151项，不重启或关闭科学任务。

第95轮完整评分及神经网络训练继续原进程。此处是实际启动核验，新增训练和官方分数均0，不读取测试标签；不是第97轮评分完成证明。成功接入后自动上传实际队列、main发布器和观察器记录，后续每轮完整验证由main发布器同步。
''').encode('utf-8')
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        selected=sorted(targets)
        for offset in range(0,len(selected),50):sync.git('add','-f','--',*selected[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())
        assert staged and staged<=set(selected)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','核验第97轮无窗口后台等待接入及原科学任务持续运行',timeout=180)
        commit=sync.git('rev-parse','HEAD');hashes={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
        assert helpers.blob_hashes(commit,hashes)==hashes
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
        receipt={'status':'pushed_verified_actual_idle_waiter_main_only','at_local':sync.now(),'commit':commit,
            'raw_git_blobs_verified':len(hashes),'new_quality_scores':0,
            'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+PREFIX.as_posix()}
        create(OUT/'receipt.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
    except BaseException as exc:
        create(OUT/'failure.json',{'status':'failed_preserved_idle_waiter_publication','error':f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
        create(OUT/'actual_hidden_publication_children.json',{'events':restore()})

if __name__=='__main__':main()
