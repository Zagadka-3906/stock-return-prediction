"""Expose the existing measured/frozen winner for complete ranking registration."""
from optimize_training_round98 import OUT, read


def selected():
    record = read(OUT / 'selection.json')
    assert len(record['ranking']) == 16
    assert record['winner']['entry_exit_buffer_complete_scheme_graph']['entry_exit_buffer']['margin'] == 0.
    assert record['winner']['connected_final_score'] == max(r['connected_final_score'] for r in record['ranking'])
    assert record['original_frozen_selection_source']
    return record
