"""Retry the failed publication and dependent unstarted phases; retain all admitted150 math and proofs."""
from pathlib import Path
from contextlib import contextmanager
import sys,re,time,hashlib
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
META=A/'HuberSparse150_serial_publication_recovery_v18_20261009.json'
NAMES=['publish_HuberSparse59_evidence_v1_20261009.py','run_HuberSparse59_official_comparison_v2_20261009.py',
 'prepare_HuberSparse59_selected_candidate_v2_20261009.py','seal_HuberSparse59_selected_candidate_v2_20261009.py',
 'run_HuberSparse59_round150_full_registration_v2_20261009.py']
DRIVERS={n:re.sub(r'_v\d+_20261009.py$','_recovery_v18_20261009.py',n) for n in NAMES}
SERVICE_MAP={f'HuberSparse59_{stem}_v1_20261008':f'HuberSparse59_{stem}_v2_20261009' for stem in
 ('controls_main_publication','official_comparison','scores_main_publication','selected_candidate_preparation','selected_candidate_sealing','round150_full_registration')}

def routed(s):
    for old,new in SERVICE_MAP.items():s=s.replace(old,new)
    s=s.replace("out=A/f'HuberSparse59_{phase}_github_v1_20261008'","out=A/f'HuberSparse59_{phase}_github_v2_20261009'")
    s=s.replace('HuberSparse59_round150_actual_registration_v2_20261009','HuberSparse59_round150_actual_registration_recovery_v18_20261009')
    s=s.replace('run_HuberSparse59_round150_full_registration_v2_file_IO_20261008','run_HuberSparse59_round150_full_registration_recovery_v18_file_IO_20261009')
    return s

def execute(name,phase=None):
    meta=read(META)
    for f,d in meta['input_sha256'].items():assert sha(f)==d,f
    import sparse150152_publication_safe_receivers_v16_20261009 as previous
    import lossless_chunked_safe_main_runtime_v1_20261009 as safe
    import run_dependency_queue_v3_20261006 as io
    import prepare_HuberSparse59_round150_sources_v2_20261009 as g
    from serial_main_publication_mutex_v1_20261009 import installed as serial
    oldroute,oldsafe,oldcreate,oldpaths=previous.route,safe.installed,io.create,g.source_paths
    previous.route=lambda n,s:routed(oldroute(n,s)) if n==150 else oldroute(n,s)
    closure=[Path(__file__),META,A/'serial_main_publication_mutex_v1_20261009.py',A/'serial_main_publication_mutex_v1_20261009.json',*(A/n for n in DRIVERS.values())]
    g.source_paths=lambda:list(dict.fromkeys([*oldpaths(),*closure]))
    log=Path('E:/赛题五_本机临时/HuberSparse150_serial_publication_recovery_v18_20261009')/(DRIVERS[name].removesuffix('.py')+('_'+phase if phase else ''))
    @contextmanager
    def installed(_ignored):
        with oldsafe(log),serial(log/'serial_publication_mutex.json'):yield
    safe.installed=installed
    def pinned(path,value):
        p=Path(path)
        if isinstance(value,dict) and 'input_sha256' in value:
            value={**value,'input_sha256':{**value['input_sha256'],**meta['input_sha256'],str(META):sha(META)},
              'actual_serial_publication_recovery18_source_bindings_pinned':True}
        result=oldcreate(path,value)
        if p.name=='receipt.json' and re.fullmatch(r'HuberSparse59_(controls|scores)_github_v2_20261009',p.parent.name):
            phase=p.parent.name.split('_')[1];canonical=A/f'HuberSparse59_{phase}_github_v1_20261008/receipt.json'
            assert value['status']=='pushed_and_remote_head_verified'
            canonical.parent.mkdir(exist_ok=True);assert not canonical.exists();canonical.write_bytes(p.read_bytes());assert sha(canonical)==sha(p)
            oldcreate(log/'canonical_phase_receipt_reconciliation.json',{'actual_receipt':str(p),'canonical_receipt':str(canonical),
              'sha256':sha(p),'failed_original_phase_records_retained':True,'new_receipt_verified_main_commit':value['commit']})
        return result
    io.create=pinned
    try:previous.execute(150,name,phase)
    finally:previous.route=oldroute;safe.installed=oldsafe;io.create=oldcreate;g.source_paths=oldpaths

def prepare():
    admission=A/'HuberSparse59_round150_source_admission_v1_20261008.json';a=read(admission)
    assert a['actual_all5_annual_model_years_stage_replayed'] and a['actual_head_year_states_stage_replayed']==20
    for f,d in a['input_sha256'].items():assert sha(f)==d,f
    oldservices={};inputs=[Path(__file__),admission,A/'HuberSparse59_actual_controls_index_v1_20261008.json',
      A/'sparse150152_publication_safe_receivers_v16_20261009.py',A/'sparse150152_publication_safe_receivers_v16_20261009.json',
      A/'serial_main_publication_mutex_v1_20261009.py',A/'serial_main_publication_mutex_v1_20261009.json']
    assert read(A/'service_owned_workflows_20261006/PureRFFHuber128_round149_full_registration_v1_20261008/service_execution.json')['status']=='passed'
    for name in SERVICE_MAP:
        folder=A/'service_owned_workflows_20261006'/name;row=read(folder/'native_launch.json')
        assert not owned(row) and read(folder/'service_execution.json')['status']=='failed'
        oldservices[name]=read(folder/'service_execution.json');inputs.extend(folder/p for p in ('job_definition.json','native_launch.json','service_execution.json','stderr.log'))
    assert not list((A/'HuberSparse59_official_comparison_v1_20261008').glob('case*_official.json'))
    assert not (A/'optimization_20261003_r150').exists()
    for name in NAMES:
        inputs.append(A/name);compile(routed((A/name).read_text(encoding='utf8')),str(A/name),'exec')
        target=A/DRIVERS[name]
        s="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom recover_HuberSparse150_serial_publication_v18_20261009 import execute\n"
        if name.startswith('publish_'):s+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+repr(name)+",p.parse_args().phase)\n"
        else:s+="if __name__=='__main__':execute("+repr(name)+")\n"
        compile(s,str(target),'exec')
        with target.open('x',encoding='utf8') as f:f.write(s)
        inputs.append(target)
    create(META,{'status':'prepared_serial150_retry_after_verified_publication_main_head_race_before_any_score',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(f):sha(f) for f in inputs},'failed_original_services':oldservices,
      'service_map':SERVICE_MAP,'drivers':DRIVERS,'admitted_original_mathematics_unchanged':True,'actual_quality_scores_before_retry':0,
      'no_native_fits_repeated':True,'failed_phase_evidence_retained':True,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    specs=[('controls_main_publication',NAMES[0],['controls']),('official_comparison',NAMES[1],[]),('scores_main_publication',NAMES[0],['scores']),
      ('selected_candidate_preparation',NAMES[2],[]),('selected_candidate_sealing',NAMES[3],[]),('round150_full_registration',NAMES[4],[])]
    rows={}
    for stem,driver,args in specs:
        name=f'HuberSparse59_{stem}_v2_20261009';rows[name]=start(name,DRIVERS[driver],args,{str(META):sha(META),str(A/DRIVERS[driver]):sha(A/DRIVERS[driver])})
    create(A/'HuberSparse150_serial_publication_hidden_launches_v18_20261009.json',rows)
    print({n:r['owned_worker_pid'] for n,r in rows.items()},flush=True)

if __name__=='__main__':prepare()
