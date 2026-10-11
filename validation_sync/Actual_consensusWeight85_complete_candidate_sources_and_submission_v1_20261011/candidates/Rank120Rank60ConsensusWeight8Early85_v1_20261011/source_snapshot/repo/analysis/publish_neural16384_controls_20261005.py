"""Publish the real instrumentation checks and complete pending wide-model workflow."""
from pathlib import Path
import hashlib
import json
import sys

import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import watch_validations_main_v2_20261005 as watcher

sync = watcher.sync
PREFIX = Path('validation_sync/neural16384_full_workflow_20261005')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    receipt_path = sync.OUT / 'neural16384_full_workflow_receipt.json'
    assert not receipt_path.exists()
    preflight = sync.read(ROOT / 'analysis/neural16384_full_preflight_20261005/verification.json')
    generator = sync.read(ROOT / 'analysis/neural16384_full_search_generator_preflight_v2_20261005/verification.json')
    assert preflight['status'] == 'passed_actual_matched_instrumentation_and_architecture_controls'
    assert generator['status'] == 'passed'
    for proof in (preflight, generator):
        for source, value in proof['source_sha256'].items():
            assert sha(source) == value, source
    observer = psutil.Process(sync.read(sync.OUT / 'owner.lock')['pid'])
    assert str(ROOT / 'analysis/watch_validations_main_v2_20261005.py') in observer.cmdline()
    parent = observer.parent()
    assert parent is not None and parent.cmdline()[1:] == observer.cmdline()[1:]
    suspended = []
    try:
        for process in (observer, parent):
            process.suspend()
            suspended.append(process)
        assert all(p.pid == observer.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status', '--porcelain')
        head = sync.git('rev-parse', 'HEAD')
        assert sync.git('ls-remote', '--heads', 'origin').splitlines() == [f'{head}\trefs/heads/main']
        sources = set((ROOT / 'analysis').glob('*neural16384*20261005.py'))
        sources.update(ROOT / 'analysis' / f'{prefix}{number}{suffix}.py' for number in (67,68)
            for prefix,suffix in (('optimize_training_round',''),('optimize_training_round','_v2'),
                                  ('finalize_training_round',''),('run_training_round','_v2_pipeline')))
        evidence = set((ROOT / 'analysis').glob('neural16384*20261005.json'))
        for folder in ('neural16384_full_preflight_20261005','neural16384_full_search_generator_preflight_v2_20261005'):
            evidence.update(p for p in (ROOT / 'analysis' / folder).glob('*') if p.is_file())
        paths, bindings = [], {}
        sync.atomic(sync.WORKTREE / PREFIX / '.gitattributes', b'* -text\n')
        paths.append((PREFIX / '.gitattributes').as_posix())
        for source in sorted(sources | evidence):
            data = source.read_bytes()
            assert len(data) < 5 * 1024**2 and not sync.SECRET.search(data)
            relative = source.relative_to(ROOT)
            destination = relative if source in sources else PREFIX / relative
            sync.atomic(sync.WORKTREE / destination, data)
            paths.append(destination.as_posix())
            bindings[str(source)] = hashlib.sha256(data).hexdigest()
        manifest = {'status':'passed_actual_instrumentation_and_complete_generator_controls_only',
            'at_local':sync.now(),'source_sha256':bindings,
            'actual4096_row_matched512_state_loss_and_prediction_bit_identical':True,
            'full16384_parameter_count':168894465,'requested_epochs_each_full_fit':32,
            'planned_actual_annual_fits':5,'planned_actual_final_fit':1,
            'planned_complete_official_records':{'67':64,'68':38},
            'real_generator_controls':generator['controls'],
            'annual_native_future_and_quality_waiters_confirmed_live':True,
            'annual_training_waits_for_fully_qualified66':True,
            'full16384_fits_and_scores_not_yet_completed':True,
            'one_step_training_and_synthetic_ordering_are_not_quality_evidence':True,
            'physical_GPU_total_bytes_from_actual_prior_control':12792037376,
            'torch_allocator_reserved_is_not_physical_resident_VRAM':True,
            'four_prior_actual_widths_and_previous_branch_history_retained':True,
            'global_resource_exhaustion_established':False,'test_labels_read':False}
        sync.atomic(sync.WORKTREE / PREFIX / 'manifest.json',sync.encoded(manifest))
        paths.append((PREFIX / 'manifest.json').as_posix())
        doc=(' # 16384宽度完整训练及完整输出比较\n\n'
            '512宽度实测对照与16384模型除层宽外的配置完全一致：32轮、批量32768、学习率0.001、'
            '权重衰减0.0001、无dropout、种子20261007、提供的排名目标。实际16384网络为168894465参数。\n\n'
            '新增资源记录器在真实过去4096行512宽度一轮控制中逐位保持权重、预处理、损失和预测；'
            '这项检查不计作16384完整训练。实际完整训练等待第66轮完整闭合后，完成五年度向前拟合、'
            '标签边界毒化、保存重载及80日冷前缀检查，再真实拟合成熟最终模型并检查全部1599600条未来X。\n\n'
            '第67轮64条用途融合、第68轮38条独立完整方案，生成器实际遍历了独立方案胜出和未胜出两条分支。'
            '生成器排序值为合成控制值，不是官方分数；真实评分必须先通过完整拟合与原生未来检查。'
            '评分前还需复现真实前轮完整验证向量、官方八指标和未来CSV，最终继续收益映射、官方复核、'
            '因果检查、候选推理、榜单更新与main同步。\n\n'
            '训练期间记录主机内存、进程RSS、外部GPU信息及每次原生拟合实际耗时和CUDA峰值。'
            '物理GPU约11.91GiB；WDDM下PyTorch保留显存可超过物理显存，不能据此声称全部驻留VRAM。'
            '14GiB主机启动条件是调度规则，不代表物理极限；没有用一步控制或缩短训练代替完整32轮。'
            '本流程没有宣告全局方法或资源耗尽，项目数据使用D盘，必要时使用已获授权的E盘。\n')
        sync.atomic(sync.WORKTREE / PREFIX / 'README.md',doc.lstrip().encode('utf-8'))
        paths.append((PREFIX / 'README.md').as_posix())
        for source,value in bindings.items():
            assert sha(source)==value,source
        for offset in range(0,len(paths),50):
            sync.git('add','--',*paths[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())
        assert staged and staged <= set(paths)
        sync.git('commit','-m','核验16384完整训练资源记录并冻结五折、未来及102项方案流程')
        commit=sync.git('rev-parse','HEAD')
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180)
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        receipt={'status':'pushed_verified_only_main','at_local':sync.now(),'commit':commit,
            'files':len(paths),'new_full16384_fits':0,'new_quality_scores':0,
            'url':f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        with receipt_path.open('x',encoding='utf-8') as stream:
            json.dump(receipt,stream,ensure_ascii=False,indent=2)
        print(json.dumps(receipt,ensure_ascii=False),flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():process.resume()


if __name__=='__main__':main()
