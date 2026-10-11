"""Publish all verified complete-workflow sources and honest pending fit counts on main."""
from pathlib import Path
import hashlib
import json
import sys
import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path.insert(0,str(A))
import watch_validations_main_v2_20261005 as watcher
from publish_main_closeout_v2_20261005 import names,blob_hashes

sync=watcher.sync
PREFIX=Path('validation_sync/memory_efficient_neural_workflows_20261005')
OUT=A/'memory_efficient_neural_workflows_github_20261005'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    assert not (OUT/'receipt.json').exists()
    folders=('memory_efficient_neural_direct_router_preflight_20261005',
        'memory_efficient_neural_search_generator_preflight_20261005',
        'memory_efficient_neural_workflow_preflight_20261005',
        'memory_efficient_neural_followups_20261005',
        'memory_efficient_neural_observer_handoff_v13_20261005')
    for folder in folders:
        proof=sync.read(A/folder/'verification.json')
        assert proof['status'].startswith('passed')
        for source,expected in proof.get('source_sha256',{}).items():
            assert sha(source)==expected,source
    followup=sync.read(A/'memory_efficient_neural_followups_20261005/verification.json')
    monitoring=sync.read(A/'memory_efficient_neural_observer_handoff_v13_20261005/verification.json')
    for job in (followup['native'],followup['future'],*followup['quality_rounds'],monitoring['monitor']):
        process=psutil.Process(job['pid'])
        assert job['script'] in process.cmdline()
        if job['script_args']:assert process.cmdline()[-len(job['script_args']):]==job['script_args']
        assert not Path(job['stderr']).read_text(encoding='utf-8')
    observer=psutil.Process(sync.read(sync.OUT/'owner.lock')['pid'])
    parent=observer.parent()
    assert str(A/'watch_validations_main_v3_20261005.py') in parent.cmdline()
    paused=[]
    try:
        for process in (observer,parent):
            process.suspend();paused.append(process)
        assert all(p.pid==observer.pid or p.name().lower()=='conhost.exe' for p in parent.children(recursive=True))
        assert not sync.git('status','--porcelain')
        head=sync.git('rev-parse','HEAD')
        assert sync.git('branch','--show-current',cwd=ROOT)=='main'
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{head}\trefs/heads/main']
        selected={ROOT/name for name in names('ls-files','--modified')|names('ls-files','--others','--exclude-standard')}
        selected.add(Path(__file__))
        evidence=set()
        for folder in folders:
            evidence.update((A/folder).glob('*.json'))
        evidence.add(A/'memory_efficient_mlp_controls_github_20261005/receipt.json')
        selected|=evidence
        captures,targets={},{}
        for source in sorted(selected):
            assert source.is_file() and source.suffix in ('.py','.json'),source
            data=source.read_bytes()
            assert len(data)<5*1024**2 and not sync.SECRET.search(data),source
            if source.suffix=='.json':json.loads(data.decode('utf-8-sig'))
            relative=source.relative_to(ROOT)
            destination=PREFIX/relative if source in evidence else relative
            name=destination.as_posix()
            targets[name]=data
            captures[relative.as_posix()]={'published_path':name,'sha256':hashlib.sha256(data).hexdigest(),
                'bytes':len(data),'runtime_snapshot':source not in evidence and source.suffix=='.json' and (
                    'state' in source.stem or 'resume' in source.stem or 'optimization_boundary' in source.stem
                    or 'cost_evidence' in source.stem or 'directions' in source.stem)}
        cost=sync.read(A/'optimization_fit_cost_evidence_20261004.json')
        assert cost['configurations']==183 and cost['memory_efficient_neural_actual_annual_fits']==0
        manifest={'status':'verified_complete_memory_layout_native_final_and_official_workflows_published',
            'at_local':sync.now(),'files':captures,'actual_direct_and_restored_codec_cases':40,
            'actual_search_generator_records_in_three_branches':[88,78,78],
            'planned_new_complete_annual_fits':15,'planned_new_complete_final_fits':3,
            'planned_new_official_records':{'77':88,'78':78},
            'actual_new_complete_annual_fits':0,'actual_new_complete_final_fits':0,'new_quality_scores':0,
            'actual_declared_configurations':183,'actual_completed_annual_fits':cost['total_actual_new_annual_fits'],
            'native_weight_and_scratch_drive':'E:','original168894465_parameters32epochs32768_effective_batch_preserved':True,
            'all_old_native_and_quality_jobs_preserved':True,'observer_actual_cost_and_E_inventory_verified_through78':True,
            'latest_qualified_round':66,'qualified_ranking_records':9822,'only_publication_branch':'main',
            'test_labels_read':False,'global_resource_exhaustion_established':False}
        targets[(PREFIX/'manifest.json').as_posix()]=sync.encoded(manifest)
        targets[(PREFIX/'README.md').as_posix()]=(
            '# 三种内存实现的完整训练与官方验证流程\n\n'
            '梯度累积、激活重算及组合方式均保留16384/8192/4096宽度、168,894,465个参数、32轮训练、有效批32768、'
            'seed20261007、原始63特征、成熟标签窗口及AdamW更新次数。逐年模型的实际输入矩阵、目标和键须与原512控制完全一致。\n\n'
            '实际40个模型的直接分发、完整codec和前缀检查已通过：4个CPU MLP控制模型、6个GOSS试验模型、30个既有完整模型。'
            '三种新实现的15次完整年度训练和3次最终训练已冻结并启动等待入口；单步和小样本检查不计作完整拟合。'
            '最终模型要求全量1,599,600条未来X推理、实际重载、原生131条及冷80日检查。\n\n'
            '第77轮37+8+18+25共88条、78轮19+42+17共78条方案网格，通过实际生成器及两种独立模型胜负分支检查。'
            '生成器中的排序值是合成控制，不是官方分数。实际评分入口等待76/77轮完整资格和全部新原生模型检查。'
            '集成角色、独立完整输出、后处理、成熟收益率校准、因果检查、候选冻结及完整榜更新均保留。'
            '实际报告入口与最终化模块的轮次和闭包已检查。\n\n'
            'D盘观察余量44,547,244,032字节，按未压缩参数副本、8GiB临时空间和20GiB预留估算需46,954,217,572字节，'
            '因此新完整模型及临时文件安排到E盘。该预留是调度规则，不是物理极限证明。'
            '完整训练等待真实GPU对照和GOSS年度/最终进程结束，原大模型及其他验证继续运行。\n\n'
            '监控扩展至78轮并实际核验E盘库存及新旧成本生产顺序。账本为183个已声明配置、697次已完成年度拟合；'
            '新内存实现的完整年度拟合数为0。第66轮仍是最新合格验证，完整榜9822条，最高分0.4510081068915626。'
            '本次没有新增官方评分或读取测试标签；所有验证年重复选模偏差未校正。\n').encode('utf-8')
        for source,item in captures.items():
            if not item['runtime_snapshot']:assert sha(ROOT/source)==item['sha256'],source
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        paths=sorted(targets)
        for offset in range(0,len(paths),50):sync.git('add','-f','--',*paths[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())
        assert staged and staged<=set(paths)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m',
            '冻结三种内存实现15年度3最终拟合及第77至78轮166项验证',timeout=180)
        commit=sync.git('rev-parse','HEAD')
        expected={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
        assert blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180)
        assert sync.git('ls-remote','--heads','origin').splitlines()==[f'{commit}\trefs/heads/main']
        watcher.advance_source_index(commit)
        receipt={'status':'pushed_only_main_verified_raw_complete_workflow_sources',
            'commit':commit,'at_local':sync.now(),'files':len(targets),
            'url':f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}',
            'actual_new_complete_annual_fits':0,'new_quality_scores':0}
        sync.atomic(OUT/'receipt.json',sync.encoded(receipt))
        print(json.dumps(receipt,ensure_ascii=False),flush=True)
    finally:
        for process in reversed(paused):
            if process.is_running():process.resume()


if __name__=='__main__':
    main()
