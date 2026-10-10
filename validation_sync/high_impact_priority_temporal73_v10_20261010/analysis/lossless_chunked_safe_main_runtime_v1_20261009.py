"""Publication-only transport: exact large-byte chunks and no research-index rewrites."""
from pathlib import Path
from contextlib import contextmanager
import builtins,hashlib,io,gzip,os,json,subprocess
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
CHUNK=16*1024**2;LIMIT=95*1024**2

def split_payload(payload,evidence):
    descriptors={}
    for name,data in list(payload.items()):
        if len(data)<LIMIT:continue
        info=evidence['exported_files'][name]
        assert info['sha256']==hashlib.sha256(data).hexdigest()
        parts=[]
        for offset in range(0,len(data),CHUNK):
            part=data[offset:offset+CHUNK];key=name+f'.part{len(parts):03d}'
            payload[key]=part;digest=hashlib.sha256(part).hexdigest()
            parts.append({'path':Path(key).name,'bytes':len(part),'sha256':digest})
            evidence['exported_files'][key]={'bytes':len(part),'sha256':digest}
        h=hashlib.sha256();size=0
        for item in parts:
            block=payload[name+'.part'+f'{parts.index(item):03d}'];h.update(block);size+=len(block)
        assert size==len(data) and h.hexdigest()==info['sha256']
        descriptor={'status':'lossless_chunked_original_bytes','original_filename':Path(name).name,
            'compressed_bytes':len(data),'compressed_sha256':info['sha256'],'parts':parts,
            'original_export_metadata':info,'original_scientific_bytes_preserved':True}
        if name.endswith('full_report_reconstructed_for_publication.json.gz'):
            raw=hashlib.sha256();raw_size=0
            with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
                while block:=stream.read(4*1024**2):raw.update(block);raw_size+=len(block)
            assert raw.hexdigest()==evidence['original_full_ranking_sha256']
            descriptor.update(original_report_sha256=raw.hexdigest(),original_report_bytes=raw_size)
        key=name+'.parts.json';blob=(json.dumps(descriptor,ensure_ascii=False,indent=2)+'\n').encode('utf8')
        payload[key]=blob;evidence['exported_files'][key]={'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest()}
        del payload[name];del evidence['exported_files'][name];descriptors[name]=descriptor
    if descriptors:
        base=Path(next(iter(descriptors))).parent
        key=(base/'reconstruct_chunked_reports.py').as_posix()
        code="""from pathlib import Path
import json,hashlib
p=Path(__file__).parent
for d in p.glob('*.parts.json'):
 m=json.loads(d.read_text(encoding='utf8'));target=p/m['original_filename'];assert not target.exists()
 h=hashlib.sha256();size=0
 with target.open('xb') as f:
  for item in m['parts']:
   b=(p/item['path']).read_bytes();assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
   f.write(b);h.update(b);size+=len(b)
 assert size==m['compressed_bytes'] and h.hexdigest()==m['compressed_sha256']
 print(target)
"""
        blob=code.encode('utf8');payload[key]=blob
        evidence['exported_files'][key]={'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest()}
    return descriptors

@contextmanager
def installed(logdir):
    import publish_classifier_consensus_workflows_20261006 as helpers
    from run_dependency_queue_v3_20261006 import sha,create
    folder=Path(logdir);folder.mkdir(parents=True,exist_ok=False)
    sync=helpers.sync;old_advance=helpers.watcher.advance_source_index;old_import=builtins.__import__;old_encoded=sync.encoded
    descriptors={};patched=[];events=[]
    index=Path(subprocess.check_output(['git','rev-parse','--git-path','index'],cwd=ROOT,creationflags=subprocess.CREATE_NO_WINDOW).decode().strip())
    if not index.is_absolute():index=ROOT/index
    before=sha(index);backup=folder/'research_index_before.bin';backup.write_bytes(index.read_bytes())
    def advance(commit):
        assert sync.git('branch','--show-current',cwd=ROOT)=='main'
        old=sync.git('rev-parse','refs/heads/main',cwd=ROOT)
        if old!=commit:
            r=subprocess.run(['git','merge-base','--is-ancestor',commit,old],cwd=ROOT,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
            if r.returncode!=0:
                assert r.returncode==1
                sync.git('merge-base','--is-ancestor',old,commit)
                sync.git('update-ref','refs/heads/main',commit,old,cwd=ROOT)
        assert sha(index)==before
        events.append({'main_commit':commit,'research_index_sha256':before,'research_index_bytes_unchanged':True})
    def importing(name,*args,**kwargs):
        module=old_import(name,*args,**kwargs)
        if name.startswith('collect_full_lossless_round') and hasattr(module,'collect') and not getattr(module,'_safe_chunk_runtime',False):
            original=module.collect
            def collect(*a,**k):
                payload,evidence=original(*a,**k);descriptors.update(split_payload(payload,evidence));return payload,evidence
            module.collect=collect;module._safe_chunk_runtime=True;patched.append((module,original))
        return module
    def encoded(value):
        if isinstance(value,dict) and value.get('status')=='validated_local_snapshot' and descriptors:
            value['chunked_original_artifacts']=dict(descriptors)
            value['large_report_original_bytes_losslessly_chunked_before_commit']=True
        return old_encoded(value)
    helpers.watcher.advance_source_index=advance;builtins.__import__=importing;sync.encoded=encoded
    try:yield
    finally:
        helpers.watcher.advance_source_index=old_advance;builtins.__import__=old_import;sync.encoded=old_encoded
        for module,original in patched:module.collect=original;del module._safe_chunk_runtime
        create(folder/'execution.json',{'chunked_original_artifacts':descriptors,'main_ref_updates':events,
            'research_index_before_sha256':before,'research_index_after_sha256':sha(index),
            'research_index_bytes_unchanged':sha(index)==before,'TLS_verification_disabled':False,'new_scoring':0})
