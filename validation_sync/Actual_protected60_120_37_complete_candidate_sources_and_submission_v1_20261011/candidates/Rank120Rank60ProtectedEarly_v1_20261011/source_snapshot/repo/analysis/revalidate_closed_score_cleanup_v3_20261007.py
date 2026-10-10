"""Rehash existing frozen documents and inspect only newly added dependency roots."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from plan_closed_local_score_scratch_cleanup_v3_20261007 import OUT,live_direct_bindings,identities
from bounded_frozen_SHA_bindings_20261007 import entries

def main():
    plan=read(OUT/'plan.json'); targets={Path(r['path']) for r in plan['deletions']}
    direct,services=live_direct_bindings();assert not targets&set(direct)
    frozen=plan['frozen_documents_sha256'];assert not targets&{Path(p) for p in frozen}
    def check(item):
        name,digest=item;assert sha(name)==digest,name;return name
    with ThreadPoolExecutor(max_workers=2) as pool:
        for n in pool.map(check,frozen.items()):pass
    pending=set(A.glob('*quality_run*.json'))|set(A.glob('*plan*.json'))|set(A.rglob('protocol.json'))
    pending.update((A/'service_owned_dependency_queue_v4_20261006').glob('queue_plan*.json'))
    pending.update((A/'service_owned_dependency_queue_v4_20261006/activated_jobs').glob('*/qualified_run.json'))
    pending.update((A/'service_owned_workflows_20261006').glob('*/job_definition.json'))
    seen={Path(p).resolve() for p in frozen};new={}
    @lru_cache(maxsize=32768)
    def resolve(name):
        path=Path(name);return (path if path.is_absolute() else ROOT/path).resolve()
    while pending:
        path=pending.pop().resolve()
        if path in seen:continue
        seen.add(path);before=sha(path)
        for name,digest in entries(path):
            if '/' not in name and '\\' not in name:continue
            p=resolve(name);assert p not in targets,f'New frozen SHA binding: {p}'
            if p.suffix.lower()=='.json' and p not in seen and p not in pending and p.is_file():pending.add(p)
        assert sha(path)==before,path;new[str(path)]=before
    for row in plan['deletions']:
        path=Path(row['path']);assert path.resolve()==path and path.is_relative_to(ROOT.resolve())
        assert identities(path)=={k:row[k] for k in identities(path)} and sha(path)==row['sha256']
    for p,d in plan['retained_records_sha256'].items():assert sha(p)==d,p
    create(OUT/'revalidated_immediately_before_native_single_file_deletion.json',{'status':'passed_actual_full_rehash_and_incremental_new_root_scan_target_identities',
        'plan_sha256':sha(OUT/'plan.json'),'source_sha256':sha(__file__),'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_previous_frozen_documents_rehashed':len(frozen),'actual_new_dependency_documents_checked':len(new),
        'new_dependency_sha256':new,'live_jobs':services,'eligible_files':len(targets),'test_labels_read':False})
    print({'status':'passed_revalidation','files':len(targets),'frozen_documents_rehashed':len(frozen),'new_documents':len(new)},flush=True)
if __name__=='__main__':main()
