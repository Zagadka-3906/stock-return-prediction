"""Check real published165 module/source namespace wiring without replaying publication."""
from pathlib import Path
import sys,builtins,hashlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from byte_exact_publication_encoder_runtime_v1_20261010 import installed as encoder
from byte_exact_dynamic_snapshot_encoder_runtime_v1_20261010 import installed as binding

def main():
    import publish_ReusedNN165Quality19_round165_full_validation_20261009 as publisher
    import publish_classifier_consensus_workflows_20261006 as helpers
    source=A/'sync_validated_rounds_main_20261005.py'
    paths=[A/'ReusedNN165_prepared_frontier_v1_20261010.json',A/'ReusedNN165Quality19_round165_plan_v1_20261009.json',A/'github_validation_sync_main_20261005/round165_receipt.json']
    assert read(paths[-1])['scored_records']==19
    raw=source.read_text(encoding='utf8');code=compile(raw,str(source),'exec')
    original=dict(helpers.sync.__dict__,__name__='original_round165_namespace_check');builtins.exec(code,original)
    actual=dict(helpers.sync.__dict__,__name__='actual_round165_namespace_check')
    assert not hasattr(publisher,'exec')
    records=[]
    with encoder(),binding(publisher) as events:
        publisher.exec(code,actual)
        assert actual['snapshot'].__globals__['encoded'] is helpers.sync.encoded
        for path in paths:
            value=read(path);expected=original['encoded'](value);observed=actual['snapshot'].__globals__['encoded'](value)
            assert expected==observed
            records.append({'actual_published165_input':str(path),'bytes_identical':True,'serialized_bytes':len(observed),'sha256':hashlib.sha256(observed).hexdigest()})
        assert len(events)==1
    assert not hasattr(publisher,'exec') and actual['encoded'].__module__=='actual_round165_namespace_check'
    create(A/'actual165_dynamic_snapshot_encoder_binding_controls_v1_20261010.json',{'status':'passed_real_published165_module_and_actual_sync_source_namespace_binding_three_real_metadata_byte_controls','records':records,'actual_complete_snapshot_or_Git_publication_replay_not_claimed':True,'old_complete15595_parameter_byte_proof_reused':True,'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(publisher.__file__),source,A/'byte_exact_dynamic_snapshot_encoder_runtime_v1_20261010.py',A/'dynamic_snapshot_encoder_binding_actual_controls_v1_20261010.json',*paths]},'new_quality_scores':0,'test_labels_read':False})
    print('passed real published165 namespace binding and3 real input byte controls',flush=True)
if __name__=='__main__':main()
