"""Attach tested publication safeguards to unadmitted150-152 pipelines; preserve canonical math."""
from pathlib import Path
import sys,ast,re,os
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
META=A/'sparse150152_publication_safe_receivers_v16_20261009.json'
CONFIG={
 150:('HuberSparse150_all5_annual_receiver_runtime_v1_20261009','prepare_HuberSparse59_round150_sources_v2_20261009',[
 'verify_HuberSparse59_round150_sources_v1_20261009.py','publish_HuberSparse59_evidence_v1_20261009.py','run_HuberSparse59_official_comparison_v2_20261009.py',
 'prepare_HuberSparse59_selected_candidate_v2_20261009.py','seal_HuberSparse59_selected_candidate_v2_20261009.py','run_HuberSparse59_round150_full_registration_v2_20261009.py','dispatch_HuberSparse150_complete_pipeline_v1_20261009.py']),
 151:('RFFSparse151_source_closure_receiver_runtime_v1_20261009','prepare_RFFSparse59_round151_sources_v1_20261009',[
 'verify_RFFSparse59_round151_sources_v1_20261009.py','publish_RFFSparse59_evidence_v2_20261009.py','run_RFFSparse59_official_comparison_v3_20261009.py',
 'prepare_RFFSparse59_selected_candidate_v3_20261009.py','seal_RFFSparse59_selected_candidate_v3_20261009.py','run_RFFSparse59_round151_full_registration_v3_20261009.py','dispatch_RFFSparse151_complete_pipeline_v1_20261009.py']),
 152:(None,'prepare_SparseAfter14829_round152_sources_v1_20261009',[
 'verify_SparseAfter14829_round152_sources_v1_20261009.py','publish_SparseAfter14829_evidence_v1_20261009.py','run_SparseAfter14829_official_comparison_v2_20261009.py',
 'prepare_SparseAfter14829_selected_candidate_v2_20261009.py','seal_SparseAfter14829_selected_candidate_v2_20261009.py','run_SparseAfter14829_round152_full_registration_v2_20261009.py','dispatch_SparseAfter148152_complete_pipeline_v1_20261009.py'])}
MAP={number:{n:re.sub(r'_v\d+_20261009.py$','_publication_v16_20261009.py',n) for n in row[2]} for number,row in CONFIG.items()}

def route(number,s):
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(MAP[number],key=len,reverse=True)))
    s=pattern.sub(lambda m:MAP[number][m[0]],s)
    s=re.sub(r'complete_hidden_launches_v[123]_20261009','complete_hidden_launches_publication_v16_20261009',s)
    if number==152:
        s=s.replace('SparseAfter14860_native_historical_calendar_controls_v1_20261009','SparseAfter14860_native_historical_calendar_controls_v2_20261009')
        s=s.replace('SparseAfter14825_full_historical_controls_v1_20261009','SparseAfter14825_full_historical_controls_v2_20261009')
    return s

def execute(number,name,phase=None):
    meta=read(META)
    for p,d in meta['input_sha256'].items():assert sha(p)==d,p
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for offset,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):
        os.environ[f'GIT_CONFIG_KEY_{count+offset}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+offset}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    import importlib,run_dependency_queue_v3_20261006 as io
    g=importlib.import_module(CONFIG[number][1]);paths=g.source_paths;extras=[Path(__file__),META,*(A/n for n in MAP[number].values()),A/'lossless_chunked_safe_main_runtime_v1_20261009.py',A/'lossless_chunked_safe_main_runtime_v1_20261009.json']
    g.source_paths=lambda:list(dict.fromkeys([*paths(),*extras]))
    before_create=io.create
    def pinned(path,value):
        p=Path(path)
        if isinstance(value,dict) and 'input_sha256' in value and ('source_admission' in p.name or 'actual_controls_index' in p.name):
            value={**value,'input_sha256':{**value['input_sha256'],**meta['input_sha256'],str(META):sha(META)},'verified_publication_only_chunking_and_index_guards_bound':True}
        return before_create(path,value)
    io.create=pinned
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed
    log=Path('E:/赛题五_本机临时/sparse150152_safe_publication_v16_20261009')/(MAP[number][name].removesuffix('.py')+('_'+phase if phase else ''))
    try:
        with installed(log):
            runtime=CONFIG[number][0]
            if runtime is None:
                ns={'__file__':str(A/MAP[number][name]),'__name__':'actual152_publication_safe_execution'}
                exec(compile(route(number,(A/name).read_text(encoding='utf8')),str(A/name),'exec'),ns)
                ns['main'](*([phase] if phase else []))
            else:
                original=importlib.import_module(runtime);tree=ast.parse(Path(original.__file__).read_text(encoding='utf8'))
                fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='execute')
                target=next(n for n in ast.walk(fn) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='source' for t in n.targets))
                target.value=ast.Call(func=ast.Name(id='ROUTE_PUBLICATION_ONLY',ctx=ast.Load()),args=[target.value],keywords=[])
                ns={**original.__dict__,'DRIVERS':{**original.DRIVERS,**MAP[number]},'ROUTE_PUBLICATION_ONLY':lambda s:route(number,s)}
                exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(Path(__file__)),'exec'),ns)
                ns['execute'](name,*([phase] if phase else []))
    finally:io.create=before_create

def prepare():
    paths=[Path(__file__),A/'lossless_chunked_safe_main_runtime_v1_20261009.py',A/'lossless_chunked_safe_main_runtime_v1_20261009.json']
    for number,(runtime,gen,names) in CONFIG.items():
        if runtime:paths.extend([A/(runtime+'.py'),A/(runtime+'.json')])
        paths.append(A/(gen+'.py'))
        for n in names:
            assert (A/n).is_file();compile(route(number,(A/n).read_text(encoding='utf8')),str(A/n),'exec');paths.append(A/n)
            new=MAP[number][n];s="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom sparse150152_publication_safe_receivers_v16_20261009 import execute\n"
            if n.startswith('publish_'):s+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+str(number)+','+repr(n)+",p.parse_args().phase)\n"
            else:s+="if __name__=='__main__':execute("+str(number)+','+repr(n)+")\n"
            compile(s,str(A/new),'exec')
            with (A/new).open('x',encoding='utf8') as f:f.write(s)
            paths.append(A/new)
    create(META,{'status':'prepared21_publication_safe_receivers_before150151152_quality_admission','input_sha256':{str(p):sha(p) for p in paths},'maps':MAP,
        'original_scientific_generated_sources_unchanged':True,'new_quality_scores':0,'new_future_inference':0,'test_labels_read':False})
    print('21 receiver wrappers prepared; scientific generated bytes unchanged.')

if __name__=='__main__':prepare()
