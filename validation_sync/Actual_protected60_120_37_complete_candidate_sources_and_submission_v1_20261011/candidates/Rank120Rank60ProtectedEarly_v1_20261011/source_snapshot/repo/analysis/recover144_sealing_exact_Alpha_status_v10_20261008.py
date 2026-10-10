"""Keep passed full native prediction bytes; repair the final metadata status literal only."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    assert read(A/'service_owned_workflows_20261006/ConeRidgeAlpha100_selected_candidate_preparation_v9_20261008/service_execution.json')['status']=='passed'
    source=A/'seal_ConeRidgeAlpha100_selected_candidate_v9_20261008.py';value=source.read_text(encoding='utf8');old='passed_actual_complete_parent_and_ConeRidge64_two_full_native_independent_replays_and_cold80';new='passed_actual_complete_parent_and_ConeRidgeAlpha8_64_two_full_native_independent_replays_and_cold80';assert value.count(old)==1
    candidate=ROOT/'candidates/ConeRidgeAlpha100_v4_20261008';proof=candidate/'ConeRidgeAlpha8_64_complete_parent_native_replay_verification.json';assert read(proof)['status']==new
    target=A/'seal_ConeRidgeAlpha100_selected_candidate_v10_20261008.py';assert not target.exists();value=value.replace(old,new);compile(value,str(target),'exec');target.write_text(value,encoding='utf8',newline='\n')
    oldreg=A/'run_ConeRidgeAlpha100_round144_full_registration_v11_20261008.py';value=oldreg.read_text(encoding='utf8').replace('ConeRidgeAlpha100_selected_candidate_sealing_v9_20261008','ConeRidgeAlpha100_selected_candidate_sealing_v10_20261008').replace('actual_registration_v11_20261008','actual_registration_v12_20261008').replace('full_registration_v11_file_IO_20261008','full_registration_v12_file_IO_20261008')
    needle='    connected_generator.source_paths=actual_current_registration_paths';assert value.count(needle)==1
    value=value.replace(needle,needle+"\n    prior_sealed_paths=connected_generator.source_paths\n    def actual_Alpha_status_paths():return list(dict.fromkeys([*prior_sealed_paths(),Path(__file__),A/'recover144_sealing_exact_Alpha_status_v10_20261008.py',A/'seal_ConeRidgeAlpha100_selected_candidate_v10_20261008.py']))\n    connected_generator.source_paths=actual_Alpha_status_paths")
    registration=A/'run_ConeRidgeAlpha100_round144_full_registration_v12_20261008.py';assert not registration.exists();compile(value,str(registration),'exec');registration.write_text(value,encoding='utf8',newline='\n')
    create(A/'actual144_Alpha_sealing_status_recovery_v10_20261008.json',{'status':'frozen_actual_passed_candidate_status_literal_only_repair_and_fresh_full_registration','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,target,oldreg,registration,proof]},'old_status_literal':old,'actual_native_proof_status':new,'new_inference_calls':0,'native_predictions_and_frozen_selection_untouched':True,'old_failed_sealer9_preserved':True})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={n:start(n,p.name,[],{str(p):sha(p)}) for n,p in [('ConeRidgeAlpha100_selected_candidate_sealing_v10_20261008',target),('ConeRidgeAlpha100_round144_full_registration_v12_20261008',registration)]}
    create(A/'actual144_Alpha_sealing_status_launches_v10_20261008.json',rows)
    print(json.dumps({'started':list(rows)},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
