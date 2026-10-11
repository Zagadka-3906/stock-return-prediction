"""Encode every report value losslessly using shared nodes and shared string chunks."""
from pathlib import Path
import ast
import hashlib
import json
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
REPORT = ROOT / 'results/all_model_rankings_20261003.json'
OLD_HTML = ROOT / 'results/all_model_rankings_20261003.html'
BUILDER = A / 'build_all_model_rankings_20261003.py'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write('\n')


def pack_report(report):
    nodes, lookup = [], {}

    def encode(value):
        if isinstance(value, dict):
            items = tuple((key, encode(child)) for key, child in value.items())
            key, node = ('object', items), [2, items]
        elif isinstance(value, list):
            items = tuple(encode(child) for child in value)
            key, node = ('array', items), [1, items]
        elif isinstance(value, str) and len(value) > 512:
            items = tuple(encode(value[offset:offset + 256]) for offset in range(0, len(value), 256))
            key, node = ('long_string', value), [3, items]
        else:
            assert value is None or isinstance(value, (str, int, float, bool))
            key, node = (type(value).__name__, value), [0, value]
        if key not in lookup:
            lookup[key] = len(nodes)
            nodes.append(node)
        return lookup[key]

    root = encode(report)
    return {'codec': 'typed_shared_nodes_and256_character_string_chunks_v1', 'root': root, 'nodes': nodes}


def unpack_report(packed):
    cache = {}

    def decode(index):
        if index not in cache:
            kind, value = packed['nodes'][index]
            if kind == 0:
                result = value
            elif kind == 1:
                result = [decode(child) for child in value]
            elif kind == 2:
                result = {key: decode(child) for key, child in value}
            else:
                assert kind == 3
                result = ''.join(decode(child) for child in value)
            cache[index] = result
        return cache[index]

    return decode(packed['root'])


DECODE_JS = """const packed=JSON.parse(document.getElementById('data').textContent);
const decodedNodes=new Map();
function decodeNode(id){
 if(!decodedNodes.has(id)){
  const [kind,value]=packed.nodes[id];
  let result;
  if(kind===0)result=value;
  else if(kind===1)result=value.map(decodeNode);
  else if(kind===2)result=Object.fromEntries(value.map(([key,child])=>[key,decodeNode(child)]));
  else if(kind===3)result=value.map(decodeNode).join('');
  else throw new Error('Invalid lossless node type');
  decodedNodes.set(id,result);
 }
 return decodedNodes.get(id);
}
const report=decodeNode(packed.root);
const fullCodecVerified=packed.nodes.every(([kind,value],id)=>{
 const result=decodeNode(id);
 if(kind===0)return result===value;
 if(kind===1)return result.length===value.length&&value.every((child,i)=>result[i]===decodeNode(child));
 if(kind===2)return Object.keys(result).length===value.length&&value.every(([key,child])=>result[key]===decodeNode(child));
 return kind===3&&result===value.map(decodeNode).join('');
});
if(!fullCodecVerified)throw new Error('Full lossless codec verification failed');"""


def main(number):
    assert number == 118
    out = A / 'lossless_ranking_display_v2_20261006' / f'round{number}'
    assert not out.exists()
    out.mkdir(parents=True)
    source_inputs = {str(path.resolve()): sha(path) for path in (Path(__file__), REPORT, OLD_HTML, BUILDER)}
    create(out / 'frozen_before_encoding.json', {'input_sha256': source_inputs,
        'all_report_values_and_all_original_six_views_must_roundtrip_exactly': True,
        'scientific_sources_scores_predictions_and_original_report_not_modified': True,
        'original_HTML_is_display_input_and_not_a_lifetime_scientific_dependency': True})
    try:
        report = json.loads(REPORT.read_text(encoding='utf-8'))
        assert report['summary']['later_round_records'][str(number)] > 0
        packed = pack_report(report)
        decoded = unpack_report(packed)
        assert decoded == report
        for view in ('representative', 'connected', 'mlp_bounds', 'historical', 'csv_test', 'legacy_annual'):
            assert decoded[view] == report[view]
        # Require the serialized codec to pass the same complete reconstruction.
        compact = json.dumps(packed, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
        assert unpack_report(json.loads(compact)) == report
        source = ast.parse(BUILDER.read_text(encoding='utf-8'))
        page = next(ast.literal_eval(node.value) for node in source.body
                    if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'PAGE' for target in node.targets))
        original_decode = "const report=JSON.parse(document.getElementById('data').textContent);"
        assert page.count(original_decode) == 1 and page.count('__DATA__') == 1
        page = page.replace(original_decode, DECODE_JS)
        all_option = '<option value="10000">全部</option>'
        assert page.count(all_option) == 1
        page = page.replace(all_option, f'<option value="{len(report["connected"])}">全部</option>')
        with OLD_HTML.open('r', encoding='utf-8') as stream:
            prefix = stream.read(32768)
        banner = re.search(r'<p style="background:#fff1d6.*?</p>', prefix, re.S)
        best = max(row['score'] for row in report['connected'] if not row['known_restriction'])
        html = (page.replace('__DATA__', compact.replace('</', '<\\/'))
            .replace('__PROVENANCE_BANNER__', banner.group(0) if banner else '')
            .replace('__REPORT_DATE__', time.strftime('%Y-%m-%d %H:%M'))
            .replace('__VALIDATION_BEST__', f'{best:.9f}')
            .replace('__CONNECTED_COUNT__', f"{len(report['connected']):,}"))
        destination = out / 'complete_rankings_lossless.html'
        with destination.open('x', encoding='utf-8') as stream:
            stream.write(html)
        for path, digest in source_inputs.items():
            assert sha(path) == digest, path
        proof = {'status': 'passed_all_original_report_values_and_six_views_lossless_roundtrip',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'round': number,
            'connected_records': len(report['connected']), 'node_count': len(packed['nodes']),
            'original_HTML_bytes': OLD_HTML.stat().st_size, 'lossless_HTML_bytes': destination.stat().st_size,
            'lossless_HTML_sha256': sha(destination), 'original_report_sha256': source_inputs[str(REPORT.resolve())],
            'all_original_record_values_parameters_source_pointers_and_scores_preserved': True,
            'all_original_six_views_fully_reconstructed': True,
            'input_sha256': source_inputs, 'new_model_fits': 0, 'new_quality_scores': 0,
            'original_scientific_sources_and_original_report_unchanged': True,
            'actual_browser_full_interaction_QA_still_required': True, 'test_labels_read': False}
        create(out / 'verification.json', proof)
        print(json.dumps({key: proof[key] for key in ('status', 'round', 'connected_records', 'node_count', 'original_HTML_bytes', 'lossless_HTML_bytes')}, ensure_ascii=False), flush=True)
        return destination
    except BaseException as error:
        create(out / 'failure.json', {'status': 'failed_preserved_lossless_encoding_attempt',
            'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'error': f'{type(error).__name__}: {error}'})
        raise


if __name__ == '__main__':
    main(int(sys.argv[1]))
