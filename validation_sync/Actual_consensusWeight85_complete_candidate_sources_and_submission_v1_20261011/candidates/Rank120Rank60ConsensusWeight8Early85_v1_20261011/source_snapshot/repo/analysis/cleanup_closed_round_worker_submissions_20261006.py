"""Remove only three closed rounds' reusable worker scratch CSVs, retaining scientific evidence."""
from pathlib import Path
import hashlib
import json
import sys
import time

import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'closed_round_worker_submission_cleanup_20261006'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create, sha, owned
from refresh_optimization_boundary_evidence_20261004 import complete_round_evidence


def identities(path):
    st = path.stat()
    return {'bytes': st.st_size, 'device': st.st_dev, 'inode': st.st_ino,
            'mtime_ns': st.st_mtime_ns, 'hardlinks': st.st_nlink}


def scan_bindings(targets):
    """Follow actual frozen JSON input maps; do not treat past output hashes as inputs."""
    pending = set(A.glob('*quality_run*.json')) | set(A.glob('*plan*.json')) | set(A.rglob('protocol.json'))
    queue = A / 'service_owned_dependency_queue_v4_20261006'
    pending.update(queue.glob('queue_plan*.json'))
    pending.update((queue / 'activated_jobs').glob('*/qualified_run.json'))
    seen, fingerprints = set(), {}
    def visit(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ('input_sha256', 'source_sha256', 'actual_QA_read_lock_input_sha256') and isinstance(item, dict):
                    for name in item:
                        p = Path(name)
                        if p.is_absolute():
                            p = p.resolve()
                            assert p not in targets, f'Frozen input: {p}'
                            if p.suffix == '.json' and p.is_file() and p not in seen:
                                pending.add(p)
                visit(item)
        elif isinstance(value, list):
            for item in value: visit(item)
    while pending:
        p = pending.pop().resolve()
        if p in seen: continue
        seen.add(p)
        value = read(p)
        visit(value)
        # Mutable live states are not roots; only original sealed/configuration documents enter here.
        fingerprints[str(p)] = sha(p)
    return fingerprints


def main():
    assert not OUT.exists(), 'Retain every prior cleanup execution.'
    OUT.mkdir()
    try:
        queue = read(A / 'service_owned_dependency_queue_v4_20261006/state.json')
        targets, retained, gates = [], {}, []
        for number in (82, 83, 84):
            folder = A / f'optimization_20261003_r{number}'
            row = queue['activated_jobs'][f'round{number}']
            assert not owned(row), f'Round {number} still executing'
            gate = complete_round_evidence(number)
            assert gate is not None
            execution = A / f'service_owned_dependency_queue_v4_20261006/activated_jobs/round{number}/execution.json'
            receipt = A / f'github_validation_sync_main_20261005/round{number}_receipt.json'
            publication = read(receipt)
            assert read(execution)['status'] == 'passed'
            assert publication['status'] == 'pushed_and_remote_head_verified' and publication['branch'] == 'main'
            assert publication['full_immutable_ranking_and_all_original_QA_preserved'] is True
            gates.append({'round': number, 'qualification': gate, 'publication': publication})
            path = folder / 'parallel_official_workers/worker_0/scoring_validation_only/submission.csv'
            resolved = path.resolve()
            assert resolved == path and resolved.is_relative_to(ROOT.resolve())
            assert resolved.drive.upper() == 'D:' and resolved.is_file()
            for parent in (resolved, *resolved.parents):
                if parent.is_relative_to(ROOT): assert not parent.is_symlink() and not parent.is_junction()
            targets.append({'path': str(resolved), 'round': number, **identities(resolved), 'sha256': sha(resolved)})
            for base in (folder, ROOT / f'candidates/optimization_20261003_r{number}'):
                for p in base.rglob('*'):
                    if p.is_file() and p.suffix in ('.json', '.jsonl', '.py', '.md', '.log', '.html'):
                        retained[str(p.resolve())] = sha(p)
            for p in (execution, receipt, ROOT / f'results/optimization_20261003_r{number}.json'):
                retained[str(p)] = sha(p)
        bindings = scan_bindings({Path(row['path']) for row in targets})
        before = psutil.disk_usage('D:/').free
        create(OUT / 'plan.json', {'status': 'frozen_before_user_authorized_worker_scratch_deletion',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'source_sha256': sha(__file__),
            'allowed_absolute_root': str(ROOT.resolve()), 'deletions': targets, 'qualification': gates,
            'frozen_documents_sha256': bindings, 'retained_records_sha256': retained,
            'authorization': '清理历史副本与弃用缓存；直接删除之前验证过不采用的模型，仅保留记录和分数等信息',
            'scope': 'Only worker_0/scoring_validation_only/submission.csv in closed, published rounds82,83,84',
            'current_selected_models_and_candidates_and_all_pending_round_inputs_retained': True})
        # Re-read current dependencies immediately before each checked single-file deletion.
        journal = OUT / 'deletions.jsonl'
        with journal.open('x', encoding='utf-8') as stream:
            for row in targets:
                path = Path(row['path'])
                assert path.resolve() == path and path.is_relative_to(ROOT.resolve())
                assert not owned(read(A / 'service_owned_dependency_queue_v4_20261006/state.json')['activated_jobs'][f'round{row["round"]}'])
                scan_bindings({path})
                assert identities(path) == {k: row[k] for k in identities(path)} and sha(path) == row['sha256']
                path.unlink()
                stream.write(json.dumps({**row, 'deleted_at_local': time.strftime('%Y-%m-%dT%H:%M:%S')}, ensure_ascii=False) + '\n')
                stream.flush()
        assert all(not Path(row['path']).exists() for row in targets)
        for path, digest in retained.items(): assert sha(path) == digest, path
        for path, digest in bindings.items(): assert sha(path) == digest, path
        after_gates = [complete_round_evidence(n) for n in (82,83,84)]
        assert after_gates == [row['qualification'] for row in gates]
        proof = {'status': 'passed_closed_published_round_worker_scratch_cleanup',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'deleted_files': len(targets),
            'deleted_logical_bytes': sum(row['bytes'] for row in targets),
            'all_deleted_files_single_hardlink': all(row['hardlinks'] == 1 for row in targets),
            'actual_D_free_bytes_change': psutil.disk_usage('D:/').free - before,
            'disk_change_includes_concurrent_work': True, 'records_verified_unchanged': len(retained),
            'frozen_documents_verified_unchanged': len(bindings), 'original_qualification_before_and_after_identical': True,
            'model_weights_deleted': 0, 'candidate_submissions_deleted': 0,
            'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False,
            'scientific_processes_stopped_or_restarted': 0, 'C_project_data_written': False,
            'immutable_past_CSV_SHA_records_describe_historical_outputs': True}
        create(OUT / 'verification.json', proof)
        print(json.dumps(proof, ensure_ascii=False), flush=True)
    except BaseException as error:
        create(OUT / 'failure.json', {'status': 'failed_preserved_cleanup', 'error': f'{type(error).__name__}: {error}'})
        raise


if __name__ == '__main__': main()
