"""Eighteen actual saved-Huber historical native hooks and18 cold prefixes; no future inputs."""
from pathlib import Path
from types import SimpleNamespace
import os,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):os.environ[key]='2'
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/HuberIRLS64_18_native_historical_hooks_v1_20261008')


def main():
    folder=A/'service_owned_workflows_20261006/HuberIRLS64_49_parent134_historical_controls_v1_20261008'
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed'
    import numpy as np,polars as pl
    from run import FEATURE_FILE,feature_names
    from HuberIRLS64_complete_parent_CDF_v1_20261008 import HEADS,required_heads,mixture,transform
    from HuberIRLS64_complete_parent_native_stage_v1_20261008 import GRAPH_KEY,after_parent,exact
    from predict_HuberIRLS64_complete_parent_scheme_v1_20261008 import prepared_backend
    bank=Path(read(A/'actual_nonflag_HuberIRLS64_bank10_location_v1_20261008.json')['output']);bank_proof=read(bank/'verification.json')
    heads=dict(zip(HEADS,bank_proof['configurations']));frame_path=A/'connected_validation_20261002/combined_fold_frame.parquet'
    teacher_path=A/'optimization_20261003_r106/selected_validation.npy';parent_path=A/'optimization_20261003_r134/selected_validation.npy'
    full_proof=Path(read(A/'actual_HuberIRLS64_49_parent134_location_v1_20261008.json')['output'])/'verification.json'
    full=read(full_proof);assert (full['actual_full_cases'],full['actual_cold_cases'])==(49,147)
    sources=[Path(__file__),A/'HuberIRLS64_complete_parent_CDF_v1_20261008.py',A/'HuberIRLS64_complete_parent_native_stage_v1_20261008.py',
        A/'predict_HuberIRLS64_complete_parent_scheme_v1_20261008.py',A/'HuberIRLS64_52_round137_plan_v1_20261008.json',
        frame_path,FEATURE_FILE,teacher_path,parent_path,full_proof,bank/'verification.json']
    for name in heads.values():
        sources.append(bank/name/'nonflag_oof_predictions.npy')
        for year in (2021,2022,2024):
            path=bank/name/f'info_{year}.json';info=read(path);sources += [path,Path(info['native_model_path']),Path(info['independent_linear_state_path'])]
    backends={'CrossFamily':'predict_CrossFamily_complete_parent_scheme_v1_20261008.py',
        'BF16':'predict_BF16_complete_parent_rank_scheme_v1_20261008.py','ReverseBayes':'predict_nonflag_residual_ReverseBayes_complete_scheme_20261007.py'}
    sources += [A/filename for filename in backends.values()];pins={str(p):sha(p) for p in dict.fromkeys(sources)}
    assert not OUT.exists();OUT.mkdir();create(OUT/'frozen_before_actual18_hooks.json',{'input_sha256':pins,
        'actual_quality_scores':0,'historical_years':[2021,2022,2024],'groups':6,'future_X_and_Y_read':False})
    backend_controls=[]
    for backend,filename in backends.items():
        path=A/filename;text=prepared_backend(path.read_text(encoding='utf8'),backend);compile(text,str(path),'exec')
        target=OUT/(backend+'_prospective_receiver.py');target.write_text(text,encoding='utf8',newline='\n')
        backend_controls.append({'backend':backend,'original_source_sha256':sha(path),'generated_source_sha256':sha(target),
            'unique_scoped_injection_and_compilation_passed':True,'actual_complete_future_parent_replay_not_claimed':True})
    names=feature_names();keys=['ts_code','trade_date'];frame=pl.read_parquet(frame_path,columns=keys+['flag_limit_up','price_valid']);dates=frame['trade_date'].to_numpy()
    teacher_all=np.load(teacher_path,mmap_mode='r');parent_all=np.load(parent_path,mmap_mode='r')
    arrays={head:np.load(bank/name/'nonflag_oof_predictions.npy',mmap_mode='r') for head,name in heads.items()};records=[]
    for year,weight in zip((2021,2022,2024),(.005,.025,.2)):
        days=np.unique(dates[dates//10000==year])[:3];positions=np.flatnonzero(np.isin(dates,days));panel=frame[positions]
        test=pl.scan_parquet(FEATURE_FILE).filter(pl.col('is_train')&pl.col('trade_date').is_in(days)).select(keys+names).sort('trade_date','ts_code').collect()
        assert test.select(keys).equals(panel.select(keys)) and len(panel)==13950 and not {'y_rank','y_ret_1d'}&set(test.columns)
        teacher=np.asarray(teacher_all[positions],dtype=np.float64);parent=np.asarray(parent_all[positions],dtype=np.float64)
        for group in range(6):
            spec={'group':group,'amplitude':weight,'universe':'all_current_raw_forecasts','position':'after_complete_qualified_parent',
                'teacher_feature':'qualified106_current_forecast_average_rank_over_N'};components=[]
            for head in required_heads(group):
                info=read(bank/heads[head]/f'info_{year}.json')
                components.append({'head':head,'name':info['name'],'state_kind':'HuberIRLS64_linear','path':info['native_model_path'],
                    'sha256':info['native_model_sha256'],'independent_state_path':info['independent_linear_state_path'],
                    'independent_state_sha256':info['independent_linear_state_sha256'],'training_info':info})
            context=SimpleNamespace(dates=panel['trade_date'].to_numpy(),flags=panel['flag_limit_up'].to_numpy(),valid=panel['price_valid'].to_numpy(),
                _nonflag_raw_features=test.select(names).to_numpy().astype(np.float64),_nonflag_raw_feature_names=names,_whole_graph={GRAPH_KEY:spec})
            value,full=after_parent(SimpleNamespace(read=read,sha=sha),context,teacher,parent,spec,components)
            residual=mixture({head:array[positions] for head,array in arrays.items()},group)
            exact(value,transform(parent,residual,context.dates,context.flags,context.valid,weight))
            cold_context=SimpleNamespace(**vars(context))
            for field in ('dates','flags','valid','_nonflag_raw_features'):setattr(cold_context,field,getattr(context,field)[:4650])
            prefix,cold=after_parent(SimpleNamespace(read=read,sha=sha),cold_context,teacher[:4650],parent[:4650],spec,components);exact(prefix,value[:4650])
            item={'year':year,'group':group,'amplitude':weight,'full':full,'cold':cold,'saved_full_OOF_and_actual_native_stage_bits_exact':True,
                'one_day_prefix_bits_exact':True};create(OUT/f'hook{len(records)+1}.json',item);records.append(item)
            print(f'Actual Huber native historical hook {len(records)}/18: {year} group{group}',flush=True)
    for path,digest in pins.items():assert sha(path)==digest,path
    create(OUT/'verification.json',{'status':'passed_actual18_HuberIRLS64_historical_native_hooks_and18_cold_prefixes',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'records':records,'actual_hooks':18,'actual_cold_hooks':18,
        'prospective_backend_compilation_controls':backend_controls,'actual_quality_scores':0,'future_X_and_Y_read':False,
        'complete52_receiver_preflight_exact_current_parent_controls_and_actual_future_replays_still_required':True})
    create(A/'actual_HuberIRLS64_18_native_hooks_location_v1_20261008.json',{'status':'passed_actual18_HuberIRLS64_historical_hooks_on_E',
        'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'actual_quality_scores':0})


if __name__=='__main__':main()
