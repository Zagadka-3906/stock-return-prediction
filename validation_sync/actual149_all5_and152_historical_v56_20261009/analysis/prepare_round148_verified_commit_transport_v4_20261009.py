from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
old=A/'recover_round148_chunked_main_publication_v3_20261009.py'
new=A/'recover_round148_verified_commit_transport_v4_20261009.py'
s=old.read_text(encoding='utf8')
s=s.replace('round148_chunked_main_recovery_v3_20261009','round148_verified_commit_transport_v4_20261009')
s=s.replace('AdaptiveJointCrossHuber242_round148_full_registration_v5_20261009','AdaptiveJointCrossHuber242_round148_full_registration_v6_20261009')
s=s.replace("['git',*args]","['git','-c','http.proxy=http://127.0.0.1:7897','-c','http.version=HTTP/1.1',*args]")
start=s.index("  rejected=value('rev-parse','HEAD')")
end=s.index("  assert value('ls-remote','origin','refs/heads/main').split()[0]==commit",start)
replacement='''  proof_path=Path('E:/赛题五_本机临时/round148_chunked_main_recovery_v3_20261009/before_remote_push.json')
  proof=read(proof_path);rejected=proof['rejected_commit'];commit=proof['new_commit']
  parent_commit=proof['remote_parent'];descriptor=proof['descriptor']
  assert value('rev-parse','HEAD')==rejected
  assert value('rev-parse',commit+'^')==parent_commit
  assert value('rev-parse',rejected+'^')==parent_commit
  previous_tree=tree(rejected);actual=tree(commit)
  prefix='validation_sync/round148/'
  large=prefix+'complete_ranking_display/lossless_ranking_display_v2_20261006/round148/full_report_reconstructed_for_publication.json.gz'
  manifest_path=prefix+'manifest.json';original=work/large
  assert all(actual[name]==item for name,item in previous_tree.items() if name not in (large,manifest_path))
  expected=proof['new_artifact_blobs'];assert large not in actual
  assert set(actual)==(set(previous_tree)-{large})|set(expected)
  for name,digest in expected.items():
   blob=git('show',commit+':'+name)
   assert hashlib.sha256(blob).hexdigest()==digest
   assert sha(work/name)==digest,name
  manifest=read(work/manifest_path)
  assert manifest['scored_records']==242 and manifest['connected_records']==14957
  assert manifest['original_full_ranking_sha256']==descriptor['original_report_sha256']
  assert sha(original)==descriptor['compressed_sha256']
  assert sha(A/'lossless_ranking_display_v2_20261006/round148/full_report_reconstructed_for_publication.json.gz')==descriptor['compressed_sha256']
  h=hashlib.sha256();size=0
  for item in descriptor['parts']:
   block=(original.parent/item['path']).read_bytes()
   assert len(block)==item['bytes'] and hashlib.sha256(block).hexdigest()==item['sha256']
   h.update(block);size+=len(block)
  assert size==descriptor['compressed_bytes'] and h.hexdigest()==descriptor['compressed_sha256']
  remote=value('ls-remote','origin','refs/heads/main').split()[0]
  assert remote in (parent_commit,commit),remote
  create(OUT/'verified_existing_commit_before_push.json',{'proof':str(proof_path),'proof_sha256':sha(proof_path),
    'commit':commit,'remote_before':remote,'original_tree_and_all_new_bytes_verified':True,
    'explicit_existing_loopback_proxy':True,'TLS_verification_enabled':True,'root_index_untouched':True})
  if remote!=commit:git('push','origin',commit+':refs/heads/main',timeout=1200)
'''
s=s[:start]+replacement+s[end:]
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
pins={str(p):sha(p) for p in (old,new,Path('E:/赛题五_本机临时/round148_chunked_main_recovery_v3_20261009/before_remote_push.json'))}
create(A/'round148_verified_commit_transport_v4_20261009.json',{'status':'prepared_verified_existing_commit_transport_only','input_sha256':pins,'new_scoring':0,'new_native_fits':0})
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
row=start('AdaptiveJointCrossHuber242_round148_full_registration_v6_20261009',new.name,[],pins)
create(A/'round148_verified_commit_transport_hidden_launch_v4_20261009.json',row)
print(row,flush=True)
