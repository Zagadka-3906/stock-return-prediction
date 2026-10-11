"""Publish actual sparse controls and later official comparison evidence as distinct phases."""
from pathlib import Path
import argparse
import hashlib
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_joint_goss_round97_full_execution_20261006 import suspended_idle
from file_backed_hidden_git_runtime_20261007 import installed
import publish_classifier_consensus_workflows_20261006 as helpers


def closed(name):
    folder = A / 'service_owned_workflows_20261006' / name
    while not (folder / 'native_launch.json').exists() or owned(read(folder / 'native_launch.json')): time.sleep(15)
    assert read(folder / 'service_execution.json')['status'] == 'passed', name
    return folder


def main(phase):
    assert phase in ('controls', 'scores')
    closed('nonflag_SparseGram40_round133_full_registration_resume_v4_20261008')
    assert read(A / 'optimization_20261003_r132/full_registration_execution.json')['status'] == 'passed'
    assert read(A / 'github_validation_sync_main_20261005/round133_receipt.json')['actual_full_QA_version'] == 44
    if phase == 'scores': closed('nonflag_ReverseBayesFine40_full37_controls_main_publication_v1')
    science = closed('nonflag_ReverseBayesFine40_actual_full37_controls_v1_20261008' if phase == 'controls' else 'nonflag_ReverseBayesFine40_official_comparison_v1')
    folder = A / ('nonflag_residual_ReverseBayesFine37_transform_preflight_20261007' if phase == 'controls' else 'nonflag_ReverseBayesFine40_official_comparison_v1_20261007')
    proof = read(folder / 'verification.json')
    expected = 'passed_actual37_full5635800_nonflag_ReverseBayes64_independent_CDF_and111_cold_controls' if phase == 'controls' else 'passed_actual40_nonflag_ReverseBayes64_full_official_comparisons'
    assert proof['status'] == expected
    assert len(proof['controls'] if phase == 'controls' else proof['records']) == (37 if phase == 'controls' else 40)
    sources = [Path(__file__), A / 'nonflag_ReverseBayesFine40_plan_20261007.json',
        A / 'prepare_nonflag_ReverseBayesFine40_science_routes_v1_20261008.py',
        A / 'nonflag_ReverseBayesFine40_science_route_preparation_v1_20261007.json',
        A / 'actual_user_submission_deadline_and_priority_20261008.json',
        A / 'nonflag_ReverseBayesFine40_round134_source_admission_v1_20261007.json',
        A / 'nonflag_ReverseBayesFine40_prospective_routes_v2_20261007.json',
        A / 'nonflag_ReverseBayesFine40_round134_mapping_v1_20261008.py',
        A / 'nonflag_empirical_Bayes64_codec_20261007.py',
        A / 'nonflag_residual_EmpiricalBayes64_bank10_20261007/verification.json',
        A / 'nonflag_ReverseBayes40_actual_native3_full37_cold111_controls_20261007.json',
        A / 'nonflag_residual_ReverseBayes64_native_stage_20261007.py',
        A / 'nonflag_residual_ReverseBayes64_native_hook3_preflight_20261007/verification.json',
        A / 'prepare_nonflag_ReverseBayesFine40_round134_sources_v1_20261007.py',
        A / 'run_nonflag_ReverseBayesFine40_official_comparison_v1_20261007.py',
        A / 'run_nonflag_ReverseBayesFine40_admitted_comparison_v1_20261007.py',
        A / 'verify_nonflag_ReverseBayesFine40_round134_sources_v1_20261007.py',
        A / 'prepare_nonflag_ReverseBayesFine40_selected_candidate_v1_20261007.py',
        A / 'seal_nonflag_ReverseBayesFine40_selected_candidate_v1_20261007.py',
        A / 'predict_nonflag_residual_ReverseBayesFine_complete_scheme_20261007.py',
        A / 'run_nonflag_ReverseBayesFine40_round134_full_registration_v1_20261007.py',
        *folder.glob('*.json'), *science.glob('*.json'), *science.glob('*.log')]
    if phase == 'scores':
        for row in proof['records']:
            capsule = Path(row['official_score_cache']['official_metrics_source'])
            assert sha(capsule) == row['official_metric_capsule_sha256'] and read(capsule)['metrics'] == row['metrics']
            sources.append(capsule)
    out = A / f'nonflag_ReverseBayesFine40_{phase}_github_v1_20261007'
    assert not out.exists()
    out.mkdir()
    sources += [A/'actual_ReverseBayesFine134_truthful_receiver_preparation_v2_20261008.json',
                A/'prepare_nonflag_ReverseBayesFine40_round134_sources_v3_20261008.py', A/'run_nonflag_ReverseBayesFine40_round134_full_registration_v3_20261008.py', A/'run_nonflag_ReverseBayesFine40_official_comparison_v3_20261008.py', A/'run_nonflag_ReverseBayesFine40_admitted_comparison_v3_20261008.py',
                A/'verify_nonflag_ReverseBayesFine40_round134_sources_v3_20261008.py', A/'prepare_nonflag_ReverseBayesFine40_selected_candidate_v3_20261008.py', A/'verify_nonflag_ReverseBayesFine40_prospective_routes_v4_20261008.py',
                A/'nonflag_ReverseBayesFine40_prospective_routes_v4_20261008.json']
    sources = list(dict.fromkeys(sources))
    pins = {**proof['input_sha256'], **{str(p): sha(p) for p in sources}}
    create(out / 'frozen_before_main_publication.json', {'input_sha256': pins, 'phase': phase,
                'full134_qualification_pending': True, 'new_native_fits': 0, 'test_labels_read': False})
    held = []
    try:
        row = read(A / 'service_owned_workflows_20261006/main_publisher_v8_20261008/native_launch.json')
        parent, worker, idle = suspended_idle(row, '    main (watch_validations_main_v7_20261006.py:71)')
        held.extend((worker, parent))
        create(out / 'actual_idle_main_hold.json', idle)
        from win32_read_handle_hash_cache_with_filename_v2_20261006 import LockedReadHashCache
        with installed(out / ('file_backed_git_' + phase)), LockedReadHashCache(pins) as scope:
            sync = helpers.sync
            previous = sync.git('rev-parse', 'HEAD')
            helpers.verify_main(previous)
            assert not sync.git('status', '--porcelain')
            prefix = Path('validation_sync') / f'nonflag_ReverseBayesFine40_{phase}_20261008'
            targets, bindings = {}, {}
            for source in sources:
                data = source.read_bytes()
                assert not sync.SECRET.search(data), source
                target = (prefix / source.relative_to(ROOT)).as_posix()
                targets[target] = data
                bindings[source.relative_to(ROOT).as_posix()] = {'published_path': target, 'raw_sha256': hashlib.sha256(data).hexdigest()}
            targets[(prefix / '.gitattributes').as_posix()] = b'* -text\n'
            targets[(prefix / 'manifest.json').as_posix()] = sync.encoded({'status': 'actual_sparse_evidence_before_full134_qualification',
                'phase': phase, 'at_local': sync.now(), 'files': bindings, 'round': 134,
                'actual_controls': 37, 'actual_cold_prefix_controls': 111,
                'actual_official_score_records': 40 if phase == 'scores' else 0,
                'actual_best': proof.get('best'), 'new_native_fits_by_publication': 0,
                'candidate_and_QA45_and_full_round_main_receipt_pending': True, 'test_labels_read': False})
            for name, data in targets.items(): sync.atomic(sync.WORKTREE / name, data)
            names = sorted(targets)
            for left in range(0, len(names), 50): sync.git('add', '-f', '--', *names[left:left+50])
            assert set(sync.git('-c', 'core.quotepath=false', 'diff', '--cached', '--name-only').splitlines()) == set(names)
            sync.git('-c', 'maintenance.auto=false', '-c', 'gc.auto=0', 'commit', '-m', '同步反向贝叶斯残差幅度加密第133轮实际证据 ' + phase, timeout=180)
            commit = sync.git('rev-parse', 'HEAD')
            expected_hashes = {name: hashlib.sha256(data).hexdigest() for name, data in targets.items()}
            assert helpers.blob_hashes(commit, expected_hashes) == expected_hashes
            sync.git('push', 'origin', 'HEAD:refs/heads/main', timeout=180)
            helpers.verify_main(commit)
            helpers.watcher.advance_source_index(commit)
            scope.reverify()
            create(out / 'receipt.json', {'status': 'pushed_and_remote_head_verified', 'commit': commit,
                'at_local': sync.now(), 'phase': phase, 'branch': 'main', 'raw_git_blobs_verified': len(expected_hashes),
                'official_score_records': 40 if phase == 'scores' else 0,
                'url': 'https://github.com/Zagadka-3906/stock-return-prediction/tree/main/' + prefix.as_posix()})
            print('Actual sparse ' + phase + ' pushed to main: ' + commit, flush=True)
    finally:
        for p in reversed(held):
            if p.is_running(): p.resume()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=('controls', 'scores'))
    main(parser.parse_args().phase)
