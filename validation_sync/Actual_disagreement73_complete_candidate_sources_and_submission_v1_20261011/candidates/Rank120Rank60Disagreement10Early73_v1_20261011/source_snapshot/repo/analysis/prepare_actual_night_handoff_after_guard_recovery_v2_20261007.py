"""Preserve the failed guard check, then prepare the same bounded manual backup."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import sha, create, read

original = A / 'prepare_actual_night_manual_handoff_API_20261007.py'
new = A / 'prepare_actual_night_manual_handoff_API_v2_20261007.py'
failed = A / 'actual_night_manual_handoff_API_20261007'
assert failed.exists() and not list(failed.iterdir())
create(failed / 'failed_guard_precondition.json', {'status': 'failed_before_payload_or_API_mutation',
    'error': 'AssertionError: publisher parent and worker were not both stopped while original guardian had failed',
    'original_source_sha256': sha(original), 'actual_guard_recovery': str(A / 'actual_failed_shutdown_guard_recovery_v2_20261007.json'),
    'new_quality_scores': 0, 'external_mutations': 0})
text = original.read_text(encoding='utf8').replace("OUT = A / 'actual_night_manual_handoff_API_20261007'", "OUT = A / 'actual_night_manual_handoff_API_v2_20261007'")
needle = "    prefix = Path('validation_sync/night_manual_handoff_20261007')"
assert text.count(needle) == 1
extras = [Path(__file__), original, failed / 'failed_guard_precondition.json', A / 'shutdown_ready_stop_v2_20261007.py',
    A / 'recover_actual_failed_shutdown_guard_v2_20261007.py', A / 'actual_failed_shutdown_guard_recovery_v2_20261007.json',
    A / 'service_owned_workflows_20261006/shutdown_ready_2355_manual_continue_20261007/service_execution.json',
    A / 'service_owned_workflows_20261006/shutdown_ready_2355_manual_continue_20261007/stderr.log']
text = text.replace(needle, '    files += [' + ','.join('A/' + repr(p.relative_to(A).as_posix()) for p in extras) + ']\n' + needle)
compile(text, str(new), 'exec')
assert not new.exists()
new.write_text(text, encoding='utf8', newline='\n')
namespace = {'__name__': 'manual_night_API_packet', '__file__': str(new)}
exec(compile(text, str(new), 'exec'), namespace)
namespace['main']()
