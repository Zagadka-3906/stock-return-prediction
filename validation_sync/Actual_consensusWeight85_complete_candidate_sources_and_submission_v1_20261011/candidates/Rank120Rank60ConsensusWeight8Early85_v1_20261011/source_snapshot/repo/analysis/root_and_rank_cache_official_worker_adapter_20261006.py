"""Combine the existing rank adapter with independently bounded root reuse."""
from pathlib import Path
import json

import exact_rank_cache_official_worker_adapter_20261006 as ranks
from bounded_root_replay_memoization_20261006 import enable, statistics, MAXIMUM_BYTES
from locked_read_hash_cache_20261004 import fresh_sha

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
PROOF = A / 'bounded_root_replay_full_controls_20261006/verification.json'
original = ranks.original


def read_control():
    proof = json.loads(PROOF.read_text(encoding='utf-8'))
    assert proof['status'] == 'passed_actual_full_root_cache_bits8_metrics_cold_prefix_poisoning_and_root_mutation_controls'
    assert (proof['actual_rows'], proof['actual_days'], proof['actual_codes']) == (5635800, 1212, 4650)
    kernel = A / 'bounded_root_replay_memoization_20261006.py'
    assert proof['input_sha256'][str(kernel)] == fresh_sha(kernel)
    assert len(proof['all5_reference_configurations']) == 5
    assert all(row['all5635800_prediction_values_bit_identical'] and row['all8_original_official_metrics_exact']
               for row in proof['all5_reference_configurations'])
    return proof


def initialize(module_name, output, slots):
    assert module_name in ('optimize_training_round95_v3', 'optimize_training_round97_v3')
    proof = read_control()
    ranks.initialize(module_name, output, slots)
    enable(original._CONTEXT, proof['input_sha256'])


def evaluate(job):
    before = statistics(original._CONTEXT)
    key, row = ranks.evaluate(job)
    row['bounded_root_execution'] = {
        'installed_in_actual_Windows_scoring_worker': True,
        'maximum_retained_array_and_stat_payload_bytes': MAXIMUM_BYTES,
        'payload_cap_is_not_total_RSS_cap': True,
        'before': before, 'after': statistics(original._CONTEXT),
        'full_control_source': str(PROOF), 'full_control_sha256': fresh_sha(PROOF),
        'adapter_source': str(Path(__file__).resolve()),
        'scientific_configuration_and_official_evaluator_unchanged': True}
    return key, row


def install():
    assert not original._POOLS
    restore_ranks = ranks.install()
    assert original._initialize is ranks.initialize and original._evaluate is ranks.evaluate
    original._initialize, original._evaluate = initialize, evaluate

    def restore():
        assert not original._POOLS
        assert original._initialize is initialize and original._evaluate is evaluate
        original._initialize, original._evaluate = ranks.initialize, ranks.evaluate
        restore_ranks()

    return restore
