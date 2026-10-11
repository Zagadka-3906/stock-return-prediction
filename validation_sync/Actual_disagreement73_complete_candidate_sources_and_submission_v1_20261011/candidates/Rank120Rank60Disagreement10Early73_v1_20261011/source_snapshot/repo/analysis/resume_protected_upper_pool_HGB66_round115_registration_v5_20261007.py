"""Finish the preserved actual66 registration after selection, without rescoring or reselection."""
from pathlib import Path
import ast
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def register_remaining():
    import register_protected_upper_pool_HGB66_round115_artifacts_v3_20261007 as registry
    old=A/'service_owned_workflows_20261006/protected_upper_pool_HGB66_round115_full_registration_v3'
    assert not owned(read(old/'native_launch.json')) and read(old/'service_execution.json')['status']=='failed'
    selection=read(registry.OUT/'selection.json');assert selection==read(registry.CANDIDATE/'selection.json')
    assert len(selection['ranking'])==66 and selection['winner']['metrics']==read(registry.SOURCE_CANDIDATE/'selection.json')['winner']['metrics']
    pins={str(ROOT/p):digest for p,digest in selection['frozen_sha256'].items()}
    pins.update(selection['frozen_external_input_sha256'])
    for path,digest in pins.items():assert sha(path)==digest,path
    pilot=read(A/'protected_upper_pool_HGB66_official_comparison_v2_20261007/verification.json')
    original=read(registry.SOURCE_CANDIDATE/'selection.json')
    actual=read(registry.SOURCE_CANDIDATE/'verification.json');manifest_path=registry.SOURCE_CANDIDATE/'manifest.json'
    assert actual['whole_scheme_graph']==selection['winner'][registry.GRAPH_FIELD]
    relocation=read(A/'protected_upper_pool_HGB66_round115_inherited_registry_alias_relocation_20261007.json')
    assert sha(relocation['destination']).upper()==relocation['sha256']
    assert read(registry.CANDIDATE/'registry_alias_verification.json')['status']=='passed_exact_file_aliases_of_actual_sealed_selected_model_residual_candidate'
    function=next(n for n in ast.parse(Path(registry.__file__).read_text(encoding='utf8')).body if isinstance(n,ast.FunctionDef) and n.name=='main')
    first=next(i for i,n in enumerate(function.body) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='create' and isinstance(n.value.args[0],ast.BinOp) and isinstance(n.value.args[0].right,ast.Constant) and n.value.args[0].right.value=='registry_alias_verification.json')
    suffix=ast.fix_missing_locations(ast.Module(body=function.body[first:-1],type_ignores=[]))
    ns=dict(registry.__dict__);ns.update(pilot_path=A/'protected_upper_pool_HGB66_official_comparison_v2_20261007/verification.json',pilot=pilot,actual=actual,selection_source=registry.SOURCE_CANDIDATE/'selection.json',original=original,manifest_path=manifest_path,pins=pins,records=selection['ranking'],winner=selection['winner'])
    def immutable_create(path,value):
        if Path(path).exists():
            assert read(path)==value,path
        else:create(path,value)
    ns['create']=immutable_create
    exec(compile(suffix,'actual_original115_registry_suffix_after_preserved_selection','exec'),ns)
    protocol=read(registry.OUT/'protocol.json')
    more=[Path(__file__),old/'service_execution.json',old/'stderr.log',A/'protected_upper_pool_HGB66_round115_inherited_registry_alias_relocation_20261007.json']
    # Separate recovery inputs accompany the original scientific scope; no earlier freeze is rewritten.
    create(registry.OUT/'registration_alias_recovery_v5.json',{'status':'passed_remaining_original_registry_after_preserved_selection',
        'input_sha256':{str(p):sha(p) for p in more},'original_selection_sha256':sha(registry.OUT/'selection.json'),
        'original_frozen_selection_and_graph_preserved':True,'new_quality_scores':0,'new_native_fits':0})
    protocol['input_sha256'].update({str(p):sha(p) for p in more})
    protocol['input_sha256'][str(registry.OUT/'registration_alias_recovery_v5.json')]=sha(registry.OUT/'registration_alias_recovery_v5.json')
    return protocol

def main():
    import run_protected_upper_pool_HGB66_round115_full_registration_v3_20261007 as previous
    text=Path(previous.__file__).read_text(encoding='utf8')
    before='from register_protected_upper_pool_HGB66_round115_artifacts_v3_20261007 import main as register'
    assert text.count(before)==1
    text=text.replace(before,'from resume_protected_upper_pool_HGB66_round115_registration_v5_20261007 import register_remaining as register')
    text=text.replace('protected_upper_pool_HGB66_round115_actual_registration_v3_20261007','protected_upper_pool_HGB66_round115_actual_registration_v5_20261007')
    ns={'__file__':str(Path(__file__)),'__name__':'actual_registration_recovery_v4'}
    exec(compile(text,str(previous.__file__),'exec'),ns);ns['main']()

if __name__=='__main__':main()
