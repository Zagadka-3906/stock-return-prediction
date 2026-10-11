"""Resume exact already-copied aliases and retain absolute external provenance sources."""
from pathlib import Path
import sys,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'HuberSparse150_partial_registry_v29_20261009.json'
DRIVER='run_HuberSparse59_round150_full_registration_recovery_v29_20261009.py'

def registry_source(module):
    s=Path(module.__file__).read_text(encoding='utf8')
    changes={"assert not OUT.exists()":"assert OUT.is_dir() and not any(OUT.iterdir())",
        'empty(CANDIDATE)':'assert CANDIDATE.resolve().is_relative_to(Path(\'E:/赛题五_本机临时/第150轮_20261008\').resolve())',
        'OUT.mkdir()':'OUT.mkdir(exist_ok=True)',
        'source.relative_to(ROOT)':"(source.relative_to(ROOT) if source.is_relative_to(ROOT) else Path('external_metadata')/(sha(source)+'_'+source.name))",
        'os.link(':'RESUME_EXACT_LINK('}
    for old,new in changes.items():assert old in s,old;s=s.replace(old,new)
    compile(s,str(module.__file__),'exec');return s

def routed(source):
    return BASE_ROUTE(source).replace('HuberSparse59_round150_full_registration_v6_20261009','HuberSparse59_round150_full_registration_v7_20261009').replace('actual_registration_recovery_v27','actual_registration_recovery_v29').replace('recovery_v27_file_IO','recovery_v29_file_IO')

def execute():
    global BASE_ROUTE
    m=read(META)
    for f,d in m['input_sha256'].items():assert sha(f)==d,f
    import recover_HuberSparse150_materialization_v27_20261009 as previous
    import register_HuberSparse59_round150_artifacts_20261008 as registry
    previous_read=previous.read;old_driver=previous.DRIVER;BASE_ROUTE=previous.routed;previous.routed=routed;previous.DRIVER=DRIVER
    def bound(path):
        v=previous_read(path)
        if Path(path)==previous.META:v={**v,'input_sha256':{**v['input_sha256'],**m['input_sha256'],str(META):sha(META)}}
        return v
    previous.read=bound;original_main=registry.main
    import os
    def exact_link(source,target):
        source,target=Path(source),Path(target)
        if target.exists():assert target.is_file() and sha(target)==sha(source),(source,target)
        else:os.link(source,target)
    ns={**registry.__dict__,'__name__':'actual150_exact_partial_registry_resume29','RESUME_EXACT_LINK':exact_link}
    exec(compile(registry_source(registry),str(Path(__file__)),'exec'),ns)
    registry.main=ns['main']
    try:previous.execute()
    finally:previous.read=previous_read;previous.DRIVER=old_driver;previous.routed=BASE_ROUTE;registry.main=original_main

def main():
    import register_HuberSparse59_round150_artifacts_20261008 as registry
    assert registry.OUT.is_dir() and not any(registry.OUT.iterdir())
    registry_source(registry)
    manifest=read(registry.SOURCE_CANDIDATE/'manifest.json');expected={}
    for relative,info in manifest['files'].items():
        target_relative='original_inference_selection_round150.json' if relative=='selection.json' else ('original_registry_alias_round150.json' if relative=='registry_alias_verification.json' else relative)
        expected[target_relative]=info['sha256']
    rows=[]
    for p in registry.CANDIDATE.rglob('*'):
        if not p.is_file():continue
        relative=p.relative_to(registry.CANDIDATE).as_posix()
        if relative.startswith('registration_sources/round150_full_scope/'):
            source=ROOT/relative.removeprefix('registration_sources/round150_full_scope/');assert source.is_file() and sha(source)==sha(p),p
        else:assert sha(p)==expected[relative],p
        rows.append({'registered_path':str(p),'sha256':sha(p)})
    folder=A/'service_owned_workflows_20261006/HuberSparse59_round150_full_registration_v6_20261009'
    assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='failed'
    code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_HuberSparse150_partial_registry_v29_20261009 import execute\nif __name__=='__main__':execute()\n"
    with (A/DRIVER).open('x',encoding='utf8') as f:f.write(code)
    inputs=[Path(__file__),A/DRIVER,A/'HuberSparse150_materialization_v27_20261009.json',A/'recover_HuberSparse150_materialization_v27_20261009.py',Path(registry.__file__),
        *(folder/n for n in ('job_definition.json','native_launch.json','service_execution.json','stderr.log'))]
    create(META,{'status':'passed_all_partial_registered_files_exact_before_idempotent_registry_resume_and_external_source_routing',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},'cached_files_verified':rows,
        'generated_scientific_sources_unchanged':True,'quality_scores_repeated':0,'native_fits_repeated':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('HuberSparse59_round150_full_registration_v7_20261009',DRIVER,[],{str(META):sha(META),str(A/DRIVER):sha(A/DRIVER)})
    create(A/'HuberSparse150_partial_registry_hidden_launch_v29_20261009.json',row)
    print({'owned_full_worker':row['owned_worker_pid'],'actual_cached_files_verified':len(rows)},flush=True)

if __name__=='__main__':main()
