"""Publish all new verified controls and actual launched full jobs to main only."""
from pathlib import Path
import hashlib
import json
import sys
import time
import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path.insert(0,str(A))
import watch_validations_main_v2_20261005 as watcher
from finalize_main_branch_consolidation_20261005 import owned_pair,verify_main
from publish_main_closeout_v2_20261005 import names,blob_hashes
sync=watcher.sync
PREFIX=Path('validation_sync/ready_fm_reference_workflows_20261005')
OUT=A/'ready_fm_reference_workflows_github_20261005'


def main():
    assert not (OUT/'receipt.json').exists()
    proofs=[A/f'{folder}/verification.json' for folder in (
        'ready_fm_reference_generator_preflight_20261005',
        'ready_fm_reference_execution_preflight_20261005',
        'ready_fm_reference_quality_followups_20261005',
        'gap_aware_optimization_monitor_handoff_v16_20261005',
        'neural16384_epoch_progress_observation_20261005')]
    for path in proofs:
        proof=sync.read(path)
        assert proof['status'].startswith('passed')
        for source,digest in proof.get('source_sha256',{}).items():assert sync.sha(Path(source).read_bytes())==digest,source
    assert [r['generated_records'] for r in sync.read(proofs[0])['controls']]==[124,138,138]
    launches=sync.read(proofs[2])['quality_rounds']
    owned_at_capture=[]
    for job in launches:
        process=psutil.Process(job['owned_worker_pid'])
        assert process.create_time()==job['owned_worker_creation_time'] and process.cmdline()[-2:]==job['script_args']
        assert not Path(job['stderr']).read_bytes()
        owned_at_capture.append({'round':job['round'],'pid':process.pid,'creation_time':process.create_time(),
            'explicit_parent_round':job['explicit_parent_round'],'owned_live':True})
    launch=sync.read(sync.OUT/'launch_v3.json')['publisher']
    publisher=owned_pair(launch['pid'],Path(launch['script']),launch['script_args'])
    assert publisher[1].pid==sync.read(sync.OUT/'owner.lock')['pid']
    monitor_launch=sync.read(A/'actual_optimization_monitor_launch_v16_20261005.json')
    monitor=owned_pair(monitor_launch['pid'],Path(monitor_launch['script']),monitor_launch['script_args'])
    suspended=[]
    try:
        for attempt in range(12):
            for parent,child in (publisher,monitor):
                for process in (child,parent):process.suspend();suspended.append(process)
            busy=[p for parent,child in (publisher,monitor) for p in parent.children(recursive=True)
                if p.pid!=child.pid and p.name().lower()!='conhost.exe']
            if not busy:break
            for process in reversed(suspended):process.resume()
            suspended.clear();time.sleep(1)
        else:raise RuntimeError('Owned publisher or observer has an active command.')
        previous=sync.git('rev-parse','HEAD')
        historical_heads=verify_main(previous)
        assert not sync.git('status','--porcelain')
        selected=names('ls-files','--modified')|names('ls-files','--others','--exclude-standard')
        evidence=set()
        for pattern in ('ready_fm_reference*20261005','gap_aware_optimization_monitor*20261005','neural16384_epoch_progress_observation_20261005'):
            for folder in A.glob(pattern):
                if folder.is_dir():evidence.update(p for p in folder.rglob('*') if p.is_file() and p.suffix in ('.json','.txt'))
        sources={ROOT/name for name in selected}|evidence
        targets,captures={},{}
        for source in sorted(sources):
            assert source.is_file() and source.suffix in ('.py','.json','.md','.yaml','.yml','.toml','.txt'),source
            data=source.read_bytes()
            assert len(data)<5*1024**2 and not sync.SECRET.search(data),source
            if source.suffix=='.json':json.loads(data.decode('utf-8-sig'))
            relative=source.relative_to(ROOT)
            destination=PREFIX/relative if source in evidence else relative
            targets[destination.as_posix()]=data
            operational=source.suffix=='.json' and (source.name=='resumed_rounds_nystrom_locked_20261004.json'
                or 'state' in source.stem or 'resume' in source.stem or source.stem.startswith(('optimization_boundary','optimization_fit_cost','next_experiment')))
            captures[relative.as_posix()]={'published_path':destination.as_posix(),'sha256':sync.sha(data),
                'bytes':len(data),'operational_snapshot':operational}
        targets[(PREFIX/'.gitattributes').as_posix()]=b'* -text\n'
        targets[(PREFIX/'manifest.json').as_posix()]=sync.encoded({'status':'verified_controls_and_actual_complete_jobs_captured_for_main',
            'at_local':sync.now(),'previous_main':previous,'files':captures,
            'explicit_parent_rounds':{'83':82,'84':83},'full_official_records_prespecified':{'83':124,'84':138},
            'generator_controls':[124,138,138],'source_and_driver_and_candidate_packaging_controls':'passed',
            'actual_native_first_epoch_log_progress_observation':sync.read(proofs[4]),'current_quality_worker_ownership':owned_at_capture,'original_rounds67_through82_retained_and_required':True,
            'progress_does_not_infer_earlier_rounds_complete_from_later_side_comparison':True,
            'actual_full_official_scores_candidates_and_ranking_updates_still_pending':True,
            'all_original_and_new_frozen_source_versions_retained':True,
            'models_and_raw_data_and_predictions_remain_local_D_or_E':True,'only_publication_branch':'main',
            'historical_branch_heads_retained':historical_heads,'new_native_configurations':0,'new_native_fits':0,
            'new_quality_scores_by_controls':0,'test_labels_read':False,'global_resource_exhaustion_established':False})
        targets[(PREFIX/'README.md').as_posix()]=(
            '# 已完成因子分解机接入轻量完整验证链\n\n'
            '六种原始63维成熟特征因子分解机比较排序/收益目标和0/8/32因子，均已有30次真实年度32轮训练及6个最终模型。'
            '第83轮以实际合格R82为基准比较124条用途、组合、权重、留存和涨停偏移方案；第84轮以合格R83为基准比较138条独立主模型及后处理细搜。'
            '所有原第67—82轮保留并仍须完成。\n\n'
            '124/138/138生成控制及真实驱动绑定、版本化前序工厂、候选源码复制、旧入口覆盖恢复、重复复制一致、封存拒写和原生FM路由安装恢复检查通过。'
            '生成控制的排序值是合成值；262条真实完整官方评分、选定冻结、因果检查、全量候选与完整榜更新仍待实际执行。'
            '入口已真实启动，等待前序合格后使用一个隔离评分进程执行，全部原方案和预测数学保留。\n\n'
            '保存原始大模型进度日志前缀：2020从训练开始到首轮日志652秒，2021相应区间7474秒。'
            '这一区间包含预处理、初始化和首轮训练，不是孤立GPU内核计时；第二年度完整32轮尚未完成。'
            '实际进程仍在运行，没有停止或重启，没有据此声称物理OOM或资源耗尽。\n\n'
            '继续使用2020—2024年5,635,800行、1,212连续交易日的完整官方综合分以及成熟过去收益率映射。'
            '验证年份重复使用，选模偏差未校正；未读取测试标签。只提交main，数据、模型、缓存保持D/E盘。\n').encode('utf-8')
        for name,record in captures.items():
            if not record['operational_snapshot']:assert sync.sha((ROOT/name).read_bytes())==record['sha256'],name
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        paths=sorted(targets)
        for offset in range(0,len(paths),50):sync.git('add','-f','--',*paths[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())
        assert staged and staged<=set(paths)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m',
            '新增262条完整因子分解机验证并记录真实大模型首轮耗时，保留所有原验证任务',timeout=180)
        commit=sync.git('rev-parse','HEAD')
        expected={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
        assert blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        receipt={'status':'pushed_verified_complete_ready_FM_workflows_main_only','at_local':sync.now(),
            'commit':commit,'files':len(targets),'verified_raw_git_blob_sha256':len(expected),
            'required_actual_official_records':262,'new_quality_scores_by_controls':0,
            'url':f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        sync.atomic(OUT/'receipt.json',sync.encoded(receipt))
        print(json.dumps(receipt,ensure_ascii=False),flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():process.resume()


if __name__=='__main__':main()
