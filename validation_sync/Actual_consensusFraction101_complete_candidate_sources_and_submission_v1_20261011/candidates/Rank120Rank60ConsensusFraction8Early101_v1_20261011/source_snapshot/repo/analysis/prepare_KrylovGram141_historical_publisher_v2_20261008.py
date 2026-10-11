"""Queue main export of completed141 historical controls, after the earlier causal publication closes."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    source=A/'publish_SpectralGram140_historical_causal_v1_20261008.py';text=source.read_text(encoding='utf8')
    for before,after in (
        ('SpectralGram24_native_historical_hooks_v2_20261008','KrylovGram24_native_historical_hooks_v1_20261008'),
        ('actual_SpectralGram24_native_hooks_location_v2_20261008','actual_KrylovGram24_native_hooks_location_v1_20261008'),
        ('SpectralGram20_causal_refit_controls_v1_20261008','KrylovGram20_causal_refit_controls_v2_20261008'),
        ('actual_SpectralGram20_causal_refit_location_v1_20261008','actual_KrylovGram20_causal_refit_location_v2_20261008'),
        ('verify_SpectralGram20_causal_refit_v1_20261008','verify_KrylovGram20_causal_refit_v2_20261008'),
        ('actual_SpectralGram20_causal_refit_hidden_launch_v1_20261008','actual_KrylovGram20_causal_refit_hidden_launch_v2_20261008'),
        ('nonflag_SpectralGram64_controls_main_v1_20261008','nonflag_KrylovGram64_controls_main_v2_20261008'),
        ('SpectralGram52_round140','KrylovGram52_round141'),('SpectralGram140','KrylovGram141'),('SpectralGram','KrylovGram')):text=text.replace(before,after)
    for fragment in (
        "'verify_KrylovGram24_native_historical_hooks_v1_20261008.py',\n        ",
        "'KrylovGram141_historical_hook_scope_recovery_v2_20261008.json',\n        ",
        "'actual_KrylovGram24_historical_hook_recovery_hidden_launch_v2_20261008.json',\n        "):
        assert text.count(fragment)==1,(fragment,text.count(fragment));text=text.replace(fragment,'')
    marker="'verify_KrylovGram24_native_historical_hooks_v1_20261008.py'";assert text.count(marker)==1
    first=text.index("    failed=A/'service_owned_workflows_20261006/");last=text.index('    controls=',first);text=text[:first]+text[last:]
    text=text.replace("len(native['adapter_controls'])==6 and native['backend_priority_cases']==6","len(native['adapter_controls'])==7 and native['backend_priority_cases']==7")
    text=text.replace("'actual_adapter_contracts':6","'actual_adapter_contracts':7").replace("'planned_round':140","'planned_round':141")
    text=text.replace('full140','full141').replace('QA51','QA52').replace('第140轮','第141轮')
    text=text.replace("'old_hook_scope_failure_and_original_sources_preserved':True,'legacy_five_adapter_or18_36_print_text_does_not_override_actual6_and24_48_evidence':True,", "'original_numerical_probe_and_bank_path_failures_preserved_in_prior_main_receipts':True,'actual_seven_adapter_contracts':True,")
    marker='def main():\n';assert text.count(marker)==1
    text=text.replace(marker,"def main():\n    prior=A/'service_owned_workflows_20261006/KrylovGram141_causal_preflight_main_publication_v1_20261008'\n    while owned(read(prior/'native_launch.json')):time.sleep(10)\n    assert read(prior/'service_execution.json')['status']=='passed'\n")
    target=A/'publish_KrylovGram141_historical_causal_v1_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    files=[Path(__file__),source,target,A/'actual_optimization_handoff_v12_20261008.json',A/'KrylovGram52_round141_plan_v1_20261008.json']
    pins={str(p):sha(p) for p in files}
    create(A/'KrylovGram141_historical_publisher_preparation_v2_20261008.json',{
        'status':'prepared_serial_main_export_after_actual49_147_24_24_24_48_controls','input_sha256':pins,
        'official_scores':0,'test_labels_read':False})
    row=start('KrylovGram141_historical_causal_main_publication_v1_20261008',target.name,[],pins)
    create(A/'actual_KrylovGram141_historical_causal_main_hidden_launch_v1_20261008.json',row)
    print('Historical141 main export queued after prior causal publication and actual proofs close.',flush=True)

if __name__=='__main__':main()
