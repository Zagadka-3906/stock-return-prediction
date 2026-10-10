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
PREFIX=Path('validation_sync/reference66_linear_leaf_baseline_20261005')
OUT=A/'reference66_linear_leaf_baseline_github_20261005'


def main():
    assert not (OUT/'receipt.json').exists()
    proofs=[A/f'{folder}/verification.json' for folder in (
        'reference66_linear_leaf_generator_preflight_v2_20261005',
        'reference66_linear_leaf_execution_preflight_20261005',
        'reference66_linear_leaf_quality_followups_20261005',
        'gap_aware_optimization_monitor_handoff_v15_20261005',
        'reference66_full_baseline_csv_qa_20261005')]
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
    monitor_launch=sync.read(A/'actual_optimization_monitor_launch_v15_20261005.json')
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
        for pattern in ('reference66_linear_leaf*20261005','gap_aware_optimization_monitor*20261005','reference66_full_baseline*20261005'):
            for folder in A.glob(pattern):
                if folder.is_dir():evidence.update(p for p in folder.rglob('*.json') if p.is_file())
        evidence.update([A/'optimization_20261003_r81/protocol.json',A/'optimization_20261003_r81/identical_official_scores/e40e0143c78ed21b9471f98886f2a48dd29a90075c0db0c4055e8fc4e95de402.json'])
        sources={ROOT/name for name in selected}|evidence
        targets,captures={},{}
        for source in sorted(sources):
            assert source.is_file() and source.suffix in ('.py','.json','.md','.yaml','.yml','.toml'),source
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
            'explicit_parent_rounds':{'81':66,'82':81},'full_official_records_prespecified':{'81':124,'82':138},
            'generator_controls':[124,138,138],'source_and_driver_and_candidate_packaging_controls':'passed',
            'actual_full_baseline_official_csv_replay':sync.read(proofs[4]),'current_quality_worker_ownership':owned_at_capture,'original_rounds67_through80_retained_and_required':True,
            'progress_does_not_infer_earlier_rounds_complete_from_later_side_comparison':True,
            'actual_full_official_scores_candidates_and_ranking_updates_still_pending':True,
            'original_failed_new_generator_and_all_frozen_source_versions_retained':True,
            'models_and_raw_data_and_predictions_remain_local_D_or_E':True,'only_publication_branch':'main',
            'historical_branch_heads_retained':historical_heads,'new_native_configurations':0,'new_native_fits':0,
            'new_quality_scores_by_controls':0,'test_labels_read':False,'global_resource_exhaustion_established':False})
        targets[(PREFIX/'README.md').as_posix()]=(
            '# R66完整基准CSV重放实际核验\n\n'
            '实际读取R81生成的训练内部验证CSV，核验5,635,800行、1,212日、4,650代码及全部有限预测。'
            'CSV字节SHA、验证X/Y、官方评分代码、计分缓存代码和运行库版本均与既有官方胶囊匹配，八项官方指标逐项相同，S=0.4510081068915626。'
            '本次为完全相同输入的官方结果重放，未产生新配置评分，也未重新调用官方评分。新增方案仍待完整比较。\n\n'
            '第81轮以已合格R66为明确基准，对六种普通树叶与线性树叶模型做124条完整用途、组合、权重及后处理评分；'
            '第82轮以合格R81为基准做138条独立主模型、逐模型参数、留存及实际最高分细搜。'
            '保留全部2020—2024年5,635,800行、1,212连续交易日及原始官方评分、成熟过去收益映射、因果和全量候选推理检查。\n\n'
            '124/138/138生成检查、真实驱动绑定、实际候选源码复制及旧入口覆盖恢复、重复复制一致和封存拒写检查通过。'
            '这些生成检查的排序值明确为合成值，不是官方评分。原始残留波次路径失败及所有冻结源码保留。'
            '全部262条真实评分、最终候选及榜单更新仍需实际执行结束。\n\n'
            '真实入口已启动，使用一个隔离评分进程控制内存，模型训练、预测数学、全部方案和官方评分口径保留。'
            '已完成的30个年度模型和6个最终模型复用，不重复计为新训练。原有第67—80轮继续保留并仍要求完成。'
            '进度台账已检查早期轮次未完成时的缺口，按所有合格方案的最高分更新最佳结果。\n\n'
            '全部代码和证据只提交main；模型、数据、缓存继续存D/E盘。测试标签未读取，未证明全局可行方向或资源已经耗尽。\n').encode('utf-8')
        for name,record in captures.items():
            if not record['operational_snapshot']:assert sync.sha((ROOT/name).read_bytes())==record['sha256'],name
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        paths=sorted(targets)
        for offset in range(0,len(paths),50):sync.git('add','-f','--',*paths[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())
        assert staged and staged<=set(paths)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m',
            '核验R66完整5635800行收益CSV及八项官方指标重放，保留262条实际验证任务',timeout=180)
        commit=sync.git('rev-parse','HEAD')
        expected={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
        assert blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        receipt={'status':'pushed_verified_full_reference66_baseline_csv_main_only','at_local':sync.now(),
            'commit':commit,'files':len(targets),'verified_raw_git_blob_sha256':len(expected),
            'required_actual_official_records':262,'new_quality_scores_by_controls':0,
            'url':f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        sync.atomic(OUT/'receipt.json',sync.encoded(receipt))
        print(json.dumps(receipt,ensure_ascii=False),flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():process.resume()


if __name__=='__main__':main()
