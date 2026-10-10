"""Export95/96 with their immutable whole ranking and complete QA v6."""
from pathlib import Path


def install(sync):
    original = sync.snapshot
    source = sync.ROOT / 'analysis/sync_validated_rounds_main_20261005.py'
    text = source.read_text(encoding='utf-8')
    patches = {
        'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
        "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'":
            "ROOT / f'analysis/lossless_ranking_display_qa_v7_20261006/round{number}/qa/interaction_result.json'",
        'assert sha(board_path.read_bytes()) == board_sha':
            'assert sha(gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())) == board_sha',
    }
    for before, after in patches.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    namespace = dict(sync.__dict__, __name__='actual_goss_reference_immutable_export')
    exec(compile(text, str(source), 'exec'), namespace)
    namespace['complete_round_evidence'] = sync.complete_round_evidence

    def snapshot(number):
        if number != 97:
            return original(number)
        from collect_full_lossless_round_publication_20261006 import collect
        expected = 151
        full_payload, full = collect(number, 7, expected)
        namespace['PUBLICATION_FULL_REPORT'] = sync.ROOT / (
            f'analysis/lossless_ranking_display_v2_20261006/round{number}/full_report_reconstructed_for_publication.json.gz')
        manifest, payload = namespace['snapshot'](number)
        assert manifest['scored_records'] == full['scored_records']
        assert manifest['connected_records'] == full['connected_records']
        assert manifest['original_full_ranking_sha256'] == full['original_full_ranking_sha256']
        payload.update(full_payload)
        manifest['local_input_source_sha256'].update(full['local_input_source_sha256'])
        manifest['exported_files'].update(full['exported_files'])
        relative = Path(f'validation_sync/round{number}')
        attributes = (relative / '.gitattributes').as_posix()
        payload[attributes] = b'* -text\n'
        manifest['exported_files'][attributes] = {'bytes': 8, 'sha256': sync.sha(payload[attributes])}
        manifest['immutable_all_values_lossless_display_and_complete_original_QA_published'] = True
        manifest['actual_complete_QA_version'] = 7
        payload[(relative / 'manifest.json').as_posix()] = sync.encoded(manifest)
        return manifest, payload

    sync.snapshot = snapshot
    return original
