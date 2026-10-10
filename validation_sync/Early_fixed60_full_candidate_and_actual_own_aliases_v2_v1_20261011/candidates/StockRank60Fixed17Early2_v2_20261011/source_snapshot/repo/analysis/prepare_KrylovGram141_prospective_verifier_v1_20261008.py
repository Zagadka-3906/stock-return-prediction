"""Prepare the independently executed24 source/1029 graph control receiver for141."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from prepare_KrylovGram141_parent_set_recovery_v2_20261008 import adapt

def main():
    source=A/'verify_SpectralGram52_prospective_routes_v3_20261008.py';text=adapt(source.read_text(encoding='utf8'))
    marker="'BF16_reverse_complete_parent_rank_CDF','nonflag_CPU_HuberCrossFamily_complete_parent_CDF'):"
    assert text.count(marker)==1
    text=text.replace(marker,"'BF16_reverse_complete_parent_rank_CDF','nonflag_CPU_HuberCrossFamily_complete_parent_CDF','nonflag_CPU_SpectralGram64_complete_parent_CDF'):")
    text=text.replace('actual25 existing native heads','actual20 existing native heads')
    text=text.replace("create(A/'KrylovGram141_receiver_preparation_v2_20261008.json',{'status':'passed_complete139_receivers_before_quality'",
        "create(A/'KrylovGram141_receiver_preparation_v2_20261008.json',{'status':'passed_complete141_receivers_before_quality'")
    marker="    create(proof_path,{'status':";assert text.count(marker)==1
    text=text.replace(marker,"    assert len(graphs)==1029 and len(baselines)==9 and len(sorts)==6 and len(model_counts)==8\n"+marker)
    target=A/'verify_KrylovGram52_prospective_routes_v1_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'KrylovGram141_prospective_verifier_preparation_v1_20261008.json',{
        'status':'prepared_independent24_source1029_graph_verifier_before_quality','input_sha256':{str(p):sha(p) for p in [Path(__file__),source,target]},
        'new_official_scores':0,'test_labels_read':False})
    print('Prospective141 verifier prepared with seven parent graph families and correct declared counts.',flush=True)

if __name__=='__main__':main()
