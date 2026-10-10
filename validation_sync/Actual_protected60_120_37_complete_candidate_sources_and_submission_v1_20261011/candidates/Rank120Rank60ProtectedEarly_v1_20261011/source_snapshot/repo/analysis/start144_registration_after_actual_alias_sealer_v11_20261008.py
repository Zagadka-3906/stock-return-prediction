from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,read,create
def main():
    source=A/'run_ConeRidgeAlpha100_round144_full_registration_v10_20261008.py';value=source.read_text(encoding='utf8')
    assert "'ConeRidgeAlpha100_selected_candidate_sealing_v8_20261008'" in value
    value=value.replace('ConeRidgeAlpha100_selected_candidate_sealing_v8_20261008','ConeRidgeAlpha100_selected_candidate_sealing_v9_20261008').replace('actual_registration_v10_20261008','actual_registration_v11_20261008').replace('full_registration_v10_file_IO_20261008','full_registration_v11_file_IO_20261008')
    needle='    connected_generator.source_paths=actual_windows_paths';assert value.count(needle)==1
    value=value.replace(needle,needle+"\n    previous_actual_paths=connected_generator.source_paths\n    def actual_current_registration_paths():return list(dict.fromkeys([*previous_actual_paths(),Path(__file__),A/'start144_registration_after_actual_alias_sealer_v11_20261008.py']))\n    connected_generator.source_paths=actual_current_registration_paths")
    target=A/'run_ConeRidgeAlpha100_round144_full_registration_v11_20261008.py';assert not target.exists();compile(value,str(target),'exec');target.write_text(value,encoding='utf8',newline='\n')
    create(A/'actual144_alias_sealer_registration_binding_v11_20261008.json',{'status':'frozen_correct_actual_live_sealer9_dependency_before_registration','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,target]},'old_failed_registration10_preserved':True,'new_quality_scores':0})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('ConeRidgeAlpha100_round144_full_registration_v11_20261008',target.name,[],{str(target):sha(target)})
    create(A/'actual144_alias_sealer_registration_launch_v11_20261008.json',row)
    print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
