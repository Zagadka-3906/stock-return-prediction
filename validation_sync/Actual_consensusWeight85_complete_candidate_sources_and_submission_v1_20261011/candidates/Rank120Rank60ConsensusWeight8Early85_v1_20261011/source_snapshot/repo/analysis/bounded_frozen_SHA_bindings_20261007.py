"""Conservative streaming SHA-map dependency scan; historical outputs may also be protected."""
from pathlib import Path
import re,json,hashlib

CHUNK=1024*1024
# Windows paths here are far shorter; this also covers escaped extended-length paths.
MAX_ENCODED_PATH=200000
ENTRY=re.compile(rb'"((?:[^"\\]|\\.){1,200000})"\s*:\s*"([a-fA-F0-9]{64})"')

def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()

def entries(path):
    carry=b'';last_end=-1;offset=0
    with Path(path).open('rb') as stream:
        while True:
            block=stream.read(CHUNK)
            if not block:break
            data=carry+block; origin=offset-len(carry)
            for match in ENTRY.finditer(data):
                absolute_end=origin+match.end()
                if absolute_end<=last_end:continue
                key=json.loads(b'"'+match.group(1)+b'"')
                last_end=absolute_end
                yield key,match.group(2).decode('ascii').lower()
            offset+=len(block);carry=data[-(MAX_ENCODED_PATH+256):]

def scan(root,targets):
    root=Path(root).resolve();a=root/'analysis';targets={Path(p).resolve() for p in targets}
    pending=set(a.glob('*quality_run*.json'))|set(a.glob('*plan*.json'))|set(a.rglob('protocol.json'))
    pending.update((a/'service_owned_dependency_queue_v4_20261006').glob('queue_plan*.json'))
    pending.update((a/'service_owned_dependency_queue_v4_20261006/activated_jobs').glob('*/qualified_run.json'))
    # Include job definitions as roots, including prospective jobs, without reading model data.
    pending.update((a/'service_owned_workflows_20261006').glob('*/job_definition.json'))
    fingerprints={};blocked=set();seen=set();bytes_scanned=0
    while pending:
        path=pending.pop().resolve()
        if path in seen:continue
        seen.add(path)
        before=sha(path)
        for name,digest in entries(path):
            if '/' not in name and '\\' not in name:continue
            p=Path(name)
            if not p.is_absolute():p=root/p
            p=p.resolve()
            if p in targets:blocked.add(p)
            if p.suffix.lower()=='.json' and p.is_file() and p not in seen:pending.add(p)
        after=sha(path);assert before==after,f'Mutated frozen dependency document: {path}'
        fingerprints[str(path)]=after;bytes_scanned+=path.stat().st_size
    return {'fingerprints':fingerprints,'blocked':sorted(map(str,blocked)),'actual_JSON_bytes_scanned':bytes_scanned,
        'stream_chunk_bytes':CHUNK,'maximum_overlap_bytes':MAX_ENCODED_PATH+256,'conservative_all_path_to_SHA_maps_not_only_inputs':True}
