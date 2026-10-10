"""Recover the exact idle seed10 startup dependency without relabeling an old GPU proof."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed()
    oldname='actual_stock_rank20seed10_embedding_small512_restart_v1_20261010'
    newname='actual_stock_rank20seed10_embedding_small512_restart_actual_fixture_v2_20261010'
    nativeprep=A/'stock_rank20seed10_embedding_own64_native_sources_preparation_v1_20261010.json'
    admission=A/'stock_rank20seed10_embedding_own64_controls46_sources_admission_v1_20261010.json'
    create(nativeprep,read(admission));assert sha(nativeprep)==sha(admission)
    paths=[]
    for original,new in [
        ('verify_stock_rank20seed10_embedding_small512_restart_v1_20261010.py','verify_stock_rank20seed10_embedding_small512_restart_actual_fixture_v2_20261010.py'),
        ('verify_stock_rank20seed10_embedding_small512_small_CPU_v1_20261010.py','verify_stock_rank20seed10_embedding_small512_small_CPU_v2_20261010.py'),
        ('train_stock_rank20seed10_embedding_small512_BF16_bank6_own64_v1_20261010.py','train_stock_rank20seed10_embedding_small512_BF16_bank6_own64_v2_20261010.py')]:
        source=A/original;text=source.read_text(encoding='utf8').replace(oldname,newname)
        text=text.replace("closed('StockRank20Seed10Embedding_actual_mature_fixture_CPU_v1_20261010')","closed('StockRank20Embedding_actual_mature_fixture_CPU_v1_20261010')")
        paths += [source,save(new,text)]
    proof=A/'seed10_actual_fixture_dependency_recovery_sources_v2_20261010.json'
    create(proof,{'status':'compiled_explicit_actual_shared_fixture_dependency_recovery_before_any_new_training',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*paths,nativeprep,admission]},
        'retired_idle_restart':oldname,'actual_restart_service':newname,'new_fits':0,'new_quality_scores':0,
        'unchanged_actual_fixture_explicitly_reused':True,'old_seed_GPU_restart_not_reused':True,'test_labels_read':False})
    oldqueue=A/'run_stock_rank20seed10_embedding_own64_controls46_queue_v1_20261010.py'
    text=oldqueue.read_text(encoding='utf8').replace(oldname,newname)
    text=text.replace('verify_stock_rank20seed10_embedding_small512_restart_v1_20261010.py',paths[1].name)
    text=text.replace('verify_stock_rank20seed10_embedding_small512_small_CPU_v1_20261010.py',paths[3].name)
    text=text.replace('train_stock_rank20seed10_embedding_small512_BF16_bank6_own64_v1_20261010.py',paths[5].name)
    text=text.replace("    assert allowed()\n", "    assert allowed()\n    old=A/'service_owned_workflows_20261006/actual_stock_rank20seed10_embedding_own64_controls46_queue_v1_20261010/service_execution.json'\n    while not old.exists(): assert allowed();time.sleep(2)\n    assert read(old)['status']=='failed'\n",1)
    driver=save('run_stock_rank20seed10_embedding_own64_controls46_queue_v2_20261010.py',text)
    retire(read(A/'service_owned_workflows_20261006'/oldname/'native_launch.json'),
        'Verified idle closed() on nonexistent renamed shared-fixture service; no GPU phase or output existed')
    assert allowed();row=start_service('actual_stock_rank20seed10_embedding_own64_controls46_queue_v2_20261010',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/'actual_stock_rank20seed10_embedding_own64_controls46_queue_v2_20261010_activation.json',row)
    print({'recovery2':'queued','old_original_status_preserved':True,'new_actual_GPU_restart_required':True},flush=True)
if __name__=='__main__':main()
