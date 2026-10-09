"""Correct prospective150 component counts and explicit comparison-parent paths before any59 score."""
from pathlib import Path
import ast,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
import prepare_HuberSparse59_round150_sources_v1_20261008 as original
from prepare_HuberSparse150_complete_receiver_refinement_v3_20261009 import MAP,META,replace
NAMES=original.NAMES
def source_paths():
    result=[]
    for path in original.source_paths():
        if path.is_relative_to(A):path=A/replace(path.relative_to(A).as_posix())
        result.append(path)
    result.extend([Path(__file__),Path(original.__file__),META,A/'prepare_HuberSparse150_complete_receiver_refinement_v3_20261009.py',
        A/'verify_HuberSparse59_prospective_routes_v1_20261009.py',A/'HuberSparse59_prospective_routes_v1_20261009.json',
        A/'verify_HuberSparse59_round150_sources_v1_20261009.py',A/'publish_HuberSparse59_evidence_v1_20261009.py',
        A/'verify_HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009.py',
        A/'actual_HuberSparse150_prior_complete_forecast_duplicate_audit_v1_20261009.json',
        A/'HuberSparse150_prior_complete_forecast_duplicate_audit_raw_v1_20261009.json',
        A/'HuberSparse59_actual_controls_index_v1_20261008.json'])
    return list(dict.fromkeys(result))
def generate(parent):
    result={}
    for name,source in original.generate(parent).items():
        source=replace(source)
        source=source.replace("len(measured['ordered_native_components']) in (2,4)","len(measured['ordered_native_components']) in (3,4)")
        source=source.replace('_r134/',f'_r{parent}/')
        compile(source,str(A/name),'exec');result[name]=source
    return result
def main():
    before=original.read
    namespace={'__file__':str(Path(__file__)),'__name__':'actual_Sparse150_source_materialization'}
    # Main only changes the selected generator call; scientific base paths remain in generate.
    source=Path(original.__file__).read_text(encoding='utf8')
    tree=ast.parse(source);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    namespace.update(read=before,sha=original.sha,create=original.create,A=A,ROOT=ROOT,generate=generate,hashlib=original.hashlib,time=original.time)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(Path(__file__)),'exec'),namespace)
    namespace['main']()
if __name__=='__main__':main()
