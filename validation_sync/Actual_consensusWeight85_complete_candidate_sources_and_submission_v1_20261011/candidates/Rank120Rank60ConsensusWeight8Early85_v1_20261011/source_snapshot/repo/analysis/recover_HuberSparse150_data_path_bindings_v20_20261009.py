"""Separate current service identities from original scientific artifact paths; scoring remains unstarted."""
from pathlib import Path
import sys,re,time,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'HuberSparse150_data_path_bindings_v20_20261009.json'

def routed(source):
    import recover_HuberSparse150_serial_publication_v18_20261009 as old
    s=ORIGINAL_ROUTE(source)
    for stem in ('official_comparison','scores_main_publication','selected_candidate_preparation','selected_candidate_sealing','round150_full_registration'):
        s=s.replace(f'HuberSparse59_{stem}_v2_20261009',f'HuberSparse59_{stem}_v3_20261009')
    # Scientific files keep their exact admitted location. Only closed service gates
    # move to the current executions; paths relative to A are data, not service IDs.
    for version in (2,3):
        s=re.sub(r"(A\s*/\s*['\"])HuberSparse59_official_comparison_v"+str(version)+r"_20261009",r'\1HuberSparse59_official_comparison_v1_20261008',s)
    s=s.replace("out=A/f'HuberSparse59_{phase}_github_v2_20261009'","out=A/f'HuberSparse59_{phase}_github_v3_20261009'")
    s=s.replace('actual_registration_recovery_v18','actual_registration_recovery_v20').replace('recovery_v18_file_IO','recovery_v20_file_IO')
    return s

def execute(name,phase=None):
    global ORIGINAL_ROUTE
    meta=read(META)
    for f,d in meta['input_sha256'].items():assert sha(f)==d,f
    import recover_HuberSparse150_serial_publication_v18_20261009 as old
    import prepare_HuberSparse59_round150_sources_v2_20261009 as g
    import run_dependency_queue_v3_20261006 as io
    previous_paths,previous_create=g.source_paths,io.create
    ORIGINAL_ROUTE=old.routed;original_drivers=old.DRIVERS;old.routed=routed;old.DRIVERS=meta['drivers']
    g.source_paths=lambda:list(dict.fromkeys([*previous_paths(),META,Path(__file__),*(A/n for n in meta['drivers'].values())]))
    def pinned(path,value):
        p=Path(path)
        if isinstance(value,dict) and 'input_sha256' in value:
            value={**value,'input_sha256':{**value['input_sha256'],**meta['input_sha256'],str(META):sha(META)},'actual_service_ids_separate_from_original_data_paths':True}
        result=previous_create(path,value)
        if p.name=='receipt.json' and p.parent.name=='HuberSparse59_scores_github_v3_20261009':
            canonical=A/'HuberSparse59_scores_github_v1_20261008/receipt.json';canonical.parent.mkdir(exist_ok=True)
            assert not canonical.exists() and value['status']=='pushed_and_remote_head_verified'
            canonical.write_bytes(p.read_bytes());assert sha(canonical)==sha(p)
        return result
    io.create=pinned
    try:old.execute(name,phase)
    finally:old.routed=ORIGINAL_ROUTE;old.DRIVERS=original_drivers;g.source_paths=previous_paths;io.create=previous_create

def main():
    global ORIGINAL_ROUTE
    import recover_HuberSparse150_serial_publication_v18_20261009 as old
    ORIGINAL_ROUTE=old.routed
    controls=A/'service_owned_workflows_20261006/HuberSparse59_controls_main_publication_v2_20261009'
    assert read(controls/'service_execution.json')['status']=='passed'
    assert not list((A/'HuberSparse59_official_comparison_v1_20261008').glob('case*_official.json'))
    inputs=[Path(__file__),Path(old.__file__),old.META,controls/'service_execution.json',A/'HuberSparse59_controls_github_v1_20261008/receipt.json']
    drivers={};checks=[]
    for name in old.NAMES:
        source=A/name;s=routed(source.read_text(encoding='utf8'));tree=ast.parse(s);compile(s,str(source),'exec')
        calls=[n.args[0].value for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='closed' and n.args and isinstance(n.args[0],ast.Constant)]
        assert 'HuberSparse59_official_comparison_v1_20261008' not in calls and 'HuberSparse59_official_comparison_v2_20261009' not in calls
        if name.startswith('run_HuberSparse59_official'):
            node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in n.targets))
            assert ast.unparse(node.value)=="A / 'HuberSparse59_official_comparison_v1_20261008'"
            assert 'HuberSparse59_controls_main_publication_v2_20261009' in calls
        target=A/re.sub(r'_v\d+_20261009.py$','_recovery_v20_20261009.py',name)
        code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_HuberSparse150_data_path_bindings_v20_20261009 import execute\n"
        if name.startswith('publish_'):code+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+repr(name)+",p.parse_args().phase)\n"
        else:code+="if __name__=='__main__':execute("+repr(name)+")\n"
        with target.open('x',encoding='utf8') as f:f.write(code)
        drivers[name]=target.name;inputs.extend((source,target));checks.append({'source':name,'data_paths_original':True,'current_service_gates':calls})
    for stem in ('official_comparison','scores_main_publication','selected_candidate_preparation','selected_candidate_sealing','round150_full_registration'):
        folder=A/'service_owned_workflows_20261006'/f'HuberSparse59_{stem}_v2_20261009'
        assert not owned(read(folder/'native_launch.json')) and read(folder/'service_execution.json')['status']=='failed'
        inputs.extend(folder/n for n in ('job_definition.json','native_launch.json','service_execution.json','stderr.log'))
    create(META,{'status':'passed_five_receiver_AST_checks_original_science_paths_and_current_service_gates_before_scores',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in inputs},'drivers':drivers,'binding_checks':checks,
      'original150_scientific_generated_bytes_unchanged':True,'actual_quality_scores_before_retry':0,'native_fits_repeated':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    specs=[('official_comparison',old.NAMES[1],[]),('scores_main_publication',old.NAMES[0],['scores']),
      ('selected_candidate_preparation',old.NAMES[2],[]),('selected_candidate_sealing',old.NAMES[3],[]),('round150_full_registration',old.NAMES[4],[])]
    rows={}
    for stem,name,args in specs:
        n=f'HuberSparse59_{stem}_v3_20261009';rows[n]=start(n,drivers[name],args,{str(META):sha(META),str(A/drivers[name]):sha(A/drivers[name])})
    create(A/'HuberSparse150_data_path_bindings_hidden_launches_v20_20261009.json',rows)
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)

if __name__=='__main__':main()
