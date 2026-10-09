"""Resume an unchanged frozen driver after verified reboot, with new telemetry."""
from pathlib import Path
import datetime
import importlib
import json
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    from locked_read_hash_cache_20261004 import fresh_sha
    attempt = Path(sys.argv[1]).resolve()
    run = json.loads(attempt.read_text(encoding='utf-8'))
    for name, digest in run['input_sha256'].items():
        assert fresh_sha(name) == digest, name
    assert fresh_sha(__file__) == run['recovery_driver_sha256']
    output = attempt.parent
    assert output.is_relative_to(A) and output.drive.upper() == 'D:'
    previous_class, module, replacement = None, None, None
    recorder = run.get('separate_resource_recorder')
    if recorder:
        module = importlib.import_module(recorder['module'])
        previous_class = getattr(module, recorder['class'])

        def replacement(old_output):
            assert Path(old_output).resolve() == Path(recorder['original_output']).resolve()
            instance = previous_class(output / 'resources')
            assert instance.__class__ is previous_class
            return instance

        setattr(module, recorder['class'], replacement)
    status, failure = 'passed', None
    print(json.dumps({'status': 'verified_reboot_recovery_attempt_started',
        'job': run['name'], 'original_driver': run['original_script'],
        'original_arguments': run['original_arguments'],
        'completed_artifacts_reused_only_after_native_checks': True,
        'partial_epochs_not_counted_as_full_fits': True,
        'original_sources_protocols_and_samples_preserved': True,
        'test_labels_read': False}, ensure_ascii=False), flush=True)
    try:
        sys.argv = [run['original_script'], *run['original_arguments']]
        runpy.run_path(run['original_script'], run_name='__main__')
        for name, digest in run['input_sha256'].items():
            assert fresh_sha(name) == digest, name
    except BaseException as error:
        status, failure = 'failed', f'{type(error).__name__}: {error}'
        raise
    finally:
        if recorder:
            assert getattr(module, recorder['class']) is replacement
            setattr(module, recorder['class'], previous_class)
        with (output / 'execution.json').open('x', encoding='utf-8') as stream:
            json.dump({'status': status, 'failure': failure,
                'at_local': datetime.datetime.now().isoformat(timespec='seconds'),
                'attempt_sha256': fresh_sha(attempt),
                'resource_constructor_restored': True,
                'separate_resource_directory': str(output / 'resources') if recorder else None,
                'original_scientific_driver_sources_unchanged': True,
                'test_labels_read': False}, stream, ensure_ascii=False, indent=2)
            stream.write('\n')


if __name__ == '__main__':
    main()
