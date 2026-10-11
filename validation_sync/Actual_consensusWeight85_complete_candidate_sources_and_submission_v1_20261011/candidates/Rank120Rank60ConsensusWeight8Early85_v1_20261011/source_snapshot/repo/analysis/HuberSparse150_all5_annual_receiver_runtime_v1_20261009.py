"""Bind the real missing2023 native supplement into150 admission, phases and dispatch before scores."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
META=A/'HuberSparse150_all5_annual_receiver_runtime_v1_20261009.json'
COVERAGE=A/'sparse150151_all20_annual_native_coverage_v1_20261009.json'
DRIVERS={
    'verify_HuberSparse59_round150_sources_v1_20261009.py':'verify_HuberSparse59_round150_sources_v3_20261009.py',
    'publish_HuberSparse59_evidence_v1_20261009.py':'publish_HuberSparse59_evidence_v3_20261009.py',
    'dispatch_HuberSparse150_complete_pipeline_v1_20261009.py':'dispatch_HuberSparse150_complete_pipeline_v3_20261009.py'}

def sources():
    from HuberSparse150_import_dependency_closure_v1_20261009 import EXTRAS,PROOF,META as earlier
    pointer=A/'actual_HuberSparse18_year2023_native_supplement_location_v1_20261009.json'
    output=Path(read(pointer)['output'])
    return list(dict.fromkeys([Path(__file__),COVERAGE,A/'verify_sparse150151_all20_annual_native_coverage_v1_20261009.py',
        earlier,PROOF,*(A/n for n in EXTRAS),*(A/n for n in DRIVERS),*(A/n for n in DRIVERS.values()),pointer,*output.glob('*.json')]))

def prepare():
    proof=read(COVERAGE);assert len(proof['records'])==2
    current=next(r for r in proof['records'] if r['round']==150)
    assert current['actual_head_year_states']==20 and current['actual_native_cases']==current['actual_cold_cases']==90
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    from HuberSparse150_import_dependency_closure_v1_20261009 import META as earlier
    preceding=read(earlier)
    pins={**preceding['input_sha256'],**proof['input_sha256'],**{str(p):sha(p) for p in sources()}}
    for p in sources():
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    create(META,{'status':'frozen150_all5_annual_native90_and_cold90_extra_sources_before_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':pins,'own20_annual_states_all5_years_actual_native_replayed':True,'original72_and_additional18_proofs_separate_and_preserved':True,
        'actual_new_native_fits':0,'actual_new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})

def execute(name,*args):
    meta=read(META)
    for p,d in meta['input_sha256'].items():assert sha(p)==d,p
    import prepare_HuberSparse59_round150_sources_v2_20261009 as generator
    previous=generator.source_paths
    generator.source_paths=lambda:list(dict.fromkeys([*previous(),*sources(),META]))
    source=(A/name).read_text(encoding='utf8')
    if name.startswith('dispatch_'):
        source=source.replace('verify_HuberSparse59_round150_sources_v1_20261009.py',DRIVERS['verify_HuberSparse59_round150_sources_v1_20261009.py'])
        source=source.replace('publish_HuberSparse59_evidence_v1_20261009.py',DRIVERS['publish_HuberSparse59_evidence_v1_20261009.py'])
        source=source.replace('HuberSparse150_complete_hidden_launches_v1_20261009','HuberSparse150_complete_hidden_launches_v3_20261009')
    elif name.startswith('publish_'):
        source=source.replace("'actual_historical_native_hooks':54", "'actual_historical_native_hooks':54,'additional_own2023_native_hooks':18,'actual_total_native_hooks':90,'actual_total_cold_native_hooks':90,'all20_head_year_states_actual_stage_replayed':True")
    ns={'__name__':'actual150_all5_annual_stage_bound_runtime','__file__':str(A/DRIVERS[name])}
    exec(compile(source,str(A/name),'exec'),ns)
    if name.startswith('verify_'):
        original_create=ns['create']
        def bound_create(path,value):
            if Path(path).name in ('HuberSparse59_actual_controls_index_v1_20261008.json','HuberSparse59_round150_source_admission_v1_20261008.json'):
                value={**value,'input_sha256':{**value['input_sha256'],**meta['input_sha256'],str(META):sha(META)},
                    'actual_inherited_best_key_import_pinned':True,'actual_all5_annual_model_years_stage_replayed':True,
                    'actual_native_stage_cases':90,'actual_cold_native_cases':90,'actual_head_year_states_stage_replayed':20}
                if 'original_external_metadata' in value:
                    external={str(p):read(p) for p in sources() if not p.is_relative_to(ROOT) and p.suffix=='.json'}
                    value['original_external_metadata']={**value['original_external_metadata'],**external}
            return original_create(path,value)
        ns['create']=bound_create
    ns['main'](*args)

if __name__=='__main__':prepare()
