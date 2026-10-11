"""Publish recovered bank/score evidence and preserve all four actual first failures."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, owned
SOURCE = A / 'publish_robust_conditional_residual_evidence_20261006.py'


def main(phase):
    assert phase in ('bank', 'scores')
    evidence = [SOURCE, Path(__file__),
        A / 'train_robust_conditional_residual_bank20_v2_20261006.py',
        A / 'run_robust_conditional_residual_comparison50_v2_20261006.py',
        A / 'conditional_identity_regression_tree_codec_20261006.py',
        A / 'robust_conditional_residual_codec_recovery_preflight_20261006.json',
        *[p for p in (A / 'robust_conditional_residual_bank20_20261006').rglob('*.json') if not p.name.startswith('model_dump_')]]
    for name in ('robust_conditional_residual_native_bank20', 'robust_conditional_residual_comparison50',
                 'robust_conditional_residual_bank20_evidence_publication', 'robust_conditional_residual_scores50_evidence_publication'):
        folder = A / 'service_owned_workflows_20261006' / name
        assert not owned(read(folder / 'native_launch.json'))
        assert read(folder / 'service_execution.json')['status'] == 'failed'
        evidence.extend([*folder.glob('*.json'), *folder.glob('*.log')])
    text = SOURCE.read_text(encoding='utf-8')
    for before, after in {
        'robust_conditional_residual_bank20_evidence_publication': 'robust_conditional_residual_bank20_evidence_publication_v2',
        'robust_conditional_residual_native_bank20': 'robust_conditional_residual_native_bank20_v2',
        'robust_conditional_residual_comparison50_20261006': 'robust_conditional_residual_comparison50_v2_20261006',
        "else 'robust_conditional_residual_comparison50')": "else 'robust_conditional_residual_comparison50_v2')",
        'robust_conditional_residual_bank20_20261006': 'robust_conditional_residual_bank20_v2_20261006',
        'robust_conditional_residual_{phase}_github_20261006': 'robust_conditional_residual_{phase}_github_v2_20261006',
        'validation_sync/robust_conditional_residual_{phase}_20261006': 'validation_sync/robust_conditional_residual_{phase}_v2_20261006',
    }.items():
        assert before in text, before
        text = text.replace(before, after)
    marker = '    namespace = {\'__file__\': __file__,'
    assert text.count(marker) == 1
    text = text.replace(marker,
        "    before = \"    sources += [p for p in bank.rglob('*.json') if not p.name.startswith('model_dump_')]\"\n"
        "    assert text.count(before) == 1\n"
        "    text = text.replace(before, '    sources += RECOVERY_EVIDENCE\\n' + before)\n" + marker)
    marker = "'PUBLICATION_TEMPLATE': SOURCE}"
    assert text.count(marker) == 1
    text = text.replace(marker, "'PUBLICATION_TEMPLATE': SOURCE, 'RECOVERY_EVIDENCE': RECOVERY_EVIDENCE}")
    namespace = {'__file__': __file__, '__name__': 'actual_recovered_robust_residual_evidence_publication',
        'RECOVERY_EVIDENCE': evidence}
    exec(compile(text, str(SOURCE), 'exec'), namespace)
    namespace['main'](phase)


if __name__ == '__main__': main(sys.argv[1])
