"""Supplement own2023 native stage replay for150 and151 without rerunning completed72 controls."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def main():
    originals=[];products=[]
    for family,date in (('HuberSparse','20261008'),('RFFSparse','20261009')):
        original=A/f'verify_{family}72_native_historical_calendar_v1_{date}.py';s=original.read_text(encoding='utf8');originals.append(original)
        s=s.replace(f'{family}72_native_historical_calendar_v1_{date}',f'{family}18_year2023_native_supplement_v1_20261009')
        s=s.replace(f'actual_{family}72_native_calendar_location_v1_{date}',f'actual_{family}18_year2023_native_supplement_location_v1_20261009')
        substitutions={
            'frozen_before_actual72_native_controls':'frozen_before_actual18_year2023_native_controls',
            "'historical_years':[2021,2022,2024]":"'historical_years':[2023]",
            "'final_model_year':2025":"'final_model_year':None",
            "'remapped_training_date_calendar_years':[2025,2026]":"'remapped_training_date_calendar_years':[]",
            "'expected_historical_cases':54":"'expected_historical_cases':18",
            "'expected_calendar_cases':18":"'expected_calendar_cases':0",
            "'expected_cold_cases':72":"'expected_cold_cases':18",
            "'expected_prefit_date_rejections':18":"'expected_prefit_date_rejections':0",
            'for year in (2021,2022,2024,2025):':'for year in (2023,):',
            "'expected':72":"'expected':18",
            'assert len(records)==72':'assert len(records)==18',
            "'actual_historical_cases':54":"'actual_historical_cases':18",
            "'actual_calendar_cases':18":"'actual_calendar_cases':0",
            "'actual_cold_cases':72":"'actual_cold_cases':18",
            "'actual_prefit_final_model_date_rejections':18":"'actual_prefit_final_model_date_rejections':0",
            f'passed_actual54_{family}_historical_native_and18_final_calendar_with72_cold_and18_prefit_rejections':f'passed_actual18_{family}_own2023_native_reload_independent_OOF_and18_cold_supplement'}
        for before,after in substitutions.items():
            assert before in s,before;s=s.replace(before,after)
        products.append(save(f'verify_{family}18_year2023_native_supplement_v1_20261009.py',s))
    create(A/'sparse150151_year2023_supplement_preparation_v1_20261009.json',{'status':'prepared_two_additional_own2023_native18_cold18_controls_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products]},
        'old72_native_controls_cover16_of20_head_year_combinations':True,'supplement_adds_missing4_head_year_combinations_per_scheme':True,
        'requires_union_coverage_proof_before_admission':True,'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'supplements':2,'native_cases_per_scheme':18,'cold_per_scheme':18,'new_quality_scores':0},flush=True)
if __name__=='__main__':main()
