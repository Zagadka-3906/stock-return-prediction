"""Real complete outputs, standalone resets and changed-root cold replays."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import json
import os
import sys
import time
for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[variable]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
from whole_scheme_replay_runtime_20261004 import ValidationContext,prefix_controls
from replay_complete_scheme_20261003 import empty_roles
from verify_role_layer_replay_20261004 import sha,dump
OUT=ROOT/'analysis/whole_scheme_runtime_preflight_20261004'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def cfg(number):return deepcopy(read(ROOT/f'analysis/optimization_20261003_r{number}/selection.json')['winner'])


def root_graph(configuration):
    configuration=deepcopy(configuration)
    configuration.setdefault('standalone',None)
    configuration.setdefault('secondary_augmentation',empty_roles())
    configuration.update(final_augmentation=empty_roles(),final_limit_delta=0.,
                         linear_augmentation=empty_roles(),linear_limit_delta=0.)
    return {'root':{'kind':'complete_r30','round':30,'configuration':configuration},
            'layers':[],'temporal_postprocessing':None}


def layer(number):
    row=cfg(number)
    return {'name':f'reference_final_r{number}','round':number,'group':'final_augmentation',
            'specs':row['final_augmentation'],'retention':row['retention'],
            'original_delta':row['limit_up_delta'],'additional_delta':row['final_limit_delta']}


def main():
    import psutil
    import optimize_training_round23 as standalone_reference
    import optimize_training_round25 as layer_reference
    from final_output_temporal_postprocessing_20261004 import transform
    while psutil.virtual_memory().available<8*2**30:time.sleep(10)
    OUT.mkdir(exist_ok=True)
    assert not (OUT/'verification.json').exists()
    paths={name:ROOT/f'analysis/optimization_20261003_r25/raw/{name}.npy'
           for name in ('tail_bce128_e32','rank512_seed18_e64')}
    paths['rank512_e32']=ROOT/'analysis/optimization_20261003_r23/raw/rank512_e32.npy'
    paths['rank_ridge_l01']=ROOT/'analysis/complete_scheme_replay_20261003/raw/rank_ridge_l01.npy'
    graphs=[root_graph(cfg(18)),root_graph(cfg(24))]
    for number in (25,26):
        graph=root_graph(cfg(24));graph['layers']=[layer(number)];graphs.append(graph)
    changed=deepcopy(graphs[-1])
    for spec in changed['root']['configuration']['secondary_augmentation'].values():
        if spec['weight']>0:spec['weight']*=.5
    assert changed!=graphs[-1]
    graphs.append(changed)
    standalone=cfg(23)
    standalone['standalone']={'model':'rank512_e32','postprocessing':dict(standalone_reference.BASE_POST,alpha=.9,weight=.25,bonus=.3)}
    standalone_graph={'root':{'kind':'standalone','round':32,'configuration':standalone},
                       'layers':[],'temporal_postprocessing':None}
    sources=[Path(__file__),ROOT/'analysis/whole_scheme_replay_runtime_20261004.py',
             ROOT/'analysis/replay_complete_scheme_20261003.py',ROOT/'analysis/role_layer_replay_20261004.py',
             ROOT/'analysis/final_output_temporal_postprocessing_20261004.py',
             ROOT/'analysis/complete_scheme_replay_20261003/protocol.json',
             ROOT/'analysis/complete_scheme_replay_20261003/oof_audit.json',
             ROOT/'analysis/role_layer_replay_preflight_20261004/verification.json',
             ROOT/'analysis/selected_scheme_graph_preflight_v2_20261004/verification.json',
             ROOT/'analysis/connected_validation_20261002/combined_fold_frame.parquet',
             ROOT/'analysis/optimize_training_round23.py',ROOT/'analysis/optimize_training_round25.py',*paths.values()]
    for number in (18,23,24,25,26):
        sources += [ROOT/f'analysis/optimization_20261003_r{number}/selection.json',
                    ROOT/f'analysis/optimization_20261003_r{number}/selected_validation.npy']
    inputs={str(path.resolve()):sha(path) for path in sources}
    dump(OUT/'frozen_before_controls.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'graphs':graphs+[standalone_graph],'input_sha256':inputs,'test_labels_read':False,'new_quality_scores':0})
    context=ValidationContext(graphs[0],paths=paths)
    records=[]
    for index,(number,graph) in enumerate(zip((18,24,25,26,None),graphs)):
        context.configure({'whole_scheme_graph':graph})
        promote=context.finished('baseline');pred,_=context.predict(context.donor(promote),0.,0.)
        if number is not None:
            assert np.array_equal(pred,np.load(ROOT/f'analysis/optimization_20261003_r{number}/selected_validation.npy',mmap_mode='r')),number
        else:
            base=context.root_context();root=graph['root']['configuration']
            raw,_=base.predict(base.donor(base.finished('baseline')),root['slow16_weight'],root['retention'],root['limit_up_delta'])
            reference=SimpleNamespace(**context.__dict__)
            reference.final_augmentation=deepcopy(graph['layers'][0]['specs'])
            reference.final_limit_delta=graph['layers'][0]['additional_delta']
            reference.signal=context.signal;reference.weights_for=context.weights_for
            expected,_=layer_reference.Context.finish_output(reference,raw,graph['layers'][0]['retention'],graph['layers'][0]['original_delta'])
            assert np.array_equal(pred,expected)
            assert not np.array_equal(pred,np.load(ROOT/'analysis/optimization_20261003_r26/selected_validation.npy',mmap_mode='r'))
        controls=prefix_controls(context,graph)
        records.append({'known_round':number,'changed_root_recomputes_final_output':number is None,
                        'full5635800_rows_exact':True,'controls':controls})
        print(json.dumps(records[-1],ensure_ascii=False),flush=True)
    del context
    context=ValidationContext(standalone_graph,paths=paths)
    context.standalone=standalone['standalone']
    ref_promote=standalone_reference.Context.finished(context,'baseline')
    expected,_=standalone_reference.Context.predict(context,ref_promote,0.,standalone['retention'],standalone['limit_up_delta'])
    actual,_=context.predict(context.donor(context.finished('baseline')),0.,0.)
    assert np.array_equal(expected,actual)
    controls=prefix_controls(context,standalone_graph)
    layered=deepcopy(standalone_graph)
    layered['layers']=[{'name':'late_linear','round':41,'group':'additive_ridge_augmentation',
        'specs':{'membership':{'model':'rank_ridge_l01','weight':.025},
                 'top':{'model':'rank512_seed18_e64','weight':.075},'rest':{'model':'none','weight':0.}},
        'retention':.97,'original_delta':standalone['limit_up_delta'],'additional_delta':.01}]
    layered['temporal_postprocessing']={'alpha':.995,'mix':.025,'power':2.}
    context.configure({'whole_scheme_graph':layered})
    actual,_=context.predict(context.donor(context.finished('baseline')),0.,0.)
    reference=SimpleNamespace(**context.__dict__)
    reference.final_augmentation=deepcopy(layered['layers'][0]['specs']);reference.final_limit_delta=.01
    reference.signal=context.signal;reference.weights_for=context.weights_for
    legacy,_=layer_reference.Context.finish_output(reference,expected,.97,standalone['limit_up_delta'])
    expected=transform(legacy,context.dates,context.valid,context.codes,layered['temporal_postprocessing'])
    assert np.array_equal(actual,expected)
    layered_controls=prefix_controls(context,layered)
    for path,digest in inputs.items():assert sha(path)==digest,path
    dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'validation_rows':5635800,'validation_days':1212,'known_complete_rounds':[18,24,25,26],
        'complete_output_controls':records,'standalone_reset_legacy_exact':True,
        'standalone_prefix_controls':controls,'late_layer_and_final_temporal_legacy_exact':True,
        'standalone_plus_late_layer_controls':layered_controls,'test_labels_read':False,'new_quality_scores':0,
        'input_sha256':inputs,'scope':'Complete runtime controls with existing selected schemes; actualR49 reconstruction andjoint optimization remain gated.'})
    print('Whole selected-scheme runtime controls passed',flush=True)


if __name__=='__main__':main()
