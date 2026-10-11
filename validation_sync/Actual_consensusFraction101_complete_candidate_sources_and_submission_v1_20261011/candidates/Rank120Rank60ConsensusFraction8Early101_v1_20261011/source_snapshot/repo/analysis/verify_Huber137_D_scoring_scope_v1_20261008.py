"""Exercise the three original D-only cache scope gates without evaluating any labels or model score."""
from pathlib import Path
from types import SimpleNamespace
import ast,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create


def main():
    proof=A/'Huber137_D_scoring_scope_v1_20261008.json';assert not proof.exists()
    current=A/'Huber52_official_comparison_v1_20261008/scoring_validation_only'
    proposed=A/'Huber137_D_scoring_v1_20261008/comparison/scoring_validation_only'
    selected=A/'Huber137_D_scoring_v1_20261008/selected/scoring_validation_only'
    assert current.resolve().drive.upper()=='E:' and proposed.resolve().drive.upper()==selected.resolve().drive.upper()=='D:'
    files=[A/name for name in ('official_validation_csv_parse_cache_20261003.py','cross_round_official_score_reuse_20261003.py','identical_official_score_cache_20261003.py')]
    records=[]
    for source in files:
        tree=ast.parse(source.read_text(encoding='utf8'))
        function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in ('run','score'))
        start=next(i for i,node in enumerate(function.body) if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='folder' for t in node.targets))
        nodes=[function.body[start]]
        for node in function.body[start+1:]:
            if not isinstance(node,ast.Assert) or 'pred' in ast.unparse(node.test):break
            nodes.append(node)
        assert len(nodes)>=2 and any('is_relative_to' in ast.unparse(node) for node in nodes)
        code=compile(ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[])),str(source),'exec')
        for path,expected in ((current,False),(proposed,True),(selected,True)):
            try:exec(code,{'Path':Path,'ROOT':ROOT,'ctx':SimpleNamespace(scoring=path)});passed=True
            except AssertionError:passed=False
            assert passed==expected,(source,path,passed)
            records.append({'unchanged_cache_source':str(source),'scoring_path':str(path),'resolved_path':str(path.resolve()),'actual_original_scope_gate_passed':passed})
    create(proof,{'status':'passed_actual3_original_scope_guards_reject_E_and_accept_both_D_scoring_directories',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),*files]},'controls':records,
        'original_cache_functions_and_official_script_unmodified':True,'new_quality_scores':0,'test_labels_read':False})
    print('Actual three unchanged cache gates: E rejected; both D scoring paths admitted. No scoring executed.',flush=True)


if __name__=='__main__':main()
