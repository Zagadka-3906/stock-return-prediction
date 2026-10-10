"""Frozen complete-root/late-layer model replay and independently cold prefixes."""
from copy import deepcopy
from pathlib import Path
import json
import os
import sys
import time
for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[variable]='8'
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import numpy as np
from verify_role_layer_replay_20261004 import sha,dump
from verify_whole_scheme_runtime_20261004 import root_graph,cfg,layer
from whole_scheme_future_runtime_20261004 import build_context,resolve_native_sources,candidate_models,copy_models
OUT=ROOT/'analysis/whole_scheme_future_runtime_qa_20261004'
FORMAL=ROOT/'deliveries/connected_topk0175_20261003'
KEYS=['ts_code','trade_date']


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def main():
    import psutil
    gate=ROOT/'analysis/whole_scheme_runtime_preflight_20261004/verification.json'
    while not gate.exists() or psutil.virtual_memory().available<8*2**30:time.sleep(10)
    assert read(gate)['status']=='passed'
    import polars as pl
    from run import FEATURE_FILE
    from return_mapping import apply_mapping,daily_percentile
    OUT.mkdir(exist_ok=True);assert not (OUT/'verification.json').exists()
    cases=[]
    for number in (18,24,26):
        graph=root_graph(cfg(18 if number==18 else 24))
        if number==26:graph['layers']=[layer(26)]
        cases.append({'name':f'known_r{number}','graph':graph,
                      'root_candidate':ROOT/f'candidates/optimization_20261003_r{18 if number==18 else 24}',
                      'expected_candidate':ROOT/f'candidates/optimization_20261003_r{number}'})
    widest=ROOT/'analysis/fourier_tuning_future_pipelines_qa_20261004'
    preset=deepcopy(read(widest/'diagnostic_frozen_before_inference.json')['standalone_configuration'])
    cases.append({'name':'standalone_fourier575','graph':{
        'root':{'kind':'standalone','round':48,'configuration':preset},'layers':[],'temporal_postprocessing':None},
        'root_candidate':widest/'standalone_candidate','expected_candidate':widest/'standalone_candidate'})
    mappings_path=ROOT/'candidates/optimization_20261003_r26/market_regime_mapping.json'
    mappings=read(mappings_path)['mappings']
    sources=[Path(__file__),ROOT/'analysis/whole_scheme_future_runtime_20261004.py',
        ROOT/'analysis/whole_scheme_replay_runtime_20261004.py',ROOT/'analysis/verify_whole_scheme_runtime_20261004.py',
        ROOT/'analysis/role_layer_replay_20261004.py',ROOT/'analysis/replay_complete_scheme_20261003.py',gate,
        Path(FEATURE_FILE),FORMAL/'generation_inputs.parquet',FORMAL/'train_test.json',
        ROOT/'data/raw/测试集_X.csv',ROOT/'active_release.json',mappings_path,
        ROOT/'analysis/fourier_tuning_model_sources_20261004.py',ROOT/'analysis/causal_model_loading_20261004.py',
        widest/'verification.json',widest/'diagnostic_frozen_before_inference.json']
    for case in cases:
        root=case['graph']['root'];overrides={root['round']:case['root_candidate']}
        case['native_sources']=resolve_native_sources(case['graph'],overrides)
        case['root_sources']=candidate_models(case['root_candidate'])
        for candidate in (case['root_candidate'],case['expected_candidate']):
            sources += [candidate/'verification.json',candidate/'selection.json',candidate/'rank_prediction.npy',
                        candidate/'return_mapping.json',candidate/'submission.csv']
        sources += [Path(info['path']) for info in case['native_sources'].values()]
        sources += [Path(info['path']) for info in case['root_sources'].values()]
    inputs_sha={str(path.resolve()):sha(path) for path in dict.fromkeys(sources)}
    dump(OUT/'frozen_before_controls.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'case_graphs':{case['name']:case['graph'] for case in cases},'input_sha256':inputs_sha,
        'new_quality_scores':0,'test_labels_read':False,'existing_return_maps_are_implementation_controls_only':True})
    inputs=pl.read_parquet(FORMAL/'generation_inputs.parquet')
    features=read(FORMAL/'train_test.json')['features']
    test=pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(KEYS+features).sort('trade_date','ts_code').collect()
    assert test.select(KEYS).equals(inputs.select(KEYS))
    dates=inputs['trade_date'].to_numpy();n=int(np.searchsorted(dates,np.unique(dates)[79],side='right'))
    bridge=pl.read_csv(ROOT/'data/raw/测试集_X.csv',schema_overrides={'trade_date':pl.Int32}).select(KEYS).with_row_index('position')
    records=[]
    for case in cases:
        graph=case['graph'];folder=OUT/case['name'];folder.mkdir(exist_ok=True)
        copied=copy_models(case['native_sources'],case['root_sources'],folder/'models')
        native={name:copied['whole_'+name] for name in case['native_sources']}
        root_sources={name:copied[name] for name in case['root_sources']}
        context,models=build_context(graph,inputs,test,native,root_sources,mappings)
        pred,_=context.predict(context.donor(context.finished('baseline')),0.,0.)
        assert np.array_equal(pred,np.load(case['expected_candidate']/'rank_prediction.npy')),case['name']
        mapping=read(case['expected_candidate']/'return_mapping.json')
        mapped=apply_mapping(mapping,daily_percentile(inputs.select('trade_date').to_pandas(),pred))
        submission=inputs.select(KEYS).with_columns(pl.Series('pred',mapped)).join(bridge,on=KEYS,how='inner',validate='1:1').sort('position').select(KEYS+['pred'])
        assert len(submission)==1599600 and submission['trade_date'].n_unique()==344
        assert submission.unique(KEYS).height==1599600 and np.isfinite(submission['pred'].to_numpy()).all()
        assert submission.select(KEYS).equals(bridge.select(KEYS))
        data=submission.write_csv(float_precision=17).encode('utf-8')
        assert data==(case['expected_candidate']/'submission.csv').read_bytes(),case['name']
        target=folder/'submission.csv';target.write_bytes(data)
        prefix,prefix_models=build_context(graph,inputs.head(n),test.head(n),native,root_sources,mappings)
        prefix_pred,_=prefix.predict(prefix.donor(prefix.finished('baseline')),0.,0.)
        assert np.array_equal(pred[:n],prefix_pred),case['name']
        records.append({'case':case['name'],'rows':1599600,'days':344,'codes':4650,
            'complete_rank_output_bit_identical':True,'complete_return_csv_byte_identical':True,
            'actual_models_reloaded_and_root_postprocessing_restarted_for80_day_prefix':True,
            'prefix_rows':n,'models':models,'prefix_model_reload_checks':prefix_models,'csv_sha256':sha(target)})
        print(json.dumps(records[-1],ensure_ascii=False),flush=True)
        del context,prefix,submission
    for path,digest in inputs_sha.items():assert sha(path)==digest,path
    dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'cases':records,'new_quality_scores':0,'test_labels_read':False,'input_sha256':inputs_sha,
        'scope':'Complete frozen-root, state-dependent late-layer and575-column standalone branches; actualR49 joint winner remains gated.'})
    print('Whole selected-scheme actual future runtime controls passed',flush=True)


if __name__=='__main__':main()
