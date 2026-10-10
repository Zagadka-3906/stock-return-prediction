from pathlib import Path
import sys
A=Path(__file__).resolve().parent
def main():
    p=A/'verify_BF16FlagAfter15222_prospective_routes_v1_20261010.py';s=p.read_text(encoding='utf8')
    for old,new in [
        ('BF16FlagAfter15222_prospective_routes_v1_20261010.json','BF16FlagAfter15222_prospective_routes_v2_20261010.json'),
        ('BF16FlagAfter152157_complete_native_predictor_preparation_v1_20261009.json','BF16FlagAfter152157_complete_native_predictor_preparation_v58_20261009.json'),
        ('collect(155, 66, 80)','collect(157, 68, 22)'),
        ("actual_full_QA_version': 66","actual_full_QA_version': 68"),
        ("namespace['snapshot'](155)","namespace['snapshot'](157)"),
        ('passed_actual56_seed09_155_prospective_sources2100_graphs21_baselines14_physical_model_sort_checks','passed_actual40_flag_after152157_prospective_sources380_graphs15_baselines10_physical_model_sort_checks')]:s=s.replace(old,new)
    target=A/'verify_BF16FlagAfter15222_prospective_routes_v2_20261010.py';assert not target.exists()
    target.write_text(s,encoding='utf8',newline='\n')
    p=A/'prepare_BF16FlagAfter15222_round157_sources_v1_20261009.py'
    s=p.read_text(encoding='utf8').replace('BF16FlagAfter15222_prospective_routes_v1_20261010','BF16FlagAfter15222_prospective_routes_v2_20261010')
    p.write_text(s,encoding='utf8',newline='\n')
if __name__=='__main__':main()
