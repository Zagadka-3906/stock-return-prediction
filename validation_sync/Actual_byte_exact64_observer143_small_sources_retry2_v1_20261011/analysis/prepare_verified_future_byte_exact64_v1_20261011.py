"""Adopt proven performance scopes only by replacing the still idle coordinator."""
from pathlib import Path
import sys,ast,subprocess,psutil
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from start_fast_completed_owned_service_v1_20261011 import start_service

def save(p,s):
    ast.parse(s);assert not p.exists();p.write_text(s,encoding='utf-8',newline='\n');return p

def idle(identity):
    assert owned(identity)
    p=psutil.Process(identity['owned_worker_pid']);assert not p.children(recursive=True)
    dump=subprocess.run([str(A.parent/'tools/readonly_pyspy_diagnostics_20261006/py-spy.exe'),'dump','--pid',str(p.pid)],capture_output=True,text=True,encoding='utf-8',check=True).stdout
    assert '(idle)' in dump and 'closed (' in dump,dump
    return dump

def main():
    assert allowed()
    oldproof=A/'verified_idle_future_single_dispatch63_admission_v1_20261011.json';data=read(oldproof)
    service=A/'service_owned_workflows_20261006/actual_verified_idle_future_single_dispatch63_v1_20261011'
    identity=read(service/'native_launch.json');dump=idle(identity)
    assert not (service/'service_execution.json').exists()
    for name,_ in data['tasks']:assert not (A/'service_owned_workflows_20261006'/name).exists(),name
    joint=A/'identity_codec_and_bounded_HTML_actual18_scope_admission_v1_20261011.json';jointdata=read(joint)
    assert jointdata['status'].startswith('passed_actual18_')
    for p,d in jointdata['input_sha256'].items():assert sha(p)==d,p
    proof=A/'verified_future_byte_exact64_admission_v1_20261011.json'
    route=A/'route_verified_future_byte_exact64_v1_20261011.py'
    text=(A/'route_verified_idle_future_single_dispatch63_v1_20261011.py').read_text(encoding='utf-8')
    text=text.replace(oldproof.name,proof.name)
    needle="'actual207_current61_parent_exact62_gates_admission_v1_20261011.json']:";assert text.count(needle)==1
    text=text.replace(needle,"'actual207_current61_parent_exact62_gates_admission_v1_20261011.json','"+oldproof.name+"']:")
    needle="with original(),admitted_installed(contract['number'],contract['codec_name'],contract['verifier_name']):yield";assert text.count(needle)==1
    text=text.replace(needle,"with original(),admitted_installed(contract['number'],contract['codec_name'],contract['verifier_name']),html_scope(),identity_scope(importlib.import_module(contract['codec_name'])):yield")
    needle="   original=stream.installed";assert text.count(needle)==1
    text=text.replace(needle,"   from bounded_original_ranking_HTML_runtime_v1_20261011 import installed as html_scope\n   from identity_memoized_original_lossless_codec_runtime_v1_20261011 import installed as identity_scope\n"+needle)
    needle="  if '_full_registration_' in name:return raw(str(source),run_name='__main__')";assert text.count(needle)==1
    replacement='''  if '_full_registration_' in name:
   import re
   from bounded_original_ranking_HTML_runtime_v1_20261011 import installed as html_scope
   from identity_memoized_original_lossless_codec_runtime_v1_20261011 import installed as identity_scope
   text=source.read_text(encoding='utf-8')
   pattern=r'with original_stream_writer\(\),shared_reader\((\d+),"([^"]+)","([^"]+)"\):yield'
   matches=list(re.finditer(pattern,text));assert len(matches)==1,(name,matches)
   hit=matches[0];number=int(hit.group(1));assert 202<=number<=207
   variants=read(A/'identity_codec_and_bounded_HTML_actual18_scope_admission_v1_20261011.json')['variants']
   assert any(v['number']==number and v['codec_name']==hit.group(2) and v['verifier_name']==hit.group(3) for v in variants)
   text=text[:hit.start()]+hit.group(0).replace(':yield',',html_scope(),identity_scope(importlib.import_module('+repr(hit.group(2))+')):yield')+text[hit.end():]
   namespace={'__name__':'__main__','__file__':str(source),'html_scope':html_scope,'identity_scope':identity_scope,'importlib':importlib}
   exec(compile(text,str(source),'exec'),namespace);return namespace'''
    text=text.replace(needle,replacement);save(route,text)
    paths=[Path(__file__),oldproof,joint,route,A/'bounded_original_ranking_HTML_runtime_v1_20261011.py',A/'identity_memoized_original_lossless_codec_runtime_v1_20261011.py']
    aliases=dict(data['service_alias_updates']);tasks=[];wrappers={}
    for name,driver in data['tasks']:
        new=name.replace('recovery63_','recovery64_',1);assert new!=name;aliases[name]=new;tasks.append((new,driver))
    for driver in data['driver_wrappers']:
        p=save(A/(Path(driver).stem+'_byte_exact64_wrapper.py'),"from route_verified_future_byte_exact64_v1_20261011 import execute\nif __name__=='__main__':execute("+repr(driver)+")\n")
        wrappers[driver]=p.name;paths.append(p)
    coordinator=A/'run_verified_future_byte_exact64_v1_20261011.py'
    s=(A/'run_verified_idle_future_single_dispatch63_v1_20261011.py').read_text(encoding='utf8').replace(oldproof.name,proof.name).replace('from handoff_ready_goss_full_execution_20261006 import start_service','from start_fast_completed_owned_service_v1_20261011 import start_service')
    save(coordinator,s);paths.append(coordinator)
    create(proof,{'status':'actual_idle_coordinator_only_replacement_with_byte_exact_full180_and18_scope_controls','input_sha256':{str(p):sha(p) for p in paths},'service_alias_updates':aliases,'tasks':tasks,'driver_wrappers':wrappers,'source_factories':data['source_factories'],'publication_module_corrections':data['publication_module_corrections'],'actual_family_folder_controls':data['actual_family_folder_controls'],'actual_idle_dump':dump,'retired_identity':identity,'scientific_workers_restarted_or_terminated':0,'original189_preserved':True,'all_original_QA_required':True,'new_scores':0,'test_labels_read':False})
    idle(identity)
    for name,_ in data['tasks']:assert not (A/'service_owned_workflows_20261006'/name).exists(),name
    p=psutil.Process(identity['owned_worker_pid']);assert owned(identity);p.terminate();p.wait(timeout=10)
    assert allowed();i=start_service('actual_verified_future_byte_exact64_v1_20261011',coordinator.name,[],{str(coordinator):sha(coordinator),str(proof):sha(proof)})
    create(A/'actual_verified_future_byte_exact64_activation_v1_20261011.json',i)
    print('Only actual idle coordinator replaced; original189 and all scientific workers preserved;54 future stages await189 actual completion',flush=True)

if __name__=='__main__':main()
