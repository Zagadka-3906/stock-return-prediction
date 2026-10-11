"""Prepare150 prospective verifier using proven route checks, actual six groups and59-case contracts."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from prepare_JointCrossHuber147_core_receivers_v1_20261008 import save

def main():
    s=(A/'verify_CrossFamilyFine125_prospective_routes_v1_20261008.py').read_text(encoding='utf8')
    substitutions={
        'prepare_CrossFamilyFine125_round145_sources_v2_20261008':'prepare_HuberSparse59_round150_sources_v2_20261009',
        'CrossFamilyFine145_storage_v1_20261008':'HuberSparse150_storage_v1_20261008',
        'CrossFamilyFine_complete_parent_CDF_v1_20261008':'HuberSparse_complete_parent_CDF_v1_20261008',
        'run_CrossFamilyFine125_official_comparison_v1_20261008':'run_HuberSparse59_official_comparison_v2_20261009',
        'CrossFamilyFine125_prospective_routes_v1_20261008':'HuberSparse59_prospective_routes_v1_20261009',
        'CrossFamilyFine125_round145_plan_v2_20261008':'HuberSparse59_round150_plan_v1_20261008',
        'CrossFamilyFine125_round145_source':'HuberSparse59_round150_source',
        'CrossFamilyFine125_actual_controls_index':'HuberSparse59_actual_controls_index',
        'CrossFamilyFine125_selected_release':'HuberSparse59_selected_release',
        'CrossFamilyFine125_scores_github':'HuberSparse59_scores_github',
        'register_CrossFamilyFine125_round145_artifacts':'register_HuberSparse59_round150_artifacts',
        'publish_CrossFamilyFine125_round145_full_validation':'publish_HuberSparse59_round150_full_validation',
        'passed_actual125_CrossFamily_complete_parent_full_official_comparisons':'passed_actual59_HuberSparse_complete_parent_full_official_comparisons',
        'zero_CrossFamily_residual_identity':'zero_HuberSparse_residual_identity',
        '[134,136,141,144]':'[146,147,148,149]',
        "len(plan['new_cases'])==120":"len(plan['new_cases'])==54",
        "plan['final_selection_rule']=='official_S_desc_unique_physical_model_SHA_count_asc_absolute_amplitude_asc_case_asc'":"plan['selection']=='highest_complete_connected2020_2024_official_score_then_physical_model_count_then_abs_weight_then_case'",
        "f'crossfamily_group4_share{cfg0[\"share\"]}'":"f'HuberSparse_group{cfg0[\"group\"]}_share{cfg0[\"share\"]}'",
        'GROUPS[4]':'GROUPS[cfg0[\'group\']]',
        "stage['group']==4":"stage['group']==cfg0['group']",
        'collect(145,56,125)':'collect(150,61,59)',
        '[(145,56,125)]':'[(150,61,59)]',
        '[145,56,125]':'[150,61,59]',
        'collect(145, 56, 125)':'collect(150, 61, 59)',
        "namespace['snapshot'](145)":"namespace['snapshot'](150)",
        "== full['scored_records'] == 125":"== full['scored_records'] == 59",
        'all125_scored_records_QA56':'all59_scored_records_QA61',
        'publish_CrossFamilyFine125_evidence_v1_20261008':'publish_HuberSparse59_evidence_v1_20261009',
        'prepare_CrossFamilyFine125_selected_candidate_v1_20261008':'prepare_HuberSparse59_selected_candidate_v2_20261009',
        'CrossFamilyFine125_{phase}_github':'HuberSparse59_{phase}_github',
        'CrossFamilyFine145_D_scoring_scope':'HuberSparse150_D_scoring_scope',
        'CrossFamilyFine145_cross_volume_byte_probe':'HuberSparse150_cross_volume_byte_probe',
        'passed_actual32_prospective145_sources':'passed_actual32_prospective150_sources',
        'original145':'original150',
        '<145_':'<150_',
        'for125 official':'for59 official'}
    for before,after in substitutions.items():s=s.replace(before,after)
    marker="    assert future<=allowed,future-allowed"
    assert s.count(marker)==1
    s=s.replace(marker,"    allowed.update({A/n for n in ('actual_HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009.json','HuberSparse150_prior_complete_forecast_duplicate_audit_raw_v1_20261009.json')})\n"+marker)
    save('verify_HuberSparse59_prospective_routes_v1_20261009.py',s)
if __name__=='__main__':main()
