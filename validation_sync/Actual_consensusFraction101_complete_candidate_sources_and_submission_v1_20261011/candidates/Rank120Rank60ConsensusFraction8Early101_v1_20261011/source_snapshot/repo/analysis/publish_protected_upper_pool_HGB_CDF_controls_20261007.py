"""Publish measured local acceleration and strict unfinished-grid repair evidence on main."""
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


def main():
    closed('protected_upper_pool_HGB_CDF_full_preflight')
    closed('cpu_full_universe_HGB24_bank_evidence_publication_v2')
    proof = read(A / 'protected_upper_pool_HGB_CDF_preflight_20261007/verification.json')
    assert proof['status'] == 'passed_actual63_full5635800_lower_pool_CDF_independent_oracle_and_cold80_260_975_controls'
    assert len(proof['controls']) == 63 and proof['new_official_quality_scores'] == 0
    out = A / 'protected_upper_pool_HGB_CDF_controls_github_20261007'
    assert not out.exists()
    out.mkdir()
    sources = [Path(__file__), A / 'protected_upper_pool_HGB_CDF_transform_20261007.py',
        A / 'verify_protected_upper_pool_HGB_CDF_20261007.py',
        A / 'protected_upper_pool_HGB_CDF_plan_20261007.json',
        A / 'protected_upper_pool_HGB_CDF_definition_preflight_20261007.json',
        A / 'protected_upper_pool_HGB66_scoring_admission_20261007.json',
        A / 'run_protected_upper_pool_HGB66_official_comparison_20261007.py',
        A / 'cpu_full_universe_HGB24_bank_recovery_v2_github_20261007/receipt.json']
    sources += list((A / 'protected_upper_pool_HGB_CDF_preflight_20261007').glob('*.json'))
    for name in ('protected_upper_pool_HGB_CDF_full_preflight',):
        service = A / 'service_owned_workflows_20261006' / name
        sources += list(service.glob('*.json')) + list(service.glob('*.log'))
    service = A / 'service_owned_workflows_20261006/protected_upper_pool_HGB66_official_comparison'
    sources += [service / 'job_definition.json', service / 'native_launch.json', service / 'verified_hidden_launch.json']
    pins = {**proof['input_sha256'], **{str(p): sha(p) for p in sources}}
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
            prefix = Path('validation_sync/protected_upper_pool_HGB_CDF_controls_20261007')
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
            manifest = {'status': 'published_actual63_full_historical_lower_pool_CDF_controls_and66_score_admission',
                'at_local': sync.now(), 'files': files, 'previous_main': previous, 'only_branch': 'main',
                'actual_full5635800_historical_controls': len(proof['controls']),
                'actual_cold_prefix_day_counts': [80, 260, 975], 'existing_native_bank_fits': 24,
                'declared_future_official_records': 66, 'declared_new_postprocessing_configurations': 63,
                'new_native_fits': 0, 'new_official_scores': 0,
                'new_score_or_future_candidate_or_round115_full_QA_not_claimed': True,
                'scientific_workers_stopped_suspended_or_restarted': 0,
                'official_Top_with_missing_labels_invariance_not_assumed_or_required_as_selection_gate': True,
                'no_data_prediction_arrays_or_model_weights_uploaded': True,
                'exact_idle_main_before_and_after_hold': idle, 'test_labels_read': False}
            payload[(prefix / 'manifest.json').as_posix()] = sync.encoded(manifest)
            payload[(prefix / 'README.md').as_posix()] = (
                '# 保留高分区的HGB低分区重排控制\n\n'
                '使用当日非涨停、价格有效且原预测可用股票池，严格选取低于50%、70%、80%分界值的样本。'
                '分界并列组整体保留；更高分区、涨停股和无效原预测逐位不变。'
                '对四个完整HGB预测头及三个固定均值组合，分别在选中子池内取平均排名百分位，'
                '按0.25、0.5、1权重与父预测百分位混合，再映回子池原预测的同日CDF范围。\n\n'
                '63个预定方案已实际检查全部5635800训练验证行：独立Pandas排名与CDF实现逐位一致，'
                '每项80、260、975交易日前缀从头重建一致；权重0恒等、边界并列、NaN、负零、涨停和无效样本控制通过。'
                '标签没有参与低分区定义或输出变换。官方Top还过滤真实标签缺失，因此不能从保护高分区推断所有未来Top必定不变。\n\n'
                '66项官方比较包含63方案和112、113、114三个合格基准；等114完成完整QA25与main后再评分，'
                '选择截至该时点112至114中官方完整总分最高的父方案，分数完全相同取最早者。'
                '只按官方总分选模，不要求Top、换手、最差年度或显著性单独改善。'
                '本记录0新拟合、0质量评分，尚未证明新方案胜出、候选1599600推理或115完整榜资格。\n').encode('utf-8')
            scope.reverify()
            for name, data in payload.items():
                sync.atomic(sync.WORKTREE / name, data)
            names = sorted(payload)
            for offset in range(0, len(names), 50):
                sync.git('add', '-f', '--', *names[offset:offset+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) <= set(payload)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '验证63种低分区HGB重排的563万行位值及冷前缀并登记66项后续评分', timeout=180)
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
