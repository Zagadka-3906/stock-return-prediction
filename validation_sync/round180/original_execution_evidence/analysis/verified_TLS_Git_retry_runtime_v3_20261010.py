"""Also retry killed, timed-out remote Git calls; preserve TLS and exact arguments."""
from contextlib import contextmanager
from pathlib import Path
import time,subprocess
from run_dependency_queue_v3_20261006 import create
from file_backed_hidden_git_runtime_20261007 import installed as original_installed

@contextmanager
def installed(folder):
    import publish_classifier_consensus_workflows_20261006 as helpers
    attempts=[]
    with original_installed(folder):
        original=helpers.sync.git
        def retry(*args,**kwargs):
            for attempt in range(5):
                try:return original(*args,**kwargs)
                except (RuntimeError,subprocess.TimeoutExpired) as error:
                    message=str(error);remote=args and args[0] in ('ls-remote','push','fetch')
                    transient=remote and (isinstance(error,subprocess.TimeoutExpired) or any(word in message.lower() for word in ('tls','ssl','http2','framing','unable to access','connection','timed out','unexpected eof','http 408','http 429','http 502','http 503','http 504','rpc failed','unexpected disconnect','remote end hung up')))
                    if not transient:raise
                    attempts.append({'command':args[0],'attempt':attempt+1,'error_class':type(error).__name__,'error':message[:1500]})
                    if attempt==4:raise
                    time.sleep(min(15,2**attempt))
        helpers.sync.git=retry
        try:yield
        finally:
            helpers.sync.git=original
            create(Path(folder)/'actual_verified_TLS_transport_retries.json',{'attempts':attempts,'TLS_verification_disabled':False,'Git_command_arguments_unchanged':True,'TimeoutExpired_retries_only_remote_calls':True,'new_quality_scores':0})
