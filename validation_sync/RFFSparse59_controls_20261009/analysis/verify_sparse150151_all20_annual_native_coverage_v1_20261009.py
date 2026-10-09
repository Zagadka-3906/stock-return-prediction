"""Prove actual native/reload/independent stage coverage of all20 own annual states per scheme."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def main():
    records=[];inputs=[Path(__file__),A/'sparse150151_year2023_supplement_preparation_v1_20261009.json']
    for family,number,date in (('HuberSparse',150,'20261008'),('RFFSparse',151,'20261009')):
        proposal_path=A/f'{family}59_round{number}_proposal_v1_{date}.json';plan=read(proposal_path);inputs.append(proposal_path)
        pointers=[A/f'actual_{family}72_native_calendar_location_v1_{date}.json',A/f'actual_{family}18_year2023_native_supplement_location_v1_20261009.json']
        stages=[]
        for pointer in pointers:
            descriptor=read(pointer);proof=Path(descriptor['output'])/'verification.json';assert sha(proof)==descriptor['verification_sha256'];stages.append(read(proof));inputs.extend([pointer,proof])
        original,additional=stages
        assert (original['actual_historical_cases'],original['actual_calendar_cases'],original['actual_cold_cases'])==(54,18,72)
        assert (additional['actual_historical_cases'],additional['actual_calendar_cases'],additional['actual_cold_cases'])==(18,0,18)
        assert all(r['year']==2023 and r['saved_OOF_bits_exact'] for r in additional['records'])
        seen={};old=set();supplement=set()
        for stage,index in ((original,0),(additional,1)):
            for record in stage['records']:
                assert record['actual_future_features_not_read']
                for mode in ('full','cold'):
                    report=record[mode]
                    assert report['native_reload_independent_arithmetic_and_Pandas_complete_parent_CDF_bits_exact'] and report['complete_parent_flag1_invalid_and2020_bits_preserved']
                    assert report['original_teacher106_feature_used'] and report['saved_fit_year_fixed_for_all_prediction_dates']
                    for control in report['controls']:
                        key=(control['head'],control['year']);assert control['reload_exact'] and control['independent_decoder_exact']
                        row=plan['heads'][key[0]];info_path=Path(row['infos'][str(key[1])]);info=read(info_path)
                        identity=(control['sha256'],control['independent_state_sha256'])
                        assert identity==(info['native_model_sha256'],info['independent_'+row['state_kind']+'_state_sha256'])
                        assert seen.setdefault(key,identity)==identity
                        (old if index==0 else supplement).add(key);inputs.append(info_path)
        expected={(h,y) for h in plan['heads'] for y in range(2021,2026)}
        assert set(seen)==expected and len(old)==16 and len(supplement)==4 and old.isdisjoint(supplement)
        for name in (f'{family}72_native_historical_calendar_controls_v1_{date}',f'{family}18_year2023_native_supplement_v1_20261009'):
            directory=A/'service_owned_workflows_20261006'/name
            assert not owned(read(directory/'native_launch.json')) and read(directory/'service_execution.json')['status']=='passed'
            inputs.extend([directory/'service_execution.json',directory/'native_launch.json',directory/'job_definition.json'])
        records.append({'round':number,'family':family,'actual_head_year_states':20,'actual_native_cases':90,'actual_cold_cases':90,
            'actual_historical_native_cases':72,'actual_final_model_calendar_cases':18,'actual_prefit_rejections':18,
            'original_head_year_states':16,'additional_own2023_head_year_states':4,
            'head_year_records':[{'head':h,'year':y,'native_sha256':seen[(h,y)][0],'independent_state_sha256':seen[(h,y)][1]} for h,y in sorted(seen)],
            'all5_annual_model_years_actual_native_reload_independent_stage_replayed':True,'new_native_fits':0,'new_quality_scores':0})
    create(A/'sparse150151_all20_annual_native_coverage_v1_20261009.json',{'status':'passed_actual20_own_annual_native_states90_full90_cold_per_scheme_after_missing2023_supplement',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in dict.fromkeys(inputs)},'records':records,
        'original72_proofs_preserved_not_overwritten_or_rerun':True,'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'schemes':2,'actual_states_per_scheme':20,'actual_native_per_scheme':90,'cold_per_scheme':90,'new_quality_scores':0},flush=True)
if __name__=='__main__':main()
