"""Bind the encoder when the receiver imports its just-generated publisher, using private builtins."""
from contextlib import contextmanager,ExitStack
from types import FunctionType
from pathlib import Path
from byte_exact_dynamic_snapshot_encoder_runtime_v1_20261010 import installed as bind
from run_dependency_queue_v3_20261006 import create

@contextmanager
def installed(receiver,module_name,log):
    previous=receiver.main;assert isinstance(previous,FunctionType)
    globals_copy=dict(previous.__globals__);builtins_copy=dict(previous.__builtins__)
    original_import=builtins_copy['__import__'];events=[];seen=set()
    with ExitStack() as stack:
        def importing(name,*args,**kwargs):
            module=original_import(name,*args,**kwargs)
            if name==module_name and name not in seen:
                seen.add(name);stack.enter_context(bind(module,Path(log).with_name('dynamic_snapshot_encoder_binding.json')))
                events.append({'module':name,'bound_after_actual_receiver_import':True})
            return module
        builtins_copy['__import__']=importing;globals_copy['__builtins__']=builtins_copy
        clone=FunctionType(previous.__code__,globals_copy,previous.__name__,previous.__defaults__,previous.__closure__)
        clone.__kwdefaults__=previous.__kwdefaults__;clone.__annotations__=previous.__annotations__
        receiver.main=clone
        try:yield events
        finally:
            assert receiver.main is clone;receiver.main=previous
    path=Path(log);path.parent.mkdir(parents=True,exist_ok=True)
    create(path,{'status':'late_publisher_binding_and_private_builtin_restoration_completed','events':events,'receiver_original_code_object_reused':True,'receiver_main_restored':True,'process_global_builtins_not_modified':True,'new_scoring_or_model_math':False})
