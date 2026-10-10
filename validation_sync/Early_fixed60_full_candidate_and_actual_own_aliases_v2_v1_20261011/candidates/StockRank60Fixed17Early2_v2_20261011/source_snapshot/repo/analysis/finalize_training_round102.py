"""Expose the already measured and frozen cohort winner without reselection."""
from optimize_training_round102 import OUT, ROOT, read, sha, GRAPH_FIELD


def selected():
    record = read(OUT / 'selection.json')
    assert len(record['ranking']) == 49
    assert record['winner']['connected_final_score'] == max(r['connected_final_score'] for r in record['ranking'])
    spec = record['winner'][GRAPH_FIELD]['conditional_flag_residual']
    measured = read(record['original_frozen_selection_source'])['chosen_postprocessor']
    assert all(spec[key] == measured[key] for key in ('model', 'weight'))
    for relative, digest in record['frozen_sha256'].items():
        assert sha(ROOT / relative) == digest, relative
    assert sha(record['original_frozen_selection_source']) == record['original_frozen_selection_sha256']
    return record
