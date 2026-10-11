"""Keep the original source publication and route remaining stages to the real restart recovery."""
from pathlib import Path
import sys,time,runpy
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import retire
def main():
    receipt=A/'StockRank20Seed10_objective_sources_main_receipt_v1_20261010.json'
    while not receipt.exists(): assert allowed();time.sleep(15)
    assert read(receipt)['status']=='pushed_and_remote_head_verified'
    old=A/'service_owned_workflows_20261006/actual_StockRank20Seed10_objective_stages_main_v1_20261010/native_launch.json'
    row=read(old)
    import psutil,subprocess
    assert owned(row) and not psutil.Process(row['owned_worker_pid']).children()
    spy=A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'
    result=subprocess.run([str(spy),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,encoding='utf8',check=True)
    assert 'closed (prepare_protected_tail_pilot76_and_selected_native14_v1_20261010.py:' in result.stdout
    create(A/'seed10_remaining_publication_exact_idle_evidence_v2_20261010.json',{'status':'verified_original_sources_main_completed_then_idle_wait_on_superseded_restart','receipt':read(receipt),'stack':result.stdout,'new_quality_scores':0})
    source=A/'publish_stock_rank20seed10_objective_stages_main_v1_20261010.py'
    text=source.read_text(encoding='utf8')
    assert text.count("('sources',()),")==1;text=text.replace("('sources',()),",'')
    text=text.replace('actual_stock_rank20seed10_embedding_small512_restart_v1_20261010','actual_stock_rank20seed10_embedding_small512_restart_actual_fixture_v2_20261010')
    marker="paths=[Path(__file__),template,ROOT/'后续选模标准.md'";assert marker in text
    text=text.replace(marker,"paths=[Path(__file__),A/'recover_seed10_actual_fixture_dependency_v2_20261010.py',A/'seed10_actual_fixture_dependency_recovery_sources_v2_20261010.json',template,ROOT/'后续选模标准.md'")
    driver=A/'publish_stock_rank20seed10_remaining_actual_stages_main_v2_20261010.py'
    assert not driver.exists();compile(text,str(driver),'exec');driver.write_text(text,encoding='utf8',newline='\n')
    retire(row,'Actual source publication passed; verified childless idle on superseded restart. Remaining actual stages routed to recovery2.')
    assert allowed();runpy.run_path(str(driver),run_name='__main__')
if __name__=='__main__':main()
