"""Explicit terminal-service aliases; keep original failures, scores and scientific drivers immutable."""
from pathlib import Path
import sys,importlib,runpy,os
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
from handoff_ready_goss_full_execution_20261006 import start_service,retire
PROOF=A/'Dual25_verified_recovery_exact_dependency_aliases_v2_20261010.json'
def installed():
    proof=read(PROOF)
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    aliases=proof['service_aliases'];drivers=proof['driver_wrappers']
    import prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 as checks
    import handoff_ready_goss_full_execution_20261006 as launch
    original_closed=checks.closed;original_start=launch.start_service
    def resolve_closed(name):return original_closed(aliases.get(name,name))
    def resolved_start(name,driver,args,pins):
        extra={str(PROOF):sha(PROOF),str(Path(__file__)):sha(__file__)}
        return original_start(aliases.get(name,name),drivers.get(driver,driver),args,{**pins,**extra})
    checks.closed=resolve_closed;launch.start_service=resolved_start
    # Actual wrapper and terminal recovery evidence must be part of every newly sealed registry.
    for name in proof['source_factories']:
        module=importlib.import_module(name);original=module.source_paths
        def augmented(original=original):return list(dict.fromkeys([*original(),PROOF,Path(__file__),*[Path(p) for p in proof['input_sha256']],*[A/n for n in drivers.values()]]))
        module.source_paths=augmented
    return resolve_closed
def execute(driver):
    assert allowed();resolve_closed=installed();source=A/driver
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for i,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):os.environ[f'GIT_CONFIG_KEY_{count+i}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+i}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    if driver.startswith('run_') and '_full_registration_' in driver:
        runpy.run_path(str(source),run_name='__main__');return
    module=importlib.import_module(source.stem)
    # Some original selected-candidate/qualifier modules define their own closed().
    if hasattr(module,'closed'):module.closed=resolve_closed
    if hasattr(module,'start_service'):
        import handoff_ready_goss_full_execution_20261006 as launch
        module.start_service=launch.start_service
    module.main()
def main():
    assert allowed();closed('actual_Dual25_verified_terminal_recovery_v1_20261010')
    recovery=A/'stock_dual_embedding_actual25_terminal_pointer_recovery_v1_20261010.json';assert read(recovery)['new_quality_scores']==0
    source=A/'publish_stock_dual_embedding_after173_completion_v57_20261010.py';text=source.read_text(encoding='utf8')
    oldscreen='actual_stock_dual_embedding_after173_high_impact25_screen_v1_20261010';newscreen='actual_Dual25_verified_terminal_recovery_v1_20261010'
    text=text.replace("closed('"+oldscreen+"')","closed('"+newscreen+"')")
    position=text.index('    bank=Path(');text=text[:position]+"    paths += [A/'stock_dual_embedding_actual25_terminal_pointer_recovery_v1_20261010.json',A/'recover_actual_Dual25_terminal_location_v1_20261010.py']\n"+text[position:]
    publisher=A/'publish_stock_dual_embedding_after173_verified_recovery_completion_v76_20261010.py';assert not publisher.exists();compile(text,str(publisher),'exec');publisher.write_text(text,encoding='utf8',newline='\n')
    oldpub='actual_stock_dual_embedding_after173_completion_main_v57_20261010';newpub='actual_stock_dual_embedding_after173_verified_recovery_completion_main_v76_20261010'
    aliases={oldscreen:newscreen,oldpub:newpub};jobs={};launches={}
    state=read(A/'optimization_live_progress_v69_20261010.json')
    for name in state['services']:
        folder=A/'service_owned_workflows_20261006'/name
        if not (folder/'job_definition.json').exists():continue
        if 'progress' in name or 'main_publisher' in name:continue
        definition=read(folder/'job_definition.json');launchrow=read(folder/'native_launch.json')
        terminal=read(folder/'service_execution.json') if (folder/'service_execution.json').exists() else {}
        if owned(launchrow) or (terminal.get('status')=='failed' and terminal.get('at_local','')>='2026-10-10T20:52:00'):
            jobs[name]=definition;launches[name]=launchrow
    forced='actual_stock_rank_dual44_after173_normalization_v2_20261010';assert forced in jobs
    selected={forced}
    while True:
        before=len(selected)
        for name in selected:aliases[name]=name.removesuffix('_20261010')+'_after_Dual25_recovery_v1_20261010'
        for name,definition in jobs.items():
            if name in (oldscreen,oldpub) or name in selected:continue
            source=Path(definition['driver']);raw=source.read_text(encoding='utf8')
            if any(key in raw for key in aliases):selected.add(name)
        if len(selected)==before:break
    drivers={};inputs=[Path(__file__),recovery,A/'recover_actual_Dual25_terminal_location_v1_20261010.py',publisher];wrappers=[]
    original_drivers={Path(jobs[name]['driver']).name for name in selected}
    # Keep the future child service names; route only their still-unlaunched immutable entry points.
    for number,kind,version in [(174,'StockRankDual',1),(175,'StockTop10Embedding',3),(176,'StockTop10Embedding',3),(177,'StockRank5Embedding',4),(178,'StockForward5Embedding',4),(179,'StockForward20Embedding',5)]:
        for candidate in [f'prepare_{kind}{number}_selected_candidate_v{version}_20261010.py']:
            if (A/candidate).exists():original_drivers.add(candidate)
        if number==174:original_drivers.add('run_StockRankDual174_full_registration_v2_20261010.py')
    for driver in sorted(original_drivers):
        source=A/driver;assert source.is_file();inputs.append(source)
        wrapper=source.with_name(source.stem+'_after_Dual25_recovery_v1.py');assert not wrapper.exists()
        body="from pathlib import Path\nimport sys\nA=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]\nfrom route_verified_Dual25_recovery_dependencies_v1_20261010 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n"
        compile(body,str(wrapper),'exec');wrapper.write_text(body,encoding='utf8',newline='\n');drivers[driver]=wrapper.name;wrappers.append(wrapper)
    factories=['prepare_stock_rank_dual174_full_registry_sources_v1_20261010','prepare_stock_top10_embedding175_full_registry_sources_v2_20261010','prepare_stock_top10_embedding176_full_registry_sources_v2_20261010','prepare_StockRank5Embedding177_complete48_pipeline_v1_20261010','prepare_StockForward5Embedding178_complete48_pipeline_v1_20261010','admit_StockForward20Embedding179_complete48_pipeline_v2_20261010']
    for name in factories:assert (A/(name+'.py')).is_file()
    # Do not terminate any helper unless it has not produced its scientific output and owns no child.
    for name in selected:
        row=launches[name]
        if owned(row):retire(row,'Replace verified childless dependency wait with explicit recovery alias; original failures and all scientific drivers retained')
    if oldpub in launches and owned(launches[oldpub]):retire(launches[oldpub],'Replace childless failed Dual25 wait with verified terminal recovery publication')
    create(PROOF,{'status':'explicit_actual_completed_Dual25_terminal_recovery_dependency_routing_original_failures_retained','service_aliases':aliases,'driver_wrappers':drivers,'source_factories':factories,'selected_helpers':sorted(selected),'input_sha256':{str(p):sha(p) for p in [*inputs,*wrappers]},'new_fits':0,'new_quality_scores':0,'all44_47_31_48_48_48_frozen_cases_unchanged':True,'no_terminal_status_forged':True,'test_labels_read':False})
    tasks=[(newpub,publisher.name)]+[(aliases[name],drivers[Path(jobs[name]['driver']).name]) for name in sorted(selected)]
    for name,driver in tasks:
        assert allowed();row=start_service(name,driver,[],{str(A/driver):sha(A/driver),str(PROOF):sha(PROOF)});create(A/(name+'_activation.json'),row)
    print({'verified_Dual25_scores_preserved':True,'routed_helpers':len(selected),'new_quality_scores':0},flush=True)
if __name__=='__main__':main()
