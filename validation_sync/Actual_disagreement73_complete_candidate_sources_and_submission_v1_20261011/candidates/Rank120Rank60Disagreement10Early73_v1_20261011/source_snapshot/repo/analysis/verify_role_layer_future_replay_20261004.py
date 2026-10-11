"""Actual frozen-model future replay for the prospective joint-layer kernel."""
from copy import deepcopy
from pathlib import Path
import json
import os
import sys
import time
for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
    os.environ[variable]='8'
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'analysis/connected_validation_20261002'
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(HERE)]
import numpy as np
import pandas as pd
import polars as pl
from run import FEATURE_FILE,to_matrix
from return_mapping import apply_mapping,daily_percentile
from optimize_wave15 import daily_ranks
import pairwise_model_sources_20261003 as trainer
import build_market_regime_bank_20261003 as regime
from role_layer_replay_20261004 import finish_layer,replay_layers
from verify_role_layer_replay_20261004 import Context,sha,dump,legacy

OUT=ROOT/'analysis/role_layer_future_replay_qa_20261004'
FORMAL=ROOT/'deliveries/connected_topk0175_20261003'
R25=ROOT/'candidates/optimization_20261003_r25'
R24=ROOT/'candidates/optimization_20261003_r24'
KEYS=['ts_code','trade_date']


class FutureContext(Context):
    def __init__(self,frame,signals,state_values):
        super().__init__(frame)
        self.cache=signals
        self.regimes=state_values

    def signal(self,name):
        return self.cache[name][:len(self.dates)]


def main():
    OUT.mkdir(exist_ok=True)
    proof=ROOT/'analysis/role_layer_replay_preflight_20261004/verification.json'
    assert json.loads(proof.read_text(encoding='utf-8'))['status']=='passed'
    if (OUT/'verification.json').exists():
        print((OUT/'verification.json').read_text(encoding='utf-8'));return
    selected=json.loads((R25/'selection.json').read_text(encoding='utf-8'))
    winner=selected['winner']
    verification=json.loads((R25/'verification.json').read_text(encoding='utf-8'))
    assert verification['status']=='passed'
    used=sorted({spec['model'] for spec in winner['final_augmentation'].values() if spec['weight']>0})
    models={name:verification['models']['final_'+name] for name in used}
    mappings_path=ROOT/'candidates/optimization_20261003_r26/market_regime_mapping.json'
    mappings=json.loads(mappings_path.read_text(encoding='utf-8'))['mappings']
    sources=[Path(__file__),ROOT/'analysis/role_layer_replay_20261004.py',
             ROOT/'analysis/verify_role_layer_replay_20261004.py',proof,
             Path(trainer.__file__),Path(regime.__file__),Path(FEATURE_FILE),
             HERE/'optimize_wave13.py',HERE/'optimize_wave15.py',HERE/'return_mapping.py',
             FORMAL/'generation_inputs.parquet',FORMAL/'train_test.json',
             R24/'rank_prediction.npy',R24/'manifest.json',R24/'verification.json',
             R25/'rank_prediction.npy',R25/'submission.csv',R25/'selection.json',R25/'verification.json',
             R25/'return_mapping.json',mappings_path,ROOT/'data/raw/测试集_X.csv',ROOT/'active_release.json']
    sources += [Path(info['path']) for info in models.values()]
    sources += [ROOT/f'analysis/optimize_training_round{number}.py' for number in (25,29,47)]
    inputs_sha={str(path.resolve()):sha(path) for path in sources}
    dump(OUT/'frozen_before_controls.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'input_sha256':inputs_sha,'test_labels_read':False,'new_quality_scores':0,
         'preset':'Frozen R25 selected layer, then two fixed additional layers; R26 state maps are implementation controls only.'})
    # All parameters and existing mature full-training models were fixed above.
    inputs=pl.read_parquet(FORMAL/'generation_inputs.parquet')
    assert 'y_ret_1d' not in inputs.columns and 'y_rank' not in inputs.columns
    features=json.loads((FORMAL/'train_test.json').read_text(encoding='utf-8'))['features']
    frame=pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(KEYS+features).sort('trade_date','ts_code').collect()
    assert frame.select(KEYS).equals(inputs.select(KEYS))
    dates=inputs['trade_date'].to_numpy();valid=inputs['price_valid'].to_numpy()
    x=to_matrix(frame,features)
    signals={};reloads=[]
    prefix_days=80
    n=int(np.searchsorted(dates,np.unique(dates)[prefix_days-1],side='right'))
    for name,info in models.items():
        source=Path(info['path']);assert sha(source)==info['sha256']
        meta=info['training_info']['training_meta']
        assert meta['last']<meta['cutoff_exclusive'] and meta['last_label_end']<=meta['cutoff_exclusive']
        raw=trainer.predict_arrays(trainer.load_bundle(source),x,dates=dates,valid=valid)
        reloaded=trainer.predict_arrays(trainer.load_bundle(source),x,dates=dates,valid=valid)
        prefix=trainer.predict_arrays(trainer.load_bundle(source),x[:n],dates=dates[:n],valid=valid[:n])
        assert np.array_equal(raw,reloaded) and np.array_equal(raw[:n],prefix)
        assert np.isfinite(raw).all()
        raw[~valid]=-1e6
        signals[name]=daily_ranks(raw,valid,dates)
        reloads.append({'name':name,'model_sha256':info['sha256'],'full_reload_exact':True,'actual80_day_model_prefix_exact':True})
    state_frame=frame.select(KEYS+['RET1','RVOL20']).with_columns(inputs['price_valid'])
    states=regime.future_values(mappings,state_frame)
    prefix_states=regime.future_values(mappings,state_frame.head(n))
    for name,values in states.items():
        assert np.array_equal(values[:n],prefix_states[name]),name
    context=FutureContext(inputs,signals,states)
    prefix_context=FutureContext(inputs.head(n),{name:values[:n] for name,values in signals.items()},prefix_states)
    foundation=np.load(R24/'rank_prediction.npy')
    manifest=json.loads((R24/'manifest.json').read_text(encoding='utf-8'))
    assert sha(R24/'rank_prediction.npy')==manifest['files']['rank_prediction.npy']['sha256']
    layer={'name':'frozen_r25','specs':winner['final_augmentation'],'retention':winner['retention'],
           'original_delta':winner['limit_up_delta'],'additional_delta':winner['final_limit_delta']}
    actual,stats=finish_layer(context,foundation,layer['specs'],layer['retention'],layer['original_delta'],layer['additional_delta'])
    assert np.array_equal(actual,np.load(R25/'rank_prediction.npy'))
    assert np.array_equal(actual[:n],replay_layers(prefix_context,foundation[:n],[layer])[0])
    mapping=json.loads((R25/'return_mapping.json').read_text(encoding='utf-8'))
    mapped=apply_mapping(mapping,daily_percentile(inputs.select('trade_date').to_pandas(),actual))
    bridge=pl.read_csv(ROOT/'data/raw/测试集_X.csv',schema_overrides={'trade_date':pl.Int32}).select(KEYS).with_row_index('position')
    submission=inputs.select(KEYS).with_columns(pl.Series('pred',mapped)).join(bridge,on=KEYS,how='inner',validate='1:1').sort('position').select(KEYS+['pred'])
    assert len(submission)==1599600 and submission['trade_date'].n_unique()==344
    assert submission.unique(KEYS).height==1599600 and np.isfinite(submission['pred'].to_numpy()).all()
    assert submission.select(KEYS).equals(bridge.select(KEYS))
    csv_bytes=submission.write_csv(float_precision=17).encode('utf-8')
    assert csv_bytes==(R25/'submission.csv').read_bytes()
    target=OUT/'replayed_frozen_r25_submission.csv';target.write_bytes(csv_bytes)
    second=deepcopy(layer);second.update(name='late_top_rest',original_delta=layer['original_delta']+layer['additional_delta'],additional_delta=.004)
    second['specs']={'membership':{'model':'none','weight':0.},
                     'top':{'model':used[0],'weight':.1},'rest':{'model':used[-1],'weight':.25}}
    third=deepcopy(second);third.update(name='late_state_membership',original_delta=second['original_delta']+.004)
    third['specs']['membership']={'model':used[-1],'weight':.1,'regime':'return_dispersion','low':0.,'high':.1}
    chain=[layer,second,third]
    chained,_=replay_layers(context,foundation,chain)
    expected=foundation
    for item,(number,group) in zip(chain,((25,'final'),(29,'linear'),(47,'fourier_tuning'))):
        expected,_=legacy(context,expected,item,number,group)
    assert np.array_equal(chained,expected)
    assert np.array_equal(chained[:n],replay_layers(prefix_context,foundation[:n],chain)[0])
    for path,digest in inputs_sha.items():
        assert sha(path)==digest,path
    dump(OUT/'verification.json',{'status':'passed','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'rows':1599600,'days':344,'codes':4650,'models':reloads,
         'frozen_r25_rank_output_exact':True,'frozen_r25_official_csv_byte_exact':True,
         'frozen_csv_sha256':sha(target),'three_layers_legacy_replay_exact':True,
         'three_layers_actual80_day_prefix_exact':True,'causal_state_actual80_day_prefix_exact':True,
         'new_quality_scores':0,'test_labels_read':False,'input_sha256':inputs_sha,
         'scope':'Prospective role kernel with actual frozen models; whole selected R49 provenance graph andjoint search remain pending.'})
    print('Role-layer actual future replay passed',flush=True)


if __name__=='__main__':main()
