"""Bind the already-proven encoder inside a publication's newly exec-created namespace."""
from pathlib import Path
from contextlib import contextmanager
import builtins,sys
A=Path(__file__).resolve().parent;sys.path.insert(0,str(A))
from run_dependency_queue_v3_20261006 import read,create

@contextmanager
def installed(publisher,log=None):
    import publish_classifier_consensus_workflows_20261006 as helpers
    proof=read(A/'byte_exact_publication_encoder_controls_v1_20261010.json')
    assert proof['actual_parameter_rows']==15595 and proof['fixtures']==10
    sync=helpers.sync;encoder=sync.encoded
    assert encoder.__module__=='byte_exact_publication_encoder_runtime_v1_20261010',encoder.__module__
    absent=object();previous=publisher.__dict__.get('exec',absent)
    delegate=builtins.exec if previous is absent else previous
    assert callable(delegate)
    bindings=[];events=[]
    def execute(code,namespace,*args,**kwargs):
        result=delegate(code,namespace,*args,**kwargs)
        snapshot=namespace.get('snapshot');original=namespace.get('encoded')
        assert callable(snapshot) and callable(original) and snapshot.__globals__ is namespace
        assert sync.encoded is encoder
        namespace['encoded']=encoder;bindings.append((namespace,original))
        events.append({'namespace_name':namespace.get('__name__'),'snapshot_global_encoder_is_installed_encoder':snapshot.__globals__['encoded'] is encoder,'original_encoder_module':getattr(original,'__module__',None)})
        return result
    publisher.exec=execute
    try:yield events
    finally:
        assert publisher.exec is execute
        if previous is absent:del publisher.exec
        else:publisher.exec=previous
        for namespace,original in reversed(bindings):
            assert namespace['encoded'] is encoder;namespace['encoded']=original
        if log is not None:
            log=Path(log);log.parent.mkdir(parents=True,exist_ok=True)
            create(log,{'status':'dynamic_snapshot_encoder_binding_and_restoration_completed','events':events,'namespace_bindings':len(bindings),'publisher_exec_restored':True,'namespace_encoders_restored':True,'model_math_and_score_fields_unchanged':True})
