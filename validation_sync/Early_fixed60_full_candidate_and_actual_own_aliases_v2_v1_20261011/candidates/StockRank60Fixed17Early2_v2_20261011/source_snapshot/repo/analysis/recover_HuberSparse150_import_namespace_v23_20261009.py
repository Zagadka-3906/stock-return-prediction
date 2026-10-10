"""Preserve scientific import modules; retry only three failed post-score150 phases."""
from pathlib import Path
import sys, ast, re, time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'HuberSparse150_import_namespace_v23_20261009.json'
STEMS=('selected_candidate_preparation','selected_candidate_sealing','round150_full_registration')

def preserve_imports(original,routed):
    before=[x for x in ast.walk(ast.parse(original)) if isinstance(x,ast.ImportFrom)]
    after=[x for x in ast.walk(ast.parse(routed)) if isinstance(x,ast.ImportFrom)]
    assert len(before)==len(after)
    for x,y in zip(before,after):
        assert ast.dump(ast.Module(body=[ast.Import(names=x.names)],type_ignores=[]))==ast.dump(ast.Module(body=[ast.Import(names=y.names)],type_ignores=[]))
        if x.module!=y.module:
            routed,n=re.subn(r'(?m)^(\s*from\s+)'+re.escape(y.module)+r'(\s+import\s+)',lambda m:m[1]+x.module+m[2],routed)
            assert n>=1,(x.module,y.module)
    assert [x.module for x in ast.walk(ast.parse(routed)) if isinstance(x,ast.ImportFrom)]==[x.module for x in before]
    return routed

def routed(source):
    s=preserve_imports(source,BASE_ROUTE(source))
    for stem in STEMS:s=s.replace(f'HuberSparse59_{stem}_v3_20261009',f'HuberSparse59_{stem}_v4_20261009')
    return s.replace('actual_registration_recovery_v20','actual_registration_recovery_v23').replace('recovery_v20_file_IO','recovery_v23_file_IO')

def execute(name):
    global BASE_ROUTE
    meta=read(META)
    for f,d in meta['input_sha256'].items():assert sha(f)==d,f
    import recover_HuberSparse150_data_path_bindings_v20_20261009 as previous
    previous_read=previous.read;BASE_ROUTE=previous.routed;previous.routed=routed
    def bound_read(path):
        value=previous_read(path)
        if Path(path)==previous.META:
            value={**value,'drivers':meta['drivers'],'input_sha256':{**value['input_sha256'],**meta['input_sha256'],str(META):sha(META)}}
        return value
    previous.read=bound_read
    try:previous.execute(name)
    finally:previous.read=previous_read;previous.routed=BASE_ROUTE

def main():
    global BASE_ROUTE
    import recover_HuberSparse150_data_path_bindings_v20_20261009 as previous
    import recover_HuberSparse150_serial_publication_v18_20261009 as earlier
    previous.ORIGINAL_ROUTE=earlier.routed;BASE_ROUTE=previous.routed
    meta=read(previous.META);drivers=dict(meta['drivers']);checks=[]
    inputs=[Path(__file__),previous.META,Path(previous.__file__)]
    assert read(A/'service_owned_workflows_20261006/HuberSparse59_official_comparison_v3_20261009/service_execution.json')['status']=='passed'
    assert len(read(A/'HuberSparse59_official_comparison_v1_20261008/verification.json')['records'])==59
    for name in earlier.NAMES:
        p=A/name;original=p.read_text(encoding='utf8');corrected=routed(original);compile(corrected,str(p),'exec')
        mods=[x.module for x in ast.walk(ast.parse(corrected)) if isinstance(x,ast.ImportFrom)]
        assert mods==[x.module for x in ast.walk(ast.parse(original)) if isinstance(x,ast.ImportFrom)]
        checks.append({'source':name,'all_import_modules_exact_original':True,'compiled':True});inputs.append(p)
    names=earlier.NAMES[2:]
    for stem,name in zip(STEMS,names):
        folder=A/'service_owned_workflows_20261006'/f'HuberSparse59_{stem}_v3_20261009'
        assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='failed'
        inputs.extend(folder/x for x in ('native_launch.json','service_execution.json','stderr.log','job_definition.json'))
        target=A/re.sub(r'_v\d+_20261009.py$','_recovery_v23_20261009.py',name)
        code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_HuberSparse150_import_namespace_v23_20261009 import execute\nif __name__=='__main__':execute("+repr(name)+")\n"
        with target.open('x',encoding='utf8') as f:f.write(code)
        drivers[name]=target.name;inputs.append(target)
    assert not list((A/'HuberSparse59_selected_release_v1_20261008').glob('*.json'))
    create(META,{'status':'passed_five_actual_import_namespace_checks_before_three_post_score_phase_retries','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':{str(p):sha(p) for p in inputs},'drivers':drivers,'checks':checks,'actual_existing_quality_scores':59,
        'scientific_math_changed':False,'native_fits_repeated':0,'quality_scores_repeated':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={}
    for stem,name in zip(STEMS,names):
        sid=f'HuberSparse59_{stem}_v4_20261009';rows[sid]=start(sid,drivers[name],[],{str(META):sha(META),str(A/drivers[name]):sha(A/drivers[name])})
    create(A/'HuberSparse150_import_namespace_hidden_launches_v23_20261009.json',rows)
    print({sid:r['owned_worker_pid'] for sid,r in rows.items()},flush=True)

if __name__=='__main__':main()
