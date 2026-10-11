"""Preserve passed inference/seal; resume registration and failed dependency helpers through real identities."""
from pathlib import Path
import sys,re,ast,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
def original_driver(path):
    tree=ast.parse(path.read_text(encoding='utf8'));calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='execute']
    return ast.literal_eval(calls[0].args[0]) if len(calls)==1 else path.name
def main():
    assert allowed();oldpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v6_20261010.json';old=read(oldpath)
    for p,d in old['input_sha256'].items():assert sha(p)==d,p
    seal='StockTop10Embedding175_selected_candidate_sealing_recovery_v2_20261010'
    assert read(A/'service_owned_workflows_20261006'/seal/'service_execution.json')['status']=='passed'
    parentold=old['service_aliases']['StockTop10Embedding175_complete47_family_v3_20261010']
    parentnew='StockTop10Embedding175_verified_registration_completion_recovery_v7_20261010'
    aliases=dict(old['service_aliases']);aliases[parentold]=parentnew;aliases['StockTop10Embedding175_selected_candidate_sealing_v1_20261010']=seal
    aliases['actual_stock_top10_embedding_after174_large_allocation29_completion_main_v72_20261010']='actual_stock_top10_embedding_after174_large_allocation29_completion_main_v80_20261010'
    jobs={};idle=[];folderbase=A/'service_owned_workflows_20261006'
    # All failures are real downstream dependency failures since seal175 failed.
    for folder in folderbase.iterdir():
        terminal=folder/'service_execution.json'
        if not terminal.exists():continue
        result=read(terminal)
        if result.get('status')!='failed' or result.get('at_local','')<'2026-10-10T22:20:00':continue
        if not result.get('failure','').startswith('AssertionError:'):continue
        name=folder.name
        if name==parentold:continue
        definition=read(folder/'job_definition.json');driver=original_driver(Path(definition['driver']))
        if not any(key in name for key in ('StockTop10Embedding','StockRank','StockForward','actual_stock_rank','actual_stock_forward','actual_stock_top10')):continue
        # Never rerun scientific score files. Only unexecuted dependent helpers,
        # or the after175 tight screen which failed before its output existed.
        if 'screen' in name:assert 'after175_tiny_CDF41' in name
        new=name.removesuffix('_20261010')+'_after_verified_seal_v7_20261010';aliases[name]=new;jobs[name]={'new':new,'driver':driver,'arguments':definition['arguments'],'definition':definition}
    # A still-idle after175 screen must be redirected before its obsolete parent
    # is checked; source publication resumes past its already published sources.
    for name in ('actual_stock_rank20_embedding_after175_tiny_CDF41_screen_v1_20261010','actual_rank20_tinyCDF82_stages_main_v68_20261010'):
        folder=folderbase/name
        if not (folder/'native_launch.json').exists():continue
        row=read(folder/'native_launch.json')
        if not owned(row):continue
        dump=subprocess.run([str(ROOT/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(row['owned_worker_pid'])],capture_output=True,text=True,check=True).stdout
        assert '(idle)' in dump and '    closed (' in dump,name
        definition=read(folder/'job_definition.json');driver=Path(definition['driver']).name
        if name=='actual_rank20_tinyCDF82_stages_main_v68_20261010':
            fresh=A/'publish_rank20_tinyCDF82_remaining_stages_main_v72_20261010.py';text=(A/driver).read_text(encoding='utf8');needle="[('sources',None,68),('after174',174,69),('after175',175,70)]";assert text.count(needle)==1
            text=text.replace(needle,"[('after174',174,69),('after175',175,70)]");assert not fresh.exists();compile(text,str(fresh),'exec');fresh.write_text(text,encoding='utf8',newline='\n');driver=fresh.name
        new=name.removesuffix('_20261010')+'_after_verified_seal_v7_20261010';aliases[name]=new;jobs[name]={'new':new,'driver':driver,'arguments':definition['arguments'],'definition':definition};idle.append({'row':row,'actual_idle_stack':dump})
    def resolve(name):
        seen=set()
        while name in aliases and aliases[name]!=name:
            assert name not in seen;seen.add(name);name=aliases[name]
        return name
    aliases={k:resolve(v) for k,v in aliases.items()}
    originals={original_driver(A/name) for name in old['driver_wrappers'].values()}|{item['driver'] for item in jobs.values()}
    for number,kind,version,sealer,cache in [(182,'StockRank20Embedding',5,2,6),(183,'StockRank20Embedding',5,2,6)]:
        originals.update([f'prepare_{kind}{number}_selected_candidate_v{version}_20261010.py',f'seal_{kind}{number}_selected_candidate_v{sealer}_20261010.py',f'run_{kind}{number}_full_registration_v{version}_20261010.py',f'run_{kind}{number}_selected_candidate_feature_cache_v{cache}_20261010.py'])
    proofpath=A/'Dual25_verified_recovery_exact_dependency_aliases_v7_20261010.json';broker=A/'route_verified_Dual25_recovery_dependencies_v7_20261010.py'
    text=(A/'route_verified_Dual25_recovery_dependencies_v6_20261010.py').read_text(encoding='utf8').replace('Dual25_verified_recovery_exact_dependency_aliases_v6','Dual25_verified_recovery_exact_dependency_aliases_v7')
    needle="    if driver.startswith('run_') and '_full_registration_' in driver:";assert text.count(needle)==1
    text=text.replace(needle,"    if driver.startswith('seal_') or (driver.startswith('run_') and '_full_registration_' in driver):")
    assert not broker.exists();compile(text,str(broker),'exec');broker.write_text(text,encoding='utf8',newline='\n')
    drivers={};wrappers=[]
    for source in sorted(originals):
        path=A/(Path(source).stem+'_after_verified_seal_routes_v7.py');assert not path.exists()
        text="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified_Dual25_recovery_dependencies_v7_20261010 import execute\nif __name__=='__main__':execute("+repr(source)+")\n"
        compile(text,str(path),'exec');path.write_text(text,encoding='utf8',newline='\n');drivers[source]=path.name;wrappers.append(path)
    for key,name in old['driver_wrappers'].items():drivers[key]=drivers[original_driver(A/name)];drivers[name]=drivers[original_driver(A/name)]
    runtime='run_StockTop10Embedding175_full_registration_v3_20261010.py';assert (A/runtime).exists()
    completion=A/'finish_StockTop10Embedding175_verified_registration_recovery_v7_20261010.py'
    text='''from pathlib import Path
import sys
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service
def main():
    from route_verified_Dual25_recovery_dependencies_v7_20261010 import installed
    installed()
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import closed
    assert allowed();closed('StockTop10Embedding175_selected_candidate_sealing_v1_20261010')
    driver='run_StockTop10Embedding175_full_registration_v3_20261010_after_verified_seal_routes_v7.py'
    name='StockTop10Embedding175_verified_full_registration_recovery_v7_20261010'
    row=start_service(name,driver,[],{str(A/driver):sha(A/driver)});create(A/(name+'_activation.json'),row);closed(name)
    receipt=read(A/'github_validation_sync_main_20261005/round175_receipt.json');assert receipt['status']=='pushed_and_remote_head_verified' and receipt['scored_records']==47
    assert read(A/'optimization_20261003_r175/full_registration_execution.json')['status']=='passed'
    from maintain_best_fully_qualified_submission_delivery_v3_20261010 import update
    update()
    create(A/'StockTop10Embedding175_verified_completion_recovery_v7_20261010.json',{'status':'passed_verified_inference_and_seal_preserved_full47_QA86_main_delivery','receipt':receipt,'new_inference':0,'new_fits':0,'new_scores':0})
if __name__=='__main__':main()
'''
    assert not completion.exists();compile(text,str(completion),'exec');completion.write_text(text,encoding='utf8',newline='\n')
    paths=[Path(__file__),oldpath,broker,completion,*wrappers,*[A/n for n in originals],A/'Top175_verified_inference_sealing_recovery_v2_20261010.json',folderbase/seal/'service_execution.json']
    factories=[*old['source_factories'],'prepare_StockRank20Complement182_complete63_pipeline_v1_20261010','prepare_StockRank20Tiny183_complete85_pipeline_v1_20261010']
    create(proofpath,{'status':'compiled_preserved_actual175_inference_and_seal_recovery_all_downstream_failures_and_sealers_original_storage_main_context_before_dispatch','service_aliases':aliases,'driver_wrappers':drivers,'source_factories':factories,'selected_helpers':[{'old':name,'new':item['new'],'driver':item['driver']} for name,item in jobs.items()],'input_sha256':{str(p):sha(p) for p in paths},'actual175_seal':seal,'actual175_completion':parentnew,'new_fits':0,'new_quality_scores':0,'new_inference':0,'original_failed_states_preserved':True,'test_labels_read':False})
    for item in idle:retire(item['row'],'Replace only verified idle unexecuted after175 tight screen/publisher following actual passed175 inference and recovered seal; no scientific scores or inference restarted.')
    for name,driver in [(parentnew,completion.name),*[(item['new'],drivers[item['driver']]) for item in jobs.values()]]:
        assert allowed();row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(proofpath):sha(proofpath)});create(A/(name+'_activation.json'),row)
    print({'preserved_actual175_inference_and_seal':True,'new_downstream_helpers':len(jobs),'broker_sealers_preserve_storage_main_context':True,'new_inference':0},flush=True)
if __name__=='__main__':main()
