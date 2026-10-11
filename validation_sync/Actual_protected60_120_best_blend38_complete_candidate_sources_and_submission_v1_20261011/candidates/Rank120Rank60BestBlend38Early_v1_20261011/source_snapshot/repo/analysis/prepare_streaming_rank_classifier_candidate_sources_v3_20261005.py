"""Preserve V2 controls and package every actual runnable versioned entrypoint."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    originals = ['streaming_rank_classifier_search_engine_v2_20261005.py',
        'run_streaming_rank_classifier_round_v2_20261005.py',
        'verify_streaming_rank_classifier_search_generators_v2_20261005.py',
        'predict_streaming_rank_classifier_scheme_codec_v2_20261005.py',
        'predict_streaming_rank_classifier_scheme_v2_20261005.py']
    originals += [f'{stem}{number}{suffix}.py' for number in (79,80)
        for stem,suffix in (('optimize_training_round','_v2'),('finalize_training_round','_v2'),('run_training_round','_v2_pipeline'))]
    replacements = {name.removesuffix('.py'):name.replace('_v2','_v3').removesuffix('.py') for name in originals}
    replacements.update({
        'streaming_rank_classifier_search_generator_preflight_v2_20261005':'streaming_rank_classifier_search_generator_preflight_v3_20261005',
        'streaming_rank_classifier_execution_source_preflight_v2_20261005':'streaming_rank_classifier_execution_source_preflight_v3_20261005',
        'streaming_rank_classifier_quality_run_v2_20261005':'streaming_rank_classifier_quality_run_v3_20261005',
        'optimize_training_round{number}_v2':'optimize_training_round{number}_v3',
        'finalize_training_round{number}_v2':'finalize_training_round{number}_v3',
        'run_training_round{number}_v2_pipeline':'run_training_round{number}_v3_pipeline',
        'optimize_training_round{ns.NUMBER}_v2':'optimize_training_round{ns.NUMBER}_v3',
        'finalize_training_round{ns.NUMBER}_v2':'finalize_training_round{ns.NUMBER}_v3',
        'run_training_round{ns.NUMBER}_v2_pipeline':'run_training_round{ns.NUMBER}_v3_pipeline'})
    prior = {str(A/name):sha(A/name) for name in originals}
    outputs = {}
    for name in originals:
        body = (A/name).read_text(encoding='utf-8')
        for before,after in sorted(replacements.items(),key=lambda pair:-len(pair[0])):
            body=body.replace(before,after)
        if name.startswith('verify_'):
            body=body.replace("glob('*memory_efficient*20261005.py')", "glob('*streaming_rank_class*20261005.py')")
            body=body.replace("('optimize_training_round', '_v2')", "('optimize_training_round', '_v3')")
            body=body.replace("('finalize_training_round', '_v2')", "('finalize_training_round', '_v3')")
            body=body.replace("('run_training_round', '_v2_pipeline')", "('run_training_round', '_v3_pipeline')")
        if name.startswith('predict_') and 'codec' in name:
            body=body.replace("'streaming_rank_classifier_search_engine_20261005.py'", "'streaming_rank_classifier_search_engine_v3_20261005.py'")
            body=body.replace("name.replace('_v2.py','.py')", "name.replace('_v3.py','.py')")
            body=body.replace("files[destination] =", "if destination != name:\n            actual = candidate/name\n            if actual.exists(): assert actual.read_bytes() == data\n            else:\n                with actual.open('xb') as stream: stream.write(data)\n            files[name] = {'project_source':str(source),'sha256':hashlib.sha256(data).hexdigest()}\n        files[destination] =")
        target=A/name.replace('_v2','_v3')
        compile(body,str(target),'exec')
        with target.open('x',encoding='utf-8',newline='\n') as stream:stream.write(body)
        outputs[str(target)]=sha(target)
    proof=A/'streaming_rank_classifier_search_generator_preflight_v2_20261005/verification.json'
    assert [row['generated_records'] for row in json.loads(proof.read_text(encoding='utf-8'))['controls']] == [100,98,98]
    with (A/'streaming_rank_classifier_candidate_source_generation_v3_20261005.json').open('x',encoding='utf-8') as stream:
        json.dump({'status':'retain_passed_V2_grids_and_complete_actual_runnable_V3_candidate_sources',
            'original_source_sha256':prior,'generated_source_sha256':outputs,'V2_generator_proof_sha256':sha(proof),
            'actual_versioned_factories_release_engine_driver_and_pipeline_packaged':True,
            'canonical_aliases_and_historical_review_copies_preserved':True,
            'same_complete100_and98_official_grids':True,'new_quality_scores':0,'new_model_fits':0,'test_labels_read':False},stream,ensure_ascii=False,indent=2)
    assert all(sha(path)==digest for path,digest in prior.items())
    print('V3 complete candidate sources prepared; V2 actual generator controls retained.',flush=True)


if __name__=='__main__':main()
