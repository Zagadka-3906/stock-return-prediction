"""Resume the finished registry after a helper path typo; preserve all original evidence."""
from pathlib import Path
import sys

SOURCE = Path(__file__).with_name('run_cohort_round99_full_registration_20261006.py')
text = SOURCE.read_text(encoding='utf-8')
assert text.count('neural17384_annual') == 2
text = text.replace('neural17384_annual', 'neural16384_annual')
assert text.count('    protocol = prepare()') == 1
text = text.replace('    protocol = prepare()',
    "    protocol = read(A / 'optimization_20261003_r99/protocol.json')\n"
    "    assert protocol['expected_scored_records'] == 17\n"
    "    for path, digest in protocol['input_sha256'].items():\n"
    "        assert sha(path) == digest, path\n"
    "    protocol['input_sha256'][str(Path(__file__).resolve())] = sha(__file__)\n"
    "    failure = read(A / 'service_owned_workflows_20261006/cohort_rank_calibration_round99_full_registration/service_execution.json')\n"
    "    assert failure['status'] == 'failed' and 'neural17384' in failure['failure']\n"
    "    assert not (ROOT / 'results/optimization_20261003_r99.json').exists()\n"
    "    create(A / 'optimization_20261003_r99/administrative_registry_path_recovery_20261006.json', {\n"
    "        'status': 'preserved_original_failed_helper_path_then_resumed_existing_registry',\n"
    "        'original_failure': failure, 'original_driver_sha256': sha(SOURCE),\n"
    "        'effective_driver_sha256': sha(__file__), 'no_original_scientific_source_edited': True,\n"
    "        'scientific_workers_restarted_or_suspended': 0, 'new_quality_scores': 0})")
namespace = {'__file__': __file__, '__name__': 'cohort_registry_recovery', 'SOURCE': SOURCE}
exec(compile(text, str(SOURCE), 'exec'), namespace)

if __name__ == '__main__':
    namespace['main']()
