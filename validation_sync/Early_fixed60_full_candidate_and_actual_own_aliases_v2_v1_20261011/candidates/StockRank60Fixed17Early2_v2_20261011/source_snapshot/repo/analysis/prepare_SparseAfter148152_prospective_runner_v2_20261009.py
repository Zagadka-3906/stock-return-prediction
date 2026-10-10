from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
old=A/'verify_SparseAfter14829_prospective_routes_v1_20261009.py';new=A/'verify_SparseAfter14829_prospective_routes_v2_20261009.py'
s=old.read_text(encoding='utf8');policy='highest_complete_connected2020_2024_official_score_then_physical_model_count_then_abs_weight_then_case'
s=s.replace("plan['selection']",'plan.get(\'selection\','+repr(policy)+')')
compile(s,str(new),'exec')
with new.open('x',encoding='utf8') as f:f.write(s)
print(new)
