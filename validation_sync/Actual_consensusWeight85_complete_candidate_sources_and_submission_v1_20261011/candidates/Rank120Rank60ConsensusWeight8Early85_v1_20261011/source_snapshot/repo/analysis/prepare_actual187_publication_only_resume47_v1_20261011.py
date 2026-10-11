from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service
assert allowed()
failed=A/'service_owned_workflows_20261006/actual187_registered_QA_main_resume45_v1_20261011';assert read(failed/'service_execution.json')['status']=='failed' and not owned(read(failed/'native_launch.json'))
native=A/'shared_live_ranking_report_round187_execution_v1_20261011.json';scope=A/'optimization_20261003_r187/provenance_scope_execution.json'
assert read(native)['status']=='passed_actual_native_graph_capture_and_private_codec_QA_reader_restored' and read(scope)['status']=='passed'
plan=A/'rank20_two_seed_complete88_after186_plan_v1_20261011.json'
for f in read(plan)['families']:
 p=Path(f['output'])/'verification.json';assert len(read(p)['records'])==f['records']
original=A/'publish_Rank20TwoSeed187_round187_full_validation_v2_20261011.py';text=original.read_text(encoding='utf8')
before="    for family in tuple(f['name']+'_screen_v1_20261010' for f in read(A/'rank20_two_seed_complete88_after186_plan_v1_20261011.json')['families']):\n        folder=Path('E:/赛题五_本机临时')/family"
after="    for family in read(A/'rank20_two_seed_complete88_after186_plan_v1_20261011.json')['families']:\n        folder=Path(family['output']);assert len(read(folder/'verification.json')['records'])==family['records']"
assert text.count(before)==1;text=text.replace(before,after)
text=text.replace('    for path in extra:',"    extra += [A/'actual187_publication_only_resume47_sources_admission_v1_20261011.json',A/'shared_live_ranking_report_round187_execution_v1_20261011.json',A/'optimization_20261003_r187/provenance_scope_execution.json',A/'service_owned_workflows_20261006/actual187_registered_QA_main_resume45_v1_20261011/stderr.log',A/'publish_Rank20TwoSeed187_round187_full_validation_v3_20261011.py',A/'run_actual187_publication_only_resume47_v1_20261011.py']\n    for path in extra:")
p=A/'publish_Rank20TwoSeed187_round187_full_validation_v3_20261011.py';ast.parse(text);assert not p.exists();p.write_text(text,encoding='utf8')
inputs=[Path(__file__),original,p,native,scope,plan,failed/'service_execution.json',failed/'stderr.log']
create(A/'actual187_publication_only_resume47_sources_admission_v1_20261011.json',{'status':'existing_actual17490_board_QA98_native_bytes_provenance_all_pass_only_explicit_family_output_paths_corrected_before_main_no_board_rescore_or_reinference','input_sha256':{str(q):sha(q) for q in inputs},'new_fits_or_scores':0,'original_failure_preserved':True})
driver=A/'run_actual187_publication_only_resume47_v1_20261011.py';assert driver.is_file()
r=start_service('actual187_completed_QA_publication_only_resume47_v1_20261011',driver.name,[],{str(driver):sha(driver),str(p):sha(p),str(A/'actual187_publication_only_resume47_sources_admission_v1_20261011.json'):sha(A/'actual187_publication_only_resume47_sources_admission_v1_20261011.json')})
create(A/'actual187_publication_only_resume47_activation_v1_20261011.json',r);print({'actual_publication_only_resumption':47,'rerun_board_scores_or_inference':False},flush=True)
