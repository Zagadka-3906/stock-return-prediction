"""Keep failed2 proof; validate literal PowerShell path bytes before the fresh3 copy/delete workflow."""
from pathlib import Path
import ast,sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    previous=A/'service_owned_workflows_20261006/Git_publisher_verified_E_relocation_v2_20261008/service_execution.json'
    assert read(previous)['status']=='failed'
    old=A/'relocate_idle_verified_Git_publisher_to_E_v2_20261008.py';text=old.read_text(encoding='utf8')
    assert text.count('powershell("""$ErrorActionPreference')==3
    text=text.replace('powershell("""$ErrorActionPreference','powershell(r"""$ErrorActionPreference')
    text=text.replace('Git_publisher_E_relocation_v2_20261008','Git_publisher_E_relocation_v3_20261008')
    text=text.replace('Git_publisher_E_relocation_location_v2_20261008','Git_publisher_E_relocation_location_v3_20261008')
    needle='def powershell(script,name):';assert text.count(needle)==1
    text=text.replace(needle,needle+"\n    assert all(ord(character)>=32 or character in '\\n\\r\\t' for character in script), 'Reject any accidentally escaped control byte before writing shell code'")
    parsed=ast.parse(text);scripts=[node.args[0].value for node in ast.walk(parsed) if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='powershell' and isinstance(node.args[0],ast.Constant)]
    assert len(scripts)==3
    for script in scripts:
        assert all(ord(c)>=32 or c in '\n\r\t' for c in script)
        assert 'D:\\3.Study\\数据分析\\赛题五_GitHub验证同步_20261005' in script
        assert 'E:\\赛题五_GitHub验证同步_20261008\\验证发布工作副本' in script
    target=A/'relocate_idle_verified_Git_publisher_to_E_v3_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'Git_publisher_E_relocation_raw_path_preflight_v3_20261008.json',{
        'status':'passed_all3_native_PowerShell_literal_path_and_control_byte_checks_before_any_mutation',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target,previous]},
        'failed2_source_hash_proof_preserved':True,'failed2_stopped_at_native_source_path_check_before_copy_rename_or_delete':True,
        'actual_source_repository_rehash_required_again':True,'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('Git_publisher_verified_E_relocation_v3_20261008',target.name,[],{str(p):sha(p) for p in [Path(__file__),target]})
    create(A/'Git_publisher_verified_E_relocation_v3_hidden_launch_20261008.json',row)
    print(json.dumps({'service':row['name'],'worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()
