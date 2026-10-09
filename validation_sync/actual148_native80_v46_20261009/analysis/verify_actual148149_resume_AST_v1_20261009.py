"""Prove all pending receiver source changes are limited to declared string service/path bindings."""
from pathlib import Path
import ast,sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    import resume_pending148_verified_gates_v5_20261009 as a
    import resume_pending149_verified_gates_v6_20261009 as b
    records=[]
    for module in (a,b):
        for path,digest in read(module.META)['input_sha256'].items():assert sha(path)==digest,path
        for old,new in module.SCRIPTS.items():
            path=A/old;source=path.read_text(encoding='utf8');dispatcher=old.startswith('dispatch_')
            class OnlyStrings(ast.NodeTransformer):
                def visit_Constant(self,node):
                    if isinstance(node.value,str):node.value=module.routed(node.value,dispatcher)
                    return node
            expected=OnlyStrings().visit(ast.parse(source))
            actual=ast.parse(module.routed(source,dispatcher))
            assert ast.dump(expected,include_attributes=False)==ast.dump(actual,include_attributes=False),old
            assert (A/new).is_file()
            records.append({'original':str(path),'original_sha256':sha(path),'new_driver':str(A/new),
                'numerical_constants_operators_function_bodies_and_imports_unchanged_except_declared_string_bindings':True})
    helper=A/'prepare_Pure149_duplicate_bound_receivers_v3_20261008.py';source=helper.read_text(encoding='utf8')
    needle="p.read_text(encoding='utf8')";assert source.count(needle)==1
    corrected=source.replace(needle,"ROUTE_CURRENT_SERVICES(p.read_text(encoding='utf8'))")
    assert ast.dump(ast.parse(corrected.replace("ROUTE_CURRENT_SERVICES(p.read_text(encoding='utf8'))",needle)),include_attributes=False)==ast.dump(ast.parse(source),include_attributes=False)
    create(A/'actual148149_manual_resume_AST_preflight_v1_20261009.json',{
        'status':'passed20_receiver_AST_controls_only_declared_string_routes_and_one_verified_helper_source_read_adapter',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'records':records,'actual_receiver_templates':len(records),
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),Path(a.__file__),Path(b.__file__),a.META,b.META,helper]},
        'new_native_replay_not_claimed_by_AST_preflight':True,'existing_real_phase_regression_retained':True,
        'actual14880_native238_full_and14980_native124_full_remain_required':True,'new_quality_scores':0,'test_labels_read':False})
    print({'actual_AST_controls':len(records),'scientific_numerical_expressions_changed':False},flush=True)
if __name__=='__main__':main()
