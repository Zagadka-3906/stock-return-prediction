"""Execute seven actual adapter contracts and prepare24 historical multi-year native checks."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def main():
    source=A/'prepare_SpectralGram140_native_preflight_v1_20261008.py'
    text=source.read_text(encoding='utf8').replace('SpectralGram','KrylovGram').replace('KrylovGram52_round140','KrylovGram52_round141').replace('KrylovGram140_','KrylovGram141_')
    marker="('BF16_reverse_complete_parent_rank_CDF','ReverseBF16'),('nonflag_CPU_HuberCrossFamily_complete_parent_CDF','HuberCrossFamily')]"
    assert text.count(marker)==1
    text=text.replace(marker,"('BF16_reverse_complete_parent_rank_CDF','ReverseBF16'),('nonflag_CPU_HuberCrossFamily_complete_parent_CDF','HuberCrossFamily'),('nonflag_CPU_SpectralGram64_complete_parent_CDF','SpectralGram64')]")
    text=text.replace("'backend_priority_cases':6","'backend_priority_cases':7")
    text=text.replace('passed_five_actual_inserted_adapter_contracts','passed_seven_actual_inserted_adapter_contracts')
    text=text.replace('Five adapter contracts passed; actual18/36 historical calendar controls started.','Seven adapter contracts passed; actual24/48 historical calendar controls started.')
    target=A/'prepare_KrylovGram141_native_preflight_actual_v1_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    namespace={'__file__':str(target),'__name__':'actual_KrylovGram141_native_preflight'}
    exec(compile(text,str(target),'exec'),namespace);namespace['main']()
    create(A/'KrylovGram141_native_preflight_lineage_v1_20261008.json',{'status':'passed_seven_native_adapter_contracts_and_calendar_receiver_preparation',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,target]},'new_official_scores':0,'test_labels_read':False})

if __name__=='__main__':main()
