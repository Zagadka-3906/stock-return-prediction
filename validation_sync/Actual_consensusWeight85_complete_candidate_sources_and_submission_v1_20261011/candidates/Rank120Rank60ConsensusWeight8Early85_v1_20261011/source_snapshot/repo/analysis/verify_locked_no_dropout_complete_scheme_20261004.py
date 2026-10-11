"""Replay actual complete scheme checks under scoped immutable SHA reuse."""
from pathlib import Path
import importlib.util
import json
import sys
import time
import traceback
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis')]
from locked_read_hash_cache_20261004 import LockedReadHashCache,fresh_sha
OUT=ROOT/'analysis/locked_no_dropout_complete_scheme_preflight_20261004'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2)

def main():
    import psutil
    while psutil.virtual_memory().available<8*2**30:time.sleep(10)
    original=ROOT/'analysis/no_dropout_seed_complete_scheme_preflight_20261004'
    old=read(original/'verification.json');assert old['status']=='passed' and old['new_quality_scores']==0
    reuse=ROOT/'analysis/locked_no_dropout_model_reuse_preflight_20261004/verification.json'
    assert read(reuse)['status']=='passed'
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    expected={}
    for manifest in (ROOT/'analysis/locked_ensemble_provenance_preflight_20261004/actual_validated_hash_inputs.json',
            original/'verification.json',ROOT/'analysis/no_dropout_seed_future_models_qa_20261004/verification.json'):
        for p,d in read(manifest)['input_sha256'].items():
            if p in expected:assert expected[p]==d,p
            expected[p]=d
    import optimize_training_round53, optimize_training_round54
    import finalize_training_round53, finalize_training_round54
    source=ROOT/'analysis/verify_no_dropout_seed_complete_scheme_20261004.py'
    spec=importlib.util.spec_from_file_location('isolated_locked_complete_scheme_checker_20261004',source)
    checker=importlib.util.module_from_spec(spec);sys.modules[spec.name]=checker;spec.loader.exec_module(checker)
    checker.OUT=OUT/'replayed_scheme'
    sources=[Path(__file__),source,ROOT/'analysis/locked_read_hash_cache_20261004.py',original/'verification.json',reuse]
    hashes={str(p.resolve()):fresh_sha(p) for p in sources}
    write(OUT/'frozen_before_controls.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':hashes,'locked_immutable_input_sha256':expected,
        'scope':'Unmodified actual complete R53/R54 prototype checker, isolated output folder, scoped SHA binding only. Compare all four final full-future CSVs against original actual implementation checks.',
        'new_quality_scores':0,'test_labels_read':False,'live_queued_sources_changed':False})
    bindings=[];seen=set()
    for name,module in sorted(sys.modules.copy().items()):
        file=getattr(module,'__file__',None)
        if not file or Path(file).resolve().parent!=ROOT/'analysis':continue
        for obj in (module,*[v for v in vars(module).values() if isinstance(v,SimpleNamespace)]):
            if id(obj) not in seen and callable(getattr(obj,'sha',None)):
                bindings.append((obj,obj.sha));seen.add(id(obj))
    assert bindings
    started=time.perf_counter();failure=None
    try:
        with LockedReadHashCache(expected) as cache:
            try:
                for obj,_ in bindings:obj.sha=cache.sha
                checker.main()
            finally:
                for obj,function in bindings:obj.sha=function
            hits,fallback=cache.hits,cache.fresh_calls
        assert all(obj.sha is function for obj,function in bindings)
        result=read(checker.OUT/'verification.json');assert result['status']=='passed' and result['new_quality_scores']==0
        csv_controls={}
        for label in old['candidate_verification_sha256']:
            prior=original/label/'candidate/submission.csv';new=checker.OUT/label/'candidate/submission.csv'
            assert fresh_sha(prior)==fresh_sha(new),label
            csv_controls[label]={'full1599600_row_return_CSV_byte_identical':True,'sha256':fresh_sha(new)}
        assert hits>0
        for p,d in hashes.items():assert fresh_sha(p)==d,p
        hashes[str((checker.OUT/'verification.json').resolve())]=fresh_sha(checker.OUT/'verification.json')
        write(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'all_original_actual_complete_scheme_controls_passed_under_hash_reuse':True,
            'all_four_original_future_CSVs_byte_identical':csv_controls,
            'unmodified_original_checker_source':str(source),'scoped_sha_bindings':len(bindings),
            'locked_immutable_inputs':len(expected),'cache_hits':hits,'nonsealed_paths_rehashed':fallback,
            'complete_seconds_including_setup_andexit':time.perf_counter()-started,
            'original_namespaces_restored':True,'background_andfilesystem_cache_not_matched':True,
            'adopted_in_live_queued_rounds':False,'new_quality_scores':0,'test_labels_read':False,
            'hardware_boundary_established':False,'input_sha256':hashes})
        print('Locked complete-scheme andfour exact future CSV controls passed',flush=True)
    except BaseException:
        failure=traceback.format_exc()
        write(OUT/'failure.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'traceback':failure,
            'all_sha_bindings_restored':all(obj.sha is f for obj,f in bindings),'new_quality_scores':0})
        raise

if __name__=='__main__':main()
