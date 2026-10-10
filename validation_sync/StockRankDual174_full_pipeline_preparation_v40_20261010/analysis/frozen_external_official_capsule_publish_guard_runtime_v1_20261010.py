"""Resolve a score capsule against its existing frozen internal or external SHA; no scoring change."""
from pathlib import Path
from contextlib import contextmanager
import types,ast

def expected_digest(source,selection,root):
    source,root=Path(source),Path(root)
    if source.is_relative_to(root):return selection['frozen_sha256'][source.relative_to(root).as_posix()]
    assert source.drive.upper()=='E:' and source.suffix=='.json'
    assert source.parent.name in ('identical_official_scores','cross_round_official_scores'),source
    return selection['frozen_external_input_sha256'][str(source)]

@contextmanager
def installed(log):
    import publish_explicit_parent_training_round_v2_20261005 as module
    from run_dependency_queue_v3_20261006 import sha,create
    original=module.publish;source=Path(module.__file__).read_text(encoding='utf8')
    before="        assert sha(source)==selection['frozen_sha256'][source.relative_to(ROOT).as_posix()]"
    after="        assert sha(source)==_expected_frozen_capsule_digest(source,selection,ROOT)"
    assert source.count(before)==1 and '_expected_frozen_capsule_digest' not in vars(module)
    changed=source.replace(before,after);assert ast.dump(ast.parse(changed.replace(after,before)))==ast.dump(ast.parse(source))
    namespace={'__file__':module.__file__,'__name__':'admitted_frozen_external_capsule_publish_guard'}
    exec(compile(changed,module.__file__,'exec'),namespace)
    fn=namespace['publish'];wrapped=types.FunctionType(fn.__code__,vars(module),'publish',fn.__defaults__,fn.__closure__)
    vars(module)['_expected_frozen_capsule_digest']=expected_digest;module.publish=wrapped
    create(log,{'status':'installed_single_guard_existing_frozen_internal_or_E_official_capsule_SHA_resolution_with_original_publish_globals',
                'input_sha256':{str(Path(__file__)):sha(__file__),str(Path(module.__file__)):sha(module.__file__)},
                'numerical_scoring_calibration_model_and_selection_code_unchanged':True})
    try:yield
    finally:
        assert module.publish is wrapped;module.publish=original;vars(module).pop('_expected_frozen_capsule_digest')
