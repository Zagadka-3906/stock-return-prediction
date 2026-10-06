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

OUT=A/'goss_reference_full_launcher_github_20261006'
PREFIX=Path('validation_sync/goss_reference_full_launcher_preflight_20261006')


def main():
    source=A/'goss_reference_full_launcher_preflight_20261006';proof=read(source/'verification.json')
    assert proof['status']=='passed_actual_two_nested_GOSS_launchers_V3_sources_cache_full_QA_and_provenance_restoration'
    assert [c['round'] for c in proof['controls']]==[95,96]
    assert all(c['scientific_stage_methods_called']==0 for c in proof['controls'])
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    assert not OUT.exists();OUT.mkdir()
    sources=[Path(__file__),A/'verify_goss_reference_full_launcher_20261006.py',*source.rglob('*.json')]
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
        targets[(PREFIX/'README.md').as_posix()]=('# 第95/96轮完整启动链检查\n\n真实执行两轮的缓存启动器和合格前序包装，只在最终科学阶段调用前截获。实际驱动绑定确认v3模型及发布工厂、缓存初始化和计分函数、全部无损榜检查、两层冻结来源均正确。有效v3源文件、真实缓存启动器和合格包装的SHA进入实际冻结范围；退出后全部函数、评分池、资格门控及隐藏子进程设置恢复。\n\n这是完整启动接线检查，不进行训练或评分，不代替5635800行连续官方评分、全量候选、因果及浏览器检查。原第67—94轮保留，新增95/96轮仍按实际队列执行。只提交main，不读取测试标签，数据和模型保持D/E盘。\n').encode('utf-8')
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        selected=sorted(targets)
        for offset in range(0,len(selected),50):sync.git('add','-f','--',*selected[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines());assert staged and staged<=set(selected)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m','核验GOSS95与96完整实际启动链及v3冻结来源和缓存无损榜绑定',timeout=180)
        commit=sync.git('rev-parse','HEAD');expected={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()};assert helpers.blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180);helpers.verify_main(commit);helpers.watcher.advance_source_index(commit)
        receipt={'status':'pushed_actual_launcher_controls_main_only','at_local':sync.now(),'commit':commit,'raw_git_blobs_verified':len(expected),'new_quality_scores':0,'url':'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/'+PREFIX.as_posix()}
        create(OUT/'receipt.json',receipt);print(json.dumps(receipt,ensure_ascii=False),flush=True)
    except BaseException as error:
        create(OUT/'failure.json',{'status':'failed_preserved_launcher_control_publication','error':f'{type(error).__name__}: {error}'});raise
    finally:
        for p in reversed(suspended):
            if p.is_running():p.resume()
        create(OUT/'actual_hidden_publication_children.json',{'events':restore()})


if __name__=='__main__':main()
