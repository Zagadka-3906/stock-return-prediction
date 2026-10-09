"""Use exact transport-error retries; a GH001 or filename containing 'lossless' is not TLS."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
 from prepare_round148_chunked_main_retry_v3_20261009 import verify_partial
 import publish_classifier_consensus_workflows_20261006 as h
 verify_partial(h.sync.WORKTREE)
 old=A/'recover_round148_chunked_main_publication_v2_20261009.py';s=old.read_text(encoding='utf8')
 s=s.replace('round148_chunked_main_recovery_v2_20261009','round148_chunked_main_recovery_v3_20261009')
 s=s.replace('AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009','AdaptiveJointCrossHuber242_round148_full_registration_v5_20261009')
 start=s.index(' def git(*args,');end=s.index(' def value(',start)
 s=s[:start]+''' def git(*args,data=None,isolated=False,timeout=300):
  for attempt in range(5):
   r=subprocess.run(['git',*args],cwd=work,input=data,capture_output=True,env=env if isolated else None,
    timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW)
   commands.append({'arguments':list(args),'exit_code':r.returncode,'attempt':attempt+1})
   if r.returncode==0:return r.stdout
   message=r.stderr.decode('utf8',errors='replace')
   transient=args[0] in ('push','ls-remote') and 'GH001' not in message and any(
    text in message.lower() for text in ('tls connect error','ssl routines','rpc failed','http2 framing','unexpected eof','connection reset','could not resolve host'))
   if not transient or attempt==4:raise RuntimeError(message[-3000:])
   time.sleep(min(15,2**attempt))
'''+s[end:]
 needle='assert helpers.blob_hashes(commit,expected)==expected';assert s.count(needle)==1
 s=s.replace(needle,"assert all(hashlib.sha256(git('show',commit+':'+name)).hexdigest()==digest for name,digest in expected.items())")
 p=A/'recover_round148_chunked_main_publication_v3_20261009.py';compile(s,str(p),'exec')
 with p.open('x',encoding='utf8') as f:f.write(s)
 failures=[A/'service_owned_workflows_20261006'/n/'service_execution.json' for n in (
  'AdaptiveJointCrossHuber242_round148_full_registration_v3_20261009','AdaptiveJointCrossHuber242_round148_full_registration_v4_20261009')]
 assert all(read(p)['status']=='failed' for p in failures)
 from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
 row=start('AdaptiveJointCrossHuber242_round148_full_registration_v5_20261009',p.name,[],
  {str(q):sha(q) for q in [Path(__file__),old,p,*failures]})
 create(A/'round148_chunked_main_recovery_hidden_launch_v3_20261009.json',row)
 print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
