"""Resume only verified alias copies after a pre-protocol cross-volume link failure."""
from pathlib import Path
from contextlib import contextmanager
import sys,os
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

@contextmanager
def installed(log):
    import register_ReturnProtected167_round167_artifacts_20261010 as module
    from protected167_storage_v2_20261010 import installed_transfer
    failed=A/'service_owned_workflows_20261006/ReturnProtected167_round167_full_registration_v1_20261010'
    assert not owned(read(failed/'native_launch.json'))
    error=read(failed/'service_execution.json');assert error['status']=='failed' and error['failure'].startswith('OSError: [WinError 17]')
    assert module.OUT.is_dir() and not any(module.OUT.iterdir()),'Only the empty pre-protocol release may resume'
    assert module.CANDIDATE.resolve().is_relative_to(Path('E:/赛题五_本机临时/第167轮_20261010').resolve())
    manifest=read(module.SOURCE_CANDIDATE/'manifest.json');expected={}
    for relative,info in manifest['files'].items():
        destination='original_inference_selection_round167.json' if relative=='selection.json' else 'original_registry_alias_round167.json' if relative=='registry_alias_verification.json' else relative
        expected[(module.CANDIDATE/destination).resolve()]=(module.SOURCE_CANDIDATE/relative,info['sha256'])
    existing=[p for p in module.CANDIDATE.rglob('*') if p.is_file()]
    assert existing
    audit=[]
    for p in existing:
        assert p.resolve() in expected,p
        source,digest=expected[p.resolve()]
        assert os.path.samefile(source,p) and sha(source)==digest
        audit.append({'target':str(p),'source':str(source),'sha256':digest,'exact_same_file_alias':True})
    source=Path(module.__file__);text=source.read_text(encoding='utf8')
    replacements={'    assert not OUT.exists()':'    assert OUT.is_dir() and not any(OUT.iterdir())','    empty(CANDIDATE)':'    _verified_prefix_admitted(CANDIDATE)','    OUT.mkdir()':'    OUT.mkdir(exist_ok=True)'}
    for before,after in replacements.items():assert text.count(before)==1;text=text.replace(before,after)
    def admitted(path):
        assert Path(path).resolve()==module.CANDIDATE.resolve()
        assert {p.resolve() for p in path.rglob('*') if p.is_file()}=={p.resolve() for p in existing}
    namespace=dict(vars(module));namespace.update(__name__='actual_verified_Return167_registration_resume',_verified_prefix_admitted=admitted)
    exec(compile(text,str(source),'exec'),namespace)
    original_main=module.main;module.main=namespace['main'];events=[]
    try:
        with installed_transfer():
            transfer=os.link
            def resume_link(source,destination,*args,**kwargs):
                src,dst=Path(source),Path(destination)
                if dst.exists():
                    assert not args and not kwargs and dst.resolve() in expected
                    original,digest=expected[dst.resolve()]
                    assert src.resolve()==original.resolve() and os.path.samefile(src,dst)
                    events.append({'target':str(dst),'source':str(src),'sha256':digest,'existing_alias_reused':True});return None
                return transfer(source,destination,*args,**kwargs)
            os.link=resume_link
            try:yield
            finally:
                assert os.link is resume_link;os.link=transfer
    finally:
        module.main=original_main
        create(Path(log),{'status':'verified_partial_registration_resume_scopes_restored','original_failure':error,'existing_aliases':audit,'reused_alias_calls':events,'original_register_source_sha256':sha(source),'only_three_administrative_prefix_admission_statements_replaced':True,'original_register_main_restored':True,'new_training_scoring_or_inference_by_runtime':0})
