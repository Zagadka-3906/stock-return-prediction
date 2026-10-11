"""Same conservative SHA-map scan with cached Windows paths and physical JSON aliases."""
from pathlib import Path
from functools import lru_cache
import time
from bounded_frozen_SHA_bindings_20261007 import sha,entries,CHUNK,MAX_ENCODED_PATH

def scan(root,targets):
    root=Path(root).resolve();a=root/'analysis';targets={Path(p).resolve() for p in targets}
    pending=set(a.glob('*quality_run*.json'))|set(a.glob('*plan*.json'))|set(a.rglob('protocol.json'))
    pending.update((a/'service_owned_dependency_queue_v4_20261006').glob('queue_plan*.json'))
    pending.update((a/'service_owned_dependency_queue_v4_20261006/activated_jobs').glob('*/qualified_run.json'))
    pending.update((a/'service_owned_workflows_20261006').glob('*/job_definition.json'))
    @lru_cache(maxsize=32768)
    def resolve(name):
        p=Path(name)
        return (p if p.is_absolute() else root/p).resolve()
    fingerprints={};blocked=set();seen=set();physical={};bytes_scanned=0;aliases=0;started=time.perf_counter()
    while pending:
        path=pending.pop().resolve()
        if path in seen:continue
        seen.add(path);st=path.stat();key=(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns)
        if key in physical:
            fingerprints[str(path)]=physical[key];aliases+=1;continue
        before=sha(path)
        for name,digest in entries(path):
            if '/' not in name and '\\' not in name:continue
            p=resolve(name)
            if p in targets:blocked.add(p)
            if p.suffix.lower()=='.json' and p not in seen and p not in pending and p.is_file():pending.add(p)
        after=sha(path);newst=path.stat()
        assert before==after and (newst.st_dev,newst.st_ino,newst.st_size,newst.st_mtime_ns)==key,path
        physical[key]=after;fingerprints[str(path)]=after;bytes_scanned+=st.st_size
        if len(physical)%100==0:print({'stage':'bounded_cached_dependency_scan','JSON_objects':len(physical),'aliases_reused':aliases,'pending':len(pending),'unique_GiB_scanned':bytes_scanned/2**30},flush=True)
    info=resolve.cache_info()
    return {'fingerprints':fingerprints,'blocked':sorted(map(str,blocked)),'actual_JSON_bytes_scanned':bytes_scanned,
        'stream_chunk_bytes':CHUNK,'maximum_overlap_bytes':MAX_ENCODED_PATH+256,'conservative_all_path_to_SHA_maps_not_only_inputs':True,
        'path_cache_hits':info.hits,'path_cache_misses':info.misses,'path_cache_max_entries':32768,'identical_physical_JSON_aliases_reused':aliases,
        'actual_unique_JSON_objects_scanned':len(physical),'elapsed_seconds':time.perf_counter()-started}
