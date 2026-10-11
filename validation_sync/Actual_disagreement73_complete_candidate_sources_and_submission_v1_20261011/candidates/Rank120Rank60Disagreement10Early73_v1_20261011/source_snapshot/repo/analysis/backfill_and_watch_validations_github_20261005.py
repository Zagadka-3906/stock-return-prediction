"""Backfill all recorded validation evidence, then publish each newly qualified round."""
from pathlib import Path
import gzip
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import sync_validated_rounds_github_20261005 as sync

DELEGATE_SOURCE = Path(sync.__file__)
sync.__file__ = str(Path(__file__))
OUT = sync.OUT
WORKTREE = sync.WORKTREE
PREFIX = Path('validation_sync/history')
FIRST = 1
LAST = 60
# User requested historical backfill at this recorded point; later work is published on completion.
CUTOFF = time.mktime(time.strptime('2026-10-05T04:32:35', '%Y-%m-%dT%H:%M:%S'))
FOLDERS = ('analysis', 'experiments', 'results', 'validation', 'candidates', 'releases', 'deliveries', 'maintenance')
EXTENSIONS = {'.json', '.md', '.png', '.html'}
MUTABLE_NAMES = {'actual_optimization_monitor_state_20261005.json', 'ongoing_optimization_state.json',
                 'ongoing_optimization_state.md', 'optimization_boundary_evidence_20261004.json',
                 'training_cost_accounting_20261003.json', 'next_experiment_directions_20261003.json',
                 'nystrom_ridge_search_execution_20261004.json'}


def file_sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def name(number):
    return 'optimization_20261003' if number == 1 else f'optimization_20261003_r{number}'


def inventory():
    files = {}
    excluded_live = []
    for folder in FOLDERS:
        for base, directories, filenames in os.walk(ROOT / folder):
            directories[:] = [item for item in directories if item not in {'__pycache__', 'github_validation_sync_20261005', 'run_logs'}]
            for filename in filenames:
                source = Path(base) / filename
                relative = source.relative_to(ROOT).as_posix()
                size = source.stat().st_size
                if source.suffix.lower() not in EXTENSIONS and not (source.suffix.lower() == '.csv' and size <= 2 * 1024**2):
                    continue
                if filename in MUTABLE_NAMES or source.stat().st_mtime > CUTOFF:
                    excluded_live.append(relative)
                    continue
                # Exclude unfinished current rounds even if they contain an older prepared protocol.
                parts = source.relative_to(ROOT).parts
                if any(part.startswith('optimization_20261003_r') and part.rsplit('_r', 1)[-1].isdigit()
                       and int(part.rsplit('_r', 1)[-1]) > LAST for part in parts):
                    excluded_live.append(relative)
                    continue
                files[relative] = source
    board = sync.read(ROOT / 'results/all_model_rankings_20261003.json')
    for entry in board['source_manifest']:
        source = Path(entry['path'])
        if not source.is_absolute():
            source = ROOT / source
        if not source.is_relative_to(ROOT) and source.suffix.lower() in EXTENSIONS:
            assert source.exists() and file_sha(source) == entry['sha256']
            key = 'external_archived_sources/' + source.parent.parent.name + '/' + source.name
            assert key not in files
            files[key] = source
    return files, excluded_live


class HashReader:
    def __init__(self, stream):
        self.stream = stream
        self.digest = hashlib.sha256()

    def read(self, size=-1):
        data = self.stream.read(size)
        self.digest.update(data)
        return data


def create_archives(files):
    groups = []
    group = []
    total = 0
    for relative, source in sorted(files.items()):
        size = source.stat().st_size
        if group and total + size > 128 * 1024**2:
            groups.append(group)
            group, total = [], 0
        group.append((relative, source))
        total += size
    if group:
        groups.append(group)
    members, archives = [], []
    for count, entries in enumerate(groups, 1):
        relative_archive = (PREFIX / f'evidence_part{count:03}.tar.gz').as_posix()
        destination = WORKTREE / relative_archive
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix('.building')
        with temporary.open('wb') as raw, gzip.GzipFile(fileobj=raw, mode='wb', compresslevel=3, mtime=0, filename='') as compressed:
            with tarfile.open(fileobj=compressed, mode='w|', format=tarfile.PAX_FORMAT) as archive:
                for relative, source in entries:
                    before = source.stat()
                    info = tarfile.TarInfo(relative)
                    info.size = before.st_size
                    info.mode = 0o644
                    info.mtime = 0
                    with source.open('rb') as stream:
                        reader = HashReader(stream)
                        archive.addfile(info, reader)
                        digest = reader.digest.hexdigest()
                    assert source.stat().st_size == before.st_size
                    assert file_sha(source) == digest, f'Historical source changed during export: {relative}'
                    members.append({'source': relative, 'original_absolute_source': str(source),
                                    'bytes': info.size, 'sha256': digest,
                                    'archive': relative_archive, 'member': relative})
        assert temporary.stat().st_size < 80 * 1024**2, 'Archive exceeds the configured Git file limit'
        os.replace(temporary, destination)
        # Read the actual compressed bytes back, verify every member and its original digest.
        expected = {row['member']: row for row in members if row['archive'] == relative_archive}
        with tarfile.open(destination, mode='r|gz') as archive:
            checked = set()
            for info in archive:
                stream = archive.extractfile(info)
                digest = hashlib.sha256()
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(block)
                assert info.name in expected and info.size == expected[info.name]['bytes']
                assert digest.hexdigest() == expected[info.name]['sha256']
                checked.add(info.name)
            assert checked == set(expected)
        archives.append({'path': relative_archive, 'bytes': destination.stat().st_size,
                         'sha256': file_sha(destination), 'members': len(entries)})
        print(json.dumps({'stage': 'historical_archive_verified', 'part': count,
                          'parts': len(groups), 'members': len(entries), 'bytes': destination.stat().st_size}), flush=True)
        sync.atomic(OUT / 'state.json', sync.encoded({'status': 'backfilling_historical_validations',
                    'pid': os.getpid(), 'at_local': sync.now(), 'verified_parts': count,
                    'parts': len(groups), 'archived_members_so_far': len(members)}))
    return members, archives


def round_payloads(members):
    indexed = {row['source']: row for row in members}
    paths, rounds = [], []
    for number in range(FIRST, LAST + 1):
        stem = name(number)
        result_path = ROOT / f'results/{stem}.json'
        selection_path = ROOT / f'analysis/{stem}/selection.json'
        result, selected = sync.read(result_path), sync.read(selection_path)
        assert result['status'] == 'complete'
        assert result['winner']['metrics'] == selected['winner']['metrics']
        evidence = sync.complete_round_evidence(number) if number > 1 else None
        # Older result schemas did not expose all newer gates. Preserve their scope as recorded.
        qualification = 'complete_declared_round' if evidence else 'legacy_published_complete_validation'
        metrics = result['winner']['metrics']
        relative = Path('validation_sync') / f'round{number}'
        paths_for_round = []
        if number != 60:
            documents = {
                relative / 'result.json': result_path.read_bytes(),
                relative / 'selected_scheme.json': sync.encoded({key: value for key, value in selected.items() if key != 'ranking'}),
            }
            rows = [{'rank': rank, 'wave': record.get('wave'), 'arm': record.get('arm'),
                     **record['metrics'], 'configuration_sha256': sync.sha(sync.encoded(record))}
                    for rank, record in enumerate(selected['ranking'], 1)]
            documents[relative / 'ranking_round.csv'] = sync.csv_bytes(rows, ['rank', 'wave', 'arm', *sync.METRICS, 'configuration_sha256'])
            documents[relative / 'README.md'] = (
                f'# 第 {number} 轮历史验证\n\n'
                f"官方连接验证分：**{metrics['final_score']:.12f}**。原始发布状态：`{result['status']}`；"
                f'本次归档口径：`{qualification}`。\n\n'
                '方案参数与本轮排名见同目录 JSON/CSV。完整原始协议、评分缓存、因果检查、候选核验及恢复记录'
                '保存在 [历史证据归档](../history/README.md)，文件索引列明对应压缩分片、成员路径与 SHA256。\n\n'
                '归档保持当时证据原样，没有重跑评分，也没有将较早轮次补写为后期检查标准。\n').encode('utf-8')
            for destination, data in documents.items():
                sync.atomic(WORKTREE / destination, data)
                paths_for_round.append(destination.as_posix())
                paths.append(destination.as_posix())
        evidence_sources = [row for row in members if row['source'].startswith(f'analysis/{stem}/') or row['source'].startswith(f'candidates/{stem}/') or row['source'] == f'results/{stem}.json' or row['source'] == f'results/optimization_ranking_20261003{"" if number == 1 else "_r" + str(number)}.json']
        assert f'results/{stem}.json' in indexed and f'analysis/{stem}/selection.json' in indexed
        metadata = {'round': number, 'recorded_status': result['status'], 'archival_qualification': qualification,
                    'metrics': metrics, 'scored_configurations_in_selection': len(selected['ranking']),
                    'score_gain': result.get('score_gain'), 'scientific_complete_evidence': evidence,
                    'source_files': evidence_sources, 'new_model_fits_this_upload': 0,
                    'new_quality_scores_this_upload': 0, 'new_test_label_reads_this_upload': 0}
        target = relative / 'history_manifest.json'
        sync.atomic(WORKTREE / target, sync.encoded(metadata))
        paths.append(target.as_posix())
        rowsummary = {'round': number, 'qualification': qualification, 'score': metrics['final_score'],
                      'selected_configurations': len(selected['ranking']), 'evidence_files': len(evidence_sources),
                      'directory': relative.as_posix()}
        rounds.append(rowsummary)
        print(json.dumps({'stage': 'historical_round_preserved', **rowsummary}, ensure_ascii=False), flush=True)
    return paths, rounds


def backfill():
    receipt = OUT / 'history_receipt.json'
    if receipt.exists() and sync.read(receipt)['status'] == 'pushed_and_remote_head_verified':
        return sync.read(receipt)
    assert not sync.git('status', '--porcelain', '--untracked-files=no')
    files, excluded_live = inventory()
    members, archives = create_archives(files)
    paths, rounds = round_payloads(members)
    metadata = {'status': 'verified_historical_evidence_archive', 'at_local': sync.now(),
                'snapshot_cutoff_local': '2026-10-05T04:32:35', 'completed_rounds': rounds,
                'original_files': len(members), 'original_bytes': sum(row['bytes'] for row in members),
                'archives': archives, 'excluded_live_or_later_files': excluded_live,
                'new_model_fits': 0, 'new_quality_scores': 0, 'new_test_label_reads': 0,
                'historical_failed_andrecovered_proofs_preserved_as_recorded': True,
                'raw_datasets_model_weights_andlarge_prediction_CSVs_remain_local': True}
    docs = {
        PREFIX / 'manifest.json': sync.encoded(metadata),
        PREFIX / 'files.json': sync.encoded(members),
        PREFIX / 'files.csv': sync.csv_bytes(members, ['source', 'bytes', 'sha256', 'archive', 'member', 'original_absolute_source']),
        PREFIX / 'rounds.csv': sync.csv_bytes(rounds, ['round', 'qualification', 'score', 'selected_configurations', 'evidence_files', 'directory']),
        PREFIX / 'README.md': (
            '# 全部历史验证\n\n已补齐第 1—60 轮方案、评分、因果检查、候选核验和原始报告。'
            '历史独立试验、资源对照、完整榜、旧测试回顾报告与失败／恢复记录也按原始字节归档。\n\n'
            '`rounds.csv` 是逐轮索引；`files.csv` / `files.json` 是全部原始文件索引；'
            '`manifest.json` 保存压缩包与每轮归档口径。\n\n'
            '每个 `evidence_part*.tar.gz` 可用 Python `tarfile` 或常用压缩工具解压。'
            '归档已逐文件解压校验 SHA256。较早轮次只保留其当时已有的检查口径。\n\n'
            '这是历史文件同步，没有重跑训练或评分。仍在执行的验证将在完整通过后单独同步。'
            '原始数据、权重与大型逐行预测 CSV 留在本地，相关路径和哈希保存在冻结协议中。\n').encode('utf-8'),
        Path('validation_sync/README.md'): (
            '# 每轮验证的方案同步\n\n[全部历史验证](history/README.md) 已补齐第 1—60 轮及其原始验证记录。'
            '每轮目录保存方案参数、指标和证据，`latest.json` 指向最新完成轮次。\n\n'
            '后续轮次只有在官方评分、方案冻结、因果检查、候选推理与来源核验完成后才自动提交。'
            '同步器依赖本地主机与进程运行；恢复后会补齐未同步的已完成轮次。\n').encode('utf-8'),
        Path('analysis') / Path(__file__).name: Path(__file__).read_bytes(),
    }
    for destination, data in docs.items():
        sync.atomic(WORKTREE / destination, data)
        paths.append(destination.as_posix())
    paths.extend(item['path'] for item in archives)
    for offset in range(0, len(paths), 50):
        sync.git('add', '--', *paths[offset:offset + 50])
    staged = sync.git('diff', '--cached', '--name-only').splitlines()
    assert set(staged) <= set(paths) and staged
    sync.git('commit', '-m', '补齐第1至60轮：全部历史验证、方案与原始证据归档')
    commit = sync.git('rev-parse', 'HEAD')
    sync.git('push', '-u', 'origin', f'HEAD:refs/heads/{sync.BRANCH}', timeout=180)
    remote = sync.git('ls-remote', '--heads', 'origin', f'refs/heads/{sync.BRANCH}')
    assert remote.split()[0] == commit
    result = {'status': 'pushed_and_remote_head_verified', 'at_local': sync.now(),
              'commit': commit, 'completed_rounds': len(rounds), 'original_files': len(members),
              'archive_parts': len(archives), 'archive_bytes': sum(item['bytes'] for item in archives),
              'commit_url': f'https://github.com/Zagadka-3906/stock-return-prediction/commit/{commit}',
              'history_url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/{sync.BRANCH}/validation_sync/history'}
    sync.atomic(receipt, sync.encoded(result))
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return result


def main():
    lock = sync.initialize()
    bindings = {str(path): file_sha(path) for path in (Path(__file__), DELEGATE_SOURCE)}
    try:
        history = backfill()
        while True:
            assert all(file_sha(Path(path)) == digest for path, digest in bindings.items())
            latest = None
            try:
                rounds = sorted(int(path.stem.rsplit('_r', 1)[1]) for path in
                                (ROOT / 'results').glob('optimization_20261003_r*.json'))
                for number in rounds:
                    if number >= 60 and sync.complete_round_evidence(number) is not None:
                        latest = sync.sync_round(number)
                state = {'status': 'monitoring_completed_validations', 'pid': os.getpid(),
                         'at_local': sync.now(), 'source_sha256': bindings,
                         'branch': sync.BRANCH, 'history_receipt': history,
                         'latest_synced': latest, 'poll_seconds': 45}
            except Exception as error:
                state = {'status': 'sync_failed_retry_pending', 'pid': os.getpid(), 'at_local': sync.now(),
                         'error': f'{type(error).__name__}: {error}', 'retry_seconds': 45}
                print(json.dumps(state, ensure_ascii=False), flush=True)
            sync.atomic(OUT / 'state.json', sync.encoded(state))
            time.sleep(45)
    except BaseException as error:
        sync.atomic(OUT / 'state.json', sync.encoded({'status': 'historical_sync_failed', 'pid': os.getpid(),
                    'at_local': sync.now(), 'error': f'{type(error).__name__}: {error}'}))
        raise
    finally:
        if lock.exists() and sync.read(lock).get('pid') == os.getpid():
            lock.unlink()


if __name__ == '__main__':
    main()
