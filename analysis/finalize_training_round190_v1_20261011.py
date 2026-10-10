"""Expose the already measured and frozen cohort winner without reselection."""
from optimize_training_round190_v1_20261011 import OUT, ROOT, read, sha, GRAPH_FIELD


def selected():
    record = read(OUT / 'selection.json')
    assert len(record['ranking']) == 39
    assert record['winner']['connected_final_score'] == max(r['connected_final_score'] for r in record['ranking'])
    original = read(record['original_frozen_selection_source'])
    assert record['winner'][GRAPH_FIELD] == original['winner'][GRAPH_FIELD]
    assert record['winner']['metrics'] == original['winner']['metrics']
    for relative, digest in record['frozen_sha256'].items():
        assert sha(ROOT / relative) == digest, relative
    for path,digest in record['frozen_external_input_sha256'].items():assert sha(path)==digest,path
    assert sha(record['original_frozen_selection_source']) == record['original_frozen_selection_sha256']
    return record
