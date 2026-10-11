"""Actual dynamic-exec integration checks; reuse the full15595-row encoder byte proof."""
from pathlib import Path
from types import SimpleNamespace
import sys,builtins,hashlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from byte_exact_publication_encoder_runtime_v1_20261010 import installed as encoder
from byte_exact_dynamic_snapshot_encoder_runtime_v1_20261010 import installed as binding

CODE='''import json
def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\\n').encode('utf8')
def snapshot(value):
    return encoded(value)
'''

def main():
    fixtures=[None,[],{},-0.,1.23456789012345,{'中文':'行\\n换行','emoji':'🧪','boolean':True}, {'nested':{'b':[1,2.,None,False],'empty':[]}},float('nan'),float('inf'),{'status':'validated_local_snapshot','exported_files':{},'中文':'验证'}]
    records=[]
    with encoder():
        import publish_classifier_consensus_workflows_20261006 as helpers
        for existing_delegate in (False,True):
            publisher=SimpleNamespace();calls=[]
            if existing_delegate:
                def delegated(*args,**kwargs):calls.append(True);return builtins.exec(*args,**kwargs)
                publisher.exec=delegated
            namespaces=[]
            with binding(publisher) as events:
                for case,value in enumerate(fixtures):
                    original={'__name__':'original_fixture'};builtins.exec(CODE,original)
                    actual={'__name__':'actual_dynamic_fixture'};publisher.exec(CODE,actual)
                    expected=original['snapshot'](value);observed=actual['snapshot'](value)
                    assert expected==observed and actual['snapshot'].__globals__['encoded'] is helpers.sync.encoded
                    namespaces.append(actual)
                    records.append({'existing_exec_delegate':existing_delegate,'case':case,'bytes_identical':True,'sha256':hashlib.sha256(observed).hexdigest()})
                assert len(events)==len(fixtures)
            assert all(ns['encoded'].__module__=='actual_dynamic_fixture' for ns in namespaces)
            if existing_delegate:assert publisher.exec is delegated and len(calls)==len(fixtures)
            else:assert not hasattr(publisher,'exec')
        publisher=SimpleNamespace()
        try:
            with binding(publisher):raise RuntimeError('intentional_cleanup_fixture')
        except RuntimeError as exc:assert str(exc)=='intentional_cleanup_fixture'
        assert not hasattr(publisher,'exec')
    proof=A/'byte_exact_publication_encoder_controls_v1_20261010.json'
    create(A/'dynamic_snapshot_encoder_binding_actual_controls_v1_20261010.json',{'status':'passed20_dynamic_namespace_byte_identity_cases_delegate_and_exception_restoration','records':records,'existing_complete_parameter_byte_proof_rows':read(proof)['actual_parameter_rows'],'existing_complete_parameter_byte_proof_bytes':read(proof)['actual_parameter_bytes'],'new_complete_board_reencoding_not_claimed':True,'input_sha256':{str(p):sha(p) for p in (Path(__file__),A/'byte_exact_dynamic_snapshot_encoder_runtime_v1_20261010.py',proof)},'new_quality_scores':0,'test_labels_read':False})
    print('passed20 actual dynamic namespace byte identity cases and exact restoration',flush=True)
if __name__=='__main__':main()
