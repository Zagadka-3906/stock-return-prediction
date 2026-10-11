from pathlib import Path
import re,sys
A=Path(__file__).resolve().parent
source=A/'recover144_fresh_selected_scoring_and_source_routes_v2_20261008.py';value=source.read_text(encoding='utf8')
mapping={
'ConeRidgeAlpha100_selected_candidate_preparation_v7_20261008':'ConeRidgeAlpha100_selected_candidate_preparation_v8_20261008',
'ConeRidgeAlpha100_selected_candidate_preparation_v8_20261008':'ConeRidgeAlpha100_selected_candidate_preparation_v9_20261008',
'ConeRidgeAlpha100_selected_candidate_sealing_v8_20261008':'ConeRidgeAlpha100_selected_candidate_sealing_v9_20261008',
'selected_candidate_v7_20261008.py':'selected_candidate_v8_20261008.py','selected_candidate_v8_20261008.py':'selected_candidate_v9_20261008.py',
'ConeRidgeAlpha144_storage_v4_20261008':'ConeRidgeAlpha144_storage_v5_20261008','ConeRidgeAlpha144_storage_v5_20261008':'ConeRidgeAlpha144_storage_v6_20261008',
'ConeRidgeAlpha100_selected_release_v2_20261008':'ConeRidgeAlpha100_selected_release_v3_20261008','ConeRidgeAlpha100_selected_release_v3_20261008':'ConeRidgeAlpha100_selected_release_v4_20261008',
'ConeRidgeAlpha100_v2_20261008':'ConeRidgeAlpha100_v3_20261008','ConeRidgeAlpha100_v3_20261008':'ConeRidgeAlpha100_v4_20261008',
"EBASE/'candidate_v3'":"EBASE/'candidate_v4'","EBASE/'selected_release_v3'":"EBASE/'selected_release_v4'",
'prepare_ConeRidgeAlpha100_round144_sources_v5_20261008':'prepare_ConeRidgeAlpha100_round144_sources_v6_20261008','prepare_ConeRidgeAlpha100_round144_sources_v6_20261008':'prepare_ConeRidgeAlpha100_round144_sources_v7_20261008',
'ConeRidgeAlpha100_round144_source_admission_v5_20261008':'ConeRidgeAlpha100_round144_source_admission_v6_20261008','ConeRidgeAlpha100_round144_source_admission_v6_20261008':'ConeRidgeAlpha100_round144_source_admission_v7_20261008',
'ConeRidgeAlpha100_round144_source_preparation_v5_20261008':'ConeRidgeAlpha100_round144_source_preparation_v6_20261008','ConeRidgeAlpha100_round144_source_preparation_v6_20261008':'ConeRidgeAlpha100_round144_source_preparation_v7_20261008',
'verify_ConeRidgeAlpha100_prospective_routes_v7_20261008':'verify_ConeRidgeAlpha100_prospective_routes_v8_20261008','verify_ConeRidgeAlpha100_prospective_routes_v8_20261008':'verify_ConeRidgeAlpha100_prospective_routes_v9_20261008',
'ConeRidgeAlpha100_prospective_routes_v5_20261008':'ConeRidgeAlpha100_prospective_routes_v6_20261008','ConeRidgeAlpha100_prospective_routes_v6_20261008':'ConeRidgeAlpha100_prospective_routes_v7_20261008',
'ConeRidgeAlpha144_receiver_preparation_v5_20261008':'ConeRidgeAlpha144_receiver_preparation_v6_20261008','ConeRidgeAlpha144_receiver_preparation_v6_20261008':'ConeRidgeAlpha144_receiver_preparation_v7_20261008',
'cross_volume_byte_probe_v7':'cross_volume_byte_probe_v8','cross_volume_byte_probe_v8':'cross_volume_byte_probe_v9',
'actual_registration_v8_20261008':'actual_registration_v9_20261008','actual_registration_v9_20261008':'actual_registration_v10_20261008',
'full_registration_v8_file_IO_20261008':'full_registration_v9_file_IO_20261008','full_registration_v9_file_IO_20261008':'full_registration_v10_file_IO_20261008',
'run_ConeRidgeAlpha100_round144_full_registration_v8_20261008':'run_ConeRidgeAlpha100_round144_full_registration_v9_20261008','run_ConeRidgeAlpha100_round144_full_registration_v9_20261008':'run_ConeRidgeAlpha100_round144_full_registration_v10_20261008',
'ConeRidgeAlpha100_round144_full_registration_v9_20261008':'ConeRidgeAlpha100_round144_full_registration_v10_20261008',
'pre_inference_source_freeze_v2':'pre_inference_source_freeze_v3','pre_inference_source_freeze_v3':'pre_inference_source_freeze_v4',
'recover144_fresh_selected_scoring_and_source_routes_v2_20261008.py':'recover144_verified_short_parent_alias_routes_v3_20261008.py',
'actual144_selected_fresh_routes_launches_v2_20261008':'actual144_verified_short_parent_alias_routes_launches_v3_20261008'}
pattern=re.compile('|'.join(re.escape(x) for x in sorted(mapping,key=len,reverse=True)));value=pattern.sub(lambda m:mapping[m.group()],value)
value=value.replace(".replace('ConeRidgeAlpha144_D_scoring_v5_20261008/selected/scoring_validation_only','ConeRidgeAlpha144_D_scoring_v5_20261008/selected_v3/scoring_validation_only')",".replace('ConeRidgeAlpha144_D_scoring_v5_20261008/selected_v3/scoring_validation_only','ConeRidgeAlpha144_D_scoring_v5_20261008/selected_v4/scoring_validation_only')")
needle="    p=A/name;assert not p.exists(),p;compile(value,str(p),'exec');p.write_text(value,encoding='utf8',newline='\\n');return p";assert value.count(needle)==1
replacement="    if name=='prepare_ConeRidgeAlpha100_selected_candidate_v9_20261008.py':\n        value=value.replace('from short_content_addressed_native_storage_v1_20261008 import installed as short_storage','from short_content_addressed_native_storage_v2_20261008 import installed as short_storage').replace('with short_storage() as storage_contract:',\"with short_storage(ns,freeze/'model_source_aliases') as storage_contract:\")\n    p=A/name;assert not p.exists(),p;compile(value,str(p),'exec');p.write_text(value,encoding='utf8',newline='\\n');return p"
value=value.replace(needle,replacement)
# Generated source packages also pin the actual alias implementation and its executed long-path control.
value=value.replace("A/'short_content_addressed_native_storage_v1_20261008.py'","A/'short_content_addressed_native_storage_v2_20261008.py',A/'actual_short_parent_alias_nested_copy_v2_20261008.json'")
target=A/'recover144_verified_short_parent_alias_routes_v3_20261008.py';assert not target.exists();compile(value,str(target),'exec');target.write_text(value,encoding='utf8',newline='\n')
