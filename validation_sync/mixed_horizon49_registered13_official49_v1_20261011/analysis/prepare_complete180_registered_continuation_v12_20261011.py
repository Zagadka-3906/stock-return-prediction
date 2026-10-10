"""Continue registered180 after its missing unversioned import, without replaying registration."""
from pathlib import Path
import sys,importlib,re,subprocess,time,psutil
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
from prepare_actual_candidate_closed180_continuation_v10_20261011 import DESCRIPTORS
PROOF=A/'complete180_registered_continuation_routes_v12_20261011.json'
def save(name,text):
    p=A/name;assert not p.exists(),p;compile(text,str(p),'exec');p.write_text(text,encoding='utf8',newline='\n');return p
def main():
    assert allowed();old=read(A/'reboot_complete_candidate_routes_v11_20261011.json');aliases=dict(old['service_aliases']);wrappers={};tasks=[];idle=[];sources=[Path(__file__),A/'reboot_complete_candidate_routes_v11_20261011.json']
    failure=A/'optimization_20261003_r180/full_registration_failure.json';assert 'optimize_training_round180' in read(failure)['error'];sources.append(failure)
    original=A/'run_StockRank20Embedding180_full_registration_v5_20261010_reboot_services_v11.py';text=original.read_text(encoding='utf8')
    text=text.replace('    protocol=register();folder=',"    protocol=read(A/'optimization_20261003_r180/protocol.json');folder=")
    text=text.replace("    pins=protocol['input_sha256']","    pins={**protocol['input_sha256'],**read(A/'complete180_registered_continuation_routes_v12_20261011.json')['input_sha256']}")
    for stem in ['frozen_before_actual_full_registration','actual_main7_idle_before_and_after_hold','full_registration_failure','actual_hidden_registration_children']:
        text=text.replace(stem+'.json',stem+'_registered_continuation_v12.json')
    rootdriver=save('run_StockRank20Embedding180_full_registration_registered_continuation_v12_20261011.py',text);sources.extend([original,rootdriver])
    def setalias(previous,actual):
        for key,value in list(aliases.items()):
            if key==previous or value==previous:aliases[key]=actual
        aliases[previous]=actual
    rootold=old['service_aliases']['StockRank20Embedding180_complete48_family_v6_20261010']
    rootnew='StockRank20Embedding180_complete48_registered_continuation_v12_20261011';setalias(rootold,rootnew)
    rootreg=old['service_aliases']['StockRank20Embedding180_round180_full_registration_v1_20261010'];regnew='StockRank20Embedding180_round180_registered_continuation_v12_20261011';setalias(rootreg,regnew)
    factories=old['source_factories'];aliasfiles=[]
    for factoryname in factories:
        f=importlib.import_module(factoryname)
        for filename in f.NAMES:
            canonical=re.sub(r'_v\d+(?=\.py$)','',filename)
            if canonical!=filename:
                source=A/filename;target=A/canonical
                if not target.exists():target.write_bytes(source.read_bytes());assert sha(target)==sha(source);aliasfiles.append({'source':str(source),'target':str(target),'sha256':sha(source)})
                sources.extend([source,target])
    for previous,driver in old['remaining_tasks'][2:-1]:
        actual=previous.replace('reboot11_','registered12_',1);setalias(previous,actual);tasks.append((actual,driver))
        folder=A/'service_owned_workflows_20261006'/previous;row=read(folder/'native_launch.json')
        if owned(row):
            assert not psutil.Process(row['owned_worker_pid']).children()
            stack=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],check=True,capture_output=True,text=True,encoding='utf8').stdout
            assert '(idle)' in stack and any(s in stack for s in ['closed','main (run_','main (qualify_','main (normalize_']),stack
            idle.append({'identity':row,'stack':stack})
        else:assert read(folder/'service_execution.json')['status']=='failed',previous
    # Rebind exact candidate child service names, retaining the completed180 candidate and sealer.
    for key,value in list(aliases.items()):
        if value.startswith('reboot11_') and any(s in value for s in ['selected_candidate_preparation','selected_candidate_sealing','_full_registration_']) and 'Embedding180_' not in value:
            setalias(value,value.replace('reboot11_','registered12_',1))
    replacements={key:value for key,value in aliases.items() if key.startswith('reboot11_')}
    pattern=re.compile(r'(?<![A-Za-z0-9_])('+'|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
    originals=list(dict.fromkeys([driver for number,name,norm,qual,family in DESCRIPTORS for driver in [*importlib.import_module(name).EXTRAS[:2],*importlib.import_module(name).EXTRAS[3:9]]]))
    for driver in originals:
        executed=driver;oldwrapper=old['driver_wrappers'][driver]
        if driver.startswith('seal_') or '_full_registration_' in driver:
            prior=A/(Path(driver).stem+'_reboot_services_v11.py');assert prior.exists()
            executed=Path(driver).stem+'_registered_services_v12.py';sources.append(save(executed,pattern.sub(lambda m:replacements[m.group()],prior.read_text(encoding='utf8'))));sources.append(prior)
        name=Path(driver).stem+'_registered_wrapper_v12.py'
        sources.append(save(name,"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_complete_registered180_v12_20261011 import execute\nif __name__=='__main__':execute("+repr(executed)+")\n"));wrappers[driver]=name;wrappers[oldwrapper]=name;sources.append(A/driver)
    brokertext=(A/'route_reboot_complete_candidate_v11_20261011.py').read_text(encoding='utf8').replace('reboot_complete_candidate_routes_v11_20261011.json','complete180_registered_continuation_routes_v12_20261011.json').replace('import route_actual_candidate_closed_and180_continuation_v10_20261011 as old','import route_reboot_complete_candidate_v11_20261011 as old')
    sources.append(save('route_complete_registered180_v12_20261011.py',brokertext))
    rootwrapper=save('run_registered180_continuation_wrapper_v12_20261011.py',"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_complete_registered180_v12_20261011 import execute\nif __name__=='__main__':execute('run_StockRank20Embedding180_full_registration_registered_continuation_v12_20261011.py')\n");sources.append(rootwrapper)
    controller=save('resume_registered180_complete_main_v12_20261011.py',"from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_complete_registered180_v12_20261011 import installed,PROOF\nfrom run_dependency_queue_v3_20261006 import read,sha,create\nfrom prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed\ndef main():\n assert allowed();closed,start=installed();row=start("+repr(regnew)+",'run_registered180_continuation_wrapper_v12_20261011.py',[],{str(PROOF):sha(PROOF)});closed("+repr(regnew)+")\n from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update\n assert allowed();update();create(A/'registered180_continuation_passed_v12_20261011.json',{'status':'passed_actual48_QA91_main_registered_continuation','receipt':read(A/'github_validation_sync_main_20261005/round180_receipt.json'),'new_model_fits':0,'new_quality_scores':0})\nif __name__=='__main__':main()\n");sources.append(controller)
    tasks.insert(0,(rootnew,controller.name))
    create(PROOF,{'status':'verified_missing_unversioned_import_aliases_and180_registered_continuation','input_sha256':{str(p):sha(p) for p in dict.fromkeys(sources)},'service_aliases':aliases,'driver_wrappers':wrappers,'source_factories':factories,'remaining_tasks':tasks,'byte_identical_new_import_aliases':aliasfiles,'verified_idle_helpers':idle,'new_model_fits':0,'new_quality_scores':0,'original_registered180_and_failure_preserved':True})
    for item in idle:assert allowed();retire(item['identity'],'Verified childless idle helper rebound after180 missing import; scientific outputs had not begun')
    for name,driver in tasks:
        assert allowed();driver=wrappers.get(driver,driver);row=start_service(name,driver,[],{str(PROOF):sha(PROOF),str(A/driver):sha(A/driver)});create(A/(name+'_activation.json'),row)
    print({'actual_registered180_and_downstream_started':len(tasks),'new_exact_import_aliases':len(aliasfiles),'new_fits':0,'new_scores':0},flush=True)
if __name__=='__main__':main()
