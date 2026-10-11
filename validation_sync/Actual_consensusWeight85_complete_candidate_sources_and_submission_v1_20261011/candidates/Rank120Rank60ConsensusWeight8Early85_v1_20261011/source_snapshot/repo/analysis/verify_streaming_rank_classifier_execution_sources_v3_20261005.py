"""Execute actual driver bindings and inspect runnable candidate source closure."""
from pathlib import Path
import ast
import hashlib
import importlib
import json
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT),str(A)]


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    from predict_streaming_rank_classifier_scheme_codec_v3_20261005 import copy_actual_sources
    import publish_training_round as publication
    driver=A/'run_streaming_rank_classifier_round_v3_20261005.py'
    tree=ast.parse(driver.read_text(encoding='utf-8'))
    body=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='main').body
    start=next(i for i,node in enumerate(body) if isinstance(node,ast.Assign)
        and any(isinstance(target,ast.Name) and target.id=='module' for target in node.targets))
    finish=next(i for i in range(start,len(body)) if isinstance(body[i],ast.FunctionDef) and body[i].name=='infer_selected')
    bindings=body[start:finish]
    assert len(bindings)==5
    executable=compile(ast.fix_missing_locations(ast.Module(body=bindings,type_ignores=[])),str(driver),'exec')
    out=A/'streaming_rank_classifier_execution_source_preflight_v3_20261005'
    assert not out.exists()
    out.mkdir()
    sources={Path(__file__),driver,A/'publish_training_round.py',A/'nystrom_ridge_release_engine_20261004.py',
        A/'predict_streaming_rank_classifier_scheme_codec_v3_20261005.py',
        A/'streaming_rank_classifier_candidate_source_generation_v3_20261005.json'}
    controls=[]
    for number in (79,80):
        namespace={'number':number,'importlib':importlib,'sys':sys}
        exec(executable,namespace)
        experiment,release=namespace['module'],namespace['release']
        assert publication.importlib.import_module(f'optimize_training_round{number}') is experiment
        assert publication.importlib.import_module(f'finalize_training_round{number}') is release
        assert release.OUT==experiment.OUT==A/f'optimization_20261003_r{number}'
        assert Path(experiment.__file__)==A/f'optimize_training_round{number}_v3.py'
        assert Path(release.__file__)==A/f'finalize_training_round{number}_v3.py'
        for name in ('selected','select','calibrate'):
            assert experiment in [cell.cell_contents for cell in getattr(release,name).__closure__]
        assert release.ReleaseContext.__bases__==(experiment.Context,)
        candidate=out/f'actual_candidate_source_control_r{number}'
        ns=SimpleNamespace(ROOT=ROOT,NUMBER=number)
        record=copy_actual_sources(ns,candidate)
        # Reproduce the historical canonical files copied by the exact numerical
        # delegate, then require the actual V3 aliases and their original names.
        for stem in ('optimize_training_round','finalize_training_round'):
            name=f'{stem}{number}.py'
            (candidate/name).write_bytes((A/name).read_bytes())
        assert copy_actual_sources(ns,candidate)==record
        assert copy_actual_sources(ns,candidate)==record
        for name,item in record['files'].items():
            assert sha(candidate/name)==sha(item['project_source'])==item['sha256'],name
            sources.add(Path(item['project_source']))
        required=[f'optimize_training_round{number}_v3.py',f'finalize_training_round{number}_v3.py',
            f'run_training_round{number}_v3_pipeline.py','streaming_rank_classifier_search_engine_v3_20261005.py',
            'run_streaming_rank_classifier_round_v3_20261005.py',
            'predict_streaming_rank_classifier_scheme_codec_v3_20261005.py']
        assert all((candidate/name).exists() for name in required)
        saved={str(path.relative_to(candidate)):sha(path) for path in candidate.rglob('*') if path.is_file()}
        (candidate/'manifest.json').write_text('{}',encoding='utf-8')
        try:copy_actual_sources(ns,candidate)
        except AssertionError as error:assert 'immutable' in str(error)
        else:raise AssertionError('Sealed candidate must reject changes.')
        assert all(sha(candidate/name)==digest for name,digest in saved.items())
        controls.append({'round':number,'actual_driver_AST_binding_statements_executed':True,
            'actual_publication_canonical_import_identity':True,'actual_release_closures_correct':True,
            'versioned_and_canonical_source_filenames_present_and_SHA_exact':True,
            'idempotent_packaging_and_numerical_delegate_legacy_copy_recovery':True,
            'sealed_candidate_rejected_without_changes':True,'source_files':record['files']})
    proof=A/'streaming_rank_classifier_search_generator_preflight_v3_20261005/verification.json'
    generator=json.loads(proof.read_text(encoding='utf-8'))
    assert generator['status']=='passed' and [row['generated_records'] for row in generator['controls']]==[100,98,98]
    for path,digest in generator['source_sha256'].items():assert sha(path)==digest,path
    sources.add(proof)
    with (out/'verification.json').open('x',encoding='utf-8') as stream:
        json.dump({'status':'passed','controls':controls,'source_sha256':{str(path):sha(path) for path in sorted(sources)},
            'actual_quality_still_requires20_annual4_final_and_complete78_79_predecessors':True,
            'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False},stream,ensure_ascii=False,indent=2)
    print('Actual79/80 driver canonical bindings, release closure and full source packaging passed.',flush=True)


if __name__=='__main__':main()
