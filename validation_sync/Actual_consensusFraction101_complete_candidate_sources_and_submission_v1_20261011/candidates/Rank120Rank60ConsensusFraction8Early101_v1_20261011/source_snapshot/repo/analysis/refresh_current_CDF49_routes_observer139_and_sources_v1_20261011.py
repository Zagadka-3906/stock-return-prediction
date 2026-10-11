"""Record the verified future CDF recovery in the observer and publish sources to main."""
from pathlib import Path
import ast,sys,time,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    assert allowed()
    routes=A/'actual_capacity_CDF49_correct_report_contract_routes_v2_20261011.json'
    oldsource=A/'monitor_verified_current_optimization_v138_20261011.py'
    source=A/'monitor_verified_current_optimization_v139_20261011.py'
    text=oldsource.read_text(encoding='utf-8')
    needle=' while True:\n  c=read('
    assert text.count(needle)==1
    text=text.replace(needle," aliases.update(read(A/'"+routes.name+"')['service_alias_updates'])\n names.append('actual_CDF49_report_contract_observer139_sources_main_v1_20261011')\n"+needle)
    text=text.replace('v138_20261011','v139_20261011').replace('v276_20261011','v277_20261011').replace("+'.138.tmp'","+'.139.tmp'")
    compile(text,str(source),'exec');assert not source.exists();source.write_text(text,encoding='utf-8',newline='\n')
    old=read(A/'service_owned_workflows_20261006/actual_fast_optimization_progress_reboot_v138_20261011/native_launch.json');assert owned(old)
    new=start_service('actual_fast_optimization_progress_reboot_v139_20261011',source.name,[],{str(source):sha(source),str(routes):sha(routes)})
    snapshot=A/'optimization_live_progress_v139_20261011.json'
    for _ in range(30):
        if snapshot.exists():break
        time.sleep(1)
    assert snapshot.exists()
    state=read(snapshot)
    assert all(n in state['services'] for n in read(routes)['service_alias_updates'].values())
    for _ in range(20):
        assert owned(old)
        dump=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(old['owned_worker_pid'])],capture_output=True,text=True,encoding='utf-8',check=True).stdout
        if '(idle)' in dump and oldsource.name in dump:break
        time.sleep(1)
    else:raise AssertionError('Old observer not idle; preserve worker')
    worker=psutil.Process(old['owned_worker_pid']);assert owned(old) and not worker.children(recursive=True);worker.terminate()
    admission=A/'actual_observer139_CDF49_future_contract_routes_snapshot_admission_v1_20261011.json'
    create(admission,{'status':'passed_actual139_verified_delivery_and_correct_future_CDF_routes_snapshot','new':new,'old':old,'actual_old_idle_dump':dump,'input_sha256':{str(p):sha(p) for p in [Path(__file__),oldsource,source,routes]},'scientific_workers_terminated':0,'actual_new_scores_claimed_by_observer':0})
    proof=A/'capacity_CDF49_future_report_contract_recovery_admission_v2_20261011.json'
    files=[Path(p) for p in read(proof)['input_sha256']]+[proof,routes,source,admission,A/'actual_observer138_verified_candidate_delivery_reporting_admission_v1_20261011.json']
    template=A/'publish_actual_capacity109_CDF49_complete_candidate_sources_main_v1_20261011.py'
    script=template.read_text(encoding='utf-8');tree=ast.parse(script)
    node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
    lines=script.splitlines(keepends=True)
    lines[node.lineno-1:node.end_lineno]=['    paths=[Path(p) for p in '+repr([str(p) for p in dict.fromkeys(files)])+']\n']
    script=''.join(lines).replace('capacity109_CDF49_gaining_complete_candidate_sources','capacity_CDF49_report_contract_observer139_sources')
    script=script.replace('预声明大小网络109项及CDF49项提分后完整候选核验、main同步与交付；12模块实际导入验证通过','修复尚未执行的CDF候选回放核验字段，实际正反接口验证通过；更新已核验交付进度')
    driver=A/'publish_actual_CDF49_report_contract_observer139_sources_main_v1_20261011.py'
    ast.parse(script);assert not driver.exists();driver.write_text(script,encoding='utf-8',newline='\n')
    assert allowed()
    pub=start_service('actual_CDF49_report_contract_observer139_sources_main_v1_20261011',driver.name,[],{str(driver):sha(driver),str(proof):sha(proof),str(admission):sha(admission)})
    create(A/'actual_CDF49_report_contract_observer139_sources_main_activation_v1_20261011.json',pub)
    print('Observer139 actual snapshot passed; future CDF source correction publication queued to main',flush=True)

if __name__=='__main__':main()
