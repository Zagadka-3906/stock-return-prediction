"""Freeze independent membership and TopK recipe, then replay calibrated test-X inference."""
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'analysis'),str(ROOT/'analysis/connected_validation_20261002')]
import optimize_training_round14 as experiment
from optimize_training_round14 import OUT,PREVIOUS,expected,WAVES,RANKERS,FIELDS,MODELS,best,Context,HERE,ARCHIVE,KEYS,BASE_POST,read,dump,sha,log,verify
import finalize_training_round7 as shared
EXPECTED=expected()
CANDIDATE=ROOT/'candidates/optimization_20261003_r14'
FORMAL=ROOT/'deliveries/connected_topk0175_20261003'


def selected():
    verify();record=read(OUT/'selection.json')
    for name,digest in record['frozen_sha256'].items():assert sha(ROOT/name)==digest,name
    return record


def select():
    import numpy as np
    verify()
    if (OUT/'selection.json').exists():selected();return
    rows=[]
    for wave in WAVES:
        payload=read(OUT/f'wave{wave}_results.json');assert payload['status']=='complete'
        rows.extend(dict(wave=wave,arm=name,**row) for name,row in payload['results'].items())
    winner=best(rows)
    rows.sort(key=lambda r:(-r['connected_final_score'],r['wave'],r['arm']));assert winner['connected_final_score']>=EXPECTED
    ctx=ReleaseContext(winner);promote=ctx.finished('baseline',winner['recipe'])
    pred,_=ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    metrics=ctx.score(pred);assert abs(metrics['final_score']-winner['connected_final_score'])<1e-12
    np.save(OUT/'selected_validation.npy',pred);np.save(OUT/'promote_baseline.npy',promote)
    paths=[Path(__file__),OUT/'protocol.json',OUT/'component_audit.json',OUT/'combination_protocol.json',OUT/'weight_refinement_protocol.json',*[OUT/f'weight_refinement_{role}_protocol.json' for role in ('membership','top','rest')],OUT/'refinement_protocol.json',*[OUT/f'wave{wave}_results.json' for wave in WAVES],
           OUT/'selected_validation.npy',OUT/'promote_baseline.npy',*[OUT/f'rankers/{name}.npy' for name in MODELS],
           RANKERS/f'{winner["ensemble_name"]}.npy',RANKERS/f'{winner["top_ensemble_name"]}.npy',RANKERS/f'{winner["membership_ensemble_name"]}.npy',
           PREVIOUS/'selection.json',ROOT/'active_release.json',FORMAL/'generation_inputs.parquet',
           ROOT/'candidates/optimization_20261003_r13/verification.json']
    dump(OUT/'selection.json',{'status':'frozen_before_test_prediction','frozen_at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
         'winner':winner,'ranking':rows,'scored_records':len(rows),'baseline_score':EXPECTED,
         'score_gain':winner['connected_final_score']-EXPECTED,'pruned_member_excluded':True,
         'fold_local_pruning_repaired':True,'test_labels_read':False,
         'selection_rule':'highest official connected composite; exact ties prefer fewer model families and role ensembles',
         'frozen_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in dict.fromkeys(paths)}},immutable=True)
    log(f'Round14 selected {winner["arm"]}: {metrics["final_score"]:.9f}, gain={winner["connected_final_score"]-EXPECTED:+.9f}')


class ReleaseContext(Context):
    def __init__(self,winner=None):
        super().__init__();winner=winner or selected()['winner']
        self.configure(winner);self.recipe=winner['recipe']
    def promote(self,name):return self.finished(name,self.recipe)


def calibrate():
    shared.OUT=OUT;shared.selected=selected;shared.ReleaseContext=ReleaseContext;shared.verify=verify
    shared.calibrate()


def predict():
    import numpy as np
    import pandas as pd
    import polars as pl
    import lightgbm as lgb
    from experiments.final_sweep_wave3 import ensemble_raw
    from optimize_wave6 import make_prediction_param
    from optimize_wave15 import daily_ranks
    from return_mapping import apply_mapping,daily_percentile
    from src.scoring import Panel
    from run import FEATURE_FILE,to_matrix
    record=selected();winner=record['winner']
    assert read(OUT/'causal_validation.json')['status']==read(OUT/'calibrated_csv_official.json')['status']=='passed'
    if (CANDIDATE/'verification.json').exists():assert sha(CANDIDATE/'submission.csv')==read(CANDIDATE/'verification.json')['csv_sha256'];return
    CANDIDATE.mkdir(parents=True,exist_ok=True)
    import train_diverse_backbones_20261003 as trainer
    used=sorted({spec['model'] for spec in winner['diverse_augmentation'].values() if spec['weight']>0})
    full_info={name:trainer.train_one(name,2025) for name in used}
    for info in full_info.values():
        mature=info['training_meta']
        assert mature['last']<mature['cutoff_exclusive'] and mature['last_label_end']<=mature['cutoff_exclusive']
    inputs=pl.read_parquet(FORMAL/'generation_inputs.parquet').with_columns(pl.lit(None,dtype=pl.Float64).alias('y_ret_1d'))
    metadata=read(FORMAL/'train_test.json');features=metadata['features']
    test=pl.scan_parquet(FEATURE_FILE).filter(~pl.col('is_train')).select(KEYS+features).sort('trade_date','ts_code').collect()
    assert test.select(KEYS).equals(inputs.select(KEYS));vx=to_matrix(test,features)
    dates=inputs['trade_date'].to_numpy();valid=inputs['price_valid'].to_numpy()
    previous_models=read(ROOT/'candidates/optimization_20261003_r13/verification.json')['models']
    models={};topk_raw=[]
    for component in winner['recipe']['components']:
        name=f'seed{component["seed"]}_f{component["fraction"]:.3f}_r{component["rounds"]}'
        info=previous_models[name];assert sha(info['path'])==info['sha256']
        text=Path(info['path']).read_text(encoding='utf-8')
        raw=lgb.Booster(model_str=text).predict(vx,num_threads=8);raw[~valid]=-1e6
        replay=lgb.Booster(model_str=text).predict(vx,num_threads=8);replay[~valid]=-1e6
        assert np.array_equal(raw,replay)
        target=CANDIDATE/f'model_{name}.txt';target.write_text(text,encoding='utf-8')
        models[name]={'path':str(target),'sha256':sha(target),'original':info,'weight':component['weight']}
        topk_raw.append((component,raw))
    source_paths={'lgb':ARCHIVE/'releases/pooled_rms25/backbone_raw.parquet',
                  'xgb':ARCHIVE/'releases/ensemble4/T2f_xgboost_test_raw.parquet',
                  'two':ARCHIVE/'releases/ensemble4/W2c_two_day_test_raw.parquet',
                  'pruned':ARCHIVE/'releases/ensemble4/W2d_pruned_test_raw.parquet',
                  'gru':HERE/'w5a_test/gru_raw_test.npy'}
    raw_members={}
    for name,path in source_paths.items():
        if path.suffix=='.npy':raw=np.load(path).astype(np.float64)
        else:
            frame=pl.read_parquet(path).sort('trade_date','ts_code');assert frame.select(KEYS).equals(inputs.select(KEYS))
            raw=frame['pred_raw'].to_numpy().astype(np.float64)
        assert len(raw)==len(inputs);raw_members[name]=raw
    panel=Panel.from_frame(inputs)
    from optimize_training_round7 import ENSEMBLES
    old_raw=ensemble_raw(panel,ENSEMBLES['five_fold_local'],raw_members)
    assert np.array_equal(old_raw,inputs['w5a_raw'].to_numpy()),'Fulltrain five-way source reconstruction failed'
    assert all('pruned' not in winner[key] for key in ('ensemble_weights','top_ensemble_weights','membership_ensemble_weights'))
    aux=inputs['aux_raw'].to_numpy()
    def process(raw,settings):return make_prediction_param(Panel.from_frame(inputs.with_columns(pl.Series('pred_raw',raw))),aux,**settings)
    ctx=Context.__new__(Context)
    ctx.dates=dates;ctx.flags=inputs['flag_limit_up'].to_numpy().astype(np.int64);ctx.valid=valid
    ctx.codes,unique=pd.factorize(inputs['ts_code'].to_pandas(),sort=True);ctx.codes=ctx.codes.astype(np.int64)
    ctx.n_codes=len(unique);ctx.tie_key=1-ctx.codes/max(ctx.n_codes-1,1)
    ctx.pdf=inputs.select(['trade_date','flag_limit_up']).to_pandas()
    ctx.ensemble_name=ctx.rest_ensemble_name=winner['ensemble_name'];ctx.top_ensemble_name=winner['top_ensemble_name']
    ctx.membership_mode=winner['membership_mode'];ctx.rerank_weight=winner['membership_w5a_weight'];ctx.top_slow_weight=winner['top_slow_weight']
    ctx.add_priority_weight=winner['add_priority_weight'];ctx.drop_priority_weight=winner['drop_priority_weight']
    ctx.priority_signal=winner['priority_signal'];ctx.membership_signal=winner['membership_signal'];ctx.rest_slow_weight=winner['slow16_weight']
    ctx.membership_ensemble_name=winner['membership_ensemble_name'];ctx.membership_slow_weight=winner['membership_slow_weight']
    ctx.membership_power=winner['membership_power'];ctx.membership_memory=winner['membership_memory']
    ctx.slow_finished=inputs['rank_score'].to_numpy()
    ctx.w5a=process(ensemble_raw(panel,winner['ensemble_weights'],raw_members),dict(BASE_POST,alpha=0,bonus=0))
    ctx.top_values=ctx.w5a if not winner['role_ensembles_split'] else process(ensemble_raw(panel,winner['top_ensemble_weights'],raw_members),dict(BASE_POST,alpha=0,bonus=0))
    ctx.membership_values=ctx.top_values if winner['membership_ensemble_name']==winner['top_ensemble_name'] else (ctx.w5a if winner['membership_ensemble_name']==winner['ensemble_name'] else process(ensemble_raw(panel,winner['membership_ensemble_weights'],raw_members),dict(BASE_POST,alpha=0,bonus=0)))
    ctx.slow=process(inputs['pred_raw'].to_numpy(),dict(BASE_POST,alpha=0,bonus=0))
    ctx.ranks={'w5a':daily_ranks(ctx.w5a,valid,dates),'slow':daily_ranks(ctx.slow,valid,dates)}
    ctx.top_ranks=ctx.ranks['w5a'] if not winner['role_ensembles_split'] else daily_ranks(ctx.top_values,valid,dates)
    ctx.membership_ranks=daily_ranks(ctx.membership_values,valid,dates)
    ctx.diverse_augmentation=winner['diverse_augmentation'];ctx._diverse_cache={}
    import shutil
    for name in used:
        info=full_info[name];assert info['training_meta']['features']==features
        source_model=trainer.OUT/name/'model_2025.joblib';assert sha(source_model)==info['model_sha256']
        new_raw=trainer.predict_arrays(trainer.load_bundle(source_model),vx)
        new_replay=trainer.predict_arrays(trainer.load_bundle(source_model),vx)
        assert np.array_equal(new_raw,new_replay) and np.isfinite(new_raw).all()
        new_raw[~valid]=-1e6;values=process(new_raw,dict(BASE_POST,alpha=0,bonus=0))
        ctx._diverse_cache[name]=(values,daily_ranks(values,valid,dates))
        target=CANDIDATE/f'model_diverse_{name}.joblib';shutil.copyfile(source_model,target)
        assert sha(target)==info['model_sha256']
        models['diverse_'+name]={'path':str(target),'sha256':sha(target),'training_info':info,
                               'reload_bit_identical':True,'original':str(source_model)}
    def construct():
        mixed=sum(c['weight']*daily_ranks(raw,valid,dates) for c,raw in topk_raw);mixed[~valid]=-10.
        promote=process(mixed,winner['recipe']['postprocessing'])
        return ctx.predict(ctx.donor(promote),winner['slow16_weight'],winner['retention'],winner['limit_up_delta'])
    rank,stats=construct();replay,_=construct();assert np.array_equal(rank,replay)
    mapping=read(OUT/'future_return_mapping.json');mapped=apply_mapping(mapping,daily_percentile(inputs.select('trade_date').to_pandas(),rank))
    assert np.array_equal(pd.Series(rank).groupby(dates).rank().to_numpy(),pd.Series(mapped).groupby(dates).rank().to_numpy())
    bridge=pl.read_csv(ROOT/'data/raw/测试集_X.csv',schema_overrides={'trade_date':pl.Int32}).select(KEYS).with_row_index('position')
    sub=inputs.select(KEYS).with_columns(pl.Series('pred',mapped)).join(bridge,on=KEYS,how='inner',validate='1:1').sort('position').select(KEYS+['pred'])
    target=CANDIDATE/'submission.csv';sub.write_csv(target,float_precision=17)
    parsed=pd.read_csv(target)
    assert len(parsed)==1599600 and not parsed.duplicated(KEYS).any() and not parsed.isna().any().any() and np.isfinite(parsed.pred).all()
    assert np.array_equal(parsed[KEYS].to_numpy(),bridge.select(KEYS).to_numpy())
    assert np.array_equal(parsed.groupby('trade_date')['pred'].rank().to_numpy(),pd.Series(sub['pred'].to_numpy()).groupby(parsed.trade_date.to_numpy()).rank().to_numpy())
    assert sub.write_csv(float_precision=17).encode('utf-8')==target.read_bytes()
    np.save(CANDIDATE/'rank_prediction.npy',rank)
    dump(CANDIDATE/'selection.json',record,immutable=True);dump(CANDIDATE/'return_mapping.json',mapping,immutable=True)
    dump(CANDIDATE/'verification.json',{'status':'passed','csv_sha256':sha(target),'rows':len(sub),'days':344,'codes':4650,
         'models':models,'model_reload_bit_identical':True,'pipeline_replay_bit_identical':True,'csv_replay_byte_identical':True,
         'csv_ranks_unchanged':True,'validation_score':winner['connected_final_score'],'test_labels_read':False,
         'role_ensembles_split':winner['role_ensembles_split'],'top_ensemble_weights':winner['top_ensemble_weights'],
         'add_priority_weight':winner['add_priority_weight'],'drop_priority_weight':winner['drop_priority_weight'],
         'priority_signal':winner['priority_signal'],'membership_signal':winner['membership_signal'],
         'membership_ensemble_weights':winner['membership_ensemble_weights'],'membership_slow_weight':winner['membership_slow_weight'],
         'membership_power':winner['membership_power'],'membership_memory':winner['membership_memory'],
         'diverse_augmentation':winner['diverse_augmentation'],'new_fulltrain_models':len(used),
         'membership_w5a_weight':winner['membership_w5a_weight'],'membership_mode':winner['membership_mode'],
         'rest_ensemble_weights':winner['ensemble_weights'],'pruned_member_excluded':True,
         'source_predictions_sha256':{str(p):sha(p) for p in source_paths.values()},'construction':stats,
         'old_delivery_pointer_unchanged':sha(ROOT/'active_release.json')==record['frozen_sha256']['active_release.json']},immutable=True)
    log(f'Round14 candidate verified: {target}')


def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=('select','calibrate','predict'))
    globals()[parser.parse_args().stage]()


if __name__=='__main__':main()
