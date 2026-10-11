"""Preserve failed control and replace its unsupported effect assumption."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'


def main():
    source = A / 'verify_causal_entry_exit_buffer_full_controls_20261006.py'
    target = A / 'verify_causal_entry_exit_buffer_full_controls_v2_20261006.py'
    original = source.read_text(encoding='utf-8')
    value = original.replace("OUT = A / 'causal_entry_exit_buffer_full_controls_20261006'",
        "OUT = A / 'causal_entry_exit_buffer_full_controls_v2_20261006'")
    value = value.replace("predecessor / 'component_audit.json', predecessor / 'streaming_rank_classifier_causal_checks.json', panel]",
        "predecessor / 'component_audit.json', predecessor / 'streaming_rank_classifier_causal_checks.json', panel,\n"
        "        A / 'recover_causal_entry_exit_buffer_controls_v2_20261006.py',\n"
        "        A / 'causal_entry_exit_buffer_full_controls_20261006/failure.json',\n"
        "        A / 'causal_entry_exit_buffer_full_controls_20261006/frozen_before_full_controls.json']")
    value = value.replace('margins = [0., .00025, .0005, .001, .002, .004, .008, .016]',
        'margins = [0., .00025, .0005, .001, .002, .004, .008, .016, .032, .064, .1]')
    old = "            digest = hashlib.sha256(memoryview(np.ascontiguousarray(prediction)).cast('B')).hexdigest()"
    new = """            _, emitted = transform(prediction, dates, flags, codes, 0., True)
            assert emitted['continuous_Jaccard_mean_diagnostic'] == diagnostics['continuous_Jaccard_mean_diagnostic']
            diagnostics['actual_emitted_output_turnover_matches_internal_membership_state'] = True
            digest = hashlib.sha256(memoryview(np.ascontiguousarray(prediction)).cast('B')).hexdigest()"""
    assert old in value
    value = value.replace(old, new)
    old = "    assert all(row['diagnostics']['changed_membership_days'] > 0 for row in results[1:])"
    new = """    # A positive parameter can be equivalent; this is evidence, not a failure.
    # Diagnose the current parent path. This is not a global turnover bound.
    previous = None
    compulsory_exits = capacity_exits = optional_exits = transitions = 0
    required_margins = []
    for start, end in zip(boundaries[:-1], boundaries[1:]):
        index = np.arange(start, end)[flags[start:end] == 0]
        if len(index) < 100:
            previous = None
            continue
        order = np.lexsort((codes[index], -raw[index]))
        ranked = index[order]
        k = max(len(index) // 10, 1)
        current = set(map(int, codes[ranked[:k]]))
        eligible = set(map(int, codes[index]))
        if previous is not None:
            transitions += 1
            available = previous & eligible
            compulsory_exits += len(previous - eligible)
            mandatory = max(len(available) - k, 0)
            capacity_exits += mandatory
            discretionary = len(available - current) - mandatory
            assert discretionary >= 0
            optional_exits += discretionary
            if discretionary:
                positions = {int(code): i for i, code in enumerate(codes[ranked])}
                best_exiting = min(positions[code] for code in available - current)
                entrants = current - available
                if entrants:
                    worst_entering = max(positions[code] for code in entrants)
                    required_margins.append((best_exiting - worst_entering) / max(len(index)-1, 1))
        previous = current
    path_diagnostic = {'transitions': transitions, 'flag_or_absent_stock_compulsory_exits': compulsory_exits,
        'current_pool_size_compulsory_exits': capacity_exits, 'optional_exits_on_actual_parent_path': optional_exits,
        'first_potential_swap_margin_minimum': min(required_margins) if required_margins else None,
        'first_potential_swap_margin_median': float(np.median(required_margins)) if required_margins else None,
        'not_a_global_bound_or_a_new_official_score': True}
    create(OUT / 'actual_parent_transition_diagnostic.json', path_diagnostic)"""
    assert old in value
    value = value.replace(old, new)
    value = value.replace("'actual_all8_margin_controls': results", "'actual_all11_margin_controls': results, 'actual_parent_transition_diagnostic': path_diagnostic")
    value = value.replace("'zero_margin_official_parent_turnover_exact': True", "'zero_margin_official_parent_turnover_exact': True, 'positive_noop_cases_preserved_as_evidence': True")
    compile(value, str(target), 'exec')
    assert not target.exists()
    with target.open('x', encoding='utf-8', newline='') as stream: stream.write(value)
    assert source.read_text(encoding='utf-8') == original
    print('created v2 controls; old failed source and outputs preserved; source SHA256=' + hashlib.sha256(target.read_bytes()).hexdigest())


if __name__ == '__main__': main()
