from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
files=[Path(__file__),A/'prepare_flag17_raw_completed_records_main_v1_20261011.py',A/'run_publish_rank60_flag17_after183_completed17_main_v1_20261011.py']
for name in ['rank60_flag17_raw_sources_predeclared_v1_20261011.json','rank60_flag17_best17_full_candidate_sources_admission_v1_20261011.json','rank60_flag17_actual_runtime_import_admission_v1_20261011.json','flag17_exact_existing_controller_aliases_admission_v1_20261011.json']:
 p=A/name;files.append(p);files.extend(Path(q) for q in read(p)['input_sha256'])
template=A/'publish_actual_two_seed37_direct_candidate_observer142_sources_main_v1_20261011.py';s=template.read_text(encoding='utf8');tree=ast.parse(s)
node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets));lines=s.splitlines(keepends=True);lines[node.lineno-1:node.end_lineno]=['    paths=[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(files)])+']\n']
s=''.join(lines).replace('two_seed37_direct_candidate_observer142_sources','flag17_frozen_sources').replace('预声明双随机种子37项提分后直接完整候选推理及交付；复用已核验CPU证据，完整科学核验保留','冻结涨停股排序17项新方案；复用已核验512模型，官方全量及因果对照、提分后完整36模型核验保留')
s=s.replace('actual12_candidate_runtime_imports_capacity109_CDF49_score_gain_only_future_native14_complete37_model_independent_cold80_main_and_delivery_predeclared_no_execution_claim','actual9_flag_only17_runtime_module_imports_and_exact_actual_controller_aliases_passed_existing_small512_bank_reused_full16_prefix48_scoring_and_gain_only_native14_complete36_cold80_pipeline_predeclared_no_science_claim')
driver=A/'publish_actual_flag17_frozen_sources_main_v1_20261011.py';ast.parse(s);assert not driver.exists();driver.write_text(s,encoding='utf8',newline='\n')
assert allowed();i=start_service('actual_flag17_frozen_sources_main_v1_20261011',driver.name,[],{str(driver):sha(driver)});create(A/'actual_flag17_frozen_sources_main_activation_v1_20261011.json',i)
print('Frozen flag17 code, namespace controls and raw/candidate publication protocols queued to main',flush=True)
