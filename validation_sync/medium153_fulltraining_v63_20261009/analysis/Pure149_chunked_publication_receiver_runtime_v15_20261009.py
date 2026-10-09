"""Retain149 scientific source bytes and attach verified publication-only safeguards."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
import recover_actual149152_after_chunked148_v14_20261009 as prior
META=A/'Pure149_chunked_publication_receiver_runtime_v15_20261009.json'
CORE={k:v.replace('_v'+v.split('_v')[-1].split('_')[0]+'_20261009.py','_publication_v15_20261009.py') for k,v in prior.CORE.items()}

def execute(original,phase=None):
    meta=read(META)
    for p,d in meta['input_sha256'].items():assert sha(p)==d,p
    prior.CORE.update(CORE)
    import prepare_PureRFFHuber128_round149_sources_v2_20261008 as g
    source_paths=g.source_paths
    extras=[Path(__file__),META,A/'lossless_chunked_safe_main_runtime_v1_20261009.py',A/'lossless_chunked_safe_main_runtime_v1_20261009.json',*(A/n for n in CORE.values())]
    g.source_paths=lambda:list(dict.fromkeys([*source_paths(),*extras]))
    if original.startswith('dispatch_'):
        import resume_pending149_verified_gates_v6_20261009 as base
        route=base.routed
        base.routed=lambda s,dispatcher=False:route(s,dispatcher).replace('complete_hidden_launches_v11_20261009','complete_hidden_launches_publication_v15_20261009')
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed
    name=CORE[original].removesuffix('.py')+('_'+phase if phase else '')
    with installed(Path('E:/赛题五_本机临时/Pure149_publication_safe_runtime_v15_20261009')/name):prior.execute(original,phase)

def prepare():
    products=[]
    for original,new in CORE.items():
        s="from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]\nfrom Pure149_chunked_publication_receiver_runtime_v15_20261009 import execute\n"
        if original.startswith('publish_'):s+="if __name__=='__main__':\n import argparse\n p=argparse.ArgumentParser();p.add_argument('phase',choices=('controls','scores'));execute("+repr(original)+",p.parse_args().phase)\n"
        else:s+="if __name__=='__main__':execute("+repr(original)+")\n"
        compile(s,str(A/new),'exec')
        with (A/new).open('x',encoding='utf8') as f:f.write(s)
        products.append(A/new)
    inputs=[Path(__file__),Path(prior.__file__),prior.META,*products,A/'lossless_chunked_safe_main_runtime_v1_20261009.py',A/'lossless_chunked_safe_main_runtime_v1_20261009.json']
    create(META,{'status':'prepared_149_original32_canonical_sources_unchanged_with_independently_verified_lossless_chunk_and_index_guards',
        'input_sha256':{str(p):sha(p) for p in inputs},'CORE':CORE,'new_quality_scores':0,'scientific_source_bytes_changed':False})
    print(CORE,flush=True)

if __name__=='__main__':prepare()
