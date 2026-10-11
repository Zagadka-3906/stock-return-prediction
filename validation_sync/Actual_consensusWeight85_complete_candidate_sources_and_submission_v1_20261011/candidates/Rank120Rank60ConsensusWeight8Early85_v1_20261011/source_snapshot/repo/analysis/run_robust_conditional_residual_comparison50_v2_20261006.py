"""Use the recovered unchanged20-fit bank and retain the original dependency failure."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, owned
SOURCE = A / 'run_robust_conditional_residual_comparison50_20261006.py'


def main():
    old = A / 'service_owned_workflows_20261006/robust_conditional_residual_comparison50'
    assert not owned(read(old / 'native_launch.json'))
    assert read(old / 'service_execution.json')['status'] == 'failed'
    text = SOURCE.read_text(encoding='utf-8')
    for before, after in {
        'robust_conditional_residual_native_bank20': 'robust_conditional_residual_native_bank20_v2',
        'robust_conditional_residual_bank20_20261006': 'robust_conditional_residual_bank20_v2_20261006',
        'robust_conditional_residual_comparison50_20261006': 'robust_conditional_residual_comparison50_v2_20261006',
    }.items():
        assert before in text, before
        text = text.replace(before, after)
    before = '    evidence = [SOURCE,'
    assert text.count(before) == 1
    text = text.replace(before, '    evidence = [*RECOVERY_EVIDENCE, SOURCE,')
    namespace = {'__file__': __file__, '__name__': 'actual_recovered_robust_residual_comparison50',
        'RECOVERY_EVIDENCE': [SOURCE, A / 'conditional_identity_regression_tree_codec_20261006.py',
            A / 'train_robust_conditional_residual_bank20_v2_20261006.py',
            A / 'robust_conditional_residual_codec_recovery_preflight_20261006.json',
            *old.glob('*.json'), *old.glob('*.log')]}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__': main()
