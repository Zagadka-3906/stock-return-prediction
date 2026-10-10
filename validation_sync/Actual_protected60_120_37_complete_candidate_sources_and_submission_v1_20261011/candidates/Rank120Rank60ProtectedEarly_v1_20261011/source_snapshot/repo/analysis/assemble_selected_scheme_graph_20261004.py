"""Assemble the actual selected history after every required round is published.

This only freezes provenance.  A numerical whole-scheme replay and its future
implementation controls must pass before any joint candidate is scored.
"""
from pathlib import Path
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
from selected_scheme_graph_20261004 import compile_graph
from verify_role_layer_replay_20261004 import sha,dump
OUT=ROOT/'analysis/whole_selected_scheme_graph_20261004'


def main():
    OUT.mkdir(exist_ok=True)
    qa_files=[ROOT/'analysis/role_layer_replay_preflight_20261004/verification.json',
              ROOT/'analysis/role_layer_future_replay_qa_20261004/verification.json',
              ROOT/'analysis/selected_scheme_graph_preflight_v2_20261004/verification.json']
    for path in qa_files:
        assert json.loads(path.read_text(encoding='utf-8'))['status']=='passed'
    gates=[ROOT/f'results/optimization_20261003_r{number}.json' for number in range(30,50)]
    missing=[str(path.relative_to(ROOT)) for path in gates if not path.exists()]
    if missing:
        readiness={'status':'waiting_for_completed_selected_rounds','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
                   'missing':missing,'kernel_and_recipe_compiler_controls_passed':True,
                   'new_quality_scores':0,'test_labels_read':False}
        (OUT/'readiness.json').write_text(json.dumps(readiness,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(readiness,ensure_ascii=False));return
    if (OUT/'graph.json').exists():
        saved=json.loads((OUT/'graph.json').read_text(encoding='utf-8'))
        for path,digest in saved['input_sha256'].items():assert sha(path)==digest,path
        print('Previously frozen selected graph verified');return
    sources=[Path(__file__),ROOT/'analysis/selected_scheme_graph_20261004.py',
             ROOT/'analysis/role_layer_replay_20261004.py',ROOT/'后续选模标准.md',*qa_files,*gates]
    configurations={}
    for number,path in zip(range(30,50),gates):
        result=json.loads(path.read_text(encoding='utf-8'))
        configurations[number]=result['winner']
        folder=ROOT/f'analysis/optimization_20261003_r{number}'
        candidate=ROOT/f'candidates/optimization_20261003_r{number}'
        selection=json.loads((folder/'selection.json').read_text(encoding='utf-8'))
        assert selection['winner']==result['winner']
        proof=json.loads((candidate/'verification.json').read_text(encoding='utf-8'))
        assert proof['status']=='passed'
        sources += [folder/'selection.json',folder/'protocol.json',folder/'selected_validation.npy',
                    candidate/'verification.json',candidate/'manifest.json']
        protocol=json.loads((folder/'protocol.json').read_text(encoding='utf-8'))
        for source,digest in protocol['input_sha256'].items():
            assert sha(source)==digest,source
            sources.append(Path(source))
    graph=compile_graph(configurations)
    frozen={'status':'provenance_graph_frozen_before_joint_refinement','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
            'graph':graph,'input_sha256':{str(path.resolve()):sha(path) for path in dict.fromkeys(sources)},
            'same_validation':'2020–2024 annual forward OOF;1212 continuous days;5635800 rows',
            'new_annual_fits':0,'new_quality_scores':0,'test_labels_read':False,
            'next_required_steps':['Numerically reproduce the complete selectedR49 validation output',
                                   'Reproduce its actual frozen-model future candidate',
                                   'Verify changed-layer cold prefixes andlabel poisoning',
                                   'Freeze bounded joint axes before mapped official scoring']}
    dump(OUT/'graph.json',frozen)
    print(json.dumps({'status':frozen['status'],'active_axes':len(graph['active_weight_axes']),
                      'effective_root_round':graph['root']['round'],'remaining_layers':len(graph['layers'])}))


if __name__=='__main__':main()
