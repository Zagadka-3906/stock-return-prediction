"""Freeze all40 actual native model hashes; start97/291 TRAIN-only134 controls before current-parent144 admission."""
from pathlib import Path
import io,sys,time,tokenize
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name
def save(name,text):
    path=A/name;assert not path.exists();compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');return path
def main():
    for name in ('nonflag_ConeRidgeAlpha8_64_bank40_v2_20261008','ConeRidgeAlpha40_causal_refit_v2_20261008'):closed(name)
    bank_pointer=A/'actual_nonflag_ConeRidgeAlpha8_64_bank40_location_v2_20261008.json';bank=Path(read(bank_pointer)['output']);proof=read(bank/'verification.json')
    causal_pointer=A/'actual_ConeRidgeAlpha40_causal_refit_location_v2_20261008.json';causal=Path(read(causal_pointer)['output'])/'verification.json'
    assert proof['actual_native_fits']==40 and proof['actual_full_OOF_heads']==8 and read(causal)['actual_causal_same_configuration_refit_controls']==40
    blueprint=A/'ConeRidgeAlpha100_round144_blueprint_v1_20261008.json';design=read(blueprint)
    sources=[Path(__file__),blueprint,bank_pointer,bank/'verification.json',causal_pointer,causal,
        A/'ConeRidgeAlpha144_native_receiver_preflight_v1_20261008.json',A/'ConeRidgeAlpha8_64_complete_parent_CDF_v1_20261008.py',
        A/'ConeRidgeAlpha8_64_complete_parent_native_stage_v1_20261008.py',A/'predict_ConeRidgeAlpha8_64_complete_parent_scheme_v1_20261008.py',
        A/'nonflag_ConeRidgeAlpha8_64_streamed_v1_20261008.py']
    heads={}
    for alias,name in design['heads'].items():
        folder=bank/name;heads[alias]={'folder':str(folder),'oof':str(folder/'nonflag_oof_predictions.npy'),
            'infos':{str(year):str(folder/f'info_{year}.json') for year in range(2021,2026)},
            'state_kind':'linear','native_stage_state_kind':'ConeRidgeAlpha8_64_linear'}
        for path in heads[alias]['infos'].values():
            info=read(path);assert sha(info['native_model_path'])==info['native_model_sha256']
            assert sha(info['independent_linear_state_path'])==info['independent_linear_state_sha256']
            sources.extend((Path(path),Path(info['native_model_path']),Path(info['independent_linear_state_path'])))
        oof=read(folder/'oof_verification.json');assert sha(heads[alias]['oof'])==oof['prediction_array_sha256']
        sources.extend((folder/'oof_verification.json',Path(heads[alias]['oof'])))
    import ConeRidgeAlpha8_64_complete_parent_CDF_v1_20261008 as codec
    assert tuple(heads)==codec.HEADS and len(codec.GROUPS)==16
    for path,digest in design['input_sha256'].items():assert sha(path)==digest,path
    plan={**design,'status':'frozen100_declared_cases_with_actual40_own_mature_model_and8_OOF_hashes_before144_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'heads':heads,'groups':codec.GROUPS,'shares':[.5],
        'actual_existing_own_mature_annual_models':40,'native_numerical_recipe_version':1,'bank_administrative_version':2,
        'preliminary_controls_parent':134,'teacher_feature':'qualified106_current_forecast_average_rank_over_N',
        'input_sha256':{str(p):sha(p) for p in sources},'additional_native_fits_by_grid':0,
        'actual143_complete_QA54_main_required_before144_scoring':True,'new_official_scores':0}
    plan_path=A/'ConeRidgeAlpha100_round144_plan_v1_20261008.json';create(plan_path,plan)
    original=A/'verify_ConeRidgeFine65_parent134_historical_v1_20261008.py';text=original.read_text(encoding='utf8')
    mapping={'ConeRidgeFine65':'ConeRidgeAlpha97','ConeRidgeFine68':'ConeRidgeAlpha100','ConeRidge64_complete_parent':'ConeRidgeAlpha8_64_complete_parent',
        'round143':'round144','final143':'final144','65_full195':'97_full291','65_full_historical':'97_full_historical'}
    for before,after in mapping.items():text=text.replace(before,after)
    tokens=list(tokenize.generate_tokens(io.StringIO(text).readline));numbers={'65':'97','195':'291','8':'16'}
    text=tokenize.untokenize([t._replace(string=numbers[t.string]) if t.type==tokenize.NUMBER and t.string in numbers else t for t in tokens])
    for before,after in (('actual65','actual97'),('and195','and291'),('/49','/97'),('frozen_before_actual65','frozen_before_actual97')):text=text.replace(before,after)
    needle='(1e-05, 2.5e-05, 5e-05, 0.0001, 0.00025, 0.0005, 0.001, 0.0015)';assert text.count(needle)==1
    text=text.replace(needle,repr(tuple(plan['amplitudes'])))
    assert 'range(16)' in text and 'len(records)==97' in text
    driver=save('verify_ConeRidgeAlpha97_parent134_historical_v1_20261008.py',text)
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    pins={str(p):sha(p) for p in [*sources,original,plan_path,driver]}
    row=start('ConeRidgeAlpha97_parent134_historical_controls_v1_20261008',driver.name,[],pins)
    create(A/'ConeRidgeAlpha100_actual_historical_hidden_launch_v1_20261008.json',{
        'status':'started97_full291_cold_TRAIN134_math_controls_before_actual144_current_parent_admission',
        'input_sha256':pins,'launch':row,'new_model_fits':0,'new_official_scores':0,
        'actual144_current_parent97_controls_and48_native48_calendar_full100_pipeline_still_required':True,'test_labels_read':False})
    print('40 saved model hashes and100-case plan frozen; actual97/291 TRAIN134 controls running.',flush=True)
if __name__=='__main__':main()
