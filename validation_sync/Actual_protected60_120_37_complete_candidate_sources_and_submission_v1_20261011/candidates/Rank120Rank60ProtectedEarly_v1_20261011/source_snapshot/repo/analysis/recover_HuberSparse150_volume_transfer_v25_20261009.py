"""Activate the admitted cross-volume byte-preserving transfer for seal and full150."""
from pathlib import Path
import sys,re,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'HuberSparse150_volume_transfer_v25_20261009.json'

def routed(source):
    s=BASE_ROUTE(source)
    for stem in ('selected_candidate_sealing','round150_full_registration'):
        s=s.replace(f'HuberSparse59_{stem}_v4_20261009',f'HuberSparse59_{stem}_v5_20261009')
    return s.replace('actual_registration_recovery_v23','actual_registration_recovery_v25').replace('recovery_v23_file_IO','recovery_v25_file_IO')

def execute(name):
    global BASE_ROUTE
    m=read(META)
    for f,d in m['input_sha256'].items():assert sha(f)==d,f
    import recover_HuberSparse150_import_namespace_v23_20261009 as previous
    BASE_ROUTE=previous.routed;original_read=previous.read;previous.routed=routed
    def bound(path):
        value=original_read(path)
        if Path(path)==previous.META:value={**value,'drivers':m['drivers'],'input_sha256':{**value['input_sha256'],**m['input_sha256'],str(META):sha(META)}}
        return value
    previous.read=bound
    from HuberSparse150_storage_v1_20261008 import installed_transfer
    from verified_TLS_Git_retry_runtime_v2_20261008 import installed
    try:
        with installed_transfer(),installed(Path('E:/赛题五_本机临时/HuberSparse150_volume_transfer_v25_20261009')/Path(m['drivers'][name]).stem/'git_file_IO'):
            previous.execute(name)
    finally:previous.read=original_read;previous.routed=BASE_ROUTE

def main():
    import recover_HuberSparse150_import_namespace_v23_20261009 as previous
    m=read(previous.META);drivers=dict(m['drivers']);inputs=[Path(__file__),previous.META,Path(previous.__file__),A/'HuberSparse150_storage_v1_20261008.py']
    assert read(A/'service_owned_workflows_20261006/HuberSparse59_selected_candidate_preparation_v4_20261009/service_execution.json')['status']=='passed'
    from HuberSparse150_storage_v1_20261008 import installed_transfer
    fixture=Path('E:/赛题五_本机临时/第150轮_20261008/volume_transfer_control_v25');fixture.mkdir()
    source=A/'optimization_20261003_r148/protocol.json';destination=fixture/'protocol.json'
    import os
    assert source.resolve().drive.upper()!=destination.parent.resolve().drive.upper()
    with installed_transfer():os.link(source,destination)
    assert sha(source)==sha(destination)
    inputs.extend((source,destination))
    names=['seal_HuberSparse59_selected_candidate_v2_20261009.py','run_HuberSparse59_round150_full_registration_v2_20261009.py']
    stems=['selected_candidate_sealing','round150_full_registration']
    for stem,name in zip(stems,names):
        folder=A/'service_owned_workflows_20261006'/f'HuberSparse59_{stem}_v4_20261009'
        assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='failed'
        inputs.extend(folder/n for n in ('job_definition.json','native_launch.json','service_execution.json','stderr.log'))
        target=A/re.sub(r'_v\d+_20261009.py$','_recovery_v25_20261009.py',name)
        code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_HuberSparse150_volume_transfer_v25_20261009 import execute\nif __name__=='__main__':execute("+repr(name)+")\n"
        with target.open('x',encoding='utf8') as f:f.write(code)
        drivers[name]=target.name;inputs.extend((A/name,target))
    create(META,{'status':'passed_actual_cross_volume_transfer_byte_identity_before_seal_and_full150_retries',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},'drivers':drivers,
        'fixture_source_drive':source.resolve().drive,'fixture_destination_drive':destination.parent.resolve().drive,
        'scientific_math_changed':False,'quality_scores_repeated':0,'native_fits_repeated':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={}
    for stem,name in zip(stems,names):
        sid=f'HuberSparse59_{stem}_v5_20261009';rows[sid]=start(sid,drivers[name],[],{str(META):sha(META),str(A/drivers[name]):sha(A/drivers[name])})
    create(A/'HuberSparse150_volume_transfer_hidden_launches_v25_20261009.json',rows)
    print({sid:r['owned_worker_pid'] for sid,r in rows.items()},flush=True)

if __name__=='__main__':main()
