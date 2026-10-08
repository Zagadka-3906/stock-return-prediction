"""Validate exact native sleeping source lines as well as closed() helpers; dispatch already-frozen source3."""
from pathlib import Path
import sys,re,ast
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    source=A/'recover_ConeRidgeAlpha144_module_routing_and_dispatch_v3_20261008.py'
    proof_path=A/'ConeRidgeAlpha100_prospective_routes_v3_20261008.json';proof=read(proof_path)
    assert proof['actual_prospective_sources']==24 and proof['actual_graph_controls']==2619
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    prep=A/'ConeRidgeAlpha144_module_receiver_preparation_v3_20261008.json';pins=read(prep)['input_sha256']
    for p,d in pins.items():assert sha(p)==d,p
    text=source.read_text(encoding='utf8')
    start=text.index('    # Diagnose each exact waiting service');finish=text.index("\nif __name__=='__main__':main()")
    tail=text[start:finish]
    needle="            assert 'closed (' in dump and '(idle)' in dump,(name,dump)"
    replacement="""            tree=ast.parse(Path(row['original_driver']).read_text(encoding='utf8'))
            sleep_lines={node.lineno for node in ast.walk(tree) if isinstance(node,ast.Call) and ast.unparse(node.func)=='time.sleep'}
            native_sleep=any(f\"main ({Path(row['original_driver']).name}:{line})\" in dump for line in sleep_lines)
            assert '(idle)' in dump and ('closed (' in dump or native_sleep),(name,dump)
""".rstrip()
    assert tail.count(needle)==1;tail=tail.replace(needle,replacement)
    from recover_ConeRidgeAlpha144_module_routing_and_dispatch_v3_20261008 import SERVICES,corrected
    import time,subprocess
    namespace=dict(ROOT=ROOT,A=A,read=read,sha=sha,create=create,Path=Path,time=time,subprocess=subprocess,
                   ast=ast,SERVICES=SERVICES,corrected=corrected,pins=pins,proof_path=proof_path)
    from run_dependency_queue_v3_20261006 import owned
    namespace['owned']=owned
    create(A/'ConeRidgeAlpha144_exact_native_sleep_dispatch_preparation_v4_20261008.json',{
        'status':'frozen_exact_source_AST_sleep_line_audit_for_sealing_and_registration_dependencies',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),source,proof_path,prep]},
        'scientific_sources3_and_existing_controls_unchanged':True,'new_quality_scores':0})
    exec(compile('if True:\n'+tail,str(source),'exec'),namespace)
if __name__=='__main__':main()
