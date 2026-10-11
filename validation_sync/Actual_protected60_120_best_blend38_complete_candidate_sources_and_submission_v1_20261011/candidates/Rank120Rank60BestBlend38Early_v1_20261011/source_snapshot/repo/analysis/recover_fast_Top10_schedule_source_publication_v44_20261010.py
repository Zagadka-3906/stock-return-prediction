"""Correct a metadata inventory filename before any Git staging; retain failed receipt."""
from pathlib import Path
import ast,sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    assert allowed()
    oldservice=A/'service_owned_workflows_20261006/actual_fast_Top10_schedule_and_large29_main_v43_20261010'
    assert read(oldservice/'service_execution.json')['status']=='failed' and not owned(read(oldservice/'native_launch.json'))
    assert not Path('E:/赛题五_本机临时/StockTop10Embedding_verified_BCE_loss_and_runtime_main_v43_20261010').exists()
    old=A/'publish_fast_Top10_schedule_and_large29_actual_main_v43_20261010.py'
    text=old.read_text(encoding='utf8')
    wrong='publish_stock_top10_verified_loss_and_runtime_main_v43_20261010.py'
    assert text.count(wrong)==1
    text=text.replace(wrong,'publish_stock_top10_verified_loss_and_runtime_main_v42_20261010.py')
    driver=A/'publish_fast_Top10_schedule_and_large29_actual_main_v44_20261010.py'
    assert not driver.exists();compile(text,str(driver),'exec')
    tree=ast.parse(text);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    assignment=next(n for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
    paths=[Path(p) for p in ast.literal_eval(assignment.value)];assert all(p.exists() for p in paths)
    driver.write_text(text,encoding='utf8',newline='\n')
    proof=A/'fast_Top10_schedule_main_metadata_inventory_recovery_v44_20261010.json'
    create(proof,{'status':'verified_exact_existing_source_inventory_before_any_Git_staging_failed43_preserved','input_sha256':{str(p):sha(p) for p in (Path(__file__),old,driver,oldservice/'service_execution.json')},'all_inventory_files_exist':True,'output_namespace_retained':'verified_BCE_loss_and_runtime_main_v43','scientific_sources_changed':False,'validation_restarted':False})
    row=start_service('actual_fast_Top10_schedule_and_large29_main_v44_20261010',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/'actual_fast_Top10_schedule_and_large29_main_activation_v44_20261010.json',row);print({'worker':row['owned_worker_pid'],'corrected_existing_inventory':True},flush=True)
if __name__=='__main__':main()
