"""Preserve failed old135 gate; start fresh exact current-parent control for next already-trained family."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    source=A/'verify_CrossFamily91_current_parent_v1_20261008.py';value=source.read_text(encoding='utf8')
    assert value.count('BF16wide40_round135_full_registration_v4_20261008')==1
    value=value.replace('BF16wide40_round135_full_registration_v4_20261008','BF16wide40_round135_full_registration_v7_20261008')
    for stem in ('CrossFamily91_current_parent','CrossFamily91_current_parent_full','actual_CrossFamily91_current_parent_location','actual_CrossFamily91_current_parent_full_location'):
        value=value.replace(stem+'_v1_20261008',stem+'_v2_20261008')
    target=A/'verify_CrossFamily91_current_parent_v2_20261008.py';assert not target.exists();compile(value,str(target),'exec');target.write_text(value,encoding='utf8',newline='\n')
    create(A/'CrossFamily91_current_parent_gate_recovery_v2_20261008.json',{'status':'frozen_fresh_next_family_current_parent_control_after_exact135_main_registration','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,target]},'old_failed_gate_and_controls_preserved':True,'native_fits_and_CDF_math_and_anchor_grid_unchanged':True,'new_quality_scores':0})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('CrossFamily91_current_parent_controls_v2_20261008',target.name,[],{str(target):sha(target)})
    create(A/'CrossFamily91_current_parent_hidden_launch_v2_20261008.json',row)
    print(row['owned_worker_pid'],flush=True)
if __name__=='__main__':main()
