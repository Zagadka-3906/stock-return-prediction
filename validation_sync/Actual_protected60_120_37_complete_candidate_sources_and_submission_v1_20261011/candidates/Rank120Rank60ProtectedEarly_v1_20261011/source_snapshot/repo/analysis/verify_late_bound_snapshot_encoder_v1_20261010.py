"""Delay publisher import until receiver execution; test byte output and exact exception cleanup."""
from pathlib import Path
from types import ModuleType
import sys,builtins,json
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import create,sha
from byte_exact_publication_encoder_runtime_v1_20261010 import installed as encoder
from late_bound_dynamic_snapshot_encoder_runtime_v1_20261010 import installed as late

def main():
    out=Path('E:/赛题五_本机临时/late_snapshot_encoder_actual_CPU_controls_v1_20261010');out.mkdir(exist_ok=False)
    records=[];original_import=builtins.__import__
    with encoder():
        for i,value in enumerate((None,{'中文':[True,-0.,.12345]},float('inf'))):
            for failing in (False,True):
                publisher=ModuleType('_actual_late_encoder_fixture_20261010');namespace={'__name__':'actual_late_fixture'}
                def publish():
                    publisher.exec("import json\ndef encoded(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\\n').encode('utf8')\ndef snapshot(v):return encoded(v)\n",namespace)
                    observed=namespace['snapshot'](value)
                    assert observed==(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf8')
                    if failing:raise RuntimeError('intentional_late_import_cleanup')
                    return observed
                publisher.main=publish;sys.modules[publisher.__name__]=publisher
                receiver=ModuleType('_actual_late_receiver_fixture_20261010')
                exec('def main():\n from _actual_late_encoder_fixture_20261010 import main as publisher\n return publisher()\n',receiver.__dict__)
                old=receiver.main;folder=out/(str(i)+'_'+str(failing));folder.mkdir()
                try:
                    with late(receiver,publisher.__name__,folder/'late_import.json'):
                        assert not hasattr(publisher,'exec')
                        receiver.main();assert not failing
                except RuntimeError as e:assert failing and str(e)=='intentional_late_import_cleanup'
                assert receiver.main is old and not hasattr(publisher,'exec') and builtins.__import__ is original_import
                assert namespace['encoded'].__module__=='actual_late_fixture'
                records.append({'case':i,'intentional_exception':failing,'delayed_binding_output_bytes_exact':True,'receiver_publisher_namespace_and_global_builtins_restored':True})
                del sys.modules[publisher.__name__]
    create(A/'late_bound_snapshot_encoder_actual_CPU_controls_v1_20261010.json',{'status':'passed6_actual_delayed_import_byte_identity_and_private_builtin_exception_cleanup_cases','records':records,'input_sha256':{str(p):sha(p) for p in (Path(__file__),A/'late_bound_dynamic_snapshot_encoder_runtime_v1_20261010.py',A/'byte_exact_dynamic_snapshot_encoder_runtime_v1_20261010.py')},'original_receiver_code_object_reused':True,'global_import_not_patched':True,'quality_scores':0})
    print('passed6 delayed import encoder and exact cleanup cases',flush=True)
if __name__=='__main__':main()
