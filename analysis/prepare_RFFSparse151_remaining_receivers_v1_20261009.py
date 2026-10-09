"""Prepare own151 prior forecast audit, source admission and evidence phases before any quality."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def own(s):
    s=s.replace('PureRFFHuber128_round149_full_registration_v1_20261008','PREVIOUS_ACTUAL_150_FULL')
    s=s.replace('prepare_HuberSparse59_round150_sources_v2_20261009','prepare_RFFSparse59_round151_sources_v1_20261009')
    s=s.replace('HuberSparse150_complete_receiver_refinement_v3_20261009','RFFSparse151_receiver_label_refinement_v3_20261009')
    s=s.replace('HuberSparse','RFFSparse').replace('RFFSparse150','RFFSparse151').replace('_round150_','_round151_').replace('prospective150','prospective151')
    s=s.replace('optimization_20261003_r149/full_registration_execution.json','optimization_20261003_r150/full_registration_execution.json')
    s=s.replace('round149_receipt.json','round150_receipt.json').replace('round149','round150')
    import re
    s=re.sub(r'(RFFSparse[A-Za-z0-9_/-]*?)_v1_20261008',r'\1_v1_20261009',s)
    s=s.replace('qa_v61_20261007','qa_v62_20261009').replace('QA61','QA62').replace('full150_qualification','full151_qualification').replace('round150_main_receipt_pending','round151_main_receipt_pending')
    s=s.replace('PREVIOUS_ACTUAL_150_FULL','HuberSparse59_round150_full_registration_v1_20261008')
    return s

def main():
    originals=[];products=[]
    for old,new in (
        ('verify_HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009.py','verify_RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009.py'),
        ('verify_HuberSparse59_round150_sources_v1_20261009.py','verify_RFFSparse59_round151_sources_v1_20261009.py'),
        ('publish_HuberSparse59_evidence_v1_20261009.py','publish_RFFSparse59_evidence_v1_20261009.py')):
        p=A/old;originals.append(p);s=own(p.read_text(encoding='utf8'))
        if old.startswith('verify_HuberSparse59_round150_sources'):
            marker='    index=A/';assert s.count(marker)==1
            extra="""    annual_path=A/'sparse150151_all20_annual_native_coverage_v1_20261009.json';annual=read(annual_path)
    coverage=next(r for r in annual['records'] if r['round']==151)
    assert coverage['actual_head_year_states']==20 and coverage['actual_native_cases']==coverage['actual_cold_cases']==90
    for path,digest in annual['input_sha256'].items():assert sha(path)==digest,path
    supplemental_pointer=A/'actual_RFFSparse18_year2023_native_supplement_location_v1_20261009.json'
    supplemental=Path(read(supplemental_pointer)['output'])/'verification.json'
    assert sha(supplemental)==read(supplemental_pointer)['verification_sha256']
    metadata.extend([annual_path,supplemental_pointer,supplemental]);pins.update(annual['input_sha256']);pins.update({str(p):sha(p) for p in (annual_path,supplemental_pointer,supplemental)})
"""
            s=s.replace(marker,extra+marker)
            s=s.replace("'actual20_saved_states':native,", "'actual20_saved_states':native,'actual90_native_and_cold_stage_cases':True,'all20_own_annual_native_states_replayed':True,")
            s=s.replace("'complete32_routes_and_graph_controls_passed':True,", "'complete32_routes_and_graph_controls_passed':True,'all20_own_annual_native_states_replayed':True,")
        if old.startswith('publish_'):
            s=s.replace("'RFFSparse55_full_historical_controls_v1_20261008'", "'RFFSparse55_full_historical_controls_v1_20261009'")
            before="'actual_RFFSparse72_native_calendar_location_v1_20261009.json','actual_RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009.json'"
            after="'actual_RFFSparse72_native_calendar_location_v1_20261009.json','actual_RFFSparse18_year2023_native_supplement_location_v1_20261009.json','actual_RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009.json'"
            assert s.count(before)==1;s=s.replace(before,after)
            s=s.replace("'round':150", "'round':151").replace('第150轮','第151轮').replace('Huber与稀疏模型','RFF与稀疏模型')
            s=s.replace("'actual_historical_native_hooks':54", "'actual_historical_native_hooks':54,'additional_own2023_native_hooks':18,'actual_total_native_hooks':90,'actual_total_cold_native_hooks':90,'all20_head_year_states_actual_stage_replayed':True")
            s=s.replace("assert index['status']=='passed_actual20_states55_fixed_base_CDF165cold72_native_calendar_controls'", "assert index['status']=='passed_actual20_states55_fixed_base_CDF165cold72_native_calendar_controls' and index['all20_own_annual_native_states_replayed']")
        products.append(save(new,s))
    create(A/'RFFSparse151_remaining_receiver_preparation_v1_20261009.json',{'status':'prepared_actual151_duplicate_source_admission_and_two_phase_main_receivers_before_quality',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in [Path(__file__),*originals,*products]},
        'all32_prospective_route_and_graph_checks_still_required':True,'quality_admitted':False,'new_quality_scores':0,'new_future_inference':0,'new_native_fits':0,'test_labels_read':False})
    print({'remaining_receivers':3,'quality_admitted':False},flush=True)
if __name__=='__main__':main()
