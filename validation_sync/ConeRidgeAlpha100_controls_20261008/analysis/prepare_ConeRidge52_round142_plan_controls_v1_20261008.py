"""Independent CPU round142 anchored to fully qualified132133134; do not change135141 plans."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def save(path,text):
    assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return path

def main():
    for name in ('nonflag_ConeRidge64_bank20_v1_20261008','ConeRidge20_causal_refit_controls_v1_20261008','ConeRidge64_controls_main_publication_v1_20261008'):closed(name)
    pointer=A/'actual_nonflag_ConeRidge64_bank20_location_v1_20261008.json';bank=Path(read(pointer)['output']);proof=read(bank/'verification.json')
    causal_pointer=A/'actual_ConeRidge20_causal_refit_location_v1_20261008.json';causal=Path(read(causal_pointer)['output'])/'verification.json'
    assert proof['actual_native_fits']==20 and proof['actual_full_OOF_heads']==4
    assert read(causal)['actual_causal_same_configuration_refit_controls']==20 and read(causal)['actual_maturity_windows']==5
    import nonflag_ConeRidge64_streamed_v1_20261008 as native
    sources=[Path(__file__),Path(native.__file__),pointer,bank/'verification.json',causal_pointer,causal,A/'ConeRidge64_controls_main_v1_20261008/causal/receipt.json']
    for n in (132,133,134):
        receipt=A/f'github_validation_sync_main_20261005/round{n}_receipt.json'
        completed=A/f'optimization_20261003_r{n}/full_registration_execution.json'
        assert read(receipt)['status']=='pushed_and_remote_head_verified' and read(completed)['status']=='passed'
        sources += [receipt,completed]
    heads={}
    for name,cfg in native.CONFIGS.items():
        alias=f"cone_a{int(cfg['alpha_per_training_row']*1000):03d}_{'positive' if cfg['feature_sign']>0 else 'negative'}";folder=bank/name
        heads[alias]={'folder':str(folder),'oof':str(folder/'nonflag_oof_predictions.npy'),
            'infos':{str(year):str(folder/f'info_{year}.json') for year in range(2021,2026)},
            'state_kind':'linear','native_stage_state_kind':'ConeRidge64_linear'}
        for p in heads[alias]['infos'].values():
            info=read(p);assert sha(info['native_model_path'])==info['native_model_sha256']
            assert sha(info['independent_linear_state_path'])==info['independent_linear_state_sha256']
            sources += [Path(p),Path(info['native_model_path']),Path(info['independent_linear_state_path'])]
        sources += [folder/'oof_verification.json',folder/'nonflag_oof_predictions.npy']
    groups=tuple((((head,),sign),((head,),sign)) for head in heads for sign in (1.,-1.))
    old=A/'KrylovGram64_complete_parent_CDF_v1_20261008.py';text=old.read_text(encoding='utf8');sources.append(old)
    first=text.index('HEADS = ');last=text.index('\n\ndef mixture',first)
    text=text[:first]+'HEADS = '+repr(tuple(heads))+'\nGROUPS = '+repr(groups)+'\n'+text[last:]
    sources.append(save(A/'ConeRidge64_complete_parent_CDF_v1_20261008.py',text))
    old=A/'KrylovGram64_complete_parent_native_stage_v1_20261008.py';text=old.read_text(encoding='utf8');sources.append(old)
    text=text.replace('KrylovGram64','ConeRidge64').replace('nonflag_ConeRidge64_streamed_v2_20261008','nonflag_ConeRidge64_streamed_v1_20261008')
    first=text.index("            assert params['solver']==");last=text.index('            values=np.zeros',first)
    text=text[:first]+'''            assert params['solver']=='fixed8192_centered_signed_ridge_NNLS64_Cholesky_v1'
            assert params['alpha']==info['training_rows']*params['alpha_per_training_row']
            assert all(params[key]==value for key,value in CONFIGS[info['name']].items())
            assert bundle['model'].coef_.shape==(64,) and bundle['model'].n_features_in_==64
            assert np.all(bundle['model'].nonnegative_parameters_>=0.)
            exact(bundle['model'].coef_,params['feature_sign']*bundle['model'].nonnegative_parameters_)
'''+text[last:]
    sources.append(save(A/'ConeRidge64_complete_parent_native_stage_v1_20261008.py',text))
    old=A/'predict_KrylovGram64_complete_parent_scheme_v1_20261008.py';text=old.read_text(encoding='utf8');sources.append(old)
    text=text.replace('KrylovGram64','ConeRidge64')
    text=text.replace('BACKENDS={',"BACKENDS={\n    'KrylovGram64':('predict_KrylovGram64_complete_parent_scheme_v1_20261008.py','KrylovGram64_complete_parent_native_stage_v1_20261008',True),")
    marker="for key,name in (('nonflag_CPU_SpectralGram64_complete_parent_CDF','SpectralGram64'),";assert text.count(marker)==1
    text=text.replace(marker,"for key,name in (('nonflag_CPU_KrylovGram64_complete_parent_CDF','KrylovGram64'),('nonflag_CPU_SpectralGram64_complete_parent_CDF','SpectralGram64'),")
    sources.append(save(A/'predict_ConeRidge64_complete_parent_scheme_v1_20261008.py',text))
    plan=A/'ConeRidge52_round142_plan_v1_20261008.json'
    create(plan,{'status':'frozen52_signed_constrained_ridge_cases_before_any_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':142,'anchors':[132,133,134],'heads':heads,'groups':groups,'shares':[.5],
        'amplitudes':[.0025,.005,.01,.025,.05,.1],
        'new_cases':[{'group':g,'share':.5,'amplitude':amp} for g in range(8) for amp in (.0025,.005,.01,.025,.05,.1)],
        'expected_scored_cases':52,'expected_transform_cases':49,'expected_cold_cases':147,'actual_existing_own_mature_annual_models':20,
        'native_numerical_recipe_version':1,'bank_administrative_version':1,'preliminary_controls_parent':134,
        'graph_key':'nonflag_CPU_ConeRidge64_complete_parent_CDF','teacher_feature':'qualified106_current_forecast_average_rank_over_N',
        'already_qualified132133134_only_no_unfinished135141_dependency':True,
        'original135141_frozen_plans_unchanged':True,'input_sha256':{str(p):sha(p) for p in sources},
        'additional_native_fits_by_grid':0,'new_official_scores':0,'test_labels_read':False})
    outputs=[]
    for filename in ('verify_KrylovGram49_parent134_historical_v1_20261008.py','verify_KrylovGram24_native_historical_hooks_v1_20261008.py',
        'verify_KrylovGram_multiyear_native_calendar_v1_20261008.py'):
        old=A/filename;text=old.read_text(encoding='utf8');sources.append(old)
        text=text.replace('KrylovGram','ConeRidge').replace('round141','round142').replace('final141','final142').replace('after140','after_already_qualified134')
        outputs.append(save(A/filename.replace('KrylovGram','ConeRidge'),text))
    pins={str(p):sha(p) for p in [*sources,*outputs,plan]};launches={}
    for name,path in zip(('ConeRidge49_parent134_historical_controls_v1_20261008','ConeRidge24_native_historical_hooks_v1_20261008','ConeRidge_multiyear_native_calendar_v1_20261008'),outputs):
        launches[name]=start(name,path.name,[],pins)
    create(A/'actual_ConeRidge52_plan_historical_hidden_launches_v1_20261008.json',{
        'status':'started49_full147_cold24_native24_cold24_calendar48_day_after20_saved_and20_causal_refits',
        'input_sha256':pins,'launches':launches,'new_official_scores':0,'no_unfinished135141_quality_prerequisite':True,'test_labels_read':False})
    print('52 CPU cases frozen against qualified132133134;49/147,24 native and24 calendar actual controls started.',flush=True)

if __name__=='__main__':main()
