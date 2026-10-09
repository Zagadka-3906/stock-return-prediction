"""Resolve publication collectors to the actual QA directories without changing any checks."""
from pathlib import Path
from contextlib import contextmanager
import sys,builtins,re,ast,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
BEFORE="qa = A / f'lossless_ranking_display_qa_v{qa_version}_20261006' / f'round{number}'"
AFTER="qa = A / f'lossless_ranking_display_qa_v{qa_version}_20261009' / f'round{number}'"
SOURCE=A/'collect_full_lossless_round_publication_20261006.py'

def corrected_namespace():
    original=SOURCE.read_text(encoding='utf8');assert original.count(BEFORE)==1
    text=original.replace(BEFORE,AFTER);assert text.replace(AFTER,BEFORE)==original
    namespace={'__file__':str(SOURCE),'__name__':'actual_QA_path_only_collector43'}
    exec(compile(text,str(SOURCE),'exec'),namespace);return namespace

@contextmanager
def installed():
    original=builtins.__import__;saved=[];seen=set()
    def checked(name,*args,**kwargs):
        module=original(name,*args,**kwargs)
        if re.fullmatch(r'collect_full_lossless_round(?:153|154|155|156)_qa(?:64|65|66|67)_20261009',name) and name not in seen:
            seen.add(name);namespace=module.namespace
            saved.append((namespace,namespace['collect']))
            namespace['collect']=corrected_namespace()['collect']
        return module
    builtins.__import__=checked
    try:yield
    finally:
        assert builtins.__import__ is checked;builtins.__import__=original
        for namespace,collect in saved:namespace['collect']=collect

def main():
    import importlib
    sources=[Path(__file__),SOURCE,A/'collect_full_lossless_round153_qa64_20261009.py',A/'verify_lossless_ranking_display_round153_v2_20261008.py']
    controls=[]
    actual=A/'lossless_ranking_display_qa_v64_20261009/round153/verification.json';proof=read(actual)
    assert proof['original_full_QA_result']['new_round_records']==78 and proof['original_full_QA_result']['connected_records']==15310
    assert proof['all_original_provenance_candidate_manifest_sorting_and_six_view_checks_passed']
    sources.append(actual)
    for number,qa,parents,gname in [(154,65,range(148,154),'prepare_BF16TwoSeed79_round154_sources_v1_20261009'),
        (155,66,range(148,155),'prepare_BF16Seed10_80_round155_sources_v1_20261009'),
        (156,67,range(148,156),'prepare_BF16Drop05_81_round156_sources_v1_20261009')]:
        generator=importlib.import_module(gname);sources.append(Path(generator.__file__))
        for parent in parents:
            generated=generator.generate(parent)
            collector=generated[f'collect_full_lossless_round{number}_qa{qa}_20261009.py']
            verifier=generated[f'verify_lossless_ranking_display_round{number}_v2_20261008.py']
            assert f'lossless_ranking_display_qa_v{qa}_20261009' in verifier
            assert "after = \"qa = A / f'lossless_ranking_display_qa_v{qa_version}_20261007'" in collector
            compile(collector,'frozen_original_collector','exec');corrected_namespace()
            controls.append({'round':number,'comparison_parent':parent,'QA_version':qa,
                'actual_verifier_directory':'20261009','legacy_collector_directory':'20261007',
                'resolver_changes_only_directory_constant':True,'all_original_collection_checks_preserved':True})
    create(A/'actual_QA_collector_path_controls_v43_20261009.json',{'status':'passed21_prospective_QA_paths_and_actual153_QA64_proof',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in dict.fromkeys(sources)},
        'controls':controls,'actual153_QA64_new_records':78,'actual153_connected_records':15310,
        'original_mathematics_and_all_QA_checks_unchanged':True,'new_quality_scores':0,'test_labels_read':False})
    print({'prospective_paths':len(controls),'actual153_QA64_passed':True},flush=True)
if __name__=='__main__':main()
