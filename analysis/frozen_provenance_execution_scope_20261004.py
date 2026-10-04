"""Add effective driver provenance before freeze, then scope immutable SHA reuse."""
from pathlib import Path
from functools import wraps
from types import SimpleNamespace
import json
import sys
from locked_read_hash_cache_20261004 import LockedReadHashCache,fresh_sha

def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))

class FrozenProvenanceExecutionScope:
    def __init__(self,module,extra_sources,driver_metadata,analysis_root):
        self.module=module;self.proto=Path(module.OUT).resolve()/'protocol.json'
        self.extra={str(Path(p).resolve()):fresh_sha(p) for p in extra_sources}
        self.metadata=dict(driver_metadata);self.analysis_root=Path(analysis_root).resolve()
        self.old_freeze=module.freeze;self.old_dump=module.dump
        self.bindings=[];self.cache=None

    def install(self):
        @wraps(self.old_dump)
        def dump(path,value,*args,**kwargs):
            if Path(path).resolve()==self.proto:
                assert not self.proto.exists(),'Existing frozen protocol must never be rewritten'
                assert kwargs.get('immutable') is True
                for source,digest in self.extra.items():
                    assert source not in value['input_sha256'] or value['input_sha256'][source]==digest,source
                value=dict(value);value['input_sha256']={**value['input_sha256'],**self.extra}
                value['effective_execution_driver']=dict(self.metadata)
                value['scoped_provenance_reuse']={'initial_full_hash':True,'final_full_rehash':True,
                    'Windows_read_share_only':True,'nonsealed_paths_always_rehashed':True,
                    'forecast_math_andofficial_scorer_unchanged':True}
            return self.old_dump(path,value,*args,**kwargs)
        @wraps(self.old_freeze)
        def freeze():
            self.old_freeze()
            protocol=read(self.proto)
            assert protocol['effective_execution_driver']==self.metadata
            assert all(protocol['input_sha256'].get(p)==d for p,d in self.extra.items())
            assert self.cache is None
            self.cache=LockedReadHashCache(protocol['input_sha256']);self.cache.__enter__()
            seen=set()
            for _,module in sorted(sys.modules.copy().items()):
                file=getattr(module,'__file__',None)
                if not file or Path(file).resolve().parent!=self.analysis_root:continue
                for obj in (module,*[v for v in vars(module).values() if isinstance(v,SimpleNamespace)]):
                    if id(obj) not in seen and callable(getattr(obj,'sha',None)):
                        self.bindings.append((obj,obj.sha));seen.add(id(obj));obj.sha=self.cache.sha
        self.module.dump=dump;self.module.freeze=freeze
        return self

    def close(self,failed=False):
        for obj,function in self.bindings:obj.sha=function
        self.module.freeze=self.old_freeze;self.module.dump=self.old_dump
        if self.cache is None:return {'scope_started':False}
        report={'scope_started':True,'sha_bindings':len(self.bindings),'cache_hits':self.cache.hits,
            'nonsealed_paths_rehashed':self.cache.fresh_calls,'failed':bool(failed)}
        try:
            if not failed:self.cache.reverify()
        finally:self.cache.close()
        assert all(obj.sha is function for obj,function in self.bindings)
        assert self.module.freeze is self.old_freeze and self.module.dump is self.old_dump
        report['all_sha_bindings_restored']=True
        return report
