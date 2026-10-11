"""Publish immutable attachment or terminal resource evidence on main, without controlling science."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from hidden_windows_child_creation_20261006 import install
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    p = A / 'service_owned_workflows_20261006' / name
    while not (p / 'native_launch.json').exists() or owned(read(p / 'native_launch.json')):
        time.sleep(15)
    assert read(p / 'service_execution.json')['status'] == 'passed', name
    return p


def terminal_service(name):
    p = A / 'service_owned_workflows_20261006' / name
    while not (p / 'native_launch.json').exists() or owned(read(p / 'native_launch.json')):
        time.sleep(15)
    assert (p / 'service_execution.json').exists(), name
    return p


def main():
    phase = sys.argv[1]
    assert phase in ('attach', 'HGB', 'ElasticNet')
    kinds = ('HGB', 'ElasticNet') if phase == 'attach' else (phase,)
    if phase == 'attach':
        closed('local_cpu_validation_recovery_chain_main_publication_v1')
    sources = [Path(__file__), A / 'observe_CPU_full_bank_resources_v4_20261007.py', A / 'prepare_ElasticNet_resource_publication_v5_20261007.py', *list((A / 'service_owned_workflows_20261006/CPU_full_bank_resource_observer_ElasticNet_main_publication_v3').glob('*.json')), *list((A / 'service_owned_workflows_20261006/CPU_full_bank_resource_observer_ElasticNet_main_publication_v3').glob('*.log'))]
    proofs = {}
    for kind in kinds:
        folder = A / f'CPU_{kind}_full_bank_resource_observation_v3_20261007'
        observer_name = f'CPU_{kind}_full_bank_resource_observer_' + ('v3' if kind == 'ElasticNet' else 'v2')
        bank_name = f'cpu_full_universe_{kind}_native_bank24_' + ('v3' if kind == 'ElasticNet' else 'v2')
        if phase == 'attach':
            path = folder / 'actual_two_live_samples_attach_verification.json'
            while not path.exists():
                assert owned(read(A / 'service_owned_workflows_20261006' / observer_name / 'native_launch.json'))
                time.sleep(5)
            proof = read(path)
            assert proof['status'] == 'passed_actual_two_birth_verified_live_read_only_Windows_resource_samples'
            sources += [path, folder / 'frozen_before_read_only_observation.json']
        else:
            terminal_service(observer_name)
            terminal_service(f'cpu_full_universe_{kind}24_bank_evidence_publication' + ('_v4' if kind == 'ElasticNet' else '_v2'))
            terminal_service('CPU_FULL_HGB44_round113_full_registration_v4' if kind == 'HGB' else 'CPU_ELASTIC44_round114_full_registration_v3')
            path = folder / 'verification.json'
            proof = read(path)
            assert proof['status'] == 'completed_actual_read_only_resource_observation_of_closed_CPU_bank'
            assert proof['actual_terminal'] == read(A / 'service_owned_workflows_20261006' / bank_name / 'service_execution.json')
            assert sha(folder / 'samples.jsonl') == proof['samples_jsonl_sha256']
            sources += [*folder.glob('*.json'), folder / 'samples.jsonl']
        assert proof['new_quality_scores'] == 0 and proof['test_labels_read'] is False
        proofs[kind] = proof
        sources += [Path(p) for p in proof['input_sha256']]
        for name in (observer_name, bank_name):
            service = A / 'service_owned_workflows_20261006' / name
            sources += [service / n for n in ('job_definition.json', 'native_launch.json')]
            if phase != 'attach':
                sources += [service / 'service_execution.json']
    out = A / f'CPU_full_bank_resource_observer_{phase}_v4_github_20261007'
    assert not out.exists()
    out.mkdir()
    pins = {str(p): sha(p) for p in sources}
    create(out / 'frozen_before_main_publication.json', {'input_sha256': pins, 'test_labels_read': False})
    from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
    held, retries = [], []
    restore = install()
    sync = helpers.sync
    old_git = sync.git

    def retry_git(*args, **kwargs):
        for attempt in range(3):
            try:
                return old_git(*args, **kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote', 'push', 'fetch') or not any(t in str(error).lower() for t in ('tls', 'ssl', 'connection', 'timed out', 'unable to access')):
                    raise
                retries.append({'command': args[0], 'attempt': attempt + 1, 'error': str(error)[:1000]})
                if attempt == 2:
                    raise
                time.sleep(2)

    sync.git = retry_git
    try:
        row = read(A / 'service_owned_workflows_20261006/main_publisher_v7/native_launch.json')
        parent, worker, idle = suspended_idle(row, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        with LockedReadHashCache(pins) as scope:
            prefix = Path(f'validation_sync/CPU_full_bank_resource_observer_{phase}_v4_20261007')
            payload = {(prefix / '.gitattributes').as_posix(): b'* -text\n'}
            files = {}
            for p in dict.fromkeys([*sources, out / 'frozen_before_main_publication.json']):
                data = p.read_bytes()
                assert not sync.SECRET.search(data), p
                raw_sha = hashlib.sha256(data).hexdigest()
                target = (prefix / p.relative_to(ROOT)).as_posix()
                if len(data) >= 5 * 1024**2:
                    data = gzip.compress(data, mtime=0)
                    assert hashlib.sha256(gzip.decompress(data)).hexdigest() == raw_sha
                    target += '.gz'
                payload[target] = data
                files[p.relative_to(ROOT).as_posix()] = {'published_path': target, 'original_sha256': raw_sha, 'published_sha256': hashlib.sha256(data).hexdigest()}
            previous = sync.git('rev-parse', 'HEAD')
            helpers.verify_main(previous)
            assert not sync.git('status', '--porcelain')
            manifest = {'status': 'published_actual_read_only_CPU_bank_resource_observer_evidence',
                'at_local': sync.now(), 'phase': phase, 'files': files, 'previous_main': previous,
                'only_branch': 'main', 'observed_banks': list(kinds),
                'actual_evidence_status': {k: v['status'] for k, v in proofs.items()},
                'new_native_fits_by_observer': 0, 'new_official_scores': 0,
                'scientific_workers_stopped_suspended_or_restarted': 0,
                'not_a_full_bank_scientific_validation_or_global_boundary_claim': True,
                'no_data_prediction_arrays_or_model_weights_uploaded': True,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 本机全股票池CPU训练的只读资源记录\n\n'
                '强身份核验原生训练进程，每5秒读取Windows工作集、私有内存、进程生命周期内存峰值、CPU时间及系统可用内存。'
                '按最后报告的阶段元数据归组采样峰值；阶段名可能尚未更新，数值不能单独归因于该次拟合；阶段采样最大值是下界，不能当作连续监测的真实峰值。'
                '初始等待和阶段名尚未写出的预处理也在采样范围内。\n\n'
                'attach记录仅证明两次真实存活采样及原代码、参数与进程身份未改变，不代表24个模型训练完成。'
                '最终记录保留训练原始成功或失败状态，资源观察完成不代表科学验证通过。'
                '没有暂停、终止、重启训练，没有读取训练数据或测试答案，没有新增模型或质量分数。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', f'记录本机CPU训练只读资源采样 {phase}', timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
            assert helpers.blob_hashes(commit, hashes) == hashes
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'commit': commit, 'at_local': sync.now(),
                'branch': 'main', 'raw_git_blobs_verified': len(hashes), 'new_quality_scores': 0,
                'all_source_inputs_initial_and_final_read_locked_full_rehash': True,
                'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
            print(json.dumps(read(out / 'receipt.json'), ensure_ascii=False), flush=True)
    finally:
        sync.git = old_git
        for p in reversed(held):
            if p.is_running():
                p.resume()
        create(out / 'actual_hidden_publication_children.json', {'events': restore()})
        create(out / 'transport_retries.json', {'attempts': retries, 'TLS_verification_unchanged': True})


if __name__ == '__main__':
    main()
