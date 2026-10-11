"""Accept one precisely identified completed route proof without changing science or proof bytes."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
PROOF = A / 'classifier_consensus_direct_router_preflight_20261005/verification.json'
SOURCE = A / 'ready_classifier_consensus_reference_search_engine_v2_20261006.py'
CONSENSUS = ('classifier_binary_mean', 'classifier_decile_mean', 'classifier_head_mix_b025',
             'classifier_head_mix_b050', 'classifier_head_mix_b075', 'classifier_decile_reflected_mean')
INHERITED = ('rank_top10_sgd_l2e3_e32', 'rank_top10_sgd_l2e4_e32',
             'rank_decile_sgd_l2e3_e32', 'rank_decile_sgd_l2e4_e32')


def verify_gate(ns, path):
    proof = ns.read(path)
    if Path(path).resolve() != PROOF.resolve():
        assert proof['status'] == 'passed', path
        return
    assert proof['status'] == 'passed_actual_consensus_and_inherited_routes'
    assert proof['future_codec_restored_to_original_object'] is True
    assert proof['new_native_fits'] == proof['new_quality_scores'] == 0
    assert proof['test_labels_read'] is False
    checks = proof['checks']
    assert len(checks) == 16
    direct = {(r['model'], r['year']): r for r in checks if 'model' in r}
    native = {r['inherited_native_classifier']: r for r in checks if 'inherited_native_classifier' in r}
    assert set(direct) == {(model, year) for model in CONSENSUS for year in (2020, 2025)}
    assert set(native) == set(INHERITED)
    assert all(r['direct_and_future_routes_bit_identical'] is True for r in direct.values())
    assert all(r['preserved_bit_identical'] is True for r in native.values())
    assert proof['input_sha256']
    for source, expected in proof['input_sha256'].items():
        assert ns.sha(source) == expected, source


def patched_namespace():
    import ready_classifier_consensus_reference_search_engine_v2_20261006 as original
    source = SOURCE.read_text(encoding='utf-8')
    before = "        for path in gates:assert ns.read(path)['status']=='passed',path"
    after = "        for path in gates:verify_gate(ns,path)"
    assert source.count(before) == 1
    effective = source.replace(before, after)
    assert effective.replace(after, before) == source
    namespace = dict(vars(original), verify_gate=verify_gate)
    exec(compile(effective, str(SOURCE), 'exec'), namespace)
    return original, namespace, effective


def install():
    original, namespace, _ = patched_namespace()
    previous = original.install
    original.install = namespace['install']

    def restore():
        assert original.install is namespace['install']
        original.install = previous

    return restore
