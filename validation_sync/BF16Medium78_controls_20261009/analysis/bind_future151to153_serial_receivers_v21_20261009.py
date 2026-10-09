"""Keep admitted science paths and bytes; update chronological service dependencies and serialize Git."""
from pathlib import Path
from contextlib import contextmanager
import sys,re,os,time,ast,importlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'future151to153_serial_receiver_binding_v21_20261009.json'
PREFIX={151:'RFFSparse59',152:'SparseAfter14829',153:'BF16Medium78'}
SERVICE_MAP={'HuberSparse59_round150_full_registration_v1_20261008':'HuberSparse59_round150_full_registration_v3_20261009'}
for n in (151,152):
    for stem in ('round'+str(n)+'_source_admission','controls_main_publication','official_comparison','scores_main_publication',
      'selected_candidate_preparation','selected_candidate_sealing','round'+str(n)+'_full_registration'):
        SERVICE_MAP[f'{PREFIX[n]}_{stem}_v1_20261009']=f'{PREFIX[n]}_{stem}_v2_20261009'
for n,label in ((151,'RFFSparse151'),(152,'SparseAfter148152'),(153,'BF16Medium153')):
    SERVICE_MAP[f'{label}_prior_complete_forecast_duplicate_audit_v1_20261009']=f'{label}_prior_complete_forecast_duplicate_audit_v2_20261009'

def route(number,s):
    for old,new in SERVICE_MAP.items():s=s.replace(old,new)
    for n in (151,152):
        s=re.sub(r"(A\s*/\s*['\"])"+PREFIX[n]+r'_official_comparison_v2_20261009',r'\1'+PREFIX[n]+'_official_comparison_v1_20261009',s)
    s=re.sub(r'complete_hidden_launches(?:_publication)?_v(?:1|16|17)_20261009','complete_hidden_launches_serial_v21_20261009',s)
    if number==153:s=s.replace("meta=A/'BF16Medium153_complete_pipeline_preparation_v17_20261009.json'","meta=A/'future151to153_serial_receiver_binding_v21_20261009.json'")
    return s

def execute(number,name,phase=None):
    m=read(META)
    for f,d in m['input_sha256'].items():assert sha(f)==d,f
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(k,v) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):
        os.environ[f'GIT_CONFIG_KEY_{count+i}']=k;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=v
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    import run_dependency_queue_v3_20261006 as io
    import lossless_chunked_safe_main_runtime_v1_20261009 as safe
    import sparse150152_publication_safe_receivers_v16_20261009 as earlier
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    generator=importlib.import_module({151:'prepare_RFFSparse59_round151_sources_v1_20261009',152:'prepare_SparseAfter14829_round152_sources_v1_20261009',153:'prepare_BF16Medium78_round153_sources_v1_20261009'}[number])
    oldpaths,oldcreate,oldroute,oldsafe=generator.source_paths,io.create,earlier.route,safe.installed
    extra=[Path(__file__),META,A/'serial_main_publication_mutex_v1_20261009.py',A/'serial_main_publication_mutex_v1_20261009.json',*(A/n for n in m['drivers'][str(number)].values())]
    generator.source_paths=lambda:list(dict.fromkeys([*oldpaths(),*extra]))
    log=Path('E:/赛题五_本机临时/future151to153_serial_receiver_v21_20261009')/(str(number)+'_'+m['drivers'][str(number)][name].removesuffix('.py')+('_'+phase if phase else ''))
    @contextmanager
    def installed(_ignored):
        with oldsafe(log),serial(log/'serial_publication_mutex.json'):yield
    safe.installed=installed
    maps={n:{**earlier.MAP.get(n,{}),**m['drivers'][str(n)]} for n in (151,152)}
    oldmaps=earlier.MAP
    earlier.MAP={**earlier.MAP,**maps}
    earlier.route=lambda n,s:route(n,oldroute(n,s))
    def pinned(path,value):
        if isinstance(value,dict) and 'input_sha256' in value:
            value={**value,'input_sha256':{**value['input_sha256'],**m['input_sha256'],str(META):sha(META)},
              'actual_v21_service_dependencies_separate_from_original_scientific_artifact_paths':True}
        return oldcreate(path,value)
    io.create=pinned
    try:
        is_direct=name.startswith('verify_') and 'prior_complete_forecast' in name
        if name.startswith('dispatch_'):is_direct=True
        if number in (151,152) and not is_direct:earlier.execute(number,name,phase)
        else:
            with installed(log):
                text=route(number,(A/name).read_text(encoding='utf8'))
                if name.startswith('dispatch_') and number in (151,152):
                    for old,new in m['drivers'][str(number)].items():text=text.replace(old,new)
                ns={'__file__':str(A/m['drivers'][str(number)][name]),'__name__':'actual_serial_chronological_receiver21'}
                exec(compile(text,str(A/name),'exec'),ns)
                if number==153 and (name.startswith('seal_') or 'full_registration' in name):
                    from BF16Medium153_storage_v1_20261009 import installed_transfer
                    from verified_TLS_Git_retry_runtime_v2_20261008 import installed as git_io
                    with installed_transfer(),git_io(log/'file_backed_git'):ns['main']()
                else:ns['main'](*([phase] if phase else []))
    finally:
        generator.source_paths=oldpaths;io.create=oldcreate;earlier.route=oldroute;earlier.MAP=oldmaps;safe.installed=oldsafe

def prepare():
    import sparse150152_publication_safe_receivers_v16_20261009 as earlier
    groups={n:[*earlier.CONFIG[n][2],f'verify_{label}_prior_complete_forecast_duplicate_audit_v1_20261009.py'] for n,label in ((151,'RFFSparse151'),(152,'SparseAfter148152'))}
    groups[153]=['verify_BF16Medium78_round153_sources_v1_20261009.py','publish_BF16Medium78_evidence_v2_20261009.py',
      'run_BF16Medium78_official_comparison_v2_20261009.py','prepare_BF16Medium78_selected_candidate_v1_20261009.py',
      'seal_BF16Medium78_selected_candidate_v1_20261009.py','run_BF16Medium78_round153_full_registration_v3_20261009.py',
      'dispatch_BF16Medium153_complete_pipeline_v17_20261009.py','verify_BF16Medium153_prior_complete_forecast_duplicate_audit_v1_20261009.py']
    sources=[Path(__file__),A/'serial_main_publication_mutex_v1_20261009.py',A/'serial_main_publication_mutex_v1_20261009.json',
      A/'sparse150152_publication_safe_receivers_v16_20261009.py',A/'sparse150152_publication_safe_receivers_v16_20261009.json',
      A/'HuberSparse150_data_path_bindings_v20_20261009.json'];drivers={};checks=[]
    for n,names in groups.items():
        drivers[str(n)]={}
        for name in names:
            p=A/name;text=route(n,p.read_text(encoding='utf8'));tree=ast.parse(text);compile(text,str(p),'exec');sources.append(p)
            if 'official_comparison' in name and name.startswith('run_'):
                node=next(x for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OUT' for t in x.targets))
                assert ast.unparse(node.value)=="A / '"+PREFIX[n]+"_official_comparison_v1_20261009'"
            checks.append({'round':n,'source':name,'source_compiles':True,'canonical_scientific_data_path_preserved':True})
            target=A/re.sub(r'_v\d+_20261009.py$','_serial_v21_20261009.py',name)
            code="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom bind_future151to153_serial_receivers_v21_20261009 import execute\n"
            if name.startswith('publish_'):code+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+str(n)+','+repr(name)+",p.parse_args().phase)\n"
            else:code+="if __name__=='__main__':execute("+str(n)+','+repr(name)+")\n"
            compile(code,str(target),'exec')
            with target.open('x',encoding='utf8') as f:f.write(code)
            drivers[str(n)][name]=target.name;sources.append(target)
    own153=read(A/'BF16Medium153_complete_pipeline_preparation_v17_20261009.json')['receiver_specs']
    specs153=[]
    for sid,driver,args in own153:
        if driver=='run_BF16Medium153_safe_registration_v17_20261009.py':driver='run_BF16Medium78_round153_full_registration_v3_20261009.py'
        specs153.append([sid,drivers['153'][driver],args])
    create(META,{'status':'prepared24_serial_receivers_with_unchanged151152153_science_and_current_chronological_dependencies',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in sources},'drivers':drivers,
      'service_map':SERVICE_MAP,'receiver_specs':specs153,'source_binding_checks':checks,
      'future_quality_scores_not_yet_claimed':True,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={};superseded=[]
    for n,label in ((151,'RFFSparse151'),(152,'SparseAfter148152'),(153,'BF16Medium153')):
        dup=f'verify_{label}_prior_complete_forecast_duplicate_audit_v1_20261009.py'
        dispatch={151:'dispatch_RFFSparse151_complete_pipeline_v1_20261009.py',152:'dispatch_SparseAfter148152_complete_pipeline_v1_20261009.py',153:'dispatch_BF16Medium153_complete_pipeline_v17_20261009.py'}[n]
        for sid,name in [(f'{label}_prior_complete_forecast_duplicate_audit_v2_20261009',dup),(f'{label}_complete_chronological_dispatch_serial_v21_20261009',dispatch)]:
            rows[sid]=start(sid,drivers[str(n)][name],[],{str(META):sha(META),str(A/drivers[str(n)][name]):sha(A/drivers[str(n)][name])})
        olddup=f'{label}_prior_complete_forecast_duplicate_audit_v1_20261009'
        olddispatch={151:'RFFSparse151_complete_chronological_dispatch_publication_v16_20261009',152:'SparseAfter148152_complete_chronological_dispatch_publication_v16_20261009',153:'BF16Medium153_complete_chronological_dispatch_v17_20261009'}[n]
        for oldsid,newkey in [(olddup,f'{label}_prior_complete_forecast_duplicate_audit_v2_20261009'),(olddispatch,f'{label}_complete_chronological_dispatch_serial_v21_20261009')]:
            oldrow=read(A/'service_owned_workflows_20261006'/oldsid/'native_launch.json')
            if not owned(oldrow):continue
            from handoff_joint_goss_round97_full_execution_20261006 import stack,suspended_idle,retire_suspended
            line=next(line for line in stack(oldrow['owned_worker_pid']).splitlines() if '    closed (' in line)
            parent,worker,idle=suspended_idle(oldrow,line)
            try:retire_suspended(oldrow,rows[newkey])
            except BaseException:
                if parent.is_running():parent.resume()
                if worker.is_running():worker.resume()
                raise
            superseded.append({'old':oldrow,'new':rows[newkey],'owned_idle_stack':idle,'scientific_jobs_retired':0})
    create(A/'future151to153_serial_hidden_launches_v21_20261009.json',{'launches':rows,'old_idle_handoffs':superseded,'scientific_jobs_retired':0})
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)

if __name__=='__main__':prepare()
