"""Independent branch and parameter-history checks before joint scoring."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import ast
import json
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
from selected_scheme_graph_20261004 import compile_graph,with_weight_overrides,prior_delta,ROLE_ROUNDS,LATE_GROUPS,SHIFT_FIELDS
from verify_role_layer_replay_20261004 import sha,dump
OUT=ROOT/'analysis/selected_scheme_graph_preflight_20261004'


def main():
    OUT.mkdir(exist_ok=True)
    assert not (OUT/'verification.json').exists()
    sources=[Path(__file__),ROOT/'analysis/selected_scheme_graph_20261004.py',
             ROOT/'analysis/optimization_20261003_r25/selection.json']
    sources += [ROOT/f'analysis/optimize_training_round{number}.py' for number in range(31,50)]
    inputs={str(path.resolve()):sha(path) for path in sources}
    dump(OUT/'frozen_before_controls.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'input_sha256':inputs,'test_labels_read':False,'new_quality_scores':0})
    base=json.loads(sources[2].read_text(encoding='utf-8'))['winner']
    empty={role:{'model':'none','weight':0.} for role in ('membership','top','rest')}
    base.update(linear_augmentation=deepcopy(empty),linear_limit_delta=.00000000000000001,
                standalone=None,standalone_replacement=False)
    for index,group in enumerate(LATE_GROUPS):
        base[group+'_augmentation']=deepcopy(empty)
        base[group+'_limit_delta']=.00000000000000001*(index+2)
    cfgs={number:deepcopy(base) for number in range(30,50)}
    for number,group in ROLE_ROUNDS.items():
        cfgs[number]['retention']=.9+number/1000.
        cfgs[number][group+'_augmentation']['rest']={'model':f'fixed_model_{number}','weight':.1}
    cfgs[49]['temporal_postprocessing']={'alpha':.9,'mix':.1,'power':1.}
    graph=compile_graph(cfgs)
    assert graph['root']['round']==30 and [node['round'] for node in graph['layers']]==list(ROLE_ROUNDS)
    assert [node['retention'] for node in graph['layers']]==[.931,.933,.935,.937,.939,.941,.943,.945,.947]
    # Compare shift arithmetic with each actual historical predict method's AST.
    shifts=[]
    for number,group in ROLE_ROUNDS.items():
        source=(ROOT/f'analysis/optimize_training_round{number}.py').read_text(encoding='utf-8-sig')
        tree=ast.parse(source)
        method=next(method for node in tree.body if isinstance(node,ast.ClassDef) and node.name=='Context'
                    for method in node.body if isinstance(method,ast.FunctionDef) and method.name=='predict')
        assignment=next(statement for statement in method.body if isinstance(statement,ast.Assign)
                        and any(isinstance(target,ast.Name) and target.id=='delta' for target in statement.targets))
        scope={'delta':cfgs[number]['limit_up_delta'],'self':SimpleNamespace(_foundation_configuration=cfgs[number])}
        exec(compile(ast.Module(body=[assignment],type_ignores=[]),f'round{number}_actual_delta','exec'),{'__builtins__':{}},scope)
        assert prior_delta(cfgs[number],group)==scope['delta']
        shifts.append({'round':number,'actual_source_arithmetic_bit_exact':True})
    original=deepcopy(graph)
    axis=(31,'regularization_augmentation','rest')
    modified=with_weight_overrides(graph,{axis:0.})
    assert graph==original and modified['layers'][0]['specs']['rest']['weight']==0.
    assert all(modified['layers'][index]==graph['layers'][index] for index in range(1,9))
    # First replacement removes31/33; the later replacement removes35/37.
    for number in (34,38):
        cfgs[number]['standalone_replacement']=True
        cfgs[number]['standalone']={'model':f'new_backbone_{number}','postprocessing':{'alpha':.9,'weight':.25}}
    replaced=compile_graph(cfgs)
    assert replaced['root']['round']==38
    assert [node['round'] for node in replaced['layers']]==[39,41,43,45,47]
    assert [node['discarded_layer_rounds'] for node in replaced['discarded_branches']]==[[31,33],[35,37]]
    assert [axis['round'] for axis in replaced['active_weight_axes']]==[39,41,43,45,47]
    assert replaced['temporal_postprocessing']==cfgs[49]['temporal_postprocessing']
    for path,digest in inputs.items():assert sha(path)==digest,path
    dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'actual_9_historical_shift_expressions':shifts,'different_per_stage_retentions_preserved':True,
        'two_standalone_replacements_discard_correct_branches':True,'weight_changes_preserve_downstream_parameters':True,
        'original_graph_not_mutated':True,'late_temporal_parameters_preserved':True,
        'test_labels_read':False,'new_quality_scores':0,'input_sha256':inputs,
        'scope':'Recipe compiler checks; actual selected R30–49 graph andwhole numerical replay await completed rounds.'})
    print('Selected-scheme graph compiler controls passed')


if __name__=='__main__':main()
