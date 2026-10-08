"""Freeze52 reorthogonalizedCG comparisons and exact complete-parent native receivers before quality."""
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
    for name in ('nonflag_KrylovGram64_bank20_v3_20261008','nonflag_KrylovGram64_probe_and_bank_main_publication_v2_20261008','KrylovGram20_causal_refit_controls_v2_20261008'):closed(name)
    pointer=A/'actual_nonflag_KrylovGram64_bank20_location_v3_20261008.json';bank=Path(read(pointer)['output']);proof=read(bank/'verification.json')
    assert proof['actual_native_fits']==20 and proof['actual_full_OOF_heads']==4 and proof['actual_official_scores']==0
    causal_pointer=A/'actual_KrylovGram20_causal_refit_location_v2_20261008.json';causal=Path(read(causal_pointer)['output'])/'verification.json'
    assert read(causal)['actual_causal_same_configuration_refit_controls']==20 and read(causal)['actual_maturity_windows']==5
    sources=[Path(__file__),pointer,bank/'verification.json',causal_pointer,causal,A/'nonflag_KrylovGram64_controls_main_v2_20261008/bank/receipt.json',A/'nonflag_KrylovGram64_streamed_v2_20261008.py']
    heads={}
    for k in (2,4,8,16):
        alias=f'krylov_s{k:02d}';name=f'nonflag_residual_krylovGram64r2_s{k:02d}';folder=bank/name
        heads[alias]={'folder':str(folder),'oof':str(folder/'nonflag_oof_predictions.npy'),
            'infos':{str(year):str(folder/f'info_{year}.json') for year in range(2021,2026)},'state_kind':'linear','native_stage_state_kind':'KrylovGram64_linear'}
        for info_path in heads[alias]['infos'].values():
            info=read(info_path);assert sha(info['native_model_path'])==info['native_model_sha256']
            assert sha(info['independent_linear_state_path'])==info['independent_linear_state_sha256']
            sources += [Path(info_path),Path(info['native_model_path']),Path(info['independent_linear_state_path'])]
        sources += [folder/'oof_verification.json',folder/'nonflag_oof_predictions.npy']
    groups=tuple((((head,),sign),((head,),sign)) for head in heads for sign in (1.,-1.))
    original=A/'CrossFamily_complete_parent_CDF_v1_20261008.py';text=original.read_text(encoding='utf8');sources.append(original)
    first=text.index('HEADS = ');last=text.index('\n\ndef mixture',first)
    text=text[:first]+'HEADS = '+repr(tuple(heads))+'\nGROUPS = '+repr(groups)+'\n'+text[last:]
    sources.append(save(A/'KrylovGram64_complete_parent_CDF_v1_20261008.py',text))
    original=A/'SpectralGram64_complete_parent_native_stage_v1_20261008.py';text=original.read_text(encoding='utf8');sources.append(original)
    text=text.replace('SpectralGram64_complete_parent_CDF','KrylovGram64_complete_parent_CDF').replace('nonflag_CPU_SpectralGram64','nonflag_CPU_KrylovGram64')
    text=text.replace('nonflag_SpectralGram64_streamed_v1_20261008','nonflag_KrylovGram64_streamed_v2_20261008').replace('SpectralGram64_linear','KrylovGram64_linear')
    first=text.index("            assert params['solver']==");last=text.index('            values=np.zeros',first)
    text=text[:first]+'''            assert params['solver']=='fixed8192_centered_reorthogonalized_CG64_v2' and params['alpha']==info['training_rows']*.01
            assert all(params[key]==value for key,value in CONFIGS[info['name']].items())
            assert bundle['model'].coef_.shape==(64,) and bundle['model'].n_features_in_==64
            assert 0<=bundle['model'].actual_iterations_<=params['maximum_iterations']
'''+text[last:]
    sources.append(save(A/'KrylovGram64_complete_parent_native_stage_v1_20261008.py',text))
    original=A/'predict_SpectralGram64_complete_parent_scheme_v1_20261008.py';text=original.read_text(encoding='utf8');sources.append(original)
    text=text.replace('SpectralGram64','KrylovGram64')
    text=text.replace('BACKENDS={',"BACKENDS={\n    'SpectralGram64':('predict_SpectralGram64_complete_parent_scheme_v1_20261008.py','SpectralGram64_complete_parent_native_stage_v1_20261008',True),")
    marker="for key,name in (('nonflag_CPU_HuberCrossFamily_complete_parent_CDF','HuberCrossFamily'),";assert text.count(marker)==1
    text=text.replace(marker,"for key,name in (('nonflag_CPU_SpectralGram64_complete_parent_CDF','SpectralGram64'),('nonflag_CPU_HuberCrossFamily_complete_parent_CDF','HuberCrossFamily'),")
    sources.append(save(A/'predict_KrylovGram64_complete_parent_scheme_v1_20261008.py',text))
    plan_path=A/'KrylovGram52_round141_plan_v1_20261008.json'
    create(plan_path,{'status':'frozen52_reorthogonalizedCG_cases_before_any_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':141,'anchors':[138,139,140],'heads':heads,'groups':groups,'shares':[.5],'amplitudes':[.0025,.005,.01,.025,.05,.1],
        'new_cases':[{'group':g,'share':.5,'amplitude':amp} for g in range(8) for amp in (.0025,.005,.01,.025,.05,.1)],
        'expected_scored_cases':52,'expected_transform_cases':49,'expected_cold_cases':147,'actual_existing_own_mature_annual_models':20,
        'native_numerical_recipe_version':2,'bank_administrative_version':3,'preliminary_controls_parent':134,
        'graph_key':'nonflag_CPU_KrylovGram64_complete_parent_CDF','teacher_feature':'qualified106_current_forecast_average_rank_over_N',
        'full140_QA51_main_and_exact_current_parent_required_before_quality':True,
        'input_sha256':{str(p):sha(p) for p in sources},'additional_native_fits_by_grid':0,'new_official_scores':0,'test_labels_read':False})
    original=A/'verify_SpectralGram49_parent134_historical_v1_20261008.py';text=original.read_text(encoding='utf8');sources.append(original)
    text=text.replace('SpectralGram49_parent134_historical','KrylovGram49_parent134_historical').replace('actual_SpectralGram49_parent134_location','actual_KrylovGram49_parent134_location')
    text=text.replace('SpectralGram52_round140_plan','KrylovGram52_round141_plan').replace('SpectralGram64_complete_parent_CDF','KrylovGram64_complete_parent_CDF')
    text=text.replace('SpectralGram_CDF','KrylovGram_CDF').replace('SpectralGram_controls','KrylovGram_controls').replace('final140','final141').replace('after139','after140')
    history=save(A/'verify_KrylovGram49_parent134_historical_v1_20261008.py',text);sources.append(history)
    original=A/'verify_SpectralGram24_native_historical_hooks_v2_20261008.py';text=original.read_text(encoding='utf8');sources.append(original)
    text=text.replace('SpectralGram24_native_historical_hooks_v2_20261008','KrylovGram24_native_historical_hooks_v1_20261008').replace('actual_SpectralGram24_native_hooks_location_v2_20261008','actual_KrylovGram24_native_hooks_location_v1_20261008')
    text=text.replace('SpectralGram49_parent134_historical','KrylovGram49_parent134_historical').replace('actual_SpectralGram49_parent134_location','actual_KrylovGram49_parent134_location')
    text=text.replace('SpectralGram52_round140_plan','KrylovGram52_round141_plan').replace('SpectralGram64_complete_parent','KrylovGram64_complete_parent').replace('actual24_SpectralGram','actual24_KrylovGram').replace('final140','final141')
    hooks=save(A/'verify_KrylovGram24_native_historical_hooks_v1_20261008.py',text);sources.append(hooks)
    pins={str(p):sha(p) for p in [*sources,plan_path]};launches={}
    for name,driver in (('KrylovGram49_parent134_historical_controls_v1_20261008',history.name),('KrylovGram24_native_historical_hooks_v1_20261008',hooks.name)):
        launches[name]=start(name,driver,[],pins)
    create(A/'actual_KrylovGram52_plan_historical_hidden_launches_v1_20261008.json',{
        'status':'started49_full147_cold_then24_native24_cold_after_actual20_saved_and20_causal_refits','input_sha256':pins,
        'launches':launches,'new_official_scores':0,'complete141_source_admission_scoring_candidate_QA52_main_still_required':True,'test_labels_read':False})
    print('Frozen52 reorthogonalizedCG cases; actual49/147 and24/24 history started after20 causal refits.',flush=True)

if __name__=='__main__':main()
