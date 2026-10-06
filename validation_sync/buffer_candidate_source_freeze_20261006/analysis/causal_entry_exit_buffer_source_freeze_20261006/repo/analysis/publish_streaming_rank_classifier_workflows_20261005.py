"""Publish actual classifier controls, complete fits, failure history and queued work."""
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
PREFIX=Path('validation_sync/streaming_rank_classifier_workflows_20261005')
OUT=A/'streaming_rank_classifier_workflows_github_20261005'


def main():
    assert not (OUT/'receipt.json').exists()
    proofs=[A/f'{name}/verification.json' for name in (
        'streaming_rank_classification_preflight_v3_20261005',
        'streaming_rank_classifier_direct_router_preflight_20261005',
        'streaming_rank_classifier_search_generator_preflight_v4_20261005',
        'streaming_rank_classifier_execution_source_preflight_v4_20261005',
        'streaming_rank_classifier_quality_followups_v4_20261005',
        'streaming_rank_classifier_monitor_handoff_v14_20261005')]
    for path in proofs:
        record=sync.read(path)
        assert record['status'].startswith('passed')
        for filename,digest in record.get('source_sha256',{}).items():
            assert hashlib.sha256(Path(filename).read_bytes()).hexdigest()==digest,filename
    assert sync.read(proofs[0])['actual_small32epoch_fits']==16
    assert sync.read(proofs[1])['actual_checks']==44
    assert [row['generated_records'] for row in sync.read(proofs[2])['controls']]==[100,98,98]
    bank=A/'streaming_rank_classification_bank_v3_20261005'
    infos=list(bank.glob('*/info_202[0-4].json'))
    assert len(infos)>=6
    fit_records=[json.loads(line) for line in (bank/'actual_native_fit_measurements.jsonl').read_bytes().splitlines()
                 if line.strip() and line.rstrip().endswith(b'}')]
    for path in infos:
        info=sync.read(path)
        assert info['status']=='passed' and info['completed_epochs']==32 and info['model_reload_bit_identical']
        matches=[row for row in fit_records if row['model']==info['model'] and row['year']==info['year']]
        assert len(matches)==1 and matches[0]['actual_rows_in_each_epoch']==[info['training_meta']['rows']]*32
        prefix=sync.read(bank/f'prefix_control_{info["model"]}_{info["year"]}.json')
        assert prefix['status']=='passed' and prefix['actual_saved_model_full_reload_and_cold80_day_prefix_bit_identical']
        assert sync.sha((path.parent/f'model_{info["year"]}.joblib').read_bytes())==info['model_sha256']
        assert sync.sha((path.parent/f'raw_{info["year"]}.parquet').read_bytes())==info['prediction_sha256']
    quality=sync.read(proofs[4])['quality_rounds']
    for job in quality:
        worker=psutil.Process(job['owned_worker_pid'])
        assert worker.cmdline()[-2:]==job['script_args'] and not Path(job['stderr']).read_bytes()
    native=sync.read(A/'streaming_rank_classifier_followups_v3_20261005/verification.json')
    for role in ('native','future'):
        job=native[role]
        worker=psutil.Process(job['owned_worker_pid'])
        assert worker.create_time()==job['owned_worker_creation_time'] and job['script'] in worker.cmdline()
        assert not Path(job['stderr']).read_bytes()
    publisher_launch=sync.read(sync.OUT/'launch_v3.json')['publisher']
    publisher_pair=owned_pair(publisher_launch['pid'],Path(publisher_launch['script']),publisher_launch['script_args'])
    assert publisher_pair[1].pid==sync.read(sync.OUT/'owner.lock')['pid']
    monitor_launch=sync.read(A/'actual_optimization_monitor_launch_v14_20261005.json')
    monitor_pair=owned_pair(monitor_launch['pid'],Path(monitor_launch['script']),monitor_launch['script_args'])
    pairs=(publisher_pair,monitor_pair)
    suspended=[]
    try:
        for attempt in range(12):
            for parent,child in pairs:
                for process in (child,parent):process.suspend();suspended.append(process)
            busy=[p for parent,child in pairs for p in parent.children(recursive=True)
                  if p.pid!=child.pid and p.name().lower()!='conhost.exe']
            if not busy:break
            for process in reversed(suspended):process.resume()
            suspended.clear();time.sleep(1)
        else:raise RuntimeError('Publisher owns an active command.')
        previous=sync.git('rev-parse','HEAD')
        old_heads=verify_main(previous)
        assert not sync.git('status','--porcelain')
        selected=names('ls-files','--modified')|names('ls-files','--others','--exclude-standard')
        tracked=names('ls-files')
        for folder in ('analysis','experiments','src','tests','config'):
            selected.update(p.relative_to(ROOT).as_posix() for p in (ROOT/folder).rglob('*.py')
                if '__pycache__' not in p.parts and p.relative_to(ROOT).as_posix() not in tracked)
        evidence=set()
        for folder in A.glob('streaming_rank_class*20261005'):
            if not folder.is_dir():continue
            evidence.update(p for p in folder.rglob('*.json') if p.is_file())
        # Capture only the complete append-only fit record prefix, excluding live
        # process samples and mutable stdout from the immutable evidence package.
        fit_snapshot=OUT/'actual_native_fit_records_at_publication.json'
        sync.atomic(fit_snapshot,sync.encoded({'at_local':sync.now(),'records':fit_records,
            'qualified_saved_annual_info_files':[str(path) for path in infos],
            'qualified_saved_annual_fits':len(infos),'full_training_execution_scope_still_pending':True,
            'new_quality_scores':0,'test_labels_read':False}))
        evidence.add(fit_snapshot)
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
            captures[relative.as_posix()]={'published_path':destination.as_posix(),
                'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),
                'runtime_snapshot':source not in evidence and source.suffix=='.json' and (
                    'state' in source.stem or 'resume' in source.stem or source.stem.startswith((
                        'optimization_boundary','optimization_fit_cost','next_experiment')))}
        targets[(PREFIX/'.gitattributes').as_posix()]=b'* -text\n'
        targets[(PREFIX/'manifest.json').as_posix()]=sync.encoded({
            'status':'actual_complete_classifier_controls_and_native_progress_captured_for_main',
            'at_local':sync.now(),'previous_main':previous,'files':captures,
            'original_failed_centered_rank_assumption_and_readonly_full_attempt_retained':True,
            'actual_full1694259_readonly_key_regression_passed':True,'small32pass_control_fits_passed':16,
            'actual_direct_and_inherited_route_controls':44,'qualified_saved_full_annual_fits_at_capture':len(infos),
            'required_full_annual_fits':20,'required_full_final_fits':4,'planned_full_official_records':198,
            'actual_quality_rounds79_80_owned_live':True,'actual_complete_final_and_native_scope_still_pending':True,
            'actual187_declared_configurations_in_monitor_preflight':True,
            'raw_data_and_models_and_predictions_remain_local_D_or_E':True,
            'only_publication_branch':'main','historical_branch_heads_retained':old_heads,
            'all_validation_years_reused_selection_bias_uncorrected':True,
            'new_quality_scores':0,'test_labels_read':False,'global_resource_exhaustion_established':False})
        targets[(PREFIX/'README.md').as_posix()]=(
            '# 流式成熟排序分类完整验证与实际进度\n\n'
            '新增二分类前10%及十分位多分类，各比较两个L2强度，使用相同63特征、成熟训练行和32次完整训练遍历。'
            '阈值及预处理仅从成熟过去拟合，分类分数须通过成熟过去收益率映射并纳入最终官方评分。\n\n'
            f'本次已核验{len(infos)}次真实完整年度训练、保存模型重载和冷80日372,000行前缀。'
            '全部20次年度训练及4个最终模型仍未完成。16次小样本32轮控制、169万行只读键回归、'
            '44条原生与继承推理路线、真实驱动入口和候选源码打包检查通过。原始失败和所有旧版源码保留。\n\n'
            '第79轮100个、第80轮98个完整方案及两种主模型胜负分支的实际生成检查通过。'
            '这些检查采用明确标记的合成排序值；198条官方评分仍须等待完整原生验证和前序78/79轮资格。'
            '真实入口已启动，后续执行连续验证、校准、因果检查、全量候选推理与完整榜更新。\n\n'
            '运行台账新增四种配置，仅统计真实完成的年度模型，不计小样本或失败尝试。'
            '全部历史及本轮代码与证据提交main，原始数据、模型与预测继续存D/E盘。'
            '没有读取测试答案，也没有证明全局优化或物理资源已经耗尽。\n').encode('utf-8')
        for name,record in captures.items():
            if not record['runtime_snapshot']:
                assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==record['sha256'],name
        for name,data in targets.items():sync.atomic(sync.WORKTREE/name,data)
        paths=sorted(targets)
        for offset in range(0,len(paths),50):sync.git('add','-f','--',*paths[offset:offset+50])
        staged=set(sync.git('-c','core.quotepath=false','diff','--cached','--name-only').splitlines())
        assert staged and staged<=set(paths)
        sync.git('-c','maintenance.auto=false','-c','gc.auto=0','commit','-m',
            '新增完整流式排序分类与198方案验证流程，保留失败并核验真实年度训练和候选源码',timeout=180)
        commit=sync.git('rev-parse','HEAD')
        expected={name:hashlib.sha256(data).hexdigest() for name,data in targets.items()}
        assert blob_hashes(commit,expected)==expected
        sync.git('push','origin','HEAD:refs/heads/main',timeout=180)
        verify_main(commit)
        watcher.advance_source_index(commit)
        receipt={'status':'pushed_verified_actual_classifier_training_controls_and_complete_workflows_main_only',
            'at_local':sync.now(),'commit':commit,'files':len(targets),'verified_raw_git_blob_sha256':len(expected),
            'qualified_saved_full_classifier_annual_fits_at_capture':len(infos),'new_quality_scores':0,
            'url':f'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/{PREFIX.as_posix()}'}
        sync.atomic(OUT/'receipt.json',sync.encoded(receipt))
        print(json.dumps(receipt,ensure_ascii=False),flush=True)
    finally:
        for process in reversed(suspended):
            if process.is_running():process.resume()


if __name__=='__main__':main()
