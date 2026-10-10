from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
original=A/'run_rank120_rank60_after183_protected37_screen_v1_20261011.py'
base=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_protected37_screen_v1_20261011');proof=read(base/'verification.json')
assert proof['new_quality_score_records']==37 and len(proof['records'])==37
for p,d in proof['input_sha256'].items():assert sha(p)==d,p
reference=proof['best'];assert reference['configuration']['kind']=='valid_pool_protection_v1'
plan=[{'kind':'anchor183','role':None,'weight':0.,'sign':1.,'protect_fraction':None,'rank120_weight':None},dict(reference['configuration'])]
for fraction in (.1,.125,.2,.25,.35,.5):
 for weight in (.004,.008,.016,.032,.064,.125):plan.append({**reference['configuration'],'weight':weight,'protect_fraction':fraction})
assert len(plan)==38
s=original.read_text(encoding='utf8');tree=ast.parse(s);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='cases');lines=s.splitlines();lines[fn.lineno-1:fn.end_lineno]=['def cases():','    return '+repr(plan)];s='\n'.join(lines)+'\n'
s=s.replace("closed('actual_rank60_rank20_after183_mixed37_screen_v1_20261011')","closed('actual_fraction38_completed_namespace_bridge_v1_20261011')\n    closed('actual_rank120_rank60_after183_protected37_screen_v2_20261011')")
s=s.replace("OUT=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_protected37_screen_v1_20261011')","OUT=Path('E:/赛题五_本机临时/StockRank120Rank60_after183_best_blend_fraction38_screen_v1_20261011')")
s=s.replace("'expected_cases':37","'expected_cases':38").replace("'new_quality_score_records':37","'new_quality_score_records':38").replace("'actual_nonidentity_full_controls':36","'actual_nonidentity_full_controls':37").replace("'actual_nonidentity_prefix_controls':108","'actual_nonidentity_prefix_controls':111")
s=s.replace('actual_StockRank120Rank60_after183_protected37_screen_location_v1_20261011','actual_StockRank120Rank60_after183_best_blend_fraction38_screen_location_v1_20261011')
s=s.replace("    pins={str(p):sha(p) for p in paths};plan=cases()", "    paths += [A/'rank120_rank60_best_blend_fraction38_predeclared_sources_admission_v1_20261011.json',Path('E:/赛题五_本机临时/StockRank120Rank60_after183_protected37_screen_v1_20261011/verification.json'),A/'actual_fraction38_completed_only_terminal_namespace_collision_bridge_v1_20261011.json']\n    pins={str(p):sha(p) for p in paths};plan=cases()")
s=s.replace("            if not i:assert metrics==baseline", "            if not i:assert metrics==baseline\n            if i==1:\n                reference=read(Path('E:/赛题五_本机临时/StockRank120Rank60_after183_protected37_screen_v1_20261011/verification.json'))['best']\n                assert metrics==reference['metrics'] and numeric==reference['prediction_numeric_sha256']")
p=A/'run_rank120_rank60_after183_best_blend_fraction38_screen_v1_20261011.py';ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf8')
protocol=A/'rank120_rank60_best_blend_fraction38_predeclared_sources_admission_v1_20261011.json'
create(protocol,{'status':'predeclared38_protection_fraction_and_weight_refinements_of_TRAIN_selected_all37_best_mix_no_new_fits','input_sha256':{str(q):sha(q) for q in [Path(__file__),original,p,base/'verification.json']},'cases':plan,'selected_reference_case':reference['case'],'selected_reference_all8_metrics':reference['metrics'],'new_fits_or_scores':0,'test_labels_read':False})
r=start_service('actual_rank120_rank60_after183_best_blend_fraction38_screen_v1_20261011',p.name,[],{str(p):sha(p),str(protocol):sha(protocol)})
create(A/'actual_rank120_rank60_best_blend_fraction38_screen_activation_v1_20261011.json',r)
print({'predeclared_cases':38,'selected_reference_case':reference['case'],'new_fits':0},flush=True)
