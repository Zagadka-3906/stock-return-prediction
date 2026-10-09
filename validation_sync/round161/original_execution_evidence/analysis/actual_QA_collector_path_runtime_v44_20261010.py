"""Resolve the actual dated QA directory for derived rounds without changing checks."""
from pathlib import Path
from contextlib import contextmanager
import builtins,re,sys
A=Path(__file__).resolve().parent
sys.path.insert(0,str(A))
from actual_QA_collector_path_runtime_v43_20261009 import corrected_namespace

@contextmanager
def installed():
    original=builtins.__import__;saved=[];seen=set()
    def checked(name,*args,**kwargs):
        module=original(name,*args,**kwargs)
        match=re.fullmatch(r'collect_full_lossless_round(\d+)_qa(\d+)_20261009',name)
        if match and name not in seen:
            number,qa=map(int,match.groups())
            assert 153<=number<=1000 and qa==number-89,(number,qa)
            seen.add(name);namespace=module.namespace
            saved.append((namespace,namespace['collect']))
            namespace['collect']=corrected_namespace()['collect']
        return module
    builtins.__import__=checked
    try:yield
    finally:
        assert builtins.__import__ is checked
        builtins.__import__=original
        for namespace,collect in saved:namespace['collect']=collect
