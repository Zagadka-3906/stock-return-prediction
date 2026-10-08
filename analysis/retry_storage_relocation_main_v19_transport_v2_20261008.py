"""Fresh immutable publisher retry after actual transient verified-TLS ls-remote failure."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def main():
    service=A/'service_owned_workflows_20261006/actual_storage_relocation_main_publication_v19_20261008'
    assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='failed'
    source=A/'publish_actual_storage_relocation_evidence_v19_20261008.py';text=source.read_text(encoding='utf8')
    text=text.replace("out=A/'actual_storage_relocation_main_v19_20261008'","out=A/'actual_storage_relocation_main_v19_retry2_20261008'")
    needle="    pins={str(p):sha(p) for p in sources};out="
    assert text.count(needle)==1
    text=text.replace(needle,"    sources += [A/'publish_actual_storage_relocation_evidence_v19_20261008.py',A/'retry_storage_relocation_main_v19_transport_v2_20261008.py',A/'service_owned_workflows_20261006/actual_storage_relocation_main_publication_v19_20261008/service_execution.json',A/'service_owned_workflows_20261006/actual_storage_relocation_main_publication_v19_20261008/stderr.log']\n"+needle)
    target=A/'publish_actual_storage_relocation_evidence_v19_retry2_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'actual_storage_relocation_transport_retry_v2_20261008.json',{
        'status':'frozen_fresh_publisher_retry_after_actual_TLS_failure','input_sha256':{str(p):sha(p) for p in (Path(__file__),source,target)},
        'TLS_verification_remains_enabled':True,'scientific_workers_and_storage_bytes_unchanged':True,'new_quality_scores':0})
    namespace={'__file__':str(target),'__name__':'actual_storage_retry2'};exec(compile(text,str(target),'exec'),namespace);namespace['main']()
if __name__=='__main__':main()
