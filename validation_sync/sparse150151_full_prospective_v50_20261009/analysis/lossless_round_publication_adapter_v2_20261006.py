"""Append immutable full display and complete QA proof to every prospective export."""
from pathlib import Path


def install(sync):
    original = sync.snapshot
    source = sync.ROOT / 'analysis/sync_validated_rounds_main_20261005.py'
    text = source.read_text(encoding='utf-8')
    patches = {
        'board_bytes = board_path.read_bytes()': 'board_bytes = gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())',
        "ROOT / 'analysis/all_model_ranking_qa/interaction_result.json'":
            "ROOT / f'analysis/lossless_ranking_display_qa_v{4 if number <= 90 else 5}_20261006/round{number}/qa/interaction_result.json'",
        'assert sha(board_path.read_bytes()) == board_sha':
            'assert sha(gzip.decompress(PUBLICATION_FULL_REPORT.read_bytes())) == board_sha',
    }
    for before, after in patches.items():
        assert text.count(before) == 1, before
        text = text.replace(before, after)
    namespace = dict(sync.__dict__, __name__='actual_immutable_full_ranking_export')
    exec(compile(text, str(source), 'exec'), namespace)
    namespace['complete_round_evidence'] = sync.complete_round_evidence

    def snapshot(number):
        if number == 81 or not 67 <= number <= 92:
            return original(number)
        root = sync.ROOT
        display = root / f'analysis/lossless_ranking_display_v2_20261006/round{number}'
        qa = root / f'analysis/lossless_ranking_display_qa_v{4 if number <= 90 else 5}_20261006/round{number}'
        from immutable_lossless_ranking_snapshot_20261006 import prepare
        full_report = prepare(display)
        namespace['PUBLICATION_FULL_REPORT'] = full_report
        manifest, payload = namespace['snapshot'](number)
        proof = sync.read(qa / 'verification.json')
        assert proof['status'] == 'passed_all_original_full_ranking_QA_and_lossless_browser_node_checks'
        assert proof['original_full_QA_result']['new_round_records'] == manifest['scored_records']
        assert proof['original_full_QA_result']['connected_records'] == manifest['connected_records']
        assert proof['original45_second_render_timeout_retained'] and proof['all_new_browser_profiles_under_D']
        relative = Path(f'validation_sync/round{number}')
        files = [display / name for name in ('frozen_before_encoding.json', 'verification.json',
            'complete_rankings_lossless.html', 'runtime_publication.json',
            'full_report_reconstructed_for_publication.json.gz', 'full_report_publication_snapshot_verification.json')]
        files += [qa / name for name in ('frozen_before_actual_full_QA.json', 'verification.json',
            'qa/interaction_result.json', 'qa/ranking_report.png')]
        for path in files:
            data = path.read_bytes()
            assert not sync.SECRET.search(data)
            destination = (relative / 'complete_ranking_display' / path.relative_to(root / 'analysis')).as_posix()
            payload[destination] = data
            manifest['local_input_source_sha256'][path.relative_to(root).as_posix()] = sync.sha(data)
            manifest['exported_files'][destination] = {'bytes': len(data), 'sha256': sync.sha(data)}
        payload[(relative / '.gitattributes').as_posix()] = b'* -text\n'
        manifest['exported_files'][(relative / '.gitattributes').as_posix()] = {'bytes': 8, 'sha256': sync.sha(b'* -text\n')}
        manifest['immutable_all_values_lossless_display_and_complete_original_QA_published'] = True
        payload[(relative / 'manifest.json').as_posix()] = sync.encoded(manifest)
        return manifest, payload

    sync.snapshot = snapshot
    return original
