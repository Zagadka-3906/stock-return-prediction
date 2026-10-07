"""File-backed Git stdout/stderr avoids inherited-pipe EOF waits; preserve command contracts."""
from pathlib import Path
from contextlib import contextmanager
import subprocess,time

@contextmanager
def installed(folder):
    import publish_classifier_consensus_workflows_20261006 as helpers
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=False);original=helpers.sync.git;calls=[]
    def git(*args,cwd=None,timeout=180):
        for attempt in range(3):
            index=len(calls);out=folder/f'git{index:03d}.stdout';err=folder/f'git{index:03d}.stderr'
            with out.open('wb') as output,err.open('wb') as errors:
                proc=subprocess.Popen(['git',*args],cwd=cwd or helpers.sync.WORKTREE,stdin=subprocess.DEVNULL,stdout=output,stderr=errors,creationflags=subprocess.CREATE_NO_WINDOW,close_fds=True)
                try:code=proc.wait(timeout=timeout)
                except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=10);raise
            message=err.read_text(encoding='utf8',errors='replace')
            calls.append({'arguments':list(args),'cwd':str(cwd or helpers.sync.WORKTREE),'exit_code':code,'stdout':str(out),'stderr':str(err)})
            if code==0:return out.read_text(encoding='utf8').strip()
            if args[0] not in ('push','fetch','ls-remote') or attempt==2 or not any(x in message.lower() for x in ('tls','ssl','internal server error','unable to access','connection','timed out')):
                raise RuntimeError('git '+args[0]+' failed: '+message[:1500])
            time.sleep(2)
    helpers.sync.git=git
    try:yield calls
    finally:
        helpers.sync.git=original
        from run_dependency_queue_v3_20261006 import create
        create(folder/'execution.json',{'calls':calls,'file_backed_stdout_stderr':True,'hidden_console':True,'TLS_verification_not_disabled':True})
