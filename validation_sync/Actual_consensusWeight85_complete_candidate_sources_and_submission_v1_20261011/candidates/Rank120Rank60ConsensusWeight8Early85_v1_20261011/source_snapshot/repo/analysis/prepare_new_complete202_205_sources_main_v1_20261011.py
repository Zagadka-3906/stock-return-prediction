from pathlib import Path
import sys,ast,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import sha,create,read
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
mods=['prepare_StockRank60Fraction202_complete40_pipeline_v2_20261011','prepare_Rank120Rank60Protected203_complete39_pipeline_v1_20261011','prepare_StockRank60Seed10Direct204_complete35_pipeline_v1_20261011','prepare_Rank60TwoSeedProtected205_complete39_pipeline_v2_20261011']
paths=[Path(__file__)]
for name in mods:
 m=importlib.import_module(name)
 for p,d in read(A/m.PROOF)['input_sha256'].items():assert sha(p)==d,p
 paths.extend(m.source_paths())
paths.extend(A/n for n in ['actual202_v1_idle_token_substitution_recovery_v2_20261011.json','actual203_204_all_runtime_imports_and_seed10_additional_callbacks_admission_v1_20261011.json','actual205_partial_factory_prospective_repair_admission_v2_20261011.json','actual205_v2_runtime_imports_source_pins_admission_v2_20261011.json','prepare_Rank60TwoSeedProtected205_complete39_pipeline_v1_20261011.py','audit_prospective205_v2_runtime_imports_v1_20261011.py','audit_prospective205_v2_runtime_imports_v2_20261011.py','prepare_per_round_new_horizon_main_publications_v1_20261011.py','actual_per_round_new_horizon_main_publications_admission_v1_20261011.json'])
assert all(p.is_file() for p in paths)
t=(A/'publish_actual_rank60_seed10_own6_and_two_seed37_predeclared_sources_main_v1_20261011.py').read_text(encoding='utf8')
lines=t.splitlines();lines=[('    paths=[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(paths)])+']') if line.strip().startswith('paths=') else line for line in lines]
t='\n'.join(lines)+'\n';t=t.replace('Actual_rank60_seed10_own6_and_two_seed37_predeclared_sources','Actual_complete202_205_prospective_sources')
t=t.replace('predeclared_seed10_mature60day_own6_full5_native42_direct33_and_two_seed37_original_seed9_models_not_reused_for_training','prospective202_to205_all_source_pins_verified_no_pending_full_family_declared_complete_errors_retained')
t=t.replace('预声明60日第二种子六年度训练与33项直接方案、37项双种子组合；未完成模型不计入核验','冻结202至205轮完整核验流程与修复记录；各轮完成记录单独同步；未来核验尚未完成')
p=A/'publish_actual_complete202_205_prospective_sources_main_v1_20261011.py';ast.parse(t);assert not p.exists();p.write_text(t,encoding='utf8')
r=start_service('actual_complete202_205_prospective_sources_main_v1_20261011',p.name,[],{str(p):sha(p),str(Path(__file__)):sha(__file__)})
create(A/'actual_complete202_205_prospective_sources_main_activation_v1_20261011.json',r)
print({'main_only_source_publication_queued':True,'new_scientific_scores':0},flush=True)
