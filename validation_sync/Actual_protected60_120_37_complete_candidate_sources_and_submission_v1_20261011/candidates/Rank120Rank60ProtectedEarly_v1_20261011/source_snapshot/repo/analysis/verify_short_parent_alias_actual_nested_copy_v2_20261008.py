from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import sys,ast,hashlib,os,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create
from short_content_addressed_native_storage_v2_20261008 import installed
def main():
    E=Path('E:/赛题五_本机临时/short_native_alias_actual_nested_copy_v2_20261008');assert not E.exists();E.mkdir()
    original={}
    for i in range(3):
        source=E/(('2337d018ef9051af__'*11)+f'model_original{i}.joblib');source.write_bytes(bytes([i])*1001);original['root'+str(i)]={'path':str(source),'sha256':sha(source)}
    candidate=E/'candidate';ns=SimpleNamespace(sha=sha,cohort_saved_models=original);storage=[]
    src=A/'predict_cohort_calibrated_scheme_20261006.py';tree=ast.parse(src.read_text(encoding='utf8'));function=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='linked_models')
    env={'Path':Path,'ns':ns,'deepcopy':deepcopy,'hashlib':hashlib,'os':os,'candidate':candidate,'storage':storage}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[])),str(src),'exec'),env)
    with installed(ns,E/'aliases') as proof:
        result=env['linked_models']({},original,candidate)
        assert set(result)==set(original)
        for key,info in result.items():assert info['sha256']==original[key]['sha256']==sha(info['path']);assert len(Path(info['path']).name)<128
    assert ns.cohort_saved_models is original and len(storage)==3
    create(A/'actual_short_parent_alias_nested_copy_v2_20261008.json',{'status':'passed_actual_original_linked_models_with_three_very_long_parent_source_names_and_exact_SHA_and_restoration','input_sha256':{str(p):sha(p) for p in [Path(__file__),src,A/'short_content_addressed_native_storage_v2_20261008.py']},'controls':proof['controls'],'actual_original_nested_copy_function_executed':True,'new_quality_scores':0})
    print('Actual original nested copy: three long parent sources, short aliases and SHA preservation passed.',flush=True)
if __name__=='__main__':main()
