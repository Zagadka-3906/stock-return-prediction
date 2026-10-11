"""Retain failed generator evidence and version actual 100/98 record metadata."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    failed = A / 'streaming_rank_classifier_search_generator_preflight_20261005/frozen_before_generator_controls.json'
    retained = json.loads(failed.read_text(encoding='utf-8'))['source_sha256']
    assert all(sha(path) == digest for path,digest in retained.items())
    sources = {}
    engine = (A / 'streaming_rank_classifier_search_engine_20261005.py').read_text(encoding='utf-8')
    assert "88 if number==79 else 80" in engine
    engine = engine.replace('88 if number==79 else 80','100 if number==79 else 98')
    replacements = {
        'streaming_rank_classifier_search_generator_preflight_20261005':'streaming_rank_classifier_search_generator_preflight_v2_20261005',
        'verify_streaming_rank_classifier_search_generators_20261005':'verify_streaming_rank_classifier_search_generators_v2_20261005',
        'streaming_rank_classifier_execution_source_preflight_20261005':'streaming_rank_classifier_execution_source_preflight_v2_20261005',
        'streaming_rank_classifier_quality_run_20261005':'streaming_rank_classifier_quality_run_v2_20261005',
        'run_streaming_rank_classifier_round_20261005':'run_streaming_rank_classifier_round_v2_20261005',
        'predict_streaming_rank_classifier_scheme_codec_20261005':'predict_streaming_rank_classifier_scheme_codec_v2_20261005',
        'predict_streaming_rank_classifier_scheme_20261005':'predict_streaming_rank_classifier_scheme_v2_20261005',
        'optimize_training_round{number}.py':'optimize_training_round{number}_v2.py',
        'finalize_training_round{number}.py':'finalize_training_round{number}_v2.py',
        'run_training_round{number}_pipeline.py':'run_training_round{number}_v2_pipeline.py'}
    def transform(body):
        for before,after in replacements.items(): body=body.replace(before,after)
        return body
    sources[A / 'streaming_rank_classifier_search_engine_v2_20261005.py'] = transform(engine)
    for number in (79,80):
        previous_import = 'import optimize_training_round79_v2\n' if number == 80 else ''
        sources[A / f'optimize_training_round{number}_v2.py'] = f'''import sys
{previous_import}from streaming_rank_classifier_search_engine_v2_20261005 import install
install({number},globals())
sys.modules['optimize_training_round{number}'] = sys.modules[__name__]
'''
        sources[A / f'finalize_training_round{number}_v2.py'] = transform((A / f'finalize_training_round{number}.py').read_text(encoding='utf-8'))
        sources[A / f'run_training_round{number}_v2_pipeline.py'] = f'from run_streaming_rank_classifier_round_v2_20261005 import main\nif __name__ == "__main__": main({number})\n'
    driver = transform((A / 'run_streaming_rank_classifier_round_20261005.py').read_text(encoding='utf-8'))
    driver = driver.replace("module = importlib.import_module(f'optimize_training_round{number}')", "module = importlib.import_module(f'optimize_training_round{number}_v2')")
    driver = driver.replace("release = importlib.import_module(f'finalize_training_round{number}')", "release = importlib.import_module(f'finalize_training_round{number}_v2')")
    sources[A / 'run_streaming_rank_classifier_round_v2_20261005.py'] = driver
    verifier = transform((A / 'verify_streaming_rank_classifier_search_generators_20261005.py').read_text(encoding='utf-8'))
    assert '88 if number == 79 else 80' in verifier
    verifier = verifier.replace('88 if number == 79 else 80','100 if number == 79 else 98')
    verifier = verifier.replace("importlib.import_module(f'optimize_training_round{number}')", "importlib.import_module(f'optimize_training_round{number}_v2')")
    verifier = verifier.replace("('optimize_training_round', '')", "('optimize_training_round', '_v2')")
    verifier = verifier.replace("('finalize_training_round', '')", "('finalize_training_round', '_v2')")
    verifier = verifier.replace("('run_training_round', '_pipeline')", "('run_training_round', '_v2_pipeline')")
    sources[A / 'verify_streaming_rank_classifier_search_generators_v2_20261005.py'] = verifier
    codec = transform((A / 'predict_streaming_rank_classifier_scheme_codec_20261005.py').read_text(encoding='utf-8'))
    # The numerical delegate copies historical canonical entrypoint names. The
    # actual V2 aliases are restored afterward while preserving those old bytes.
    codec = codec.replace("for name in names:\n        source = ns.ROOT/'analysis'/name\n        data, target = source.read_bytes(), candidate/name", "for name in names:\n        source = ns.ROOT/'analysis'/name\n        destination = name.replace('_v2.py','.py') if name.startswith(('optimize_training_round','finalize_training_round')) else name\n        data, target = source.read_bytes(), candidate/destination")
    codec = codec.replace("if target.exists():\n            assert target.read_bytes() == data, name", "if target.exists() and target.read_bytes() != data:\n            assert destination.startswith(('optimize_training_round','finalize_training_round'))\n            old = target.read_bytes()\n            assert old == (ns.ROOT/'analysis'/destination).read_bytes()\n            historical = candidate/'legacy_review_sources'/destination\n            historical.parent.mkdir(exist_ok=True)\n            if historical.exists(): assert historical.read_bytes() == old\n            else: historical.write_bytes(old)\n            target.write_bytes(data)\n        elif target.exists():\n            assert target.read_bytes() == data, name")
    codec = codec.replace("files[name] =", "files[destination] =")
    sources[A / 'predict_streaming_rank_classifier_scheme_codec_v2_20261005.py'] = codec
    sources[A / 'predict_streaming_rank_classifier_scheme_v2_20261005.py'] = 'from predict_streaming_rank_classifier_scheme_codec_v2_20261005 import predict\n'
    for path,body in sources.items():
        compile(body,str(path),'exec')
        with path.open('x',encoding='utf-8',newline='\n') as stream: stream.write(body)
    path = A / 'streaming_rank_classifier_official_recovery_v2_20261005.json'
    with path.open('x',encoding='utf-8') as stream:
        json.dump({'status':'original_generator_count_assertion_failure_retained_and_actual_V2_sources_prepared',
            'retained_original_source_sha256':retained,
            'original_failed_assertion':'88 if number == 79 else 80; generated full role grid contains100 records',
            'repair':'Declared totals100/98 agree with unchanged4-model full grids; correct actual V2 canonical execution aliases.',
            'new_source_sha256':{str(p):sha(p) for p in sources},
            'native_V3_training_unchanged':True,'new_model_fits':0,'new_quality_scores':0,'test_labels_read':False},stream,ensure_ascii=False,indent=2)
    assert all(sha(path) == digest for path,digest in retained.items())
    print('Original failure retained; complete100/98 engine, generator and actual V2 entrypoints prepared.',flush=True)


if __name__ == '__main__': main()
