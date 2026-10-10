"""Bind the preflight to the actual175 storage assertion, before exclusive outputs."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def save(name,text):
    p=A/name;assert not p.exists();compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();import psutil
    folder=A/'service_owned_workflows_20261006/StockTop10Embedding175_complete47_family_v1_20261010';row=read(folder/'native_launch.json')
    assert owned(row) and not psutil.Process(row['owned_worker_pid']).children()
    assert not (A/'StockTop10Embedding175_complete_family_v1_20261010').exists()
    oldpre=A/'verify_StockTop10Embedding175_full47_preflight_v1_20261010.py';text=oldpre.read_text(encoding='utf8')
    assert text.count("'assert number == 173'")==1
    text=text.replace("'assert number == 173'","'assert number == 175'")
    replacements={'run_StockTop10Embedding175_complete_family_v1_20261010':'run_StockTop10Embedding175_complete_family_v2_20261010','run_StockTop10Embedding175_full_registration_v1_20261010':'run_StockTop10Embedding175_full_registration_v2_20261010','verify_StockTop10Embedding175_full47_preflight_v1_20261010':'verify_StockTop10Embedding175_full47_preflight_v2_20261010','stock_top10_embedding175_full_family_preflight_v1_20261010':'stock_top10_embedding175_full_family_preflight_v2_20261010'}
    def current(t):
        for old,new in replacements.items():t=t.replace(old,new)
        return t
    preflight=save('verify_StockTop10Embedding175_full47_preflight_v2_20261010.py',current(text))
    outputs=[preflight];inputs=[oldpre]
    for old,new in [('run_StockTop10Embedding175_complete_family_v1_20261010.py','run_StockTop10Embedding175_complete_family_v2_20261010.py'),('run_StockTop10Embedding175_full_registration_v1_20261010.py','run_StockTop10Embedding175_full_registration_v2_20261010.py')]:
        source=A/old;inputs.append(source);outputs.append(save(new,current(source.read_text(encoding='utf8'))))
    import stock_top10_embedding175_storage_v1_20261010 as storage
    assert len(storage.OUTPUTS)==6 and 'assert number == 175' in Path(storage.__file__).read_text(encoding='utf8')
    assert all(not p.exists() and not q.exists() for p,q in storage.OUTPUTS.items())
    for p in outputs:importlib.import_module(p.stem)
    proof=A/'stock_top10_embedding175_full_execution_sources_admission_v2_20261010.json'
    create(proof,{'status':'compiled_actual47_family2_preflight2_runtime2_exact175_storage_and_existing_inventory_before_future_dispatch','input_sha256':{str(p):sha(p) for p in [Path(__file__),*inputs,*outputs,Path(storage.__file__),A/'stock_top10_embedding175_full_execution_sources_admission_v1_20261010.json']},'expected_records':47,'expected_full_board':16839,'scientific_parameters_changed':False,'new_fits':0,'new_quality_scores':0,'test_labels_read':False})
    retire(row,'Verified childless before47 qualifier completion and all exclusive outputs. Storage preflight literal corrected from173 to actual175; scientific cases unchanged.')
    driver=A/'run_StockTop10Embedding175_complete_family_v2_20261010.py';row=start_service('StockTop10Embedding175_complete47_family_v2_20261010',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof)})
    create(A/'actual_StockTop10Embedding175_complete47_family_activation_v2_20261010.json',row)
    print({'actual_full175_pipeline_version':2,'exact_storage_scalar':175,'actual_future_dispatch_not_started':True},flush=True)
if __name__=='__main__':main()
