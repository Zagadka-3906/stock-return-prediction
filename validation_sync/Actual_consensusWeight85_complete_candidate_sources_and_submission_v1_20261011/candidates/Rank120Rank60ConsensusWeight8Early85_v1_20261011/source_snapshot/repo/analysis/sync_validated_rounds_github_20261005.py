"""Publish completed, qualified research rounds without changing the working checkout."""
from pathlib import Path
import argparse
import csv
import gzip
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence

BRANCH = 'codex/validated-rounds'
REMOTE = 'https://github.com/Zagadka-3906/stock-return-prediction.git'
WORKTREE = ROOT.parent / '赛题五_GitHub验证同步_20261005'
OUT = ROOT / 'analysis/github_validation_sync_20261005'
METRICS = ('ic_mean', 'ic_std', 'icir', 'ic_positive_ratio', 'annual_excess',
           'top1_annual_ret', 'mean_turnover', 'final_score')
SECRET = re.compile(rb'(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|sk-proj-[A-Za-z0-9_-]{40,}|AKIA[A-Z0-9]{16})')


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%S')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_bytes().decode('utf-8-sig'))


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.sync-tmp')
    temporary.write_bytes(data)
    os.replace(temporary, path)


def git(*args, cwd=WORKTREE, timeout=90):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never')
    result = subprocess.run(['git', *args], cwd=cwd, env=env, capture_output=True,
                            text=True, encoding='utf-8', errors='replace', timeout=timeout)
    if result.returncode:
        raise RuntimeError(f'git {args[0]} failed: {result.stderr.strip()[:1500]}')
    return result.stdout.strip()


def initialize():
    assert git('remote', 'get-url', 'origin', cwd=ROOT) == REMOTE
    if not WORKTREE.exists():
        git('worktree', 'add', '-b', BRANCH, str(WORKTREE), 'HEAD', cwd=ROOT)
    assert git('branch', '--show-current') == BRANCH
    assert git('remote', 'get-url', 'origin') == REMOTE
    assert Path(git('rev-parse', '--git-common-dir')).resolve() == (ROOT / '.git').resolve()
    OUT.mkdir(parents=True, exist_ok=True)
    lock = OUT / 'owner.lock'
    # A live owner prevents accidental duplicate publishers; a stale owner is recorded.
    import psutil
    if lock.exists():
        previous = read(lock)
        try:
            owner = psutil.Process(previous['pid'])
            owned = Path(__file__).name in ' '.join(owner.cmdline())
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            owned = False
        if owned:
            raise RuntimeError('An owned GitHub validation publisher is already running')
        atomic(OUT / ('previous_owner_' + str(previous['pid']) + '.json'), encoded(previous))
    atomic(lock, encoded({'pid': os.getpid(), 'source_sha256': sha(Path(__file__).read_bytes()), 'at_local': now()}))
    return lock


def csv_bytes(rows, fields):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode('utf-8-sig')


def snapshot(number):
    evidence = complete_round_evidence(number)
    if evidence is None:
        raise RuntimeError(f'Round {number} has not passed the complete scientific gates')
    directory = ROOT / f'analysis/optimization_20261003_r{number}'
    result_path = ROOT / f'results/optimization_20261003_r{number}.json'
    publication = read(result_path)
    assert publication['test_labels_read_this_round'] is False
    selection_path = directory / 'selection.json'
    selection = read(selection_path)
    assert selection['winner']['metrics'] == publication['winner']['metrics']
    assert len(selection['ranking']) == publication['scored_records']
    board_path = ROOT / 'results/all_model_rankings_20261003.json'
    board_bytes = board_path.read_bytes()
    board = json.loads(board_bytes.decode('utf-8-sig'))
    qa_path = ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'
    qa = read(qa_path)
    assert qa['status'] == 'passed'
    assert qa['connected_records'] == len(board['connected'])
    assert board['summary']['later_round_records'][str(number)] == publication['scored_records']
    board_sha = sha(board_bytes)
    del board_bytes
    relative = Path('validation_sync') / f'round{number}'
    payload = {}
    bindings = {}

    def copy(source, destination):
        data = source.read_bytes()
        assert len(data) < 5 * 1024**2, f'Unexpected large review artifact: {source}'
        assert not SECRET.search(data), f'Credential-shaped content detected in {source.name}'
        payload[str(destination).replace('\\', '/')] = data
        bindings[str(source.relative_to(ROOT)).replace('\\', '/')] = sha(data)

    copy(result_path, relative / 'result.json')
    candidate = Path(publication['candidate_submission']).parent
    copy(candidate / 'verification.json', relative / 'candidate_verification.json')
    copy(candidate / 'manifest.json', relative / 'candidate_manifest.json')
    required = ['protocol.json', 'component_audit.json', 'causal_validation.json',
                'calibrated_csv_official.json', 'provenance_scope_execution.json']
    for name in required:
        copy(directory / name, relative / name)
    for source in directory.glob('*causal_checks.json'):
        copy(source, relative / source.name)
    for name in ['zero_axis_handoff_execution.json', 'publication_recovery_execution_20261005.json']:
        if (directory / name).exists():
            copy(directory / name, relative / name)
    copy(qa_path, relative / 'ranking_qa.json')
    selected = {key: value for key, value in selection.items() if key != 'ranking'}
    payload[str(relative / 'selected_scheme.json').replace('\\', '/')] = encoded(selected)
    # Preserve every attempted complete configuration, without multiplying repeated graphs in Git.
    payload[str(relative / 'all_round_configurations.json.gz').replace('\\', '/')] = gzip.compress(
        encoded(selection['ranking']), compresslevel=6, mtime=0)
    bindings[str(selection_path.relative_to(ROOT)).replace('\\', '/')] = sha(selection_path.read_bytes())
    rows = []
    for rank, record in enumerate(selection['ranking'], 1):
        rows.append({'rank': rank, 'wave': record['wave'], 'arm': record['arm'],
                     **record['metrics'], 'configuration_sha256': sha(encoded(record))})
    payload[str(relative / 'ranking_round.csv').replace('\\', '/')] = csv_bytes(
        rows, ['rank', 'wave', 'arm', *METRICS, 'configuration_sha256'])
    full_rows = []
    for record in board['connected']:
        source = str(record['source']).replace('\\', '/')
        prefix = str(ROOT).replace('\\', '/') + '/'
        if source.startswith(prefix):
            source = source[len(prefix):]
        full_rows.append({key: record.get(key) for key in
                          ['rank', 'rank_without_known_restrictions', 'id', 'name', 'wave', 'score', 'status', 'known_restriction']}
                         | record['metrics'] | {'source': source, 'source_pointer': record['source_pointer'],
                                                'parameters_sha256': sha(encoded(record.get('parameters', {})))})
    fields = ['rank', 'rank_without_known_restrictions', 'id', 'name', 'wave', 'score', *METRICS,
              'status', 'known_restriction', 'source', 'source_pointer', 'parameters_sha256']
    payload[str(relative / 'ranking_all.csv').replace('\\', '/')] = csv_bytes(full_rows, fields)
    payload[str(relative / 'ranking_metadata.json').replace('\\', '/')] = encoded({
        'summary': board['summary'], 'catalog': board['catalog'], 'ranking_rule': board['ranking_rule'],
        'notes': board['notes'], 'original_source_manifest': board['source_manifest'],
        'original_full_ranking_sha256': board_sha})
    # Research code is small; copy its complete source tree so imports remain reviewable.
    sources = set(ROOT.glob('*.py'))
    for folder in ['analysis', 'experiments', 'src']:
        sources.update((ROOT / folder).glob('*.py'))
    sources.update((ROOT / 'config').glob('*.json'))
    sources.update(ROOT.glob('requirements*.txt'))
    sources.add(ROOT / '后续选模标准.md')
    for source in sorted(sources):
        copy(source, source.relative_to(ROOT))
    for file, digest in evidence['source_sha256'].items():
        assert sha((ROOT / file).read_bytes()) == digest
    assert sha(board_path.read_bytes()) == board_sha
    for file, digest in bindings.items():
        assert sha((ROOT / file).read_bytes()) == digest, f'Source changed while exporting: {file}'
    manifest = {'status': 'validated_local_snapshot', 'round': number, 'at_local': now(),
                'remote': REMOTE, 'branch': BRANCH, 'scientific_evidence': evidence,
                'metrics': publication['winner']['metrics'], 'score_gain': publication['score_gain'],
                'scored_records': publication['scored_records'], 'connected_records': len(full_rows),
                'training_only_validation': True, 'test_labels_read_this_round': False,
                'test_score_of_this_candidate': publication.get('test_score_of_this_candidate'),
                'selection_bias_uncorrected': publication.get('selection_bias_uncorrected'),
                'local_input_source_sha256': bindings, 'original_full_ranking_sha256': board_sha,
                'exported_files': {file: {'bytes': len(data), 'sha256': sha(data)} for file, data in payload.items()},
                'large_assets': 'Raw datasets, trained weights and prediction CSVs remain in the local asset store; their original SHA bindings are retained.'}
    payload[str(relative / 'manifest.json').replace('\\', '/')] = encoded(manifest)
    payload['validation_sync/latest.json'] = encoded({'round': number, 'directory': str(relative).replace('\\', '/'),
                                                     'metrics': manifest['metrics'], 'connected_records': len(full_rows)})
    explanation = (f'# 第 {number} 轮验证\n\n'
                   f"连续向前验证官方分：**{manifest['metrics']['final_score']:.12f}**；本轮增量：{manifest['score_gain']:+.12f}。\n\n"
                   f"本轮完整评分记录 {manifest['scored_records']} 条；累计连接榜 {len(full_rows)} 条。\n\n"
                   '选择冻结、官方评分复核、因果前缀检查、候选推理及文件哈希核验均通过。'
                   '验证年份已多次参与选择，累计选择偏差尚未校正；本轮没有候选测试评分。\n\n'
                   '- `selected_scheme.json`：冻结赢家及完整参数权威图。\n'
                   '- `all_round_configurations.json.gz`：所有本轮完整配置，可用 Python gzip 解压。\n'
                   '- `ranking_round.csv`、`ranking_all.csv`：本轮与累计完整榜。\n'
                   '- `protocol.json`、各检查 JSON 及 `manifest.json`：验证证据与原始文件 SHA256。\n\n'
                   '方案代码位于仓库的 `analysis/`、`experiments/` 和 `src/`。'
                   '完整复现需要本地数据、历史缓存及模型文件；文件来源和 SHA256 保存在冻结协议与候选清单中。\n')
    payload[str(relative / 'README.md').replace('\\', '/')] = explanation.encode('utf-8')
    if not (WORKTREE / 'validation_sync/README.md').exists():
        payload['validation_sync/README.md'] = (
            '# 验证完成后的方案同步\n\n每轮只有在官方评分、方案冻结、因果检查、候选推理与来源核验完成后才提交。'
            '每轮目录保留不可变证据，`latest.json` 指向最新完成轮次。\n\n'
            '同步器在本地后台运行；主机或进程停止期间不会自动执行。'
            '恢复运行后会补齐尚未同步的已完成轮次。\n').encode('utf-8')
        original_readme = git('show', 'HEAD:README.md').encode('utf-8')
        payload['README.md'] = ('> 已完成验证的优化方案与完整榜见 [validation_sync](validation_sync/README.md)。\n\n').encode('utf-8') + original_readme
    return manifest, payload


def sync_round(number):
    receipt = OUT / f'round{number}_receipt.json'
    if receipt.exists() and read(receipt)['status'] == 'pushed_and_remote_head_verified':
        return read(receipt)
    existing = WORKTREE / f'validation_sync/round{number}/manifest.json'
    if not existing.exists():
        manifest, payload = snapshot(number)
        for file, data in payload.items():
            destination = WORKTREE / file
            atomic(destination, data)
            assert sha(destination.read_bytes()) == sha(data)
        filenames = sorted(payload)
        for offset in range(0, len(filenames), 60):
            git('add', '--', *filenames[offset:offset + 60])
        staged = git('diff', '--cached', '--name-only').splitlines()
        assert len(staged) > 0
        git('commit', '-m', f'验证第{number}轮：冻结方案、官方指标与完整榜')
    else:
        manifest = read(existing)
        assert manifest['round'] == number
        staged = git('diff', '--cached', '--name-only').splitlines()
        allowed = set(manifest['exported_files']) | {
            f'validation_sync/round{number}/manifest.json',
            f'validation_sync/round{number}/README.md', 'validation_sync/latest.json',
            'validation_sync/README.md', 'README.md'}
        assert set(staged) <= allowed, 'Unexpected staged files in publisher worktree'
        if staged:
            git('commit', '-m', f'验证第{number}轮：冻结方案、官方指标与完整榜')
        assert not git('status', '--porcelain', '--untracked-files=no')
    commit = git('rev-parse', 'HEAD')
    git('push', '-u', 'origin', f'HEAD:refs/heads/{BRANCH}')
    remote = git('ls-remote', '--heads', 'origin', f'refs/heads/{BRANCH}')
    assert remote.split()[0] == commit, 'Remote HEAD did not match the actual commit'
    result = {'status': 'pushed_and_remote_head_verified', 'round': number, 'at_local': now(),
              'commit': commit, 'branch': BRANCH, 'remote': REMOTE,
              'commit_url': f'https://github.com/Zagadka-3906/stock-return-prediction/commit/{commit}',
              'scheme_url': f'https://github.com/Zagadka-3906/stock-return-prediction/tree/{BRANCH}/validation_sync/round{number}',
              'official_score': manifest['metrics']['final_score'],
              'connected_records': manifest['connected_records']}
    atomic(receipt, encoded(result))
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--start-round', type=int, default=60)
    arguments = parser.parse_args()
    lock = initialize()
    own_sha = sha(Path(__file__).read_bytes())
    try:
        while True:
            assert sha(Path(__file__).read_bytes()) == own_sha
            rounds = sorted(int(path.stem.rsplit('_r', 1)[1]) for path in
                            (ROOT / 'results').glob('optimization_20261003_r*.json'))
            latest = None
            try:
                for number in rounds:
                    if number < arguments.start_round:
                        continue
                    if complete_round_evidence(number) is not None:
                        latest = sync_round(number)
                state = {'status': 'monitoring_completed_validations', 'pid': os.getpid(),
                         'at_local': now(), 'source_sha256': own_sha, 'branch': BRANCH,
                         'latest_synced': latest, 'poll_seconds': 45}
            except Exception as error:
                state = {'status': 'sync_failed_retry_pending', 'pid': os.getpid(), 'at_local': now(),
                         'source_sha256': own_sha, 'error': f'{type(error).__name__}: {error}',
                         'branch': BRANCH, 'retry_seconds': 45}
                print(json.dumps(state, ensure_ascii=False), flush=True)
                if arguments.once:
                    atomic(OUT / 'state.json', encoded(state))
                    raise
            atomic(OUT / 'state.json', encoded(state))
            if arguments.once:
                return
            time.sleep(45)
    finally:
        if lock.exists() and read(lock).get('pid') == os.getpid():
            lock.unlink()


if __name__ == '__main__':
    main()
