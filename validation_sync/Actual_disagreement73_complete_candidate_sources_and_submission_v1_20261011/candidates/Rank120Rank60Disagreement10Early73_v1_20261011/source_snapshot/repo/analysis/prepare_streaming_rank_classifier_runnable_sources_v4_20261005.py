"""Fix the actual missing versioned candidate entrypoints; retain V3 test artifacts."""
from pathlib import Path
import hashlib
import json

A=Path(__file__).resolve().parent


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    originals=['streaming_rank_classifier_search_engine_v3_20261005.py',
        'run_streaming_rank_classifier_round_v3_20261005.py',
        'verify_streaming_rank_classifier_search_generators_v3_20261005.py',
        'predict_streaming_rank_classifier_scheme_codec_v3_20261005.py',
        'predict_streaming_rank_classifier_scheme_v3_20261005.py',
        'verify_streaming_rank_classifier_execution_sources_v3_20261005.py']
    originals += [f'{stem}{number}{suffix}.py' for number in (79,80)
        for stem,suffix in (('optimize_training_round','_v3'),('finalize_training_round','_v3'),('run_training_round','_v3_pipeline'))]
    replacements={name.removesuffix('.py'):name.replace('_v3','_v4').removesuffix('.py') for name in originals}
    replacements.update({
        'streaming_rank_classifier_search_generator_preflight_v3_20261005':'streaming_rank_classifier_search_generator_preflight_v4_20261005',
        'streaming_rank_classifier_execution_source_preflight_v3_20261005':'streaming_rank_classifier_execution_source_preflight_v4_20261005',
        'streaming_rank_classifier_quality_run_v3_20261005':'streaming_rank_classifier_quality_run_v4_20261005',
        'optimize_training_round{number}_v3':'optimize_training_round{number}_v4',
        'finalize_training_round{number}_v3':'finalize_training_round{number}_v4',
        'run_training_round{number}_v3_pipeline':'run_training_round{number}_v4_pipeline',
        'optimize_training_round{ns.NUMBER}_v3':'optimize_training_round{ns.NUMBER}_v4',
        'finalize_training_round{ns.NUMBER}_v3':'finalize_training_round{ns.NUMBER}_v4',
        'run_training_round{ns.NUMBER}_v3_pipeline':'run_training_round{ns.NUMBER}_v4_pipeline'})
    retained={str(A/name):sha(A/name) for name in originals}
    generated={}
    for name in originals:
        body=(A/name).read_text(encoding='utf-8')
        for before,after in sorted(replacements.items(),key=lambda item:-len(item[0])):body=body.replace(before,after)
        if 'scheme_codec' in name:
            for before,after in (
                ("f'optimize_training_round{ns.NUMBER}.py'","f'optimize_training_round{ns.NUMBER}_v4.py'"),
                ("f'finalize_training_round{ns.NUMBER}.py'","f'finalize_training_round{ns.NUMBER}_v4.py'"),
                ("f'run_training_round{ns.NUMBER}_pipeline.py'","f'run_training_round{ns.NUMBER}_v4_pipeline.py'"),
                ("name.replace('_v3.py','.py')","name.replace('_v4.py','.py')")):
                assert before in body,before
                body=body.replace(before,after)
            body=body.replace("'actual_canonical_release':f'finalize_training_round{ns.NUMBER}_v4.py'", "'actual_release':f'finalize_training_round{ns.NUMBER}_v4.py',\n        'actual_canonical_release':f'finalize_training_round{ns.NUMBER}.py'")
        if name.startswith('verify_') and 'generators' in name:
            body=body.replace("('optimize_training_round', '_v3')","('optimize_training_round', '_v4')")
            body=body.replace("('finalize_training_round', '_v3')","('finalize_training_round', '_v4')")
            body=body.replace("('run_training_round', '_v3_pipeline')","('run_training_round', '_v4_pipeline')")
        target=A/name.replace('_v3','_v4')
        compile(body,str(target),'exec')
        with target.open('x',encoding='utf-8',newline='\n') as stream:stream.write(body)
        generated[str(target)]=sha(target)
    assert all(sha(path)==digest for path,digest in retained.items())
    with (A/'streaming_rank_classifier_runnable_source_recovery_v4_20261005.json').open('x',encoding='utf-8') as stream:
        json.dump({'status':'retained_actual_V3_candidate_packaging_failure_and_prepared_explicit_V4_source_filenames',
            'retained_source_sha256':retained,'generated_source_sha256':generated,
            'original_failure':'Versioned optimize, finalize and pipeline filenames absent from actual V3 packaged control.',
            'actual_old_control_directory':str(A/'streaming_rank_classifier_execution_source_preflight_v3_20261005'),
            'numerical_models_graph_search_grid_and_return_mapping_unchanged':True,
            'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False},stream,ensure_ascii=False,indent=2)
    print('Actual candidate filename failure retained; explicit runnable V4 package prepared.',flush=True)


if __name__=='__main__':main()
