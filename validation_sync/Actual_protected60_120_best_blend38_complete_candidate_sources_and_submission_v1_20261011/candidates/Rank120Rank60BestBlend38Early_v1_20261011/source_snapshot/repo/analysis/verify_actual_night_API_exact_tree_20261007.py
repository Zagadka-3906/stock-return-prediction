"""Check the API tree with an isolated Git index; do not change publisher HEAD/index."""
from pathlib import Path
import sys
import os
import json
import hashlib
import subprocess
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, create
import publish_classifier_consensus_workflows_20261006 as helpers

folder = A / 'actual_night_manual_handoff_API_v2_20261007'
packet = read(folder / 'bounded_tree_packet.json')
index = folder / 'isolated_API_tree.index'
assert not index.exists()
env = dict(os.environ, GIT_INDEX_FILE=str(index))

def git(*args, data=None):
    r = subprocess.run(['git', *args], input=data, cwd=helpers.sync.WORKTREE,
        env=env, capture_output=True, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW, close_fds=True)
    assert r.returncode == 0, r.stderr.decode('utf8', errors='replace')
    return r.stdout.decode('utf8').strip()

git('read-tree', packet['base_tree_sha'])
hashes = {}
for entry in packet['tree_elements']:
    raw = entry['content'].encode('utf8')
    blob = git('hash-object', '-w', '--stdin', data=raw)
    assert blob == hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    git('update-index', '--add', '--cacheinfo', entry['mode'] + ',' + blob + ',' + entry['path'])
    hashes[entry['path']] = {'sha256': hashlib.sha256(raw).hexdigest(), 'git_blob_sha': blob}
tree = git('write-tree')
assert tree == '599216f6f7a9256199a3a525ef8bc26d39bf8460'
create(folder / 'actual_API_exact_tree_verification.json', {'status': 'passed_all20_backup_blobs_and_exact_API_tree',
    'tree_sha': tree, 'files': hashes, 'main_publisher_HEAD_and_real_index_unchanged': True,
    'full131_publication_not_claimed': True, 'new_quality_scores': 0})
print('Verified all20 actual backup file blobs and exact API tree: ' + tree)
