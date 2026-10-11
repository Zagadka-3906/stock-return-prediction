"""Upload the six actual population/tensor controls using the established verified main-only transport."""
from pathlib import Path
import sys,re
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed();template=A/'publish_StockRank20_actual_own6_full5_main_v66_20261010.py'
    proof=A/'rank20_two_seed_actual_six_population_and_weights_CPU_v1_20261010.json'
    assert read(proof)['actual_completed_physical_models']==12
    paths=[Path(__file__),template,proof,A/'verify_rank20_two_seed_actual_six_population_and_weights_CPU_v1_20261010.py',ROOT/'后续选模标准.md']
    text=template.read_text(encoding='utf8')
    start=text.index('    paths=');end=text.index('    import publish_classifier_consensus_workflows_20261006 as h',start)
    text=text[:start]+'    paths=[Path(__file__),*[Path(p) for p in '+repr([str(p) for p in paths])+']]\n'+text[end:]
    text=text.replace('StockRank20_actual_own6_full5_v66_20261010','Rank20_two_seed_actual_weights_CPU_v3_20261010').replace('StockRank20_actual_own6_full5_main_v66_20261010','Rank20_two_seed_actual_weights_CPU_main_v3_20261010').replace('StockRank20_actual_own6_full5_main_receipt_v66_20261010','Rank20_two_seed_actual_weights_CPU_main_receipt_v3_20261010')
    start=text.index("    payload[(prefix/'manifest.json').as_posix()]");end=text.index('    out=Path(',start)
    manifest={'status':'actual6_equal_mature_populations_and_distinct_parameter_tensor_pairs_CPU','actual_completed_physical_models':12,
        'seeds':[20261009,20261010],'own_completed_epochs_each':64,'new_quality_scores':0,'new_native_fits_by_this_verifier':0,
        'actual_future_X_read':False,'test_labels_read':False,'submission_qualified':False}
    text=text[:start]+"    payload[(prefix/'manifest.json').as_posix()]=h.sync.encoded({**"+repr(manifest)+",'files':bindings})\n"+text[end:]
    text,count=re.subn(r"'保存实际股票身份与120维特征二十日排名目标[^']*'",repr('保存两个20日排名独立种子的六组相同成熟训练样本及实际不同参数张量CPU检查'),text);assert count==1
    driver=A/'publish_Rank20_two_seed_actual_weights_CPU_main_v3_20261010.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    assert allowed();row=start_service('actual_Rank20_two_seed_actual_weights_CPU_main_v3_20261010',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/'actual_Rank20_two_seed_actual_weights_CPU_main_v3_20261010_activation.json',row)
    print({'actual_tensor_CPU_proof_main_sync_queued':True},flush=True)
if __name__=='__main__':main()
