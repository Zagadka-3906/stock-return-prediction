"""Resume only the naturally failed registry conversion, retaining all input pins."""
from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, owned
SOURCE = A / 'register_conditional_flag_round101_artifacts_20261006.py'


def main():
    service = A / 'service_owned_workflows_20261006/conditional_flag_round101_full_registration'
    assert not owned(read(service / 'native_launch.json'))
    failure = read(service / 'service_execution.json')
    assert failure['status'] == 'failed' and 'not in the subpath' in failure['failure']
    out = A / 'optimization_20261003_r101'
    candidate = ROOT / 'candidates/optimization_20261003_r101'
    source_candidate = ROOT / 'candidates/conditional_flag_rank_20261006'
    assert out.exists() and not list(out.iterdir())
    assert not (candidate / 'manifest.json').exists()
    manifest = read(source_candidate / 'manifest.json')
    for relative, info in manifest['files'].items():
        alias = 'original_inference_selection.json' if relative == 'selection.json' else relative
        assert sha(candidate / alias) == sha(source_candidate / relative) == info['sha256']
        assert os.path.samefile(candidate / alias, source_candidate / relative)
    additional = [SOURCE, Path(__file__),
        A / 'run_conditional_flag_round101_full_registration_v2_20261006.py',
        A / 'publish_conditional_flag_round101_full_validation_v2_20261006.py',
        *service.glob('*.json'), *service.glob('*.log'),
        *(candidate / 'registration_sources').glob('*')]
    pins = {str(p): sha(p) for p in additional}
    text = SOURCE.read_text(encoding='utf-8')
    before = '    assert not OUT.exists() and not CANDIDATE.exists()'
    assert text.count(before) == 1
    text = text.replace(before, '    assert OUT.exists() and CANDIDATE.exists()')
    before = "    pins = {**read(RELEASE / 'protocol.json')['input_sha256'],"
    assert text.count(before) == 1
    text = text.replace(before, "    sources += RECOVERY_SOURCES\n    pins = {**RECOVERY_PINS, **read(RELEASE / 'protocol.json')['input_sha256'],")
    before = '    OUT.mkdir()\n    CANDIDATE.mkdir()'
    assert text.count(before) == 1
    text = text.replace(before, '    # Verified existing exact aliases are resumed, never removed or retrained.')
    before = '        os.link(SOURCE_CANDIDATE / relative, target)'
    assert text.count(before) == 1
    text = text.replace(before, "        if target.exists():\n            assert sha(target) == sha(SOURCE_CANDIDATE / relative)\n        else:\n            os.link(SOURCE_CANDIDATE / relative, target)")
    before = '        os.link(source, target)'
    assert text.count(before) == 1
    text = text.replace(before, "        if target.exists():\n            assert sha(target) == sha(source)\n        else:\n            os.link(source, target)")
    before = "    selection['frozen_sha256'].update({Path(p).relative_to(ROOT).as_posix(): digest for p, digest in pins.items()})"
    assert text.count(before) == 1
    text = text.replace(before,
        "    selection['frozen_sha256'].update({Path(p).relative_to(ROOT).as_posix(): digest for p, digest in pins.items() if Path(p).is_relative_to(ROOT)})\n"
        "    selection['frozen_external_input_sha256'] = {p: digest for p, digest in pins.items() if not Path(p).is_relative_to(ROOT)}\n"
        "    selection['all_external_inputs_still_in_absolute_protocol_Windows_read_locks_and_final_rehash'] = True\n"
        "    selection['original_failed_registry_and_existing_verified_aliases_preserved'] = True")
    namespace = {'__file__': __file__, '__name__': 'actual_conditional101_registry_recovery',
        'RECOVERY_SOURCES': additional, 'RECOVERY_PINS': pins}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    return namespace['main']()


if __name__ == '__main__':
    main()
