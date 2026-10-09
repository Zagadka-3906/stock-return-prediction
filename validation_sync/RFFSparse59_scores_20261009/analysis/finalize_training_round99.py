"""Expose the already measured and frozen cohort winner without reselection."""
from optimize_training_round99 import OUT, ROOT, read, sha, GRAPH_FIELD


def selected():
    record = read(OUT / 'selection.json')
    assert len(record['ranking']) == 17
    assert record['winner']['connected_final_score'] == max(r['connected_final_score'] for r in record['ranking'])
    spec = record['winner'][GRAPH_FIELD]['cohort_rank_calibration']
    assert (spec['weight'], spec['bins'], spec['pseudocount']) == (1., 32, 0.)
    for relative, digest in record['frozen_sha256'].items():
        assert sha(ROOT / relative) == digest, relative
    assert sha(record['original_frozen_selection_source']) == record['original_frozen_selection_sha256']
    return record
