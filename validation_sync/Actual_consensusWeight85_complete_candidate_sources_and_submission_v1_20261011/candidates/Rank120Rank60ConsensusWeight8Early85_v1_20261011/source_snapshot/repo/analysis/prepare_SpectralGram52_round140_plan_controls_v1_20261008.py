"""Freeze52 spectral comparisons and dispatch full-history/native controls after twenty real fits."""
from pathlib import Path
from copy import deepcopy
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned


def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name


def save(path,text):
    assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return path


def main():
    closed('nonflag_SpectralGram64_bank20_v1_20261008')
    closed('nonflag_SpectralGram64_probe_and_bank_main_publication_v1_20261008')
    pointer=A/'actual_nonflag_SpectralGram64_bank20_location_v1_20261008.json';bank=Path(read(pointer)['output']);bank_proof=read(bank/'verification.json')
    assert bank_proof['actual_native_fits']==20 and bank_proof['actual_full_OOF_heads']==4 and bank_proof['actual_official_scores']==0
    sources=[Path(__file__),pointer,bank/'verification.json',A/'nonflag_SpectralGram64_controls_main_v1_20261008/bank/receipt.json']
    heads={}
    for k in (8,16,32,48):
        alias=f'spectral_k{k:02d}';name=f'nonflag_residual_spectralGram64_k{k:02d}';folder=bank/name
        heads[alias]={'folder':str(folder),'oof':str(folder/'nonflag_oof_predictions.npy'),
            'infos':{str(year):str(folder/f'info_{year}.json') for year in range(2021,2026)},
            'state_kind':'linear','native_stage_state_kind':'SpectralGram64_linear'}
        for info_path in heads[alias]['infos'].values():
            info=read(info_path);assert sha(info['native_model_path'])==info['native_model_sha256']
            assert sha(info['independent_linear_state_path'])==info['independent_linear_state_sha256']
            sources += [Path(info_path),Path(info['native_model_path']),Path(info['independent_linear_state_path'])]
        sources += [folder/'oof_verification.json',folder/'nonflag_oof_predictions.npy']
    groups=tuple((( (head,),sign),((head,),sign)) for head in heads for sign in (1.,-1.))
    original=A/'CrossFamily_complete_parent_CDF_v1_20261008.py';text=original.read_text(encoding='utf8');sources.append(original)
    first=text.index('HEADS = ');last=text.index('\n\ndef mixture',first)
    text=text[:first]+'HEADS = '+repr(tuple(heads))+'\nGROUPS = '+repr(groups)+'\n'+text[last:]
    sources.append(save(A/'SpectralGram64_complete_parent_CDF_v1_20261008.py',text))
    original=A/'CrossFamily_complete_parent_native_stage_v2_20261008.py';text=original.read_text(encoding='utf8');sources.append(original)
    text=text.replace('from CrossFamily_complete_parent_CDF_v1_20261008 import','from SpectralGram64_complete_parent_CDF_v1_20261008 import')
    text=text.replace("GRAPH_KEY='nonflag_CPU_CrossFamily_complete_parent_CDF'","GRAPH_KEY='nonflag_CPU_SpectralGram64_complete_parent_CDF'")
    needle='    from threadpoolctl import threadpool_limits';assert text.count(needle)==1
    text=text.replace(needle,'    from nonflag_SpectralGram64_streamed_v1_20261008 import CONFIGS,predict_native as spectral_native,predict_decoded as spectral_decoded\n'+needle)
    text=text.replace("native,decoded=(rff_native,rff_decoded) if kind=='random_fourier_linear' else (lin_native,lin_decoded)","native,decoded=(spectral_native,spectral_decoded)")
    text=text.replace("assert kind in ('linear','random_fourier_linear')","assert kind=='SpectralGram64_linear'")
    first=text.index("            if head.startswith('ridge_'):");last=text.index('            values=np.zeros',first)
    text=text[:first]+'''            params=bundle['model'].get_params();assert params==info['parameters']==state['training_configuration']
            assert params['solver']=='fixed8192_centered_top_eigen_Gram64' and params['alpha']==info['training_rows']*.01
            assert all(params[key]==value for key,value in CONFIGS[info['name']].items())
            assert bundle['model'].training_basis_.shape==(64,params['n_components'])
            assert bundle['model'].retained_eigenvalues_.shape==(params['n_components'],)
''' +text[last:]
    sources.append(save(A/'SpectralGram64_complete_parent_native_stage_v1_20261008.py',text))
    original=A/'predict_HuberCrossFamily_complete_parent_scheme_v1_20261008.py';text=original.read_text(encoding='utf8');sources.append(original)
    text=text.replace('HuberCrossFamily_complete_parent_native_stage_v1_20261008','SpectralGram64_complete_parent_native_stage_v1_20261008')
    text=text.replace('HuberCrossFamily','SpectralGram64')
    text=text.replace('BACKENDS={',"BACKENDS={\n    'HuberCrossFamily':('predict_HuberCrossFamily_complete_parent_scheme_v1_20261008.py','HuberCrossFamily_complete_parent_native_stage_v1_20261008',True),")
    text=text.replace("for key,name in (('BF16_reverse_complete_parent_rank_CDF','ReverseBF16'),","for key,name in (('nonflag_CPU_HuberCrossFamily_complete_parent_CDF','HuberCrossFamily'),('BF16_reverse_complete_parent_rank_CDF','ReverseBF16'),")
    sources.append(save(A/'predict_SpectralGram64_complete_parent_scheme_v1_20261008.py',text))
    plan_path=A/'SpectralGram52_round140_plan_v1_20261008.json'
    create(plan_path,{'status':'frozen52_spectral_cases_before_any_quality','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'round':140,'anchors':[137,138,139],'heads':heads,'groups':groups,'shares':[.5],'amplitudes':[.0025,.005,.01,.025,.05,.1],
        'new_cases':[{'group':g,'share':.5,'amplitude':amp} for g in range(8) for amp in (.0025,.005,.01,.025,.05,.1)],
        'expected_scored_cases':52,'expected_transform_cases':49,'expected_cold_cases':147,
        'actual_existing_own_mature_annual_models':20,'preliminary_controls_parent':134,
        'graph_key':'nonflag_CPU_SpectralGram64_complete_parent_CDF','teacher_feature':'qualified106_current_forecast_average_rank_over_N',
        'full139_QA50_and_main_and_exact_current_parent_required_before_quality':True,
        'input_sha256':{str(p):sha(p) for p in sources},'additional_native_fits_by_grid':0,'new_official_scores':0,'test_labels_read':False})
    original=A/'verify_HuberCrossFamily109_parent134_historical_v1_20261008.py';text=original.read_text(encoding='utf8');sources.append(original)
    text=text.replace('HuberCrossFamily109_parent134_historical_v1_20261008','SpectralGram49_parent134_historical_v1_20261008')
    text=text.replace('actual_HuberCrossFamily109_parent134_location_v1_20261008','actual_SpectralGram49_parent134_location_v1_20261008')
    text=text.replace('HuberCrossFamily112_round139_plan_v1_20261008','SpectralGram52_round140_plan_v1_20261008')
    text=text.replace('HuberCrossFamily_complete_parent_CDF_v1_20261008','SpectralGram64_complete_parent_CDF_v1_20261008')
    text=text.replace('range(6)','range(8)').replace('for share in (.25,.5,.75):','for share in (.5,):')
    text=text.replace('actual109','actual49').replace('/109','/49').replace('len(records)==109','len(records)==49').replace('==327','==147')
    text=text.replace("'actual_full_cases':109,'actual_cold_cases':327","'actual_full_cases':49,'actual_cold_cases':147")
    text=text.replace('Huber_crossfamily_CDF_and327','SpectralGram_CDF_and147').replace('Huber_crossfamily_controls','SpectralGram_controls')
    text=text.replace('final139','final140').replace('after138','after139')
    history=save(A/'verify_SpectralGram49_parent134_historical_v1_20261008.py',text);sources.append(history)
    original=A/'verify_HuberCrossFamily18_native_historical_hooks_v1_20261008.py';text=original.read_text(encoding='utf8');sources.append(original)
    mapping={'HuberCrossFamily109_parent134_historical_controls_v1_20261008':'SpectralGram49_parent134_historical_controls_v1_20261008',
        'actual_HuberCrossFamily109_parent134_location_v1_20261008':'actual_SpectralGram49_parent134_location_v1_20261008',
        'HuberCrossFamily18_native_historical_hooks_v1_20261008':'SpectralGram24_native_historical_hooks_v1_20261008',
        'actual_HuberCrossFamily18_native_hooks_location_v1_20261008':'actual_SpectralGram24_native_hooks_location_v1_20261008',
        'HuberCrossFamily112_round139_plan_v1_20261008':'SpectralGram52_round140_plan_v1_20261008',
        'HuberCrossFamily_complete_parent_CDF_v1_20261008':'SpectralGram64_complete_parent_CDF_v1_20261008',
        'HuberCrossFamily_complete_parent_native_stage_v1_20261008':'SpectralGram64_complete_parent_native_stage_v1_20261008'}
    for before,after in mapping.items():text=text.replace(before,after)
    text=text.replace('range(6)','range(8)').replace('(.25,.5,.75),(.005,.025,.1)','(.5,.5,.5),(.005,.025,.1)')
    text=text.replace("proof['actual_full_cases']==109","proof['actual_full_cases']==49")
    text=text.replace('actual18_Huber_crossfamily','actual24_SpectralGram').replace('18_cold_prefixes','24_cold_prefixes').replace('/18','/24')
    text=text.replace("'actual_hooks':18,'actual_cold_hooks':18","'actual_hooks':24,'actual_cold_hooks':24").replace('final139','final140')
    hooks=save(A/'verify_SpectralGram24_native_historical_hooks_v1_20261008.py',text);sources.append(hooks)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in [*sources,plan_path]};launches={}
    for name,driver in (('SpectralGram49_parent134_historical_controls_v1_20261008',history.name),
        ('SpectralGram24_native_historical_hooks_v1_20261008',hooks.name)):
        launches[name]=start(name,driver,[],pins)
    create(A/'actual_SpectralGram52_plan_historical_hidden_launches_v1_20261008.json',{'status':'started49_full147_cold_then24_native24_cold_after_actual20_models',
        'input_sha256':pins,'launches':launches,'new_official_scores':0,'complete140_source_admission_scoring_candidate_QA51_main_still_required':True,'test_labels_read':False})
    print('Frozen52 spectral cases and actual49/147 then24/24 historical controls started.',flush=True)


if __name__=='__main__':main()
