"""Prepare150 phase publishers with own measured72/55 evidence and unique controls/scores output scopes."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def main():
    s=(A/'publish_CrossFamilyFine125_evidence_v1_20261008.py').read_text(encoding='utf8')
    replacements={
        'KrylovGram52_round141_full_registration_v18_20261008':'PureRFFHuber128_round149_full_registration_v1_20261008',
        'CrossFamilyFine125_round145_source_admission':'HuberSparse59_round150_source_admission',
        'CrossFamilyFine125_controls_main_publication':'HuberSparse59_controls_main_publication',
        'CrossFamilyFine121_actual_full_historical_controls_v1_20261008':'HuberSparse55_full_historical_controls_v1_20261008',
        'CrossFamilyFine125_official_comparison':'HuberSparse59_official_comparison',
        'prepare_CrossFamilyFine125_round145_sources_v2_20261008':'prepare_HuberSparse59_round150_sources_v2_20261009',
        'CrossFamilyFine125_actual_controls_index':'HuberSparse59_actual_controls_index',
        'passed_actual20_heads121_fixed_base_CDF363cold30_historical_native_hooks':'passed_actual20_states55_fixed_base_CDF165cold72_native_calendar_controls',
        'passed_actual125_CrossFamily_complete_parent_full_official_comparisons':'passed_actual59_HuberSparse_complete_parent_full_official_comparisons',
        'CrossFamilyFine125_{phase}':'HuberSparse59_{phase}',
        'main_publisher_v8_20261008':'main_publisher_v9_20261009',
        'actual_completed_CrossFamily_controls_or_scores_before_full145_qualification':'actual_completed_HuberSparse_controls_or_scores_before_full150_qualification',
        "'round':145":"'round':150",
        '第145轮跨模型':'第150轮Huber与稀疏模型',
        'full145_qualification_pending':'full150_qualification_pending',
        'future_candidate_and_QA56_and_round145_main_receipt_pending':'future_candidate_and_QA61_and_round150_main_receipt_pending',
        "len(proof['records'])==125":"len(proof['records'])==59",
        '125 if phase':'59 if phase',
        "'actual_full_CDF_controls':121":"'actual_full_CDF_controls':55",
        "'actual_cold_CDF_controls':363":"'actual_cold_CDF_controls':165",
        "'actual_historical_native_hooks':30":"'actual_historical_native_hooks':54,'actual_final_calendar_native_hooks':18,'actual_cold_native_hooks':72"}
    for before,after in replacements.items():s=s.replace(before,after)
    before="for pointer in ('actual_CrossFamily_bank30_synthetic_location_v1_20261008.json',\n        'actual_CrossFamilyFine121_parent134_location_v1_20261008.json','actual_CrossFamilyFine30_native_hooks_location_v1_20261008.json'):"
    after="for pointer in ('actual_HuberSparse55_parent134_location_v1_20261008.json','actual_HuberSparse72_native_calendar_location_v1_20261008.json','actual_HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009.json'):"
    assert s.count(before)==1;s=s.replace(before,after)
    save('publish_HuberSparse59_evidence_v1_20261009.py',s)
if __name__=='__main__':main()
